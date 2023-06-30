class FriendAlreadyExistsError(Exception):
    message = "The friend specified already exists."

    def __str__(self):
        return FriendAlreadyExistsError.message


class FriendsNotFoundError(Exception):
    message = "No friends found from the API."

    def __str__(self):
        return FriendsNotFoundError.message


class FriendNotFoundError(Exception):
    message = "The friend does not exist."

    def __str__(self):
        return FriendNotFoundError.message
