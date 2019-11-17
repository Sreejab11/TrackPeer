import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import base64

def subscription(sns_client,phone):
    
    try:
        topic = sns_client.create_topic(Name=phone)
        topic_arn = topic['TopicArn']  # get its Amazon Resource Name

        snsResponse=sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='sms',
            Endpoint=phone  # <-- number who'll receive an SMS message.
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        snsResponse=str(e.response['Error']['Message'])

    
    return(str(snsResponse))

def lambda_handler(event, context):
    
    print(event)
    
    #print(event["queryStringParameters"])
    orgName=str(event["queryStringParameters"]["orgName"])
    email=str(event["queryStringParameters"]["email"])
    phone=str(event["queryStringParameters"]["phone"])
    password=str(event["queryStringParameters"]["password"])
    
    data=email+password
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    orgId = str(encodedBytes, "utf-8")
    #orgId=str(base64.b64encode(orgName+email+password))
    
    client = boto3.resource('dynamodb')

    table = client.Table("signin-orglist")
    print(table.table_status)
    
    #response=""
    
    try:
        response = table.put_item(Item= {'orgId': orgId,'orgName': orgName , 'email':email,'phone':phone,'password':password})
        
    except ClientError as e:
        print(e.response['Error']['Message'])
        response=str(e.response['Error']['Message'])
    
    ######################   
    sns_client = boto3.client("sns",region_name="us-east-1")
    phoneSubscription=subscription(sns_client,phone)
    print(phoneSubscription)
    ######################
    return {
        'statusCode': 200,
        'body': json.dumps(orgId)
    }