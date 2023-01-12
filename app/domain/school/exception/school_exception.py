class SchoolNamelAlreadyExistsError(Exception):
    message = "The school with the name you specified already exists."

    def __str__(self):
        return SchoolNamelAlreadyExistsError.message