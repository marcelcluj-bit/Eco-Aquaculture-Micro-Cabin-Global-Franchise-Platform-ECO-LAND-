import os
from google import genai
from google.genai import types

def analyze_eco_site_feasibility(region: str, land_cost_eur: float, water_access_type: str) -> str:
    """
    Uses Gemini AI to perform a preliminary feasibility, SWOT, and stakeholder analysis 
    for a 1-Hectare eco-aquaculture project node.
    """
    # Initialize the Gemini client (expects GEMINI_API_KEY environment variable)
    client = genai.Client()

    prompt = f"""
    You are an expert project architect and EU grant / global infrastructure consultant.
    Perform a feasibility analysis for a 1-Hectare project in {region}:
    - Land Cost: €{land_cost_eur}
    - Water Body Type: {water_access_type}
    - Model: 20 plots of 5 Ares each, equipped with €1,000 modular wooden cabins, sold at €6,000/plot.
    
    Please provide:
    1. Key environmental & zoning risk assessment (Ishikawa-style root causes).
    2. Estimated municipal economic benefits (property tax, tourism boost).
    3. Recommendations for Web3 tokenized franchise integration in this specific region.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    return response.text

if __name__ == "__main__":
    # Example execution for an EU (Romania) site
    region_target = "Cluj-Napoca / Transylvania Region (EU)"
    print(f"--- Running Gemini AI Feasibility Analysis for {region_target} ---")
    
    analysis_report = analyze_eco_site_feasibility(
        region=region_target,
        land_cost_eur=15000.0,
        water_access_type="Pisciculture lake / Inland river basin"
    )
    print(analysis_report)
