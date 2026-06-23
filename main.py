from fastapi import FastAPI,Depends
from database import get_db,engine,Base
from scraper import fetch_data
from routes import countries
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from routes.countries import router
from models import country
from database import SessionLocal
from contextlib import asynccontextmanager

def has_data(db: Session):

    count = db.scalar(select(func.count(country.name)))
    return count>0

@asynccontextmanager
async def lifespan(app:FastAPI):
    db = SessionLocal()
    try:
        if not has_data(db):
            fetch_data(db)
        yield
    finally:
        db.close()


Base.metadata.create_all(bind= engine)
app=FastAPI(lifespan=lifespan)
app.include_router(router)
