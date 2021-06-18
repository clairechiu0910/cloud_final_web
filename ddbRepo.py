import boto3
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('ArduinoData')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)

# response = table.query(
#     KeyConditionExpression=Key('time').lt('14:56:00')
# )
# items = response['Items']
# print(items)

response = table.scan(
    FilterExpression=Attr('humidity').lt(64)
)
items = response['Items']
print(items)