from kendra_tools import getPdfResources

def lambda_handler(event, context):
    """
    :param event: Lex event
    :return: A string response containing the Kendra response and the link of the PDF resource
    """

    return_object = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "confirmationState": "Confirmed",
                "name": "CarIntent",
                "state": "Fulfilled",
            },
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": getPdfResources(event) #'~'.join(getPdfResources(event))
            }
        ]
    }

    return return_object



