import re
from anthropic import Anthropic
from .search_retriever import search_company_web, search_clients
from .financial_api import fetch_financial_data

client = Anthropic(api_key="")


def resolve_ticker(company_name: str) -> str | None:
    """
    Asks Claude to resolve company name to stock ticker.
    Returns None if private or unlisted.
    """
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=20,
        temperature=0.0,
        messages=[{
            "role": "user",
            "content": (
                f"What is the stock ticker symbol for '{company_name}'? "
                "If it is publicly listed on NSE or BSE, reply with ONLY the ticker "
                "(e.g. BHARATFORG.NS or TATAMOTORS.NS). "
                "If it is private or unlisted, reply with only the word NULL. "
                "No explanation. No punctuation. Just the ticker or NULL."
            )
        }]
    )
    result = response.content[0].text.strip()
    return None if result.upper() == "NULL" else result


def detect_company_type(financial_context: str) -> str:
    """
    Returns 'listed' or 'private' based on financial API response.
    """
    null_indicators = ["null", "not found", "unavailable", "no data", "error", "empty"]
    if any(indicator in financial_context.lower() for indicator in null_indicators):
        return "private"
    return "listed"


def build_system_prompt(company_type: str) -> str:
    """
    Builds system prompt branched on company type.
    """
    financial_instructions = (
    """
    FINANCIAL OVERVIEW — LISTED COMPANY:
    - Use the multi-year financial data from Yahoo Finance provided below.
    - The unit and currency are explicitly stated in the data header — use them
      exactly as provided. Do not convert, rescale, or relabel any numbers.
    - YOU MUST include EVERY single row from the financial data table provided.
      Do not drop, summarize, or skip any metric.
    - Build a clean markdown table with fiscal years as columns.
    - The table header must show the unit exactly as stated in the data.
    - Add 3-4 bullet point highlights below the table (revenue growth %,
      net income growth, EBITDA margin trend).
    - Do not add or invent any metric not present in the data.
    """
    if company_type == "listed"
    else
    """
    FINANCIAL OVERVIEW — PRIVATE COMPANY:
    - No stock API data is available for this company.
    - Search the web context and client context carefully for any numbers —
      revenue, turnover, capacity, funding, growth targets, group financials.
    - If multi-year data exists, build a comparative markdown table.
    - If only scattered figures exist, build a table with columns:
      Metric | Value | Source | Confidence.
    - Only write "Data not found in available sources" if the context contains
      absolutely zero financial figures or mentions.
    """
)

    return f"""
    You are an expert private equity analyst. Generate a structured company one-pager
    based strictly on the provided context. Do not invent or infer any information
    not explicitly present in the context.

    {financial_instructions}

    ANTI-HALLUCINATION RULES:
    - If a section has no data in the context, write "Data not found in available sources."
    - Do not include image links, logos, or any markdown image syntax.
    - Do not calculate or derive figures not explicitly in the context.

    OUTPUT FORMAT:
    Return clean markdown with exactly these four sections, fully completed,
    no truncation:

    ## Company Overview
    ## Financial Overview
    ## Select Products
    ## Select Clients
    """


def generate_one_pager(company_name: str, ticker: str = None) -> str:
    """
    Full pipeline: resolves ticker, fetches data, generates one-pager.
    Returns a clean markdown string.
    """

    # Step 1 — resolve ticker if not passed manually
    if ticker is None or ticker == "":
        print(f"[{company_name}] Step 1 — Resolving ticker...")
        ticker = resolve_ticker(company_name)
        print(f"  Ticker: {ticker if ticker else 'Not found (private company)'}")
    else:
        print(f"[{company_name}] Step 1 — Ticker provided manually: {ticker}")

    # Step 2 — fetch financial data
    print(f"[{company_name}] Step 2 — Fetching financial data...")
    financial_context = (
        fetch_financial_data(ticker)
        if ticker
        else "NULL: Private company. No ticker available."
    )

    # Step 3 — detect company type
    company_type = detect_company_type(financial_context)
    print(f"  Detected company type: {company_type}")

    # Step 4 — fetch web context
    print(f"[{company_name}] Step 3 — Fetching web context...")
    web_context = search_company_web(company_name, company_type=company_type)

    # Step 5 — dedicated client search
    print(f"[{company_name}] Step 4 — Fetching client data...")
    client_context = search_clients(company_name)

    # Step 6 — generate with Claude
    print(f"[{company_name}] Step 5 — Generating one-pager with Claude...")
    system_prompt = build_system_prompt(company_type)
    user_prompt = f"""
    Company: {company_name}
    Company Type: {company_type}

    FINANCIAL DATA:
    {financial_context}

    GENERAL WEB CONTEXT:
    {web_context}

    CLIENT DISCOVERY DATA:
    {client_context}

    CITATION INSTRUCTIONS:
    The web context above contains blocks formatted as:
    SOURCE_URL: <url>
    CONTENT: <text>

    Every claim you make must be traced to one of these SOURCE_URLs.
    Format every citation exactly as: [Source: <the exact SOURCE_URL>] [Confidence: High/Medium/Low]
    If a claim cannot be traced to any SOURCE_URL above, do not include it.
    Generate the one-pager now following all rules.
    """

   
    

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            temperature=0.0,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        raw_output = response.content[0].text

        if len(raw_output.strip()) < 300:
            print(f"  WARNING: Output is suspiciously short ({len(raw_output)} chars).")

        return raw_output

    except Exception as e:
        print(f"[{company_name}] ERROR: {e}")
        return f"# {company_name} — Generation Failed\n\nError: {str(e)}"
