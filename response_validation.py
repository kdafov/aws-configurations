def construct_response(successState, sources):
    """
    :param successState: True: valid request | False: invalid request
    :param sources: The body that should be returned with the response
    :return: JSON structure containing the response
    """

    if successState:
        returnObject = {
            'statusCode': 200,
            'sources': sources
        }
    else:
        returnObject = {
            'statusCode': 401,
            'sources': 'Your request has invalid body. Make sure that you only send keys: sessionId, message. Make sure each key has a value length of at least 1 and that there are no extra keys sent.'
        }

    return returnObject