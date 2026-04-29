import pandas as pd

def generate_insights(df):

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


    if "google_status" in df:
        insights["Google Success Rate %"] = (
            (df["google_status"] == "success").mean() * 100
        )

    # convert to dataframe
    return pd.DataFrame(insights.items(), columns=["Metric", "Value"])