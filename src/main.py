def init_db():
    from database.main import init_db_psycopg
    init_db_psycopg()

if __name__ == "__main__":
    import uvicorn
    # init_db()
    uvicorn.run('backend.main:app', host='127.0.0.1', port=8000)
