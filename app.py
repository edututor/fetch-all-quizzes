from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from database import SessionLocal
from models import QuizModel, QuizQuestionsModel
from schemas import AllQuizResponseSchema, AnswerSchema, QuestionSchema, QuizSchema
from sqlalchemy.orm import Session, joinedload
from typing import List
import os


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

@app.get("/api/get-all-quizzes", response_model=List[AllQuizResponseSchema])
async def fetch_all_quizzes(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching quizzes from database")
        
        quizzes = db.query(QuizModel).all()  # Fetch ORM objects

        logger.info(f"Successfully fetched {len(quizzes)} quizzes")
        return quizzes  # Directly return the ORM objects (FastAPI + Pydantic auto-serialize)

    except Exception as e:
        logger.error(f"Error fetching quizzes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/get-selected-quiz/{quiz_id}", response_model=QuizSchema)
async def fetch_selected_quiz(quiz_id: int, db: Session = Depends(get_db)):
    try:
        logger.info("Fetching quizzes from database")
        
        quiz = (
            db.query(QuizModel)
            .options(joinedload(QuizModel.questions).joinedload(QuizQuestionsModel.answers))
            .filter(QuizModel.id == quiz_id)
            .first()
        )

        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        
        return quiz  # Directly return the ORM objects (FastAPI + Pydantic auto-serialize)

    except Exception as e:
        logger.error(f"Error fetching quizzes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
