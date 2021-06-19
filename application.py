 zfrom flask import Flask, render_template, jsonify
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
    time, humidity, temperature = ArduinoDataRepo().get_today_data()
    data = {
        'time': time,
        'humidity': humidity,
        'temperature': temperature
    }
    return jsonify(data)

@application.route('/api/pred/<t_h>', methods=['GET'])
def get_model_pred(t_h):
    import boto3 
    import json 
    # return t_h 
    endpoint = ''
    aws_access_key_id=''
    aws_secret_access_key=''

    runtime = boto3.client('sagemaker-runtime', region_name="us-east-1", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    csv_text = '12, 90, 6'
    # Send CSV text via InvokeEndpoint API
    response = runtime.invoke_endpoint(EndpointName=endpoint, ContentType='text/csv', Body=csv_text)
    result = json.loads(response['Body'].read().decode())
    result = str(result)
    
    model_pred = {
        'prediction_result': result
    }
    return jsonify(model_pred)
    

if __name__ == "__main__":
    application.debug = True
    application.run()
