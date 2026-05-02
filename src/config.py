from pathlib import Path

# raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# credenciais
CREDENTIALS_PATH = PROJECT_ROOT / "credentials" / "api_google_credentials.json"

# Google Sheets
SHEET_ID = "1IdJH7ZP7hlmwWEFAnQtqq-Tz_Mq-47slWqi2j-VjLvU"