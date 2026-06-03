import os
from src.generator import generate_one_pager

def main():
    # Define the two test companies
    companies = [
        {"name": "Bharat Forge Limited", "ticker": "BHARATFORG.NS"},
        {"name": "Brakes India Private Limited", "ticker": ""},
    ]
    
    
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)
    
    for company in companies:
        print(f"\n==================================================")
        print(f"Processing: {company['name']}")
        print(f"==================================================")
        
        # Run the pipeline
        markdown_output = generate_one_pager(company["name"], company["ticker"])
        
        # Format the filename safely
        filename = company["name"].lower().replace(" ", "_") + "_output.md"
        filepath = os.path.join("data", filename)
        
        # Save the result to a markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(markdown_output)
            
        print(f" Success! Report saved to {filepath}")

if __name__ == "__main__":
    main()