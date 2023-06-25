class SmeetsNotFoundError(Exception):
    message = "No smeets found from the API."

    def __str__(self):
        return SmeetsNotFoundError.message