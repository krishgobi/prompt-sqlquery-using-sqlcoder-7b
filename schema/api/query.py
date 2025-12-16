from fastapi import APIRouter
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from services.query_service import process_user_prompt

router = APIRouter()

@router.post("/query")
def query(payload: dict):
    try:
        return process_user_prompt(payload["prompt"])
    except ValueError as e:
        return {
            "error": str(e),
            "status": "validation_error"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "execution_error"
        }
