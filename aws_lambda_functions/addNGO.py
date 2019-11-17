import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    print(event)
    print(event["queryStringParameters"])
    location=event["queryStringParameters"]["location"]

    client = boto3.resource('dynamodb')

    table = client.Table("Zoohackathon")
    print(table.table_status)
    
    #response=""
    
    try:
        response = table.query(
            IndexName='location-index',
            KeyConditionExpression=Key('location').eq(location)
        )
        print(response)
        if 'Items' in response :
            if (len(response['Items']) == 0) :
                print("noNGO")
                response="No_NGO"
            else:
                response = str(response['Items'])
    except ClientError as e:
        print(e.response['Error']['Message'])
        response=str(e.response['Error']['Message'])
        
    #table.put_item(Item= {'id': '34','company':  'microsoft'})
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
