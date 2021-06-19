import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime

class predictionRepo():
    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        self.table = dynamodb.Table('prediction')
        a = 0
        
    def get_all_data(self):
        response = self.table.scan(
            FilterExpression=Attr('propability').lt(120)
        )
        items = response['Items']
        items.sort(key=lambda item: datetime.strptime(item['datetime'], '%Y%m%d%H%M%S'), reverse=True)
        
        predicts = list()
        for item in items:
            get_time = datetime.strptime(item['datetime'], '%Y%m%d%H%M%S')
            predicts.append({
                'date': get_time.strftime("%Y/%m/%d %H:%M:%S"),
                'result': float(item['propability'])
            })
        return predicts
    
if __name__ == '__main__':
    print(predictionRepo().get_all_data())