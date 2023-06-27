class InvalidTypeNotifException(Exception):
    message = "This type of notification is not valid"

    def __init__(self, type_notif: str):
        self.type_notif = type_notif

    def __str__(self):
        return f"{self.type_notif} is not valid"

class NotificationsNotFoundError(Exception):
    message = "No notifications found from the API."

    def __str__(self):
        return NotificationsNotFoundError.message


class NotificationNotFoundError(Exception):
    message = "The notification does not exist."

    def __str__(self):
        return NotificationNotFoundError.message
