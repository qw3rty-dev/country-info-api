from fastapi import FastAPI
from database import init_db,get_connection
from scraper import fetch_data
from routes import countries
from contextlib import asynccontextmanager

def has_data():
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM country")
    count= cursor.fetchone()[0]
    conn.close()
    return count>0
    



@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    if not has_data():
        fetch_data()
    yield

app=FastAPI(lifespan=lifespan)

app.include_router(countries.router)