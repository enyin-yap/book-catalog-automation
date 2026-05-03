import pandas as pd

def compute_data_quality_score(df):

    key_fields = {
        "title": 25,
        "author": 25,
        "price (TWD)": 25,
        "publisher_date": 15,
        "description": 10
    }

    score_series = pd.Series(0, index=df.index)

    for field, weight in key_fields.items():
        if field in df.columns:
            score_series += df[field].notna().astype(int) * weight

    df["data_quality_score"] = score_series

    return df

def generate_insights(df):

    df = compute_data_quality_score(df.copy())

    total = len(df)

    def pct_missing(col):
        return df[col].isna().mean() * 100 if col in df else None

    insights = {
        "Total Books": total,

        "Missing Title %": pct_missing("title"),
        "Missing Author %": pct_missing("author"),
        "Missing Price %": pct_missing("price (TWD)"),
        "Missing Publish Date %": pct_missing("publisher_date"),

        "Price Coverage %": (df["price (TWD)"].notna().mean() * 100) if "price (TWD)" in df else None,

        "Avg Price (TWD)": df["price (TWD)"].dropna().mean() if "price (TWD)" in df else None,
    }

    insights["Avg Data Quality Score"] = df["data_quality_score"].mean()
    insights["Low Quality Books (<50)"] = (df["data_quality_score"] < 50).sum()
    insights["High Quality Books (>80)"] = (df["data_quality_score"] > 80).sum()

    # Success Rate
    if "google_status" in df.columns:
        insights["Google Success Rate %"] = (
            (df["google_status"] == "success").mean() * 100
        )
    
    if "openlibrary_status" in df.columns:
        insights["OpenLibrary Success Rate %"] = (
            (df["openlibrary_status"] == "success").mean() * 100
        )

    # Failure Rate
    if "google_status" in df.columns and "openlibrary_status" in df.columns:

        both_failed = df[
            (df["google_status"] != "success") &
            (df["openlibrary_status"] != "success")
        ]

        insights["Both Sources Failed %"] = len(both_failed) / len(df) * 100

    # Data Completeness Score
    key_cols = ["title", "author", "price (TWD)", "publisher_date"]
    
    existing_cols = [c for c in key_cols if c in df.columns]

    if existing_cols:
        df["completeness_score"] = df[existing_cols].notna().mean(axis=1)

        insights["Avg Completeness Score %"] = df["completeness_score"].mean() * 100

    # High Value Missing Data
    if "price (TWD)" in df.columns:

        price_series = df["price (TWD)"].dropna()

        if not price_series.empty:
            threshold = price_series.quantile(0.75)

            high_value_missing = df[
                (df["price (TWD)"] >= threshold) &
                (df["title"].isna() | df["author"].isna())
            ]

            insights["High Value Books Missing Metadata"] = len(high_value_missing)

    # convert to dataframe
    return pd.DataFrame(insights.items(), columns=["Metric", "Value"])