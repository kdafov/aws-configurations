import boto3
from logger import log

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLE_NAME')


def check_item_and_update(sessionId, user_and_lex_message):
    """
    This function will check if a row with the session exists,
    and if yes update the state of the conversation,
    if no - create a new row and add the current state of the conversation.

    :param sessionId: The ID of the session
    :param user_and_lex_message: An array with the structure: [user_message, lex_response_to_user_message]
    :return: True: successful operation | False: error with exception log
    """

    try:
        log("API_process_message/dynamo_tools()", "1", "Connection to database successful.", "")

        log("API_process_message/dynamo_tools()", "2", "Trying to find a row matching the sessionId.", "")
        response = table.get_item(
            Key={
                'sessionId': sessionId
            })

        if 'Item' in response:
            log("API_process_message/dynamo_tools()", "3", "Conversation with the given sessionId found! [ID]",
                sessionId)

            # Get list of all previous messages
            all_previous_messages = response['Item']['messages']
            log("API_process_message/dynamo_tools()", "4", "All previous messages from session acquired. Content",
                all_previous_messages)

            log("API_process_message/dynamo_tools()", "5", "Updating content in database with new content.", "")
            return update_item(sessionId, all_previous_messages, user_and_lex_message)

        if 'Item' not in response:
            log("API_process_message/dynamo_tools()", "3",
                "Session with given ID was not found. Creating a new session with ID", sessionId)
            return create_item(sessionId, user_and_lex_message)
    except Exception as e:
        log("API_process_message/dynamo_tools()/check_item_and_update()", "E1", "EXCEPTION", e)
        return False


def create_item(sessionId, message_list):
    """
    This function will create new row in the database with the given sessionId
    :param sessionId: The ID of the session
    :param message_list: A list containing the user message and the lex response to it
    :return: True: successful operation | False: error with exception log
    """

    try:
        response = table.put_item(
            Item={
                'sessionId': sessionId,
                'messages': message_list

            })

        # return list of messages
        log("API_process_message/dynamo_tools()", "4", "New record with given sessionId created.", "")
        return True

    except Exception as e:
        log("API_process_message/dynamo_tools()/create_item()", "E2", "EXCEPTION", e)
        return False


# Appends the new message to the retrieves list of messages in the get function
# Updates the item in the database to have that new message array and saves it
def update_item(sessionId, all_previous_messages, lex_and_user_messages):
    """
    This function will append the new content given to the current content in the database
    :param sessionId: The ID of the session
    :param all_previous_messages: Current content in the database
    :param lex_and_user_messages: A list containing the user message and the lex response to it
    :return: True: successful operation | False: error with exception log
    """

    # creates a new list, combining the old and new messages from user and lex
    all_previous_messages.extend(lex_and_user_messages)

    try:
        response = table.update_item(
            Key={
                'sessionId': sessionId,
            },

            # UpdateExpression='SET messages = :val1',
            UpdateExpression='SET messages = list_append(messages, :val1)',
            ExpressionAttributeValues={
                ':val1': lex_and_user_messages  # all_previous_messages
            },
            ReturnValues="UPDATED_NEW"
        )

        log("API_process_message/dynamo_tools()", "6", "Conversation successfully updated!", "")
        return True

    except Exception as e:
        log("API_process_message/dynamo_tools()/update_item()", "E3", "EXCEPTION", e)
        return False


def return_current_conversation(sessionId):
    """
    :param :The session Id of the chat
    :return :Returns the state of the conversation from the database
    """

    try:
        log("API_process_message/dynamo_tools()", "1", "Connection to database successful.", "")

        log("API_process_message/dynamo_tools()", "2", "Trying to find a row matching the sessionId.", "")
        response = table.get_item(
            Key={
                'sessionId': sessionId
            })

        if 'Item' in response:
            log("API_process_message/dynamo_tools()", "3", "Conversation with the given sessionId found! [ID]",
                sessionId)

            # Get list of all previous messages
            all_previous_messages = response['Item']['messages']
    except Exception as e:
        log("API_process_message/dynamo_tools()/check_item_and_update()", "E1", "EXCEPTION", e)
        all_previous_messages = ''

    return all_previous_messages