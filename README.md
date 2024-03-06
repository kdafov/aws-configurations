# AWS Configuration file featuring AWS Lex,

*AWS Lex*: Chatbot interface with multiple configurations for the best user experience\
*AWS Lambda*: Serverless functions that will link all AWS components\
*AWS Kendra*: A service that will scrape web pages and/or PDF files to match content to input word and return matched content

## Create a bot with AWS Lex
1. Go to AWS Lex Console and create a new bot
2. Create an empty intent and give it an appropriate name
3. In the Intent configuration setup the following:
* Sample utterances
* Slots
* Confirmation prompts and decline responses (Optional)
4. Save/Build and Test the current Bot configuration

``You should be able to prompt the slots you created using a sample utterance.``


## Setup AWS Lambda (Python 3.9)
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
1. Create an index and follow the steps
2. Add data source from either S3 or Web Crawler
3. Test your kendra index internally by using the `Search indexed content` from the navigation menu
4. Create a new lambda function and add the following code:
```
kendra = boto3.client("kendra")

response = kendra.query(
    QueryText = event['inputTranscript'],
    IndexId = "{ PUT_YOUR_KENDRA_INDEX_ID_HERE }")
    
answer = response["ResultItems"][0]["DocumentExcerpt"]["Text"]
```
**Note:** The response from Kendra is stored in the `answer` variable. Use the above response structure for Lex to return it properly.

5. In the IAM panel add appropriate permissions (Kendra permission) to your Lambda function.
6. Test


## Create a layer and link it to lambda function
1. On local machine, `cd` to the python project you want to import as a layer
2. Make a new directory inside using `mkdir -p layer/python/lib/python3.9/site-packages/ `
3. Install PIP packages using the command `pip install { MODULE_NAME } -t layer/python/lib/python3.9/site-packages/ `
4. Navigate to the layer folder and zip it: `cd layer` followed by `zip -r mypackage.zip *  `
5. In AWS Lambda select Layers under Additional resources from the navigation menu
6. Create new layer and upload the zip file generated from step 4
7. Select compatible architectures (x86_64 default) and add runtime (Python 3.9 in this example) and click `Create`
8. Back inside your lambda function, in the Layers section at the bottom of the screen, click on `Add a layer` 
9. Select `Custom layers`, add you AWS Layers and click `Add`
10. Test


## Create API Gateway
1. Go to the API Gateway console and click `Create API`
2. Click on `Build` for the non-private REST API version
3. Give it name and description and click `Create`
4. In the Resources section click on `Actions` and select `Create method` and select `GET`
5. Select Lambda function to which to link the API endpoint\
If you need to create one add the following content to it:
```
responseObject = {
    'statusCode': 200,
    'headers': {
        "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST,OPTIONS"
    },
    'message': 'This is the response message from my GET method'
}
return responseObject
```
6. Click `Save` and `OK`
7. Go to the `Actions` menu and select `Deploy API`
8. For `Deployment stage` create new one and give it a name and click `Deploy`
9. Test the URL

