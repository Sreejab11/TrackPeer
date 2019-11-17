import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import base64

def lambda_handler(event, context):
    
    print(event)
    
    print(event["queryStringParameters"])
    email=str(event["queryStringParameters"]["email"])
    password=str(event["queryStringParameters"]["password"])
    
    data=email+password
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    orgIdprovided = str(encodedBytes, "utf-8")
    print(orgIdprovided)
    #orgId=str(base64.b64encode(orgName+email+password))
    
    client = boto3.resource('dynamodb')

    table = client.Table("signin-orglist")
    print(table.table_status)
    
    #response=""
    
    try:
        response = table.query(
            KeyConditionExpression=Key('orgId').eq(orgIdprovided)
        )
        print(response)
        if 'Items' in response :
            if (len(response['Items']) == 0) :
                print("Incorrect email or password")
                responseMain="Incorrect email or password"
            else:
                str1=str(response['Items'][0]['orgName'])
                str2=str(response['Items'][0]['orgId'])
                print(str1,str2)
                responseMain = str1+","+str2
                
    except ClientError as e:
        print(e.response['Error']['Message'])
        responseMain=str(e.response['Error']['Message'])
        
    
    return {
        'statusCode': 200,
        'body': json.dumps(responseMain)
    }