from sqlalchemy import text
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from db.connection import engine

def load_schema():
    query = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
    ORDER BY table_name, ordinal_position;
    """
    schema = {}
    with engine.connect() as conn:
        for table, column in conn.execute(text(query)):
            schema.setdefault(table, []).append(column)

    schema_text = ""
    for table, cols in schema.items():
        schema_text += f"TABLE {table} ({', '.join(cols)})\n"

    return schema_text
