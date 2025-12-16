import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "finance")

# URL-encode the password to handle special characters like @
DB_PASSWORD_ENCODED = quote(DB_PASSWORD, safe='')
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}/{DB_NAME}"

VLLM_URL = os.getenv("VLLM_URL", "http://localhost:8001/v1/chat/completions")
MODEL_NAME = os.getenv("MODEL_NAME", "defog/sqlcoder-7b-2")
