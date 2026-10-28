from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
        description="Question about sales or inventory.",
    )


class AskResponse(BaseModel):
    answer: str