from datetime import datetime

from recognizers_number import recognize_number, Culture
from recognizers_date_time import recognize_datetime

from botbuilder.core import (
    ActivityHandler,
    ConversationState,
    TurnContext,
    UserState,
    MessageFactory,
)
from botbuilder.schema import ChannelAccount

from models import FlightSearch, ConversationFlow, Question

class ValidationResult:
    def __init__(
        self, is_valid: bool = False, value: object = None, message: str = None
    ):
        self.is_valid = is_valid
        self.value = value
        self.message = message

class FlightSearchBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        if conversation_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. user_state is required but None was given"
            )
        

        self.conversation_state = conversation_state
        self.user_state = user_state

        self.flow_accessor = self.conversation_state.create_property("ConversationFlow")
        self.profile_accessor = self.user_state.create_property("UserProfile")

        self.WELCOME_MESSAGE = """My name is John Doe, I am here to help you search for the
                                  best flight to your destination"""

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have ocurred during the turn.
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        """
        Greet when users are added to the conversation.
        Note that all channels do not send the conversation update activity.
        If you find that this bot works in the emulator, but does not in
        another channel the reason is most likely that the channel does not
        send this activity.
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Hi there { member.name }. " + self.WELCOME_MESSAGE
                )

    async def on_message_activity(self, turn_context: TurnContext):
        # Get the state properties from the turn context.
        flight_search = await self.profile_accessor.get(turn_context, FlightSearch)
        flow = await self.flow_accessor.get(turn_context, ConversationFlow)

        await self._flight_profile(flow, flight_search, turn_context)

        # Save changes to UserState and ConversationState
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def _flight_profile(self, flow: ConversationFlow, flight_search: FlightSearch, turn_context: TurnContext):
        user_input = turn_context.activity.text.strip()

        # ask for destination
        if flow.last_question_asked == Question.NONE:
            await turn_context.send_activity(
                MessageFactory.text("Where will be flying to?")
            )
            flow.last_question_asked = Question.DESTINATION

        # ask for origin
        elif flow.last_question_asked == Question.DESTINATION:
            flight_search.destination = user_input
            await turn_context.send_activity(
                MessageFactory.text("Where will be flying from?")
            )
            flow.last_question_asked = Question.ORIGIN

        # ask for travel date
        elif flow.last_question_asked == Question.ORIGIN:
            flight_search.origin = user_input
            await turn_context.send_activity(
                MessageFactory.text("Enter the date of travel?")
            )
            flow.last_question_asked = Question.TRAVEL_DATE
        
        # ask for return date
        elif flow.last_question_asked == Question.TRAVEL_DATE:
            validate_result = self._validate_date(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                flight_search.travel_date = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text("Enter the date of return?")
                )
                flow.last_question_asked = Question.RETURN_DATE

        # show user a summary message and retrieve flights
        elif flow.last_question_asked == Question.RETURN_DATE:
            validate_result = self._validate_date(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                flight_search.return_date = validate_result.value
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"""Here is a summary of your search
                         Origin - {flight_search.origin}
                         Destination - {flight_search.destination}
                         Travel Date - {flight_search.travel_date}
                         Return Date - {flight_search.return_date}
                         """
                    )
                )
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"I will be back shortly with the best flights from your search"
                    )
                )
                flow.last_question_asked = Question.NONE

    def _validate_date(self, user_input: str) -> ValidationResult:
        try:
            # Try to recognize the input as a date-time. This works for responses such as "11/14/2018", "9pm",
            # "tomorrow", "Sunday at 5pm", and so on. The recognizer returns a list of potential recognition results,
            # if any.
            results = recognize_datetime(user_input, Culture.English)
            for result in results:
                for resolution in result.resolution["values"]:
                    if "value" in resolution:
                        now = datetime.now()

                        value = resolution["value"]
                        if resolution["type"] == "date":
                            candidate = datetime.strptime(value, "%Y-%m-%d")
                        elif resolution["type"] == "time":
                            candidate = datetime.strptime(value, "%H:%M:%S")
                            candidate = candidate.replace(
                                year=now.year, month=now.month, day=now.day
                            )
                        else:
                            candidate = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

                        # user response must be more than an hour out
                        diff = candidate - now
                        if diff.total_seconds() >= 3600:
                            return ValidationResult(
                                is_valid=True,
                                value=candidate.strftime("%m/%d/%y"),
                            )

            return ValidationResult(
                is_valid=False,
                message="I'm sorry, please enter a date at least an hour out.",
            )
        except ValueError:
            return ValidationResult(
                is_valid=False,
                message="I'm sorry, I could not interpret that as an appropriate "
                "date. Please enter a date at least an hour out.",
            )