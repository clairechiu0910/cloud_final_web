import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

class ArduinoDataRepo():
    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        self.table = dynamodb.Table('ArduinoData')
        
    def get_today_data(self):
        response = self.table.scan(
            FilterExpression=Attr('day').eq(datetime.now().day)
        )
        items = response['Items']
        items.sort(key=lambda item: datetime.strptime(item['time'], '%Y/%m/%d %H:%M:%S'))
        time = list()
        humidity = list()
        temperature = list()
        for item in items:
            get_time = datetime.strptime(item['time'], '%Y/%m/%d %H:%M:%S')
            time.append(get_time.strftime("%Y/%m/%d %H:%M")),
            humidity.append(float(item['humidity']))
            temperature.append(float(item['temperature']))
        return time, humidity, temperature
    
    def get_latest_data(self):
        response = self.table.scan(
            FilterExpression=Attr('day').eq(datetime.now().day)
        )
        items = response['Items']
        items.sort(key=lambda item: datetime.strptime(item['time'], '%Y/%m/%d %H:%M:%S'), reverse=True)
        humidity = float(items[0]['humidity'])
        temperature = float(items[0]['temperature'])
        return humidity, temperature
        
        
    
if __name__ == '__main__':
    print(ArduinoDataRepo().get_today_data())
    print(ArduinoDataRepo().get_latest_data())