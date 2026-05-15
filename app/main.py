from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.routers.auth import router as auth_router
from app.routers.patient import router as patient_router
from app.routers.users import router as users_router

app = FastAPI(
    title='PSIA API',
    version='0.1.0',
)

app.include_router(patient_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/db-check')
def db_check():
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))

    return {'database': 'ok'}
