from flask import Flask, render_template, jsonify
from ddbRepo import ArduinoDataRepo
import json

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

@application.route('/api/t_h/d/')
def get_temperature_humidity():
    time, himidity, temperature = ArduinoDataRepo().get_today_data()
    data = json.dumps({
        'time': time,
        'himidity': himidity,
        'temperature': temperature
    })
    return jsonify(data)

if __name__ == "__main__":
    application.debug = True
    application.run()
