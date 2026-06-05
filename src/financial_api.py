import yfinance as yf
import pandas as pd

KEY_METRICS = [
    "Total Revenue",
    "Gross Profit",
    "Operating Income",
    "EBITDA",
    "EBIT",
    "Net Income",
    "Diluted EPS",
    "Interest Expense",
    "Tax Provision",
    "Normalized EBITDA",
]

EPS_METRICS = ["Diluted EPS", "Basic EPS"]

def fetch_financial_data(ticker_symbol: str) -> str:
    """
    Fetches key income statement metrics from Yahoo Finance.
    Automatically detects currency and scales to the most readable unit.
    EPS is kept in raw currency units, all other metrics scaled to Crores/Millions.
    """
    if not ticker_symbol:
        return "NULL: No ticker provided. Company is likely private or unlisted."

    try:
        company = yf.Ticker(ticker_symbol)
        financials = company.financials

        if financials is None or financials.empty:
            return f"NULL: Yahoo Finance returned empty data for ticker '{ticker_symbol}'."

        # Detect currency automatically
        info = company.fast_info
        currency = getattr(info, "currency", "INR")

        currency_symbols = {
            "INR": "₹",
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
        }
        currency_symbol = currency_symbols.get(currency, currency)

        # Get last 4 years
        available_years = financials.iloc[:, :4]

        # Filter to key metrics only
        filtered = available_years[
            available_years.index.isin(KEY_METRICS)
        ]
        filtered = filtered.reindex(
            [m for m in KEY_METRICS if m in filtered.index]
        )

        # Separate EPS rows from the rest — EPS must not be scaled
        eps_data = filtered[filtered.index.isin(EPS_METRICS)].round(2)
        non_eps_data = filtered[~filtered.index.isin(EPS_METRICS)]

        # Scale non-EPS rows based on currency
        if currency == "INR":
            scaled_non_eps = (non_eps_data / 1e7).round(2)
            unit_label = f"{currency_symbol} Crores"
        else:
            scaled_non_eps = (non_eps_data / 1e6).round(2)
            unit_label = f"{currency_symbol} Millions"

        scaled = pd.concat([scaled_non_eps, eps_data])
        scaled = scaled.reindex([m for m in KEY_METRICS if m in scaled.index])

        markdown_table = scaled.to_markdown()

        return (
            f"Source: Yahoo Finance API | Ticker: {ticker_symbol} | "
            f"Currency: {currency} | Unit: {unit_label}\n"
            f"Note: EPS figures are in {currency_symbol} per share (not scaled)\n\n"
            f"All figures in {unit_label} unless noted\n\n"
            f"{markdown_table}"
        )

    except Exception as e:
        return f"ERROR: Could not fetch financial data for '{ticker_symbol}'. Reason: {str(e)}"


# Quick test
if __name__ == "__main__":
    print("Testing Bharat Forge...")
    print(fetch_financial_data("BHARATFORG.NS"))

    print("\nTesting private company fallback...")
    print(fetch_financial_data(""))
