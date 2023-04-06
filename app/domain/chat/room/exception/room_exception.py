class RoomNotFoundError(Exception):
    message = "The room does not exist."

    def __str__(self):
        return RoomNotFoundError.message


class RoomsNotFoundError(Exception):
    message = "No rooms found from the API."

    def __str__(self):
        return RoomsNotFoundError.message
