from pathlib import Path
import pandas as pd

def load_data(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix in [".csv"]:
        return pd.read_csv(path)
    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    if suffix in [".parquet"]:
        return pd.read_parquet(path)

    raise ValueError(f"Formato não suportado: {suffix}")
