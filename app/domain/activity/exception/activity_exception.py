class InvalidTypeException(Exception):
    message = "This type is not a valid type"

    def __init__(self, type: int):
        self.type = type

    def __str__(self):
        return f"{self.type} is not a valid type"


class ActivitiesNotFoundError(Exception):
    message = "No activities found from the API."

    def __str__(self):
        return ActivitiesNotFoundError.message


class ActivityNotFoundError(Exception):
    message = "The activity does not exist."

    def __str__(self):
        return ActivityNotFoundError.message
