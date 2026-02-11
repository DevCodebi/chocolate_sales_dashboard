import pandas as pd

def compute_metrics(df: pd.DataFrame) -> dict:
    out = {}
    out["total_sales"] = df["amount"].sum()
    out["n_orders"] = df["order_id"].nunique()
    out["sales_by_country"] = df.groupby("country", as_index=False)["amount"].sum()
    return out
