import json
import boto3 

def lambda_handler(event, context):
    region_name = "us-east-1"
    time = event['time']
    tmp = event['tmp']
    hum = event['hum']

    endpoint = 'xgboost-2021-06-18-13-39-26-663'
    aws_access_key_id='AKIARO6BBYISAGPKSZMI'
    aws_secret_access_key='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'

    runtime = boto3.client('sagemaker-runtime', region_name="us-east-1", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    text = str(tmp) + ',' + str(hum) + ',10'
    
    
    response = runtime.invoke_endpoint(EndpointName=endpoint, ContentType='text/csv', Body=text)
    result = json.loads(response['Body'].read().decode())
    result = float(result)

    result = result * 100
    result = float("{0:.2f}".format(result))
    
    send_mail_to_notify(result)
    
    result = str(result)
    write_ddb(time, result)


    model_pred = {
        'prediction_result': result
    }

    # 寫進ddb
    write_ddb(time, result)


def send_mail_to_notify(result):
    if result <= 50:
        # 低機率會下雨
        sub = "【保持平常心】您的衣服正在曝曬中"
        msg = "您好, \n請保持平常心！目前僅有" + str(result) +"% 可能會降雨。\n請安心繼續讓衣服持續曝曬。\n不過，也許你想收衣服了，那請點以下連結告訴我\nhttp://finalgroup5.us-east-1.elasticbeanstalk.com/notifications\n\n\n\n\n------\nBest Regards, 收衣機"
    elif result > 50 and result <= 80:
        sub = "【保持平常心】別擔心！我們會幫您隨時注意天氣"
        msg = "您好, \n降雨機率來到了" + str(result) +"%！\n請安心繼續讓衣服持續曝曬，降雨時再呼喚我們。\n\n不過，也許你想收衣服了，那請點以下連結告訴我。http://finalgroup5.us-east-1.elasticbeanstalk.com/notifications\n\n\n-----\nBest Regards, 收衣機"
    elif result > 80:
        sub = "【我的天，要下雨啦】趕快收衣服"
        msg = "您好, \n降雨機率來到了" + str(result) +"%！\n我們強烈建議您點選以下網址，告訴我們您的決定。\nhttp://finalgroup5.us-east-1.elasticbeanstalk.com/notifications\n\n\n\n------\nBest Regards, 收衣機"
    
    cli = boto3.client('sns', region_name="us-east-1")

    response = cli.publish(
        TopicArn='arn:aws:sns:us-east-1:099287135517:finalproj',
        Message=msg,
        Subject=sub,
        MessageStructure='string'
    )
def write_ddb(time, result):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('prediction')
    response = table.put_item(
       Item={
            'datetime': time,
            'propability': result
        }
    )
    return response
    