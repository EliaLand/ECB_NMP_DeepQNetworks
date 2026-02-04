# ECB NMP DeepQNetworks
<div align="center">
<img src="Images/MB-3D.png" alt="System Architecture" width="500"/>


<div align="left">

# Project VEILLE – NYrepo AI Experimentation - cBM25RCRAG FOMC Report Generation

Welcome to the repository for **Project VEILLE**, an AI-powered system designed and developed at the **Banque de France, New York Representative Office**. Project VEILLE is an AI-powered pipeline designed to generate real-time analytical reports, capturing the deep economic meaning of the FOMC speeches periodically held by the US Federal Reserve. It combines cBM25-based reranked contextual RAG, Langchain agents, and dynamic scraping of 150+ financial sources for high-relevance retrieval and generation. Deployed within the Banque de France environment, VEILLE produces human-aligned outputs within minutes, supporting fast, accurate policy analysis at the BdF New York Representative Office.

---

## Repo Structure

```
│
├── Documentation
│
├── projectVEILLE_n8n_backup/                           # Backup of n8n workflows and associated logic
│   │
│   ├── projectVEILLE_cbm25RCRAGmodel/                  # Core RAG pipeline combining cBM25 retrieval, reranking, and generation
│   │    ├── Text Training/                             # Data extraction workflows for external sources, FOMC minutes, FOMC BdF-drafted reports
│   │    │   ├── Data retrieval & Manipulation/         # Data manipulation, text cleaning, html to markdown, tokenization & translation 
│   │    │   └── VDB Construct
