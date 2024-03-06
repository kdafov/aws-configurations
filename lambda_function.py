from request_validation import checkRequest
from response_validation import construct_response
from lex_tools import interact, ask_second_question
from dynamo_tools import check_item_and_update
from video_resource import return_video_resources
from logger import log
from web_resource import retrieve_web_resource


def lambda_handler(event, context):
    """
    Lambda handler for endpoint POST:/messages
    :param event: JSON of the event (auto)
    :param context: The context of event (auto)
    :return: Returns JSON response
    """

    log("API_process_message/lambda_function()", "1", "Event received to Lambda function", event)

    # Check request type
    requestType = checkRequest(event)
    log("API_process_message/lambda_function()", "2", "Request received is valid?", requestType)

    if (requestType):
        # Get user message & sessionId
        message = event['body']['message']
        sessionId = event['body']['sessionId']
        multipleQuestions = event['body']['multipleQuestions']
        log("API_process_message/lambda_function()", "3", "User input received",
            "message: " + str(message) + " ;sessionId: " + str(sessionId))

        # Check if second question is asked
        if multipleQuestions:
            log("API_process_message/lambda_function()", "4-1", "Another question asked. Manipulating Lex.", "")
            lex_response = ask_second_question(sessionId, message)
            log("API_process_message/lambda_function()", "5-2",
                "Manipulation successfull. Response from lex received with content", lex_response)
        else:
            # Get the response from Lex
            log("API_process_message/lambda_function()", "4-2", "Sending message and sessionId to Lex", "")
            lex_response = interact(message, sessionId)
            log("API_process_message/lambda_function()", "5-2", "Response from lex received with content", lex_response)

        # Check if lex session state is closed i.e., if the user is at the end of the conversation
        log("API_process_message/lambda_function()", "6", "Checking if user asked question", "")

        try:
            if lex_response['sessionState']['dialogAction']['type'] == 'Close':
                log("API_process_message/lambda_function()", "7-1",
                    "User asked questions. Getting appropriate responses.", "")

                # Get youtube response
                model = lex_response['sessionState']['intent']['slots']['carNumber']['value']['resolvedValues'][0]
                question = lex_response['sessionState']['intent']['slots']['question']['value']['originalValue']
                youtube_response = return_video_resources(model, question)
                log("API_process_message/lambda_function()", "7-2", "Youtube response acquired.", "")

                # Get web response
                web_response = retrieve_web_resource(model)
                log("API_process_message/lambda_function()", "7-3", "Web response acquired.", "")
            else:
                log("API_process_message/lambda_function()", "7", "User is still completing slots. Continue.", "")
                youtube_response = ''
                web_response = ''

            # Refactor Lex response
            lex_message_content = lex_response['messages'][0]['content']

            # Save user message and lex response to database
            log("API_process_message/lambda_function()", "8", "Database operation started. Saving conversation state.",
                "")

            check_item_and_update(sessionId, [message, lex_message_content])
            log("API_process_message/lambda_function()", "9",
                "Database operation successfully completed. Conversation state is up to date!", "")

            # Construct response JSON (valid request)
            log("API_process_message/lambda_function()", "10", "Returning response to user. Type", requestType)
            response = construct_response(requestType,
                                          {"websiteResource": web_response, "lexResponse": lex_message_content,
                                           "videoResource": youtube_response})
        except Exception as e:
            log("API_process_message/lambda_function()", "E4", "EXCEPTION", e)
            response = construct_response(requestType,
                                          "Invalid utterance was send and could not be handled. Please try again.")
    else:
        # Construct response JSON (invalid request)
        log("API_process_message/lambda_function()", "3", "Returning response to user. Type", requestType)
        response = construct_response(requestType, None)

    # Return response
    return response

