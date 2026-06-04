from tavily import TavilyClient

TAVILY_API_KEY = ""

def _run_search(client: TavilyClient, query: str, max_results: int = 4) -> str:
    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results
        )
        results = response.get("results", [])
        if not results:
            return ""
        block = ""
        for result in results:
            block += f"SOURCE_URL: {result['url']}\n"
            block += f"CONTENT: {result['content']}\n"
            block += f"---\n"
        return block
    except Exception as e:
        return f"Search error for query '{query}': {str(e)}\n"


def search_company_web(company_name: str, company_type: str = "unknown") -> str:
    """
    Runs multiple targeted searches based on company type.
    Returns a single combined context string for Claude.
    """
    if not company_name:
        return "ERROR: No company name provided."

    print(f"  Searching general context for: {company_name}...")
    client = TavilyClient(api_key=TAVILY_API_KEY)

    queries = [
        f"{company_name} company overview business segments",
        f"{company_name} products manufacturing capabilities",
    ]

    if company_type == "listed":
        queries += [
            f"{company_name} annual report investor presentation revenue EBITDA",
            f"{company_name} financial performance operating margin",
        ]
    else:
        queries += [
            f"{company_name} MCA filing annual turnover revenue",
            f"{company_name} annual report 2023 2024 financial performance",
        ]

    context_block = f"--- GENERAL WEB SEARCH RESULTS FOR {company_name.upper()} ---\n\n"
    for query in queries:
        context_block += _run_search(client, query)

    return context_block


def search_clients(company_name: str) -> str:
    """
    Dedicated client discovery search.
    Uses supplier-specific queries to surface OEM relationships
    that general searches miss.
    """
    if not company_name:
        return "ERROR: No company name provided."

    print(f"  Searching client data for: {company_name}...")
    client = TavilyClient(api_key=TAVILY_API_KEY)

    queries = [
        f"{company_name} supplies to which OEM customers clients",
        f"{company_name} supplier partnership contract award",
        f"who are the major clients of {company_name}",
        f"{company_name} Maruti Toyota Hyundai Tata Mahindra Honda supplier",
    ]

    context_block = f"--- CLIENT DISCOVERY SEARCH RESULTS FOR {company_name.upper()} ---\n\n"
    for query in queries:
        context_block += _run_search(client, query)

    return context_block


# Quick test
if __name__ == "__main__":
    print("Testing Bharat Forge (listed)...")
    print(search_company_web("Bharat Forge Limited", company_type="listed"))
    print(search_clients("Bharat Forge Limited"))

    print("\n" + "-" * 50 + "\n")

    print("Testing Brakes India (private)...")
    print(search_company_web("Brakes India Private Limited", company_type="private"))
    print(search_clients("Brakes India Private Limited"))