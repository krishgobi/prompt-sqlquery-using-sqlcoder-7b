from fastapi import FastAPI
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from schema.api.query import router

app = FastAPI(title="Finance AI SQL Backend")

app.include_router(router)
