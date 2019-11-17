import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    print(event)
    print(event["queryStringParameters"])
    orgId=str(event["queryStringParameters"]["orgId"])
    location=str(event["queryStringParameters"]["location"])
    date=str(event["queryStringParameters"]["date"])
    keywords=str(event["queryStringParameters"]["keywords"])
    projectName=str(event["queryStringParameters"]["projectName"])

    client = boto3.resource('dynamodb')

    table = client.Table("allFlags")
    print(table.table_status)
    
    #response=""
    
    try:
        response = table.put_item(Item= {'orgId': orgId,'location': location,'date':date,'keywords':keywords,'projectName':projectName})
        
    except ClientError as e:
        print(e.response['Error']['Message'])
        response=str(e.response['Error']['Message'])
        
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
