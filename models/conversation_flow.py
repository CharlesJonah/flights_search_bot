from enum import Enum


class Question(Enum):
    DESTINATION = 1
    ORIGIN = 2
    TRAVEL_DATE = 3
    RETURN_DATE = 4
    NONE = 5


class ConversationFlow:
    def __init__(
        self, last_question_asked: Question = Question.NONE,
    ):
        self.last_question_asked = last_question_asked