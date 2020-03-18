import os
from datetime import datetime

from recognizers_number import recognize_number, Culture
from recognizers_date_time import recognize_datetime

from botbuilder.core import (
    ActivityHandler,
    ConversationState,
    TurnContext,
    UserState,
    MessageFactory,
    CardFactory
)
from botbuilder.schema import (
    ChannelAccount, 
    CardAction, 
    CardImage, 
    ActionTypes, 
    HeroCard,
    Attachment,
    AttachmentLayoutTypes
)

from models import FlightSearch, ConversationFlow, Question

from resources import AdaptiveCardHelper

from helpers.authentication import Authenticate
from helpers.services import HttpService
from constants import AIRPORT_SEARCH_API, FLIGHT_OFFERS_API

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

        # Amadesus API authentication for flight search
        self.authenticate = Authenticate()
        self.authenticate.login()
        self.http_service = self.authenticate.http_service
        self.airport_codes_http_service = HttpService()
        self.http_service.config_service({
            "APC-Auth": os.environ['AIRPORT_CODES_API_KEY'], 
            "APC-Auth-Secret": os.environ['AIRPORT_CODES_API_SECRET']
        })

        # store a map of airport iata codes to names
        self.airports = {}
        
        self.flights_search_summary = MessageFactory.list([])

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

        airports = {}

        # ask for destination
        if flow.last_question_asked == Question.NONE:
            await turn_context.send_activity(
                MessageFactory.text("Which airport will be flying to?")
            )
            flow.last_question_asked = Question.DESTINATION

        # ask for airport of destination choice and save
        elif flow.last_question_asked == Question.DESTINATION:
            res = self._search_airports_by_location(user_input)
            validate_result =  self._validate_airports_result(res)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                await self._send_card(
                                turn_context=turn_context,
                                title="Choose Destination Airport",
                                text="""Please choose the correct 
                                     Aiport that you will be going to""",
                                buttons=self._create_card_actions_for_airport(validate_result.value))
                flow.last_question_asked = Question.DESTINATION_CHOICE

        #save choosen destination
        elif flow.last_question_asked == Question.DESTINATION_CHOICE:
            flight_search.destination = user_input
            flight_search.destination_city = self.airports[user_input]
            await turn_context.send_activity(
                MessageFactory.text("Which airport will be flying to?")
            )
            flow.last_question_asked = Question.ORIGIN

        # ask for airport of origin choice
        elif flow.last_question_asked == Question.ORIGIN:
            res = self._search_airports_by_location(user_input)
            validate_result =  self._validate_airports_result(res)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                await self._send_card(
                                turn_context=turn_context,
                                title="Choose Airport of Origin",
                                text="""Please choose the correct 
                                     Aiport that you will be departing from""",
                                buttons=self._create_card_actions_for_airport(validate_result.value))
                flow.last_question_asked = Question.ORIGIN_CHOICE

        # ask for travel date
        elif flow.last_question_asked == Question.ORIGIN_CHOICE:
            flight_search.origin = user_input
            flight_search.origin_city = self.airports[user_input]
            await turn_context.send_activity(
                MessageFactory.text("Enter the date of travel (mm/dd/yyy)?")
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
                    MessageFactory.text("Enter the date of return (mm/dd/yyy)?")
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
                         Origin - {flight_search.origin_city}
                         Destination - {flight_search.destination_city}
                         Travel Date - {flight_search.travel_date}
                         Return Date - {flight_search.return_date}
                         """
                    )
                )

                self.flights_search_summary.attachments.append(self._create_flights_summary(flight_search))
                await turn_context.send_activity(self.flights_search_summary)
                flow.last_question_asked = Question.NONE
    
    async def _send_card(self, turn_context: TurnContext, title, text, buttons):
        card = HeroCard(
            title=title,
            text=text,
            images=[CardImage(url="https://www.aurecongroup.com/-/media/images/aurecon/content/projects/property/hanoi-airport/hanoi-airport-interior.jpg")],
            buttons=buttons
        )
        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(card))
        )

    def _create_card_actions_for_airport(self, airports):
        buttons = []
        self.airports = {}
        for airport in airports:
            self.airports[airport["iata"]] = airport["city"]
            buttons.append(
                CardAction(
                    type=ActionTypes.post_back,
                    title=airport["name"],
                    text=airport["iata"],
                    display_text=airport["name"],
                    value=airport["iata"]
                )
            )
        return buttons

    def _search_flights(self, flight_search):
        travel_date = flight_search.travel_date.split('/')
        return_date = flight_search.return_date.split('/')
        search_params = {
            'originLocationCode': flight_search.origin,
            'destinationLocationCode': flight_search.destination,
            'departureDate': f"{travel_date[2]}-{travel_date[0]}-{travel_date[1]}",
            'returnDate': f"{return_date[2]}-{return_date[0]}-{return_date[1]}",
            'adults':1

        }

        res = self.http_service.get(FLIGHT_OFFERS_API, search_params)
        if res.status_code != 200:
            return ValidationResult(
                is_valid=False,
                message="I'm sorry, we couldn't retrieve flights for you, please retry the process",
            )
        else:
            flights =  res.json()["data"]["itineraries"]
            if flights:
                return ValidationResult(
                is_valid=True,
                value=flights,
            )
            else:
                return ValidationResult(
                is_valid=False,
                message="I'm sorry, we couldn't retrieve flights for you, please retry the process",
            )

    def _search_airports_by_location(self, airport):
        res = self.http_service.post(AIRPORT_SEARCH_API, { "term": airport })
        return res.json()
    
    def _validate_airports_result(self, res):
        if len(res["airports"]) > 0:
            return ValidationResult(
                is_valid=True,
                value=res["airports"],
            )
        else:
            return ValidationResult(
                is_valid=False,
                message="I'm sorry, we couldn't retrieve that airport, please enter a different name",
            )

    def _create_flights_summary(self, flight_search):
        return CardFactory.adaptive_card(AdaptiveCardHelper.create_search_summary_adapative_card(
            flight_search.origin,
            flight_search.origin_city,
            flight_search.travel_date

        ))

    def _create_hero_card(self) -> Attachment:
        card = HeroCard(
            title="",
            images=[
                CardImage(
                    url="https://www.bls.gov/cpi/factsheets/airline-fares-image.jpg"
                )
            ],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Get Started",
                    value="https://docs.microsoft.com/en-us/azure/bot-service/",
                )
            ],
        )
        return CardFactory.hero_card(card)

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
                                value=candidate.strftime("%m/%d/%Y"),
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