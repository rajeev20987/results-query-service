from fastapi import FastAPI
from app.api.routes import results
from app.db.models import Base
from app.db.connection import engine

# Create DB tables
Base.metadata.create_all(bind=engine)

# ✅ This is REQUIRED
app = FastAPI()
app.include_router(results.router)


@app.get("/")
def root():
    return {"message": "Request Query Service is running"}