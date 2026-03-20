# refs

## ml

modelos de predição - clássico, dl convencional, aplicações regionais

- Di Giuseppe et al (2025) - "Global data-driven prediction of fire activity", modelo PoF do ECMWF/Copernicus. Nature Comms. https://www.nature.com/articles/s41467-025-58097-7
- He et al (2024) - ConvLSTM com atenção canal-espacial + Visual Transformer, predição diária China Oriental. Ecological Indicators. TODO -> https://ieeexplore.ieee.org/abstract/document/10919175
- Mambile et al (2025) - ConvLSTM no Monte Kilimanjaro, contexto tropical. Natural Hazards Research. https://www.sciencedirect.com/science/article/pii/S2666592124000933?via%3Dihub
- Marjani et al (2024) - CNN-BiLSTM spread diário Austrália, F1 0.64. Remote Sensing. https://www.mdpi.com/2072-4292/16/8/1467
- Illarionova et al (2025) - comparação RF/XGBoost/ConvLSTM/Autoencoder/etc, 5 dias. Scientific Reports. https://www.nature.com/articles/s41598-024-52821-x
- Zhu et al (2025) - SimAM Full Attention network, risco global, teleconexões. Climate Dynamics. sem doi
- Zhou et al (2025) - Swin-UNet vs UNet complementares pra wildfire spread. JGR Machine Learning. doi:10.1029/2024JH000409
- Lahrichi et al (2025) - Res18-Unet + focal loss, 37% melhoria em AP. aceito WACV. arxiv:2502.12003
- Shadrin et al (2024) - transfer learning wildfire Rússia, F1 cai de 0.85→0.65 norte→sul. Sci Reports. doi:10.1038/s41598-024-52821-x
- Zhang et al (2024) - CNN + CMIP6 projetando queimadas globais, aumento no hemisfério sul. Earth's Future. doi:10.1029/2023EF004088
- Jiang et al (2024) - CNN sazonal Guangdong, AUC 0.962, GDP como fator chave. Int J Applied Earth Obs. doi:10.1016/j.jag.2024.103750
- Ji et al (2024) - SLA-ConvLSTM (Static Location-Aware), teleconexões globais. Forests. doi:10.3390/f15010216
- Zhang & Wang (2025) - predição sazonal Yunnan, 6 modelos ML. npj Natural Hazards. doi:10.1038/s44304-025-00112-4
- Liu et al (2024) - LightGBM + bayesian optimization em Sichuan/Yunnan. Emergency Mgmt Sci Tech. doi:10.48130/emst-0024-0026
- Eaturu & Vadrevu (2025) - comparação 6 arquiteturas, 10 países SE asiático. Sci Reports. doi:10.1038/s41598-025-00628-9
- Karlsson et al (2025) - MODIS vs VIIRS next-day Austrália, VIIRS melhor. doi:10.1007/978-3-031-95918-9_5
- Andrianarivony et al (2025) - APAU-Net (Atrous Pyramid Attention U-Net), F1 0.72, mIoU 0.635. Science of Remote Sensing. sem doi
- Zhu et al (2025) - YOLOv8 melhorado c/ EMA e AgentAttention, detecção fogo/fumaça drone. Sci Reports. doi:10.1038/s41598-025-86239-w
- Kim et al (2025) - DL vs FARSITE no caso Maui 2023. Natural Hazards. doi:10.1007/s11069-025-07807-x
- Oliveira et al (2023) - FISC-Cerrado, sistema operacional de predição no Cerrado, 65-89% concordância. Sci Reports. doi:10.1038/s41598-023-30560-9


## ai

fronteira - PINNs, GNNs, modelos generativos, sim2real, incerteza

- Vogiatzoglou et al (2025) - primeiro (e único) paper de PINN pra wildfire, aprendizado de parâmetros de propagação. CMAME. arxiv:2406.14591
- Michail et al (2025) - FireCastNet, GNN tipo GraphCast, Terra como grafo. Sci Reports. doi:10.1038/s41598-025-30645-7
- Zhao et al (2024) - GNN causal com PCMCI pra adjacência, 8 dias Mediterrâneo. ICLR workshop. arxiv:2403.08414
- Rösch et al (2024) - STGNN com grids hexagonais H3, spread na Europa. Fire. doi:10.3390/fire7060207
- GraphFire-X (2025) - GNN + probabilidades físicas de convecção/radiação/brasas, preprint. arxiv:2512.20813
- Tong & Quaife (2025) - NN pra dinâmica de fogo, problema direto + inverso (calibração real-time). Env Modelling & Software. doi:10.1016/j.envsoft.2024.106253
- Li et al (2024) - Sim2Real-Fire, transformer cross-attention multi-modal, 1M simulados → real. NeurIPS
- Dahan et al (2026) - difusão probabilística pra spread, gera ensembles de cenários. Geosci Model Dev. doi:10.5194/gmd-19-1027-2026
- Google/USFS - surrogate DL pra substituir Rothermel, 550M+ exemplos, ~1000x speedup. sem paper formal ainda
- Schwerdtner et al (2024) - UQ multi-fidelity wildfire-atmosfera, 3 meses → 3 horas treinamento. PNAS Nexus. doi:10.1093/pnasnexus/pgae554
- Kondylatos et al (2025) - BBB vs MC Dropout vs Deep Ensembles, Mediterrâneo next-day. NeurIPS workshop. sem doi
- Chakravarty et al (2025) - incerteza espacial em buffer 20-60m ao redor do perímetro. NeurIPS. arxiv:2510.09666
- Pimentel et al (2024) - GLMM bayesiano espaço-temporal, 2.2M focos INPE, Cerrado mais afetado. Sci Reports
- Legrand et al (2024) - bayesiano hierárquico (Poisson + Pareto generalizado) c/ INLA-SPDE. Computo


## datasets

benchmarks, reviews, dados

- Zhao et al (2025) - TS-SatFire, 3552 imagens VIIRS multi-espectrais, 3 tarefas. Scientific Data. doi:10.1038/s41597-025-06271-3
- Porta et al (2025) - CanadaFireSat, benchmark alta resolução ~100m Sentinel-2. arxiv:2506.08690
- Lahrichi et al (2025) - WSTS+, estende horizonte temporal do WildfireSpreadTS. arxiv:2502.12003
- Li et al (2024) - Sim2Real-Fire dataset, 1M simulados + 1K reais. NeurIPS
- Xu et al (2025) - review abrangente DL + remote sensing pra wildfire, 138 estudos. ISPRS JPRS. doi:10.1016/j.isprsjprs.2025.06.002
- Yarmohammadian et al (2025) - review de physics-informed surrogate modelling em fire engineering. Applied Sciences. doi:10.3390/app15158740
