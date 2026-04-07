# Database Management — Neon PostgreSQL
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

# ── Connection management ────────────────────────────────────────────────────
# Neon is serverless — connections can be dropped after periods of inactivity.
# We hold one connection and reconnect transparently when needed.

_conn = None

def _get_conn():
    """Return a live psycopg2 connection, reconnecting if necessary."""
    global _conn
    try:
        if _conn is None or _conn.closed:
            raise Exception("Connection closed")
        # Lightweight ping to verify the connection is still alive
        _conn.cursor().execute("SELECT 1")
    except Exception:
        _conn = psycopg2.connect(DATABASE_URL)
    return _conn

# Expose as `mydb` for backward-compatibility with customer.py
def _commit():
    _get_conn().commit()

class _DBProxy:
    """Proxy that lets legacy code call mydb.commit() safely."""
    def commit(self):
        _get_conn().commit()

mydb = _DBProxy()

# ── Core query helper ────────────────────────────────────────────────────────

def db_query(sql):
    """Execute a SQL statement and return rows for SELECT, [] otherwise."""
    conn = _get_conn()
    cur  = conn.cursor()
    cur.execute(sql)
    # Only SELECT statements have rows to fetch
    if sql.strip().upper().startswith("SELECT"):
        result = cur.fetchall()
    else:
        result = []
    conn.commit()
    return result

# ── Schema initialisation ────────────────────────────────────────────────────

def createcustomertable():
    conn = _get_conn()
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            username     VARCHAR(50)  NOT NULL,
            password     VARCHAR(50)  NOT NULL,
            name         VARCHAR(50)  NOT NULL,
            age          INTEGER      NOT NULL,
            city         VARCHAR(50)  NOT NULL,
            balance      INTEGER      NOT NULL,
            account_number INTEGER    NOT NULL,
            status       BOOLEAN      NOT NULL
        )
    """)
    conn.commit()

createcustomertable()

if __name__ == "__main__":
    print("Neon PostgreSQL database initialized successfully.")
