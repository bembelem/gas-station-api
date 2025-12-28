from database.database import engine
from sqlalchemy import text
from database.seed import seed

def init_db_psycopg():
    create_tables_psycopg()
    seed_db()

def create_tables_orm():
    from database.models import Base
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_tables_psycopg():
    with engine.begin() as conn:
        conn.execute(text('DROP SCHEMA public CASCADE'))

        with open('src/database/schema.sql', 'r', encoding='utf-8') as f:
            sql_query = f.read()

        conn.exec_driver_sql(sql_query)

def seed_db():
    seed()