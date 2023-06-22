class QuizsNotFoundError(Exception):
    message = "No quizs found from the API."

    def __str__(self):
        return QuizsNotFoundError.message


class QuestionsNotFoundError(Exception):
    message = "No questions found from the API for this quiz."

    def __str__(self):
        return QuizsNotFoundError.message


class QuizNotFoundError(Exception):
    message = "The quiz does not exist."

    def __str__(self):
        return QuizNotFoundError.message


class ScoreNotFoundError(Exception):
    message = "The score for this quiz and this user does not exist."

    def __str__(self):
        return ScoreNotFoundError.message
