def build_prompt(user_prompt, schema):
    return f"""
You are an expert MySQL 8 SQL generator. Generate ONLY valid MySQL SQL.

CRITICAL RULES:
1. Use ONLY MySQL 8 syntax - NEVER PostgreSQL or Oracle functions
2. NEVER use: interval '30 days', to_date(), to_char(), NULLS LAST, ILIKE, ::, RETURNING
3. For date arithmetic use: DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY) or INTERVAL syntax
4. Every table alias used in SELECT/WHERE MUST be defined in FROM/JOIN
5. Check all column names and table aliases match the schema
6. Use proper JOIN conditions with matching data types
7. DO NOT include <s>, </s>, ```, explanations or anything except the SQL

Database schema:
{schema}

User request:
{user_prompt}

Return ONLY the executable MySQL SQL query, nothing else.
"""
