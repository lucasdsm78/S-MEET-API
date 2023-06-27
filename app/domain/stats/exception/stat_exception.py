class StatNotFoundError(Exception):
    message = "The stat does not exist."

    def __str__(self):
        return StatNotFoundError.message