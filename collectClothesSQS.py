import boto3
from botocore.exceptions import ClientError

class collectClothesSQS():
    def __init__(self):
        queue_name = 'collectClothes'
        
        sqs = boto3.resource('sqs')
        self.queue = sqs.get_queue_by_name(QueueName=queue_name)   

    def send_message(self, message_body, message_attributes=None):
        if not message_attributes:
            message_attributes = {}

        try:
            response = self.queue.send_message(
                MessageBody=message_body,
                MessageAttributes=message_attributes
            )
        except ClientError as error:
            print("Send message failed: %s", message_body)
            raise error
        else:
            return response

if __name__ == '__main__':
    print(collectClothesSQS().send_message('hello'))