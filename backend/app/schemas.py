from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    conversation_id: int | None = None


class AskResponse(BaseModel):
    conversation_id: int
    answer: str
