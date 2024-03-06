import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('testTable')


def delete_db_content():
    """
    This function will wipe the content of the database
    :returns Response code: 200 Success/OK | 501 Internal Server Error
    """

    try:
        # Scan all rows in the database
        scan = table.scan()
        with table.batch_writer() as batch:
            # For each item...
            for each in scan['Items']:
                # ...Delete row
                batch.delete_item(
                    Key={
                        'sessionId': each['sessionId']
                    }
                )
        return 200

    except Exception as e:
        print("API_reset_db/delete_db_content() in dynamo_tools.py : THROWS EXCEPTION: >>>", e)
        return 501
