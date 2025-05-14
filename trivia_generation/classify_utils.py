def classify_field_out(description):
    """
    Infer if a field_out was a groundout or flyout based on the description.
    """
    desc_lower = description.lower()
    if any(keyword in desc_lower for keyword in ["grounds out", "grounded into"]):
        return "ground_out"
    elif any(keyword in desc_lower for keyword in ["flies out", "fly out", "pops out", "lines out"]):
        return "fly_out"
    else:
        return "field_out"  # fallback

