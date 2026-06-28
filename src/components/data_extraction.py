import pandas as pd

def extract_metadata(text, academic_year):
    import re

    college_match = re.search(
        r'^\s*(\d{4})\s*-\s*(.+)$',
        text,
        re.MULTILINE
    )

    branch_match = re.search(
        r'(\d{9})\s*-\s*(.+)',
        text
    )

    status_match = re.search(
        r'Status:\s*(.+)',
        text
    )

    metadata = {
        "academic_year": academic_year,
        "college_code": college_match.group(1) if college_match else None,
        "college_name": college_match.group(2).strip() if college_match else None,
        "branch_code": branch_match.group(1) if branch_match else None,
        "branch_name": branch_match.group(2).strip() if branch_match else None,
        "status": status_match.group(1).strip() if status_match else None
    }

    return metadata


def extract_table(table, metadata):
    rows = []

    if table is None or len(table) < 2:
        return pd.DataFrame()

    headers = table[0][1:]
    stage = table[1][0]
    values = table[1][1:]

    for category, value in zip(headers, values):

        if value is None:
            continue

        merit_rank = None
        percentile = None

        parts = value.split("\n")

        if len(parts) == 2:
            merit_rank = parts[0]
            percentile = parts[1].replace("(", "").replace(")", "")

        rows.append({
            **metadata,
            "seat_category": category,
            "stage": stage,
            "merit_rank": merit_rank,
            "percentile": percentile
        })

    return pd.DataFrame(rows)