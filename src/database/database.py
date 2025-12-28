from sqlalchemy.orm import sessionmaker
from functools  import lru_cache
from config import PostgresSettings
from sqlalchemy import create_engine

@lru_cache
def get_postgres_settings():
    return PostgresSettings()

engine = create_engine(url=get_postgres_settings().sqlalchemy_url)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()