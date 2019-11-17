import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    print(event)
    print(event["queryStringParameters"])
    phone=event["queryStringParameters"]["phone"]
    message=event["queryStringParameters"]["message"]
    client = boto3.client(
    "sns",
    region_name="us-east-1"
    )
    
    topic_arn="arn:aws:sns:us-east-1:716038874109:"+str(phone)
    print(topic_arn)
    try:
        print(client.publish(Message=message, TopicArn=topic_arn))
        clientResponse="message sent"
    except ClientError as e:
        print(e.response['Error']['Message'])
        clientResponse=str(e.response['Error']['Message'])
    return {
        'statusCode': 200,
        'body': json.dumps(clientResponse)
    }


