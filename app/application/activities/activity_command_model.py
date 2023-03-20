from pydantic import BaseModel, Field


class ActivityCreateModel(BaseModel):
    """ActivityCreateModel represents a write model to create an activity."""

    name: str = Field(example="repas chez KFC")
    type: str = Field(example="activity")
    description: str = Field(example="manger midi chez kfc à pontoise")
    start_date: int
    end_date: int
    place: str = Field(example="Cergy")
    image_activity: str
    category: str = Field(example='after_work')
    max_members: int


class ActivityParticipateResponse(BaseModel):
    message: str = "Your participation is well saved"


class ActivityCreateResponse(BaseModel):
    message: str = "The activity is well created"


class ActivityCancelParticipationResponse(BaseModel):
    message: str = "Your participation is well canceled"
