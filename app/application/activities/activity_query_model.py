from pydantic import Field, BaseModel

from app.domain.activity.model.activity import Activity


class ActivityReadModel(BaseModel):
    """ActivityReadModel represents data structure as a read model."""

    id: int
    type: int
    name: str = Field(example="Sortie à la ptinoire")
    description: str = Field(example="Sortie à la patinoire à 12h00")
    more: str = Field(example="ramener vos repas")
    start_date: int = Field(example=1136214245000)
    end_date: int = Field(example=1136214245000)
    place: str = Field(example="Cergy")
    max_members: int = Field(example=20)
    user_creator: str = Field(example="lucas@esieeit.fr")
    createdAt: int = Field(example=1136214245000)
    updatedAt: int = Field(example=1136214245000)

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(activity: Activity) -> "ActivityReadModel":
        return ActivityReadModel(
            id=activity.id,
            type=activity.type.value,
            name=activity.name,
            description=activity.description,
            more=activity.more,
            start_date=activity.start_date,
            end_date=activity.end_date,
            place=activity.place,
            max_members=activity.max_members,
            user_creator=activity.user.email.value,
            createdAt=activity.created_at,
            updatedAt=activity.updated_at
        )
