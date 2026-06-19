import csv


def read(filepath):
    """Read a CSV file and return a list of row dicts."""
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            # auto-cast numbers
            cleaned = {}
            for key, val in row.items():
                try:
                    cleaned[key] = int(val)
                except ValueError:
                    try:
                        cleaned[key] = float(val)
                    except ValueError:
                        cleaned[key] = val
            rows.append(cleaned)
    return rows
