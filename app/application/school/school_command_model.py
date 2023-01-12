from pydantic import BaseModel, Field


class SchoolCreateModel(BaseModel):
    """SchoolCreateModel represents a write model to create a school."""

    name: str = Field(example="ESIEEIT")


class SchoolCreateResponse(BaseModel):
    message: str = "The school is well created"