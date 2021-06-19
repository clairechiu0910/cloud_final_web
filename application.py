from flask import Flask, render_template, jsonify
from ddbRepo import ArduinoDataRepo
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
    time, himidity, temperature = ArduinoDataRepo().get_today_data()
    data = {
        'time': time,
        'himidity': himidity,
        'temperature': temperature
    }
    return jsonify(data)

# @application.route('/api/pred/d/')
# def get_rain_pred():
#     endpoint = 'xgboost-2021-06-18-13-39-26-663'
 
#     runtime = boto3.Session().client('sagemaker-runtime')
    
#     csv_text = '12, 90, 6'
#     # Send CSV text via InvokeEndpoint API
#     response = runtime.invoke_endpoint(EndpointName=endpoint, ContentType='text/csv', Body=csv_text)
#     # Unpack response
#     result = json.loads(response['Body'].read().decode())
#     print(result)

#     return jsonify(result)

if __name__ == "__main__":
    application.debug = True
    application.run()
