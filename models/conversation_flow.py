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
    PASSENGERS = 9
    NONE = 10
    COMPLETED = 11


class ConversationFlow:
    def __init__(
        self, last_question_asked: Question = Question.NONE,
        question_being_modified: Question = Question.COMPLETED,
    ):
        self.last_question_asked = last_question_asked
        self.question_being_modified = question_being_modified


class State(Enum):
    NORMAL = 1
    MODIFY = 2


class ChatState:
    def __init__(
        self, chat_state: State = State.NORMAL,
    ):
        self.chat_state = chat_state
