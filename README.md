# Company One-Pager Generator

A pipeline that takes a company name and generates a structured briefing document — company overview, financials, products, and clients — with every claim cited to a real source.

---

## How to Run

### 1. Requirements

Python 3.10 or higher.

### 2. Clone the repo

```cmd
git clone https://github.com/vatsal3512/bynd-intern-assignment.git
cd bynd-intern-assignment
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Add your API keys

Open `src/generator.py` and paste your Anthropic key:

```python
client = Anthropic(api_key="your_anthropic_api_key_here")
```

Open `src/search_retriever.py` and paste your Tavily key:

```python
TAVILY_API_KEY = "your_tavily_api_key_here"
```

### 5. Run

```cmd
python main.py
```

Output files are saved as Markdown in the `/data` folder.

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

Pulls income statement data from Yahoo Finance for listed companies. Automatically detects the currency (INR, USD etc.) and converts to the right unit — crores for Indian companies, millions for others. EPS is kept separate so it does not get incorrectly scaled. If the company has no ticker, it returns a clear null signal instead of crashing.

### 2. Web Research Engine (`src/search_retriever.py`)

Runs multiple targeted Tavily searches instead of one generic query. General searches cover company overview and products. A separate dedicated search looks specifically for client and supplier relationships because client names almost never appear in generic search results. Each result keeps its source URL tightly bound to its content so Claude can cite it.

### 3. Synthesis & Fact-Grounding Engine (`src/generator.py`)

Sends all the collected context to Claude with strict instructions — cite every single claim with the exact source URL, and if something cannot be traced to a source, leave it out entirely. Runs at temperature 0.0 so it does not guess or fill gaps. Automatically detects whether a company is listed or private and adjusts the financial section accordingly.
