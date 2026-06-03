# Company One-Pager Generator

An automated, data-grounded Retrieval-Augmented Generation (RAG) pipeline that takes a company name and an optional stock ticker to produce a structured, fully-sourced, and confidence-tagged briefing "one-pager".

This system is engineered with strict constraint handling and zero-hallucination degradation to remain reliable across both data-rich and data-sparse corporate environments.

---

## How to Run the System

### 1. Prerequisites

Ensure you have **Python 3.10 or higher** installed on your operating system.

### 2. Clone the Workspace

Clone this repository to your local machine and navigate into the root directory:

```cmd
git clone https://github.com/vatsal3512/bynd-intern-assignment.git
cd bynd-intern-assignment
```

### 3. Install Project Dependencies

```cmd
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Security Failsafe)

To prevent API key leakage and comply with industry security standards, the system dynamically loads keys from your environment rather than hardcoding them into scripts. Set your access tokens in your terminal:

```cmd
setx ANTHROPIC_API_KEY "your_anthropic_api_key_here"
setx TAVILY_API_KEY "your_tavily_api_key_here"
```

> **Note:** After running `setx` on Windows, you must restart your command prompt or code editor terminal for the system context variables to refresh.

### 5. Execute the Core Pipeline

Run the master orchestration script to dynamically look up data and generate reports for the target test suite:

```cmd
python main.py
```

The completed profiles will be saved immediately as clean Markdown files inside the `/data` folder.

---

## System Architecture & Design Rationale

The generator is designed as a decoupled, multi-stage pipeline to isolate structured factual engines from unstructured semantic scrapers:

```
[Company Name / Ticker]
          │
          ├──► Financial Registry Engine (yfinance) ──► Programmatic Multi-Year Tables
          └──► Web Research Engine (Tavily API)    ──► Semantic Text Snippets & Source URLs
          │
          ▼
   Factual Ingestion & Context Structuring Layer
          │
          ▼
   Inference & Fact-Grounding Engine (Claude)     ──► Strict Zero-Temperature Processing
          │
          ▼
   Structured Markdown Outputs (/data)             ──► Fully Sourced & Confidence Tagged
```

### 1. Financial Registry Layer (`src/financial_api.py`)

**Mechanism:** Leverages `yfinance` to programmatically extract financial database rows directly from public market registries if a corporate ticker is present.

**Design Choice:** Bypasses traditional scraping of investor relations pages to eliminate structural breakage. If a firm is unlisted, the registry safely passes an explicit warning marker to prevent pipeline crashes.

### 2. Web Research Engine (`src/search_retriever.py`)

**Mechanism:** Powered by the Tavily API to query and pull clean Markdown content blocks across public filings, media assets, and credit profiles.

**Design Choice:** Raw HTML scraping (e.g., via `requests` or `BeautifulSoup` against search engines) is inherently fragile and highly vulnerable to bot-detection 403 blocks. Tavily handles proxy rotation and strips bloated boilerplate elements, exposing high-density semantic facts directly to the model.

### 3. Synthesis & Fact-Grounding Engine (`src/generator.py`)

**Mechanism:** Integrated with `claude-sonnet-4-5-20250929` running at a hard deterministic `temperature=0.0`.

**Design Choice:** Claude Sonnet offers top-tier compliance when responding to complex text injection and strict systemic constraints. Setting the temperature to absolute zero forces the engine to act strictly as a data compiler rather than an imaginative language generator, drastically cutting down on potential hallucinations.
