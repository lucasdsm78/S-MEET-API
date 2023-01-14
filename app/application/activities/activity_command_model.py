from pydantic import BaseModel, Field


class ActivityCreateModel(BaseModel):
    """ActivityCreateModel represents a write model to create an activity."""

    name: str = Field(example="repas chez KFC")
    type: int = Field(example=1)
    description: str = Field(example="manger midi chez kfc à pontoise")
    more: str = Field(example="moredetails")
    start_date: int
    end_date: int
    place: str = Field(example="Cergy")
    max_members: int


class ActivityCreateResponse(BaseModel):
    message: str = "The activity is well created"