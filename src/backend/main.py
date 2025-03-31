from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import router
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield  # This allows FastAPI to continue running

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Bank Transcript Scanner API"}
