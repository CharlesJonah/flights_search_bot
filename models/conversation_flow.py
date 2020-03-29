from enum import Enum


class Question(Enum):
    DESTINATION = 1
    DESTINATION_CHOICE = 2
    ORIGIN = 3
    RETURN_TRIP = 4
    ORIGIN_CHOICE = 5
    TRAVEL_DATE = 6
    RETURN_DATE = 7
    CABIN_CLASS = 8
    ADULTS = 9
    NONE = 10


class ConversationFlow:
    def __init__(
        self, last_question_asked: Question = Question.NONE,
    ):
        self.last_question_asked = last_question_asked