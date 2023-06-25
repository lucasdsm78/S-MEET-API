from pydantic import BaseModel, Field


class SmeetCreateModel(BaseModel):
    """SmeetCreateModel represents a write model to create a smeet."""

    content: str = Field(example="salut toi !!")
    is_edited: bool = Field()


class SmeetCreateResponse(BaseModel):
    message: str = "The smeet is well sent"