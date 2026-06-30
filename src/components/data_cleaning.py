import pandas as pd


def clean_dataset(df):

    df = df.copy()

    # Remove rows where cutoff is unavailable
    df = df.dropna(subset=["merit_rank", "percentile"])

    # Convert data types
    df["college_code"] = df["college_code"].astype(str)
    df["branch_code"] = df["branch_code"].astype(str)

    df["merit_rank"] = df["merit_rank"].astype(int)
    df["percentile"] = df["percentile"].astype(float)

    # Remove hidden newline characters
    df["category"] = (
        df["category"]
        .str.replace("\n", "", regex=False)
        .str.strip()
    )

    return df