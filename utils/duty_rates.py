"""
HTS Dashboard - Duty Rate Information

This module provides duty rate categorization for HTS codes.
In a production system, this would integrate with a real duty rate API.
"""


# Mock duty rate data - in production, this would come from an API or database
DUTY_RATE_MAP = {
    # Common patterns for demonstration
    "0101": "Free",      # Live horses
    "0102": "Free",      # Live cattle
    "0201": "Low",       # Beef
    "0301": "Free",      # Live fish
    "0401": "Low",       # Milk
    "0801": "Free",      # Nuts
    "1001": "Free",      # Wheat
    "3923": "Low",       # Plastic articles (bottles, etc.)
    "3924": "Low",       # Plastic tableware
    "6109": "Medium",    # T-shirts, knitted
    "6205": "Medium",    # Men's shirts
    "7318": "Low",       # Screws, bolts
    "8471": "Free",      # Computers
    "8517": "Free",      # Telephones
    "9401": "Free",      # Seats
}


def get_duty_category(hts_code: str) -> str:
    """
    Get the duty rate category for an HTS code.
    
    Args:
        hts_code: HTS code (e.g., "3923.30.00")
    
    Returns:
        Duty category: "Free", "Low", "Medium", or "High"
    """
    
    # Try to match by first 4 digits
    if len(hts_code) >= 4:
        prefix = hts_code[:4].replace(".", "")
        if prefix in DUTY_RATE_MAP:
            return DUTY_RATE_MAP[prefix]
    
    # Try first 2 digits (chapter)
    if len(hts_code) >= 2:
        chapter = hts_code[:2]
        
        # General patterns by chapter
        if chapter in ["01", "02", "03", "04", "05"]:  # Live animals, meat, fish
            return "Low"
        elif chapter in ["84", "85"]:  # Machinery, electrical
            return "Free"
        elif chapter in ["61", "62", "63"]:  # Textiles, apparel
            return "Medium"
        elif chapter in ["71"]:  # Precious metals
            return "High"
    
    # Default to Medium if unknown
    return "Medium"


def get_duty_description(category: str) -> str:
    """
    Get a human-readable description of the duty category.
    
    Args:
        category: Duty category ("Free", "Low", "Medium", "High")
    
    Returns:
        Description string
    """
    descriptions = {
        "Free": "Duty-free entry",
        "Low": "Low duty rate (typically <5%)",
        "Medium": "Moderate duty rate (typically 5-15%)",
        "High": "High duty rate (typically >15%)",
    }
    
    return descriptions.get(category, "Duty rate varies")


def estimate_duty_rate(hts_code: str) -> dict:
    """
    Estimate duty rate information for an HTS code.
    
    Args:
        hts_code: HTS code
    
    Returns:
        Dictionary with category, description, and estimated range
    """
    
    category = get_duty_category(hts_code)
    description = get_duty_description(category)
    
    # Estimated rate ranges
    rate_ranges = {
        "Free": "0%",
        "Low": "0-5%",
        "Medium": "5-15%",
        "High": "15%+",
    }
    
    return {
        "category": category,
        "description": description,
        "estimated_range": rate_ranges.get(category, "Varies"),
        "note": "⚠️ This is an estimate. Verify actual rates with official HTS database."
    }
