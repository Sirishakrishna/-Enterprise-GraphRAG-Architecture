# 🌐 Enterprise GraphRAG Architecture

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Neo4j](https://img.shields.io/badge/Neo4j-Graph_Database-018bff)
![LangChain](https://img.shields.io/badge/LangChain-LLM_Orchestration-green)
![License](https://img.shields.io/badge/License-MIT-purple)

## 📌 The Problem: LLM Hallucinations in the Enterprise
In highly regulated industries (Finance, Healthcare, FMCG), probabilistic Large Language Models (LLMs) cannot be trusted as standalone decision engines. Traditional RAG (Retrieval-Augmented Generation) relying solely on Vector Databases often loses the *relational context* of data, leading to hallucinations and disconnected insights.

## 💡 The Solution: Deterministic Grounding via Knowledge Graphs
This repository demonstrates a production-grade **GraphRAG (Graph Retrieval-Augmented Generation)** architecture. By integrating an LLM agent with an **Enterprise Knowledge Graph (Neo4j)**, we create an AI-native semantic layer. 

Instead of searching for semantic similarity, the LLM translates natural language into a deterministic query (Cypher/SPARQL), retrieving factual ground truth from the ontology before generating an answer.

### 🏗️ Architecture Flow
1. **User Intent Parsing:** User asks a natural language question.
2. **Agentic Routing:** LangChain agent determines if the query requires structural data (Graph) or unstructured text (Vector).
3. **Graph Retrieval (Cypher):** LLM generates a Cypher query mapped to the enterprise ontology.
4. **Deterministic Context:** Neo4j returns factual, multi-hop subgraphs.
5. **Synthesis:** LLM generates a mathematically sound, hallucination-free response.

## 📂 Repository Structure
```text
├── data/                  # Unstructured documents and raw CSVs
├── notebooks/             # Jupyter notebooks for data exploration & ontology design
├── src/                   # Core Python application modules
│   ├── __init__.py
│   ├── graph_builder.py   # ETL pipeline to ingest data into Neo4j
│   ├── llm_agent.py       # LangChain orchestration and Cypher generation
├── tests/                 # Unit tests for Graph queries and LLM evals
├── .gitignore             # Security and cache ignorance rules
├── requirements.txt       # Core dependencies (LangChain, Neo4j, etc.)
└── README.md              # Project documentation
