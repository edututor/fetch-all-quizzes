from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from database import SessionLocal
from models import QuizResponse
from schemas import QuizResponseSchema  # Import Pydantic schema
from sqlalchemy.orm import Session
import os
from typing import List

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/quizzes", response_model=List[QuizResponseSchema])  # Specify response model
async def fetch_quizzes(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching quizzes from database")
        
        quizzes = db.query(QuizResponse).all()  # Fetch ORM objects

        logger.info(f"Successfully fetched {len(quizzes)} quizzes")
        return quizzes  # Directly return the ORM objects (FastAPI + Pydantic auto-serialize)

    except Exception as e:
        logger.error(f"Error fetching quizzes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
