from logger import log

def checkRequest(event):
    """
    This function will check the body of the request send to the API
    :param event: The event (auto)
    :return: True: valid request body | False: invalid body
    """

    log("API_process_message/request_validation()", "1", "Validation of request body started", "")

    try:
        # Check if message and sessionId values are passed inside the JSON of the body of the request
        message = event['body']['message']
        sessionId = event['body']['sessionId']
        multipleQuestions = event['body']['multipleQuestions']
        validBody = True
        log("API_process_message/request_validation()", "2", "Required parameters found inside request body", "")
    except:
        # Message value has not been found
        validBody = False
        log("API_process_message/request_validation()", "2", "Required parameters NOT found inside request body", "")

    # Check that there are no other unnecessary values are sent in the JSON of the body of the request
    if validBody and len(message) > 0 and len(sessionId) > 2 and len(event['body']) == 3:
        log("API_process_message/request_validation()", "3", "Length of request body verified. Returning TRUE.", "")
        return True  # Request from user is with valid body
    else:
        log("API_process_message/request_validation()", "3", "Length of request body NOT verified. Returning FALSE.",
            "")
        return False  # Request from user has invalid body
