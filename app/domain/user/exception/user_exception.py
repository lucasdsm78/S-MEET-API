class UserEmailAlreadyExistsError(Exception):
    message = "The user with the email code you specified already exists."

    def __str__(self):
        return UserEmailAlreadyExistsError.message


class UsersNotFoundError(Exception):
    message = "No users found from the API."

    def __str__(self):
        return UsersNotFoundError.message
