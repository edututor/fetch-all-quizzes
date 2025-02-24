from pydantic import BaseModel

class QuizResponseSchema(BaseModel):
    id: int
    title: str
    document_name: str

    class Config:
        from_attributes = True  # Allows conversion from ORM objects
