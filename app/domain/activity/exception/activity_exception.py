class InvalidTypeException(Exception):
    message = "This type is not a valid type"

    def __init__(self, type: int):
        self.type = type

    def __str__(self):
        return f"{self.type} is not a valid type"