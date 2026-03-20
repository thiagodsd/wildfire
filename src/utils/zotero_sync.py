import os
import re
from pathlib import Path

import fitz
import requests
from dotenv import load_dotenv
from pyzotero import zotero

ROOT = Path(__file__).resolve().parents[2]
FILES = ROOT / "files"


def get_library_id(api_key):
    r = requests.get(f"https://api.zotero.org/keys/{api_key}")
    r.raise_for_status()
    return str(r.json()["userID"])


def extract_doi(path):
    doc = fitz.open(path)
    text = ""
    for page in doc[:3]:
        text += page.get_text()
    doc.close()

    m = re.search(r"(10\.\d{4,9}/\S+)", text)
    if not m:
        return None
    return m.group(1).rstrip(".,;:)]\\'\"")


def crossref_meta(doi):
    r = requests.get(
        f"https://api.crossref.org/works/{doi}",
        headers={"User-Agent": "wildfire-sync/0.1"},
        timeout=15,
    )
    if r.status_code != 200:
        return None
    return r.json()["message"]


def make_filename(meta):
    authors = meta.get("author", [])
    surname = authors[0]["family"] if authors else "Unknown"

    year = None
    for key in ("published-print", "published-online", "created"):
        if key in meta:
            year = str(meta[key]["date-parts"][0][0])
            break
    year = year or "nd"

    title = meta.get("title", ["untitled"])[0]
    words = re.sub(r"[^\w\s]", "", title).split()[:3]
    slug = "_".join(w.capitalize() for w in words)

    return f"{surname}_{year}_{slug}.pdf"


def collection_items_by_doi(zot, collection_key):
    items = zot.collection_items(collection_key, itemType="-attachment")
    out = {}
    for it in items:
        doi = it["data"].get("DOI")
        if doi:
            children = zot.children(it["key"])
            has_pdf = any(
                ch["data"].get("contentType") == "application/pdf" for ch in children
            )
            out[doi] = {"key": it["key"], "has_pdf": has_pdf}
    return out


def find_or_create_collection(zot, name):
    for c in zot.collections():
        if c["data"]["name"] == name:
            return c["key"]
    resp = zot.create_collection([{"name": name}])
    return resp["successful"]["0"]["data"]["key"]


def build_item(meta, collection_key):
    creators = []
    for a in meta.get("author", []):
        creators.append({
            "creatorType": "author",
            "firstName": a.get("given", ""),
            "lastName": a.get("family", ""),
        })

    date = ""
    for key in ("published-print", "published-online", "created"):
        if key in meta:
            parts = meta[key]["date-parts"][0]
            date = "-".join(str(p) for p in parts)
            break

    container = meta.get("container-title", [])

    return {
        "itemType": "journalArticle",
        "title": meta.get("title", [""])[0],
        "creators": creators,
        "DOI": meta.get("DOI", ""),
        "date": date,
        "publicationTitle": container[0] if container else "",
        "url": meta.get("URL", ""),
        "collections": [collection_key],
    }


def sync():
    load_dotenv(ROOT / ".env")
    api_key = os.environ["ZOTERO_API_KEY"]
    lib_id = get_library_id(api_key)

    zot = zotero.Zotero(lib_id, "user", api_key)
    coll_key = find_or_create_collection(zot, "wildfire")
    known = collection_items_by_doi(zot, coll_key)

    pdfs = sorted(FILES.glob("*.pdf"))
    if not pdfs:
        print("nenhum PDF em files/")
        return

    for pdf in pdfs:
        print(f"{pdf.name}")

        doi = extract_doi(pdf)
        if not doi:
            print("  sem DOI, pulando")
            continue

        meta = crossref_meta(doi)
        if not meta:
            print(f"  crossref falhou pra {doi}")
            continue

        new_name = make_filename(meta)
        new_path = pdf.parent / new_name
        if new_path != pdf and not new_path.exists():
            pdf.rename(new_path)
            print(f"  -> {new_name}")
        elif new_path != pdf:
            new_path = pdf

        existing = known.get(doi)

        if existing and existing["has_pdf"]:
            print(f"  já existe com PDF ({doi})")
            continue

        if existing:
            zot.attachment_simple([str(new_path)], existing["key"])
            print(f"  PDF adicionado ao item existente")
            continue

        item = build_item(meta, coll_key)
        resp = zot.create_items([item])
        parent_key = resp["successful"]["0"]["key"]

        zot.attachment_simple([str(new_path)], parent_key)
        print(f"  criado: {item['title'][:60]}")

    print("sync completo")


if __name__ == "__main__":
    sync()
