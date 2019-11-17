import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    print(event)
    #print(event["queryStringParameters"])

    
    try:
        location=event["queryStringParameters"]["location"]
    except:
        location="None"
        
    try:
        keyword=event["queryStringParameters"]["keyword"]
    except:
        keyword="None"
    
    client = boto3.resource('dynamodb')

    table = client.Table("FlagList")
    
    print(table.table_status)
    
    #response=""
    
    try:
        if(location!="None"):
            response = table.query(
                IndexName='Location-index',
                KeyConditionExpression=Key('Location').eq(location)
            )
        else:
            response = table.query(
                IndexName='KeyWords-index',
                KeyConditionExpression=Key('location').between('a','z'),
                FilterExpression=Attr('KeyWords').is_in(keyword)
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