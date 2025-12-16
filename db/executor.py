from sqlalchemy import text
from .connection import engine
import re

def convert_postgres_to_mysql(sql):
    """Convert common PostgreSQL syntax to MySQL syntax."""
    # Convert interval '30 days' to INTERVAL 30 DAY
    sql = re.sub(
        r"interval\s+'(\d+)\s+days?'",
        r"INTERVAL \1 DAY",
        sql,
        flags=re.IGNORECASE
    )
    # Convert interval '30 hours' to INTERVAL 30 HOUR
    sql = re.sub(
        r"interval\s+'(\d+)\s+hours?'",
        r"INTERVAL \1 HOUR",
        sql,
        flags=re.IGNORECASE
    )
    # Convert interval '30 minutes' to INTERVAL 30 MINUTE
    sql = re.sub(
        r"interval\s+'(\d+)\s+minutes?'",
        r"INTERVAL \1 MINUTE",
        sql,
        flags=re.IGNORECASE
    )
    return sql

def validate_mysql_sql(sql):
    """Validate that SQL uses only MySQL syntax, not PostgreSQL or Oracle."""
    blocked = [
        "to_date",
        "to_char",
        "NULLS LAST",
        "ILIKE",
        "::",
        "RETURNING"
    ]
    for word in blocked:
        if word.lower() in sql.lower():
            raise ValueError(f"Invalid MySQL syntax detected: {word}. Please use MySQL 8 compatible syntax.")

def validate_table_aliases(sql):
    """Validate that all table aliases in SELECT/WHERE are defined in FROM/JOIN."""
    # Extract table aliases from FROM and JOIN clauses
    from_pattern = r'FROM\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?'
    join_pattern = r'JOIN\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?'
    
    defined_aliases = set()
    
    # Find all aliases in FROM clause
    from_matches = re.finditer(from_pattern, sql, re.IGNORECASE)
    for match in from_matches:
        # If an explicit alias is given (group 2), use it; otherwise use the table name (group 1)
        alias = match.group(2) if match.group(2) else match.group(1)
        if alias:
            defined_aliases.add(alias)
    
    # Find all aliases in JOIN clauses
    join_matches = re.finditer(join_pattern, sql, re.IGNORECASE)
    for match in join_matches:
        # If an explicit alias is given (group 2), use it; otherwise use the table name (group 1)
        alias = match.group(2) if match.group(2) else match.group(1)
        if alias:
            defined_aliases.add(alias)
    
    # Find all table references (alias.column)
    ref_pattern = r'(\w+)\.\w+'
    ref_matches = re.finditer(ref_pattern, sql)
    
    undefined = set()
    for match in ref_matches:
        alias = match.group(1)
        if alias.upper() not in ['SELECT', 'FROM', 'WHERE', 'JOIN', 'ON', 'GROUP', 'ORDER', 'HAVING', 'LIMIT']:
            if alias not in defined_aliases:
                undefined.add(alias)
    
    if undefined:
        raise ValueError(f"Undefined table aliases in query: {', '.join(sorted(undefined))}. Check JOIN conditions and table aliases.")

def execute_sql(sql):
    """Execute SQL query and return results as list of dictionaries."""
    # Convert PostgreSQL syntax to MySQL
    sql = convert_postgres_to_mysql(sql)
    print(f"Converted SQL:\n{sql}")
    
    validate_mysql_sql(sql)
    validate_table_aliases(sql)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            return [dict(row._mapping) for row in result]
    except Exception as e:
        error_msg = str(e)
        print(f"Database Error: {error_msg}")
        raise ValueError(f"SQL execution failed: {error_msg}")

