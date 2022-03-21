# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from ask_sdk_model.interfaces.alexa.presentation.apl import ExecuteCommandsDirective

import json 

def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)



class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Say hello to play a video"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"
        if handler_input.request_envelope.context.system.device.supported_interfaces.alexa_presentation_apl is not None:
            #document=_load_apl_document("./APL/layout/videoLayout.json"), 
            #document=_load_apl_document("./APL/layout/controls.json"),
            return (
                handler_input.response_builder
                    .add_directive(
                            RenderDocumentDirective(
                                token="videoID",
                                document=_load_apl_document("./APL/layout/videoLayout.json"), 
                                datasources={
                                    "track": {
                                          "url": [
                                            "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/1080/Big_Buck_Bunny_1080_10s_1MB.mp4",
                                            "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                                            "https://d2o906d8ln7ui1.cloudfront.net/videos/AdobeStock_277864451.mov",
                                            "https://d2o906d8ln7ui1.cloudfront.net/videos/AdobeStock_292807382.mov",
                                            "https://d2o906d8ln7ui1.cloudfront.net/videos/AdobeStock_320293418.mov"
                                         ]}
                                    }
                            )
                        )
                    .add_directive(
                            ExecuteCommandsDirective(
                                token="videoID",
                                commands = [
                                    {
                                        "type": "ControlMedia",
                                        "componentId": "videoPlayerId",
                                        "command": "play"
                                    }
                                ]
                            )
                        )
    
                    .response
            )
        else:
            speak_output = "Sorry your device can't show videos"
            return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class PlayIntentHandler(AbstractRequestHandler):
    """Handler for Play Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("playIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("in play handler")
        speak_output = "Playing"

        return (
            handler_input.response_builder
            .add_directive(
                    ExecuteCommandsDirective(
                        token="videoID",
                        commands = [
                            {
                                "type": "ControlMedia",
                                "componentId": "videoPlayerId",
                                "command": "play"
                            }
                        ]
                    )
            )
            .speak(speak_output)
            .response
        )

class NextIntentHandler(AbstractRequestHandler):
    """Handler for Next Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NextIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("in next handler")
        speak_output = "Skipping to next track"

        return (
            handler_input.response_builder
            .add_directive(
                    ExecuteCommandsDirective(
                        token="videoID",
                        commands = [
                            {
                                "type": "ControlMedia",
                                "componentId": "videoPlayerId",
                                "command": "next"
                            }
                        ]
                    )
            )
            .speak(speak_output)
            .response
        )


class PreviousIntentHandler(AbstractRequestHandler):
    """Handler for Previous Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.PreviousIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("in previous handler")
        speak_output = "Going to previous track"

        return (
            handler_input.response_builder
            .add_directive(
                    ExecuteCommandsDirective(
                        token="videoID",
                        commands = [
                            {
                                "type": "ControlMedia",
                                "componentId": "videoPlayerId",
                                "command": "previous"
                            }
                        ]
                    )
            )
            .speak(speak_output)
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(PlayIntentHandler())
sb.add_request_handler(NextIntentHandler())
sb.add_request_handler(PreviousIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()