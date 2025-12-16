import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from schema.schema_loader import load_schema
from llm.prompt import build_prompt
from llm.client import call_llm
from db.executor import execute_sql

def process_user_prompt(user_prompt: str):
    print(f"\n=== Processing user prompt ===")
    print(f"User request: {user_prompt}")
    
    schema = load_schema()
    print(f"\nDatabase schema loaded successfully")
    
    prompt = build_prompt(user_prompt, schema)
    print(f"\nGenerated prompt for LLM")
    
    sql_query = call_llm(prompt)
    print(f"\nGenerated SQL:\n{sql_query}")
    
    result = execute_sql(sql_query)
    print(f"\nQuery executed successfully. Results: {len(result)} rows")

    return {
        "generated_sql": sql_query,
        "data": result
    }
