import yfinance as yf
import pandas as pd

def fetch_financial_data(ticker_symbol: str) -> str:
    """
    Fetches multi-year financial figures (Income Statement) using Yahoo Finance.
    If the company is unlisted or data is missing, returns an honest fallback string.
    """
    if not ticker_symbol:
        return "CRITICAL: No public stock ticker provided. Financial data is unavailable via public market registries."
        
    try:
        # Fetch data using the yfinance ticker
        company = yf.Ticker(ticker_symbol)
        financials = company.financials  # This pulls the annual income statement
        
        if financials is None or financials.empty:
            return f"NOTICE: Public financial registry entries for ticker '{ticker_symbol}' returned empty datasets."
        
        # We slice the last 4 years of data if available to match the GPIL sample format
        available_years = financials.iloc[:, :4]
        
        # Convert the Pandas DataFrame to a clean Markdown table for the LLM to read perfectly
        markdown_table = available_years.to_markdown()
        return markdown_table

    except Exception as e:
        return f"ERROR: Failed to retrieve data from financial registry API. Reason: {str(e)}"

# Quick sandbox test to verify it works locally
if __name__ == "__main__":
    print("Testing Data-Rich Company (Bharat Forge)...")
    print(fetch_financial_data("BHARATFORG.NS"))  # .NS is the Yahoo suffix for the National Stock Exchange of India
    
    print("\nTesting Data-Sparse Company (Brakes India)...")
    print(fetch_financial_data(""))  # Passing empty string because Brakes India is unlisted