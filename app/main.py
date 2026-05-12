from fastapi import FastAPI
from http import HTTPStatus

from sqlalchemy import text
from app.database import engine

app = FastAPI(title='PSI App API')


@app.get('/health', status_code=HTTPStatus.OK)
def health():
    return {'status': 'healthy'}


@app.get('/db-check')
def db_check():
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
