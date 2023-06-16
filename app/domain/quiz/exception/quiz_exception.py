class QuizsNotFoundError(Exception):
    message = "No quizs found from the API."

    def __str__(self):
        return QuizsNotFoundError.message


class QuizNotFoundError(Exception):
    message = "The quiz does not exist."

    def __str__(self):
        return QuizNotFoundError.message
