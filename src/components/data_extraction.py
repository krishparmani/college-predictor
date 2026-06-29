import pdfplumber
import pandas as pd
import os

def extract_metadata(text, academic_year):
    import re

    college_match = re.search(
        r'^\s*(\d{4,5})\s*-\s*(.+)$',
        text,
        re.MULTILINE
    )

    branch_match = re.search(
        r'(\d{9})\s*-\s*(.+)',
        text
    )

    status_match = re.search(
    r"Status:\s*(.*?)\s*Home University",
    text,
    re.DOTALL
    )

    status = status_match.group(1).strip() if status_match else None

    metadata = {
        "academic_year": academic_year,
        "college_code": college_match.group(1) if college_match else None,
        "college_name": college_match.group(2).strip() if college_match else None,
        "branch_code": branch_match.group(1) if branch_match else None,
        "branch_name": branch_match.group(2).strip() if branch_match else None,
        "status": status
    }

    return metadata


def extract_single_table(table, section_name, metadata):

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
            "section": section_name,
            "category": category,
            "stage": stage,
            "merit_rank": merit_rank,
            "percentile": percentile
        })

    return pd.DataFrame(rows)


def process_page(page, academic_year):

    text = page.extract_text()

    tables = page.extract_tables()

    metadata = extract_metadata(text, academic_year)

    section_names = [
        "Home University",
        "Home University (Other Than HU)",
        "Other Than Home University",
        "State Level"
    ]

    all_tables = []

    for table, section in zip(tables, section_names):

        df = extract_single_table(
            table=table,
            section_name=section,
            metadata=metadata
        )

        if not df.empty:
            all_tables.append(df)

    if len(all_tables) == 0:
        return pd.DataFrame()

    return pd.concat(all_tables, ignore_index=True)

def process_pdf(pdf_path, academic_year):

    all_pages = []

    previous_metadata = {
        "college_code": None,
        "college_name": None,
        "branch_code": None,
        "branch_name": None,
        "status": None
    }

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            try:

                text = page.extract_text()
                tables = page.extract_tables()

                metadata = extract_metadata(text, academic_year)

                # Carry forward previous metadata if missing
                for key in previous_metadata:

                    if metadata[key] is None:
                        metadata[key] = previous_metadata[key]
                    else:
                        previous_metadata[key] = metadata[key]

                section_names = [
                    "Home University",
                    "Home University (Other Than HU)",
                    "Other Than Home University",
                    "State Level"
                ]

                page_tables = []

                for table, section in zip(tables, section_names):

                    df = extract_single_table(
                        table=table,
                        section_name=section,
                        metadata=metadata
                    )

                    if not df.empty:
                        page_tables.append(df)

                if page_tables:
                    all_pages.append(
                        pd.concat(page_tables, ignore_index=True)
                    )

            except Exception:
                continue

    if not all_pages:
        return pd.DataFrame()

    return pd.concat(all_pages, ignore_index=True)


def save_dataset(df, output_path):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"Dataset saved successfully at: {output_path}") 