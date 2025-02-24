from database import Base
from sqlalchemy import Column, Integer, String

class QuizResponse(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    document_name = Column(String, unique=True)
