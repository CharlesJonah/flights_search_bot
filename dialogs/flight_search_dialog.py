from botbuilder.core import MessageFactory, UserState
from datetime import datetime, date

from models import FlightSearch, ConversationFlow, Question

class ValidationResult:
    def __init__(
        self, is_valid: bool = False, value: object = None, message: str = None):
        self.is_valid = is_valid
        self.value = value
        self.message = message

class FlightSearchDialog(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState):
        if conversation_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. user_state is required but None was given"
            )

        self.conversation_state = conversation_state
        self.user_state = user_state

        self.flow_accessor = self.conversation_state.create_property("ConversationFlow")
        self.profile_accessor = self.user_state.create_property("UserProfile")

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        step_context.values["origin"] = step_context.result

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Where will be flying from ?")
            ),
        )

    async def return_trip_confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        step_context.values["destination"] = step_context.result

        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Do you want to book for a return trip?")
            ),
        )
  
    async def travel_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        step_context.values["return_trip"] = step_context.result

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Select your travel date please?")
            ),
        )
    
    async def return_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["travel_date"] = step_context.result
        if step_context.values["return_trip"]:
            return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Select your return date please?")
            ),
        )
        return await step_context.next(-1)

    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            flight_search = await self.user_profile_accessor.get(
                step_context.context, FlightSearchModel
            )

            flight_search.origin = step_context.values["origin"]
            flight_search.destination = step_context.values["destination"]
            flight_search.return_trip = step_context.values["return_trip"]
            flight_search.travel_date = step_context.values["travel_date"]
            flight_search.return_date = step_context.result

            msg = f"I have your mode of transport as {flight_search.origin} and your name as {flight_search.destination}."

            await step_context.context.send_activity(MessageFactory.text(msg))
            return await step_context.end_dialog()

    @staticmethod
    async def date_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day
        date_value = prompt_context.recognized.value
        try:
            valid_date = datetime.strptime(date_value, "%m/%d/%Y").date()
            if date(current_year, current_month, current_day) <= valid_date \
                 <= date(current_year+1, current_month, current_day+1):
                is_valid = True
            else:
                is_valid = False
        except:
            is_valid = False

        return is_valid

    # @staticmethod
    # async def picture_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
    #     if not prompt_context.recognized.succeeded:
    #         await prompt_context.context.send_activity(
    #             "No attachments received. Proceeding without a profile picture..."
    #         )

    #         # We can return true from a validator function even if recognized.succeeded is false.
    #         return True

    #     attachments = prompt_context.recognized.value

    #     valid_images = [
    #         attachment
    #         for attachment in attachments
    #         if attachment.content_type in ["image/jpeg", "image/png"]
    #     ]

    #     prompt_context.recognized.value = valid_images

    #     # If none of the attachments are valid images, the retry prompt should be sent.
    #     return len(valid_images) > 0