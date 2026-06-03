import json
from anthropic import Anthropic
from .search_retriever import search_company_web
from .financial_api import fetch_financial_data

client = Anthropic(api_key="")

def generate_one_pager(company_name: str, ticker: str) -> str:
    """
    Orchestrates the RAG pipeline: fetches data, prompts Claude, and returns Markdown.
    """
    print(f"[{company_name}] 1. Fetching financial data...")
    financial_context = fetch_financial_data(ticker)
    
    print(f"[{company_name}] 2. Fetching web context...")
    web_context = search_company_web(company_name)
    
    print(f"[{company_name}] 3. Synthesizing One-Pager with Claude...")
    system_prompt = f"""
    You are an expert private equity analyst assistant. Your task is to generate a highly accurate company one-pager based STRICTLY on the provided context.
    
    NON-NEGOTIABLE RULES FOR CITATIONS & CONFIDENCE:
    1. Every single claim, individual sentence in the overview, financial figure, product, or client MUST end with an explicit inline citation AND a confidence tag.
    2. Format every single data point exactly like this: [Source: <URL, Document Name, or Specific API>] [Confidence: High/Medium/Low].
    3. For the financial table metrics:
       - If the company is listed, explicitly cite the underlying engine provided in the metadata: [Source: Yahoo Finance API] [Confidence: High].
       - Never use vague placeholders like '[Source: Financial Data Table Provided]'. Cite the actual origin.
       
    NON-NEGOTIABLE RULES FOR THE FINANCIAL OVERVIEW (FALLBACK HANDLING):
    4. Listed Companies: Output the complete multi-year table provided by the API.
    5. Unlisted/Private Companies: Because programmatic market registries return NULL for unlisted entities, you MUST deeply analyze the Web Search Data to find any financial data points (such as estimated revenue, revenue shares, capacity figures, or growth targets).
    6. Table Structure Fallback for Unlisted Entities:
       - IF multi-year trends are available in the text, build a comparative multi-year Markdown table.
       - IF multi-year data is missing but isolated financial facts are present, you MUST construct an 'Available Financial Metrics' table with columns: [Metric | Value | Source | Confidence]. Populating this table with scattered data is mandatory if any numbers exist in the text.
       - ONLY output 'Data not found in available sources' if the text contains absolutely zero financial context or numbers.
    
    NON-NEGOTIABLE RULES FOR HONESTY (ANTI-HALLUCINATION):
    7. If a detail is entirely missing from both the API and web search context, DO NOT invent, calculate, or guess it. Write 'Data not found in available sources' explicitly for that specific section or item.
    8. LOGOS & IMAGES: Because the injected context is text-only and does not contain verified image URLs, you MUST cleanly leave all images out. Do NOT hallucinate markdown image links.
    
    OUTPUT FORMAT & COMPLETENESS:
    9. Output clean, structured Markdown matching these four sections exactly. Complete every section without truncation:
       - ## Company Overview
       - ## Financial Overview
       - ## Select Products
       - ## Select Clients
    """
    user_prompt = f"""
    Here is the retrieved context for {company_name}:
    
    FINANCIAL DATA:
    {financial_context}
    
    WEB SEARCH DATA:
    {web_context}
    
    Generate the strict Markdown one-pager now following all compliance rules.
    """
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",  # Automatically points to the newest stable Sonnet engine
            max_tokens=4000,
            temperature=0.0,  # Zero temperature forces absolute adherence to facts without creative guessing
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"Failed to generate one-pager: {str(e)}"