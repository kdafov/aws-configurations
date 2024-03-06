import boto3
from logger import log
from dynamo_tools import return_current_conversation


def interact(message, sessionID):
    """
    This function will pass a message to Lex UI and return the response
    :param message: Message to send to Lex
    :param sessionID: Unique session Id for Lex
    :return: Response from Lex
    """

    # Establish client connection
    client = boto3.client('lexv2-runtime')
    log("API_process_message/lex_tools()", "1", "Connection to lexv2-runtime established.", "")

    # Make query and save the response
    log("API_process_message/lex_tools()", "2",
        "Creating a request to Lex with sessionId: " + sessionID + " and text: " + message, "")
    response = client.recognize_text(
        botId='YOUR-BOT-ID',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId=sessionID,
        text=message)
    log("API_process_message/lex_tools()", "3", "Request to Lex was successful with response", response)

    # Return response from the query
    return response


def ask_second_question(sessionId, question):
    """
    :param sessionId: The chat session Id
    :param question: The next question of the user
    :return Lex's response for the next question of the user
    """

    # Get the initial utterance of the chat and the car model
    log("API_process_message/lex_tools()", "1", "Trying to get user inputs from conversation state.", "")
    conversation = return_current_conversation(sessionId)
    del conversation[-1]
    for each in conversation:
        if each == "Hi, I am here to help you! Can you tell me your car model?" or each == "Thank you! How can I help you?":
            conversation.remove(each)
    for each in conversation:
        if any(char.isdigit() for char in each) == False and each.lower() != "hi":
            conversation.remove(each)
    log("API_process_message/lex_tools()", "1", "User input found in conversation state. Continuing.", "")

    # Send utterance, model and question to lex
    client = boto3.client('lexv2-runtime')
    log("API_process_message/lex_tools()", "2",
        "Connection to lexv2-runtime established. Sending utterance and model to prepare Lex for second question.", "")

    for chatInput in conversation:
        client.recognize_text(
            botId='YOUR-BOT-ID',
            botAliasId='TSTALIASID',
            localeId='en_US',
            sessionId=sessionId,
            text=chatInput)

    response = client.recognize_text(
        botId='YOUR-BOT-ID',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId=sessionId,
        text=question)

    # Return response
    return response