from fastapi import FastAPI
from app.api.routes import health
from app.core.dictionary import load_dictionary

from app.db import Base, engine
import app.models

app = FastAPI(title="Lexora Backend")

load_dictionary()


app.include_router(health.router)
# app.include_router(matches.router)

# Startup event: create all tables
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)