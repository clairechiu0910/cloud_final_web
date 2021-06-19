from flask import Flask, render_template, jsonify
from flask import request
from ArduinoDataRepo import ArduinoDataRepo
from DB_rainRepo import DB_rainRepo
from predictionRepo import predictionRepo
import json
import boto3 

application = Flask(__name__)
jinja_options = application.jinja_options.copy()
jinja_options.update(dict(
    variable_start_string='(%',
    variable_end_string='%)'
))
application.jinja_options = jinja_options
application.config["DEBUG"] = True 

@application.route('/')
def hello_world():
    return notifications()

@application.route('/notifications')
def notifications():
    return render_template('notifications.html')

@application.route('/data_history')
def data_history():
    return render_template('data_history.html')

@application.route('/api/t_h/d/', methods=['GET'])
def get_temperature_humidity():
    time, humidity, temperature = ArduinoDataRepo().get_today_data()
    data = {
        'time': time,
        'humidity': humidity,
        'temperature': temperature
    }
    return jsonify(data)

@application.route('/api/pi/', methods=['GET'])
def get_pi_all_data():
    states = DB_rainRepo().get_all_data()
    return jsonify(states)

@application.route('/api/model/', methods=['GET'])
def get_model_all_data():
    results = predictionRepo().get_all_data()
    return jsonify(results)

@application.route('/api/pred/', methods=['GET'])
def get_model_pred():
    import boto3 
    import json 
    tmp, hum = ArduinoDataRepo().get_latest_data()
    
    # tmp = 30
    # hum = 90
    endpoint = 'xgboost-2021-06-18-13-39-26-663'
    aws_access_key_id=''
    aws_secret_access_key=''

    runtime = boto3.client('sagemaker-runtime', region_name="us-east-1", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    text = str(tmp) + ',' + str(hum) + ',10'
    
    
    response = runtime.invoke_endpoint(EndpointName=endpoint, ContentType='text/csv', Body=text)
    result = json.loads(response['Body'].read().decode())
    result_float = float(result)

    #sns
    send_mail_to_notify(result_float)
    
    result = str(result)


    model_pred = {
        'prediction_result': result
    }
    return jsonify(model_pred)
    
def send_mail_to_notify(result):
    result = result * 100 
    result = float("{0:.2f}".format(result))
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

if __name__ == "__main__":
    application.debug = True
    application.run()
