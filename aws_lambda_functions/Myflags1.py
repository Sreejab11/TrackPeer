import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    print(event)
    print(event["queryStringParameters"])
    orgId=str(event["queryStringParameters"]["orgId"])

    client = boto3.resource('dynamodb')

    table = client.Table("allFlags")
    print(table.table_status)
    
    #response=""
    
    try:
        response = table.query(
            KeyConditionExpression=Key('orgId').eq(orgId)
        )
        print(response)
        if 'Items' in response :
            if (len(response['Items']) == 0) :
                print("noItems")
                response="No_Items"
            else:
                response = str(response['Items'])
    except ClientError as e:
        print(e.response['Error']['Message'])
        response=str(e.response['Error']['Message'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
