from pydantic import BaseModel
from typing import List
from datetime import datetime


class AllQuizResponseSchema(BaseModel):
    id: int
    title: str
    document_name: str

    class Config:
        from_attributes = True  # Allows conversion from ORM objects

class AnswerSchema(BaseModel):
    id: int
    answer_text: str
    is_correct_answer: bool

    class Config:
        orm_mode = True

class QuestionSchema(BaseModel):
    id: int
    question_text: str
    hint: str
    answers: List[AnswerSchema] = []

    class Config:
        orm_mode = True

class QuizSchema(BaseModel):
    id: int
    title: str
    document_name: str
    created_at: datetime
    questions: List[QuestionSchema] = []

    class Config:
        orm_mode = True  

class QuizRequestSchema(BaseModel):
    id: int
    title: str


