class InvalidTypeException(Exception):
    message = "This type is not a valid type"

    def __init__(self, type: str):
        self.type = type

    def __str__(self):
        return f"{self.type} is not a valid type"


class InvalidCategoryException(Exception):
    message = "This category is not a valid category"

    def __init__(self, category: str):
        self.category = category

    def __str__(self):
        return f"{self.category} is not a valid category"


class ActivitiesNotFoundError(Exception):
    message = "No activities found from the API."

    def __str__(self):
        return ActivitiesNotFoundError.message


class EventsNotFoundError(Exception):
    message = "No events found from the API."

    def __str__(self):
        return EventsNotFoundError.message


class ActivityNotFoundError(Exception):
    message = "The activity does not exist."

    def __str__(self):
        return ActivityNotFoundError.message


class ActivityParticipantNotFoundError(Exception):
    message = "You are not participating in this activity."

    def __str__(self):
        return ActivityParticipantNotFoundError.message


class MaxParticipantsAtteintsError(Exception):
    message = "Le max de participants a été atteint"

    def __str__(self):
        return MaxParticipantsAtteintsError.message
