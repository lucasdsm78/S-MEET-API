class MessagesNotFoundError(Exception):
    message = "No messages found."

    def __str__(self):
        return MessagesNotFoundError.message

class MessageNotFoundError(Exception):
    message = "The message does not exist."

    def __str__(self):
        return MessageNotFoundError.message