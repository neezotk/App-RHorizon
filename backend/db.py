from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from .config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=5, future=True)

def init_db():
    ddl = text("""
    CREATE TABLE IF NOT EXISTS items (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    )
    """)
    with engine.begin() as conn:
        conn.execute(ddl)

def db_healthcheck():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, None
    except SQLAlchemyError as e:
        return False, str(e)

def insert_item(name: str):
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO items(name) VALUES (:n)"), {"n": name})

def list_items():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, name, created_at FROM items ORDER BY id DESC LIMIT 50"))
        return [dict(r._mapping) for r in rows]
