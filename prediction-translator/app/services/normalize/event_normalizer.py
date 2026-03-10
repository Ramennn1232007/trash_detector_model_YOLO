from app.services.normalize.category_rules import CATEGORY_RULES


def normalize_event_text(title: str, description: str | None = None) -> dict:
    haystack = f"{title} {description or ''}".lower()
    for rule in CATEGORY_RULES:
        if any(token in haystack for token in rule["match_any"]):
            return {
                "category": rule["category"],
                "subcategory": rule["subcategory"],
                "normalized_key": rule["normalized_key"],
                "region": "us",
            }

    return {
        "category": "other",
        "subcategory": "other",
        "normalized_key": "other_unclassified",
        "region": "global",
    }
