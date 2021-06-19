import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime

RAINING = 0
NOT_RAIN = 1

IS_CLOTHES_COLLECTED = 1
IS_CLOTHES_OUTSIDE = 0

# const rain_state == 1, not rain
# rain_state == 0, raining

class DB_rainRepo():
    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        self.table = dynamodb.Table('DB_rain')
        
    def is_rain(self):
        response = self.table.scan(
            FilterExpression=Attr('motor_state').between(0, 1)
        )
        items = response['Items']
        
        items.sort(key=lambda item: datetime.strptime(item['date'], '%Y/%m/%d %H:%M:%S'), reverse=True)
        
        is_rain = items[0]['rain_state'] == RAINING
        
        return is_rain

    def get_all_data(self):
        response = self.table.scan(
            FilterExpression=Attr('motor_state').between(0, 1)
        )
        items = response['Items']
        
        items.sort(key=lambda item: datetime.strptime(item['date'], '%Y/%m/%d %H:%M:%S'), reverse=True)
        
        states = list()        
        for item in items:
            is_rain = False
            rain = "No rain detected."
            if item['rain_state'] == RAINING:
                is_rain = True
                rain = "It's raining outside."
            
            clothes = "The clothes is swinging outside."
            if item['motor_state'] == IS_CLOTHES_COLLECTED:
                clothes = "The clothes is collected."
            
            states.append({
                'date': item['date'],
                'is_rain': is_rain,
                'rain': rain,
                'cloth': clothes
            })
        
        return states
    
if __name__ == '__main__':
    print(f'Is rain: {DB_rainRepo().is_rain()}')
    print('all data:')
    print(DB_rainRepo().get_all_data())