import pandas as pd

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def basic_null_report(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.isna()
          .sum()
          .to_frame("nulls")
          .assign(pct=lambda x: (x["nulls"] / len(df)).round(4))
          .sort_values("nulls", ascending=False)
    )

def clean_currency(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
              .str.replace(r"[$,]", "", regex=True)   # remove $ e separador de milhar
              .pipe(pd.to_numeric, errors="coerce")
    )
def clean_sales_df(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)
    df["amount"] = clean_currency(df["amount"])
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
    return df

