class MessagesNotFoundError(Exception):
    message = "No messages found."

    def __str__(self):
        return MessagesNotFoundError.message
