class BadgesNotFoundError(Exception):
    message = "No badges found from the API."

    def __str__(self):
        return BadgesNotFoundError.message


class BadgeNotFoundError(Exception):
    message = "The badge does not exist."

    def __str__(self):
        return BadgeNotFoundError.message


class UserBadgeNotFoundError(Exception):
    message = "The badge does not exist for this user and for this badge."

    def __str__(self):
        return UserBadgeNotFoundError.message


class InvalidGradeException(Exception):
    message = "This grade is not a valid grade"

    def __init__(self, grade: str):
        self.grade = grade

    def __str__(self):
        return f"{self.grade} is not a valid grade"