# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite file will be created in the repo root as data.db
DB_URL = "sqlite:///data.db"

# create the engine to talk to the database.
engine = create_engine(
    DB_URL,
    future=True,
)
# create a seesion for this operation
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)