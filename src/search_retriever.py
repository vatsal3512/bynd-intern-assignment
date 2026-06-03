from tavily import TavilyClient

def search_company_web(company_name: str) -> str:
    """
    Searches the web for public company information using Tavily API.
    Optimized for LLM context retrieval.
    """
    if not company_name:
        return "ERROR: No company name provided for web search."
        
    print(f"Searching web sources for: {company_name}...")
    
    try:
        client = TavilyClient(api_key="")
        
        query = f"{company_name} company overview, key products, notable clients and customers"
        
        response = client.search(
            query=query, 
            search_depth="advanced", 
            max_results=4
        )
        
        results = response.get('results', [])
        if not results:
            return f"No public search records found for '{company_name}'. Verification status: Unlisted / Private."
            
        # Format the results cleanly for Claude
        context_block = f"--- WEB SEARCH RESULTS FOR {company_name.upper()} ---\n"
        for i, result in enumerate(results, 1):
            context_block += f"[Source URL: {result['url']}]\n"
            context_block += f"Content: {result['content']}\n\n"
            
        return context_block

    except Exception as e:
        return f"NOTICE: Search pipeline encountered an issue: {str(e)}."

# Quick testing sandbox
if __name__ == "__main__":
    print("Testing Data-Rich Company (Bharat Forge)...")
    print(search_company_web("Bharat Forge Limited"))
    
    print("\n" + "-" * 50 + "\n")
    
    print("Testing Data-Sparse Company (Brakes India)...")
    print(search_company_web("Brakes India Private Limited"))