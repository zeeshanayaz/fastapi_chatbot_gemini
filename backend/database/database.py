import asyncio
import sqlite3
from typing import List, Dict, Any

DB_NAME = "database.db"


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# Initialize the database and create necessary tables
async def init_database():

    def create_table():
        conn = get_db_connection()
        try:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                         user_query TEXT,
                         gemini_response TEXT
                    );
            ''')
            # Ensure DDL is persisted
            conn.commit()
        except Exception as e:
            # Log the error so it isn't silently swallowed during init
            print(f"init_database error: {e}")
        finally:
            conn.close()

    await asyncio.to_thread(create_table)



# Saves a new chat entry to the database and returns the ID.
async def save_chat_entry(user_query: str, gemini_response: str) -> int:
    def run_save():
        conn = get_db_connection()
        cursor = None
        lastrowid = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (user_query, gemini_response) VALUES (?, ?)",
                (user_query, gemini_response)
            )
            conn.commit()
            lastrowid = cursor.lastrowid
        finally:
            conn.close()

        return int(lastrowid) if lastrowid is not None else -1

    return await asyncio.to_thread(run_save)


async def fetch_all_history() -> List[Dict[str, Any]]:
    def run_fetch():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chat_history ORDER BY timestamp ASC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    return await asyncio.to_thread(run_fetch)
