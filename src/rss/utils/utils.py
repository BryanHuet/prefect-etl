import sqlite3

def get_db_connection(row=False):
    conn = sqlite3.connect('db.sqlite3')
    if row :
        conn.row_factory = sqlite3.Row
    return conn

def get_sql_file(path):
    with open(path, "r", encoding="utf-8") as f:
        sql_query = f.read().strip()
    return sql_query