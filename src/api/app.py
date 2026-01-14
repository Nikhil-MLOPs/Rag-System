from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="ClinicaAI RAG")

app.include_router(router)