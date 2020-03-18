from enum import Enum


class Question(Enum):
    DESTINATION = 1
    DESTINATION_CHOICE = 2
    ORIGIN = 3
    ORIGIN_CHOICE = 4
    TRAVEL_DATE = 5
    RETURN_DATE = 6
    NONE = 7


class ConversationFlow:
    def __init__(
        self, last_question_asked: Question = Question.NONE,
    ):
        self.last_question_asked = last_question_asked