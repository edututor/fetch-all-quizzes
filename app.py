from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from typing import List
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Settings configuration
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    db_url: str

    def __init__(self, **data):
        super().__init__(**data)

settings = Settings()

# Database setup
engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizResponse(BaseModel):
    id: int
    title: str
    document_name: str

@app.get("/api/quizzes")
async def fetch_all_quizzes():
    try:
        logger.info("Fetching quizzes from database")
        db = SessionLocal()
        result = db.execute("SELECT id, title, document_name FROM quizzes")
        quizzes = [{"id": row[0], "title": row[1], "document_name": row[2]} for row in result]
        db.close()
        logger.info(f"Successfully fetched {len(quizzes)} quizzes")
        return JSONResponse(
            status_code=200,
            content={"data": quizzes}
        )
    except Exception as e:
        logger.error(f"Error fetching quizzes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)