# Python script connected to a chatbot which is created using AWS Lex, AWS Kendra used for document parsing, and serverless architecture (AWS Lambda) to provide a natural language processing conversations

Python script: Simple script to send questions to the chatbot and retrieve answers\
AWS Lex: Chatbot interface with multiple configurations for the best user experience\
AWS Lambda: Serverless functions that will link all AWS components
AWS Kendra: A service that will scrape web pages

## Create a bot with AWS Lex
1. Go to AWS Lex Console and create a new bot
2. Create an empty intent and give it an appropriate name
3. In the Intent configuration setup the following:
* Sample utterances
* Slots
* Confirmation prompts and decline responses (Optional)
4. Save/Build and Test the current Bot configuration

``You should be able to prompt the slots you created using a sample utterance.``


## Setup AWS Lambda (Python)
1. Inside the following block of code `def lambda_handler(event, context):` add `print(event)`
2. Go back to AWS Lex Console and inside your Intent configuration
3. Under Fulfilment section, click advanced options, under Fulfilment Lambda code hook, select `Use a Lambda function for fulfilment` checkbox
4. Save, Build, and test Lex (make sure to complete all slots)
``You should get an error.``


## Checking error logs
1. Go to your Lambda function configuration 
2. Go to Monitor -> Logs
3. Under Recent invocations you should be able to see your error logs and explore them further by clicking on the `LogStream` which should take you to the CloudWatch Management Console


## Writing Lambda function to return a response back to Lex
1. Go to your Lambda function and paste the following code inside the `def lambda_handler(event, context):` block:
```
return_object = {
    "sessionState": {
        "dialogAction": {
          "type": "Close"
        },
        "intent": {
          "confirmationState": "Confirmed",
          "name": "CarIntent",
          "state": "Fulfilled"
        }
    },
    "messages": [
        {
          "contentType": "PlainText",
          "content": "First response",

        },
        {
            "contentType":"PlainText",
            "content": "Second response"

        }
    ]
}


return return_object
```

2. Test the function using Lex\
`As soon as you complete all slots you should get two responses from Lex`


## Create Kendra index and datasource (PDF)
1. TBC


## Connect Kendra to a Lambda funcion
1. TBC


## Update Lambda permissions so it can access Kendra
1. TBC
