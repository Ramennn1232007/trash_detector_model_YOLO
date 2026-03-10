CATEGORY_RULES = [
    {
        "match_any": ["fed", "rate cut", "fomc"],
        "category": "rates",
        "subcategory": "fed_cut",
        "normalized_key": "us_fed_cut_near_term",
    },
    {
        "match_any": ["oil", "brent", "wti", "shipping disruption"],
        "category": "energy",
        "subcategory": "oil_shock",
        "normalized_key": "oil_shock_near_term",
    },
    {
        "match_any": ["recession", "hard landing", "growth slowdown"],
        "category": "macro",
        "subcategory": "recession",
        "normalized_key": "us_recession_odds",
    },
]
