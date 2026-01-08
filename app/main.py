from fastapi import FastAPI
from app.api.routes import health
from app.core.dictionary import load_dictionary

app = FastAPI(title="Lexora Backend")

load_dictionary()

app.include_router(health.router)
# app.include_router(matches.router)