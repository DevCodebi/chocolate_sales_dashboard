from pathlib import Path
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


def load_data(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)

    raise ValueError(f"Formato não suportado: {suffix}")


def load_google_sheet(
    sheet_id: str,
    worksheet_name: str,
    credentials_path: str | Path
) -> pd.DataFrame:

    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    creds = Credentials.from_service_account_file(
        str(credentials_path),  # garante compatibilidade com Path
        scopes=scopes
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)

    data = worksheet.get_all_records()

    df = pd.DataFrame(data)

    return df