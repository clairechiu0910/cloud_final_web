import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

class ArduinoDataRepo():
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')

        self.table = dynamodb.Table('ArduinoData')
        
    def get_today_data(self):
        response = self.table.scan(
            FilterExpression=Attr('day').eq(datetime.now().day)
        )
        items = response['Items']
        himidity = list()
        temperature = list()
        time = list()
        for item in items:
            time.append(item['time'])
            himidity.append(float(item['humidity']))
            temperature.append(float(item['temperature']))
        return time, himidity, temperature
    
if __name__ == '__main__':
    print(ArduinoDataRepo().get_today_data())