# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite file will be created in the repo root as data.db
DB_URL = "sqlite:///data.db"

engine = create_engine(
    DB_URL,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)