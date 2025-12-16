import requests
from app.config import VLLM_URL, MODEL_NAME

def clean_sql(sql: str) -> str:
    """Remove unwanted tokens from generated SQL."""
    bad_tokens = ["<s>", "</s>", "```sql", "```"]
    for token in bad_tokens:
        sql = sql.replace(token, "")
    return sql.strip()

def call_llm(prompt):
    # Ollama API format
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(VLLM_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        raw_sql = result.get("response", "").strip()
        return clean_sql(raw_sql)
    except requests.exceptions.ConnectionError:
        raise Exception(f"Cannot connect to LLM service at {VLLM_URL}. Make sure Ollama is running on port 11434.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"LLM API error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        raise Exception(f"Error calling LLM: {str(e)}")
