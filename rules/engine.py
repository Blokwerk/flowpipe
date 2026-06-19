"""
Rules engine — the if/then brain of the pipeline.

A Rule is just a function: (row) -> bool
An Action is just a function: (row) -> row  (transforms the data)

Add your business rules here. They read like plain English.
"""


def flag_large_orders(row):
    """Flag any order over 1 million units for approval."""
    if row.get("quantity", 0) > 1_000_000:
        row["status"] = "needs_approval"
        row["flag"] = "LARGE_ORDER"
    return row


def calculate_total(row):
    """Add a total_cost column to every row."""
    row["total_cost"] = round(row.get("quantity", 0) * row.get("unit_price", 0.0), 2)
    return row


def route_by_vendor(row):
    """Tag rows with a department based on the vendor name."""
    vendor = row.get("vendor", "").lower()
    if "boeing" in vendor:
        row["department"] = "aerospace_procurement"
    elif "french" in vendor:
        row["department"] = "food_manufacturing"
    elif "acme" in vendor:
        row["department"] = "general_supply"
    else:
        row["department"] = "unclassified"
    return row


# The master rule list — order matters, runs top to bottom
RULES = [
    calculate_total,
    flag_large_orders,
    route_by_vendor,
]


def apply(row):
    """Run every rule against a single row and return the transformed row."""
    for rule in RULES:
        row = rule(row)
    return row
