import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    print(event)
    print(event["queryStringParameters"])

    
    try:
        location=event["queryStringParameters"]["location"]
    except:
        location="None"
        
    try:
        keywords=event["queryStringParameters"]["keyword"]
    except:
        keywords="None"
        
    try:
        orgId=event["queryStringParameters"]["orgId"]
    except:
        orgId="None"
    
    client = boto3.resource('dynamodb')

    table = client.Table("allFlags")
    
    print(table.table_status)
    
    #response=""
    
    try:
        if(location!="None"):
            response = table.query(
                IndexName='location-index',
                KeyConditionExpression=Key('location').eq(location)
            )
        else:
            response = table.query(
                IndexName='keywords-index',
                KeyConditionExpression=Key('keywords').eq(keywords)
                #KeyConditionExpression=Key('location').between('a','z'),
                #FilterExpression=Attr('keywords').is_in(keywords)
            )
        print(response)
        if 'Items' in response :
            if (len(response['Items']) == 0) :
                print("noNGO")
                responseMain="No_NGO"
            else:
                resultStringList=[]
                orgTable=client.Table("signin-orglist")
                for i in response['Items']:
                    print(i)
                    orgResponse=orgTable.query(
                        KeyConditionExpression=Key('orgId').eq(orgId)
                    )
                    print(orgResponse)
                    email=orgResponse['Items'][0]['email']
                    #orgName=orgResponse['Items'][0]['orgName']
                    phone=orgResponse['Items'][0]['phone']
                    # {'keywords': 'xyz', 'orgId': 'abc', 'location': 'noida', 'date': 'abc'}
                    #resultString="Positive flag {} - please contact {} by - email:{} or phone:{}".format(i['date'],projectName,email,phone)
                    resultdict={'date': i['date'], 'projectName': i['projectName'], 'email': email, 'phone': phone}
                    #‘‘Positive flag 12/08/2019 – please contact WCP Graeme Ellis – graeme.ellis@wcp.org’’
                    resultStringList.append(resultdict)
                
                responseMain = resultStringList
                print(responseMain)
                
        else:
            responseMain="No_NGO"
                
    except ClientError as e:
        print(e.response['Error']['Message'])
        responseMain=str(e.response['Error']['Message'])
        
    #table.put_item(Item= {'id': '34','company':  'microsoft'})
    
    return {
        'statusCode': 200,
        'body': json.dumps(responseMain)
    }



