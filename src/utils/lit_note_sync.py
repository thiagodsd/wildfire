import os
import re
import sys
from glob import glob
from pathlib import Path

import pymupdf4llm
import requests
from dotenv import load_dotenv
from pyzotero import zotero

ROOT = Path(__file__).resolve().parents[2]
VAULT = Path.home() / "Documentos" / "Obsidian Vault"
LIT_DIR = VAULT / "02-literature"
ZOTERO_STORAGE = Path.home() / "snap" / "zotero-snap" / "common" / "Zotero" / "storage"

load_dotenv(ROOT / ".env")


def _zot():
    api_key = os.environ["ZOTERO_API_KEY"]
    r = requests.get(f"https://api.zotero.org/keys/{api_key}")
    r.raise_for_status()
    lib_id = str(r.json()["userID"])
    return zotero.Zotero(lib_id, "user", api_key)


def read_note(citekey):
    p = LIT_DIR / f"{citekey}.md"
    txt = p.read_text()
    get = lambda pat: (m.group(1).strip() if (m := re.search(pat, txt)) else None)
    return {
        "path": p, "text": txt,
        "title": get(r"\*\*Título:\*\*\s*(.+)"),
        "year_raw": get(r"\*\*Ano:\*\*\s*(.*)"),
        "tags_line": get(r"\*\*Tags:\*\*\s*(.+)") or "",
    }


def find_item(zot, title):
    query = " ".join(title.split()[:8])
    items = zot.items(q=query)
    prefix = title[:30].lower()
    for it in items:
        if it["data"].get("title", "").lower().startswith(prefix):
            return it["data"], zot.children(it["data"]["key"])
    if items:
        d = items[0]["data"]
        return d, zot.children(d["key"])
    return None, []


def find_pdf(children):
    for ch in children:
        if ch["data"].get("contentType") != "application/pdf":
            continue
        folder = ZOTERO_STORAGE / ch["key"]
        pdfs = glob(str(folder / "*.pdf"))
        if pdfs:
            return pdfs[0]
    return None


def pdf_pages(pdf_path):
    import fitz
    return fitz.open(pdf_path).page_count


def extract_text(pdf_path, pages=None):
    return pymupdf4llm.to_markdown(pdf_path, pages=pages)


def dump(citekey, n=5):
    note = read_note(citekey)
    zot = _zot()
    item, children = find_item(zot, note["title"])

    if not item:
        print(f"nao achei: {note['title'][:60]}")
        return

    year_m = re.search(r"(\d{4})", item.get("date", ""))
    year = year_m.group(1) if year_m else "?"

    print(f"=== {citekey} ===")
    print(f"title: {item['title']}")
    print(f"year (zotero): {year}  |  year (note): {note['year_raw']}")
    print(f"doi: {item.get('DOI', '')}")
    print(f"tags na nota: {note['tags_line']}")
    print()

    pdf = find_pdf(children)
    if not pdf:
        print("pdf nao encontrado no storage local")
        abstract = item.get("abstractNote", "")
        if abstract:
            print(f"\n--- abstract ---\n{abstract}")
        return

    total = pdf_pages(pdf)
    first = list(range(min(n, total)))
    last = list(range(max(total - n, n), total))
    pages = sorted(set(first + last))

    md = extract_text(pdf, pages=pages)
    print(f"--- pdf: {Path(pdf).name} | {total}p, reading {len(pages)} ---\n")
    print(md)


def patch(citekey, year=None, tags=None, resumo=None):
    note = read_note(citekey)
    txt = note["text"]

    if year and note["year_raw"] is not None:
        txt = txt.replace(f"**Ano:** {note['year_raw']}", f"**Ano:** {year}")

    if tags:
        existing = set(re.findall(r"#([\w/\-]+)", note["tags_line"]))
        new = [t for t in tags if t not in existing]
        if new:
            extra = " ".join(f"#{t}" for t in new)
            txt = txt.replace(
                f"**Tags:** {note['tags_line']}",
                f"**Tags:** {note['tags_line']} {extra}",
            )

    if resumo:
        txt = re.sub(
            r"(## Resumo\n).*",
            rf"\g<1>{resumo}",
            txt, count=1, flags=re.DOTALL,
        )

    note["path"].write_text(txt)
    print(f"atualizado: {citekey}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("uso:")
        print(f"  {sys.argv[0]} dump <citekey> [-n PAGES]")
        print(f"  {sys.argv[0]} patch <citekey> [--year YYYY] [--tag TAG ...] [--resumo 'texto']")
        sys.exit(1)

    cmd, ck = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]

    if cmd == "dump":
        n = 5
        if "-n" in args:
            n = int(args[args.index("-n") + 1])
        dump(ck, n=n)

    elif cmd == "patch":
        yr, resumo = None, None
        if "--year" in args:
            yr = args[args.index("--year") + 1]
        if "--resumo" in args:
            resumo = args[args.index("--resumo") + 1]
        tgs = []
        i = 0
        while i < len(args):
            if args[i] == "--tag" and i + 1 < len(args):
                tgs.append(args[i + 1])
                i += 2
            else:
                i += 1
        patch(ck, year=yr, tags=tgs or None, resumo=resumo)
