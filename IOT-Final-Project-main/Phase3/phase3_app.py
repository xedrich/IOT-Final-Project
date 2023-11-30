from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt
import time

app = Flask(__name__)

# Initialize sensor data
sensor_data = {
    'light_intensity': 0,
    'status': 'OFF',
    'email_message': 'No email sent'
}

# MQTT settings
mqtt_broker_ip = '192.168.0.105'
mqtt_topic = 'light_intensity'

def on_message(client, userdata, message):
    global sensor_data
    sensor_data['light_intensity'] = int(message.payload.decode("utf-8"))

    # Check light intensity and update status and email message
    if sensor_data['light_intensity'] < 400:
        sensor_data['status'] = 'ON'
        sensor_data['email_message'] = f'The Light is ON at {time.strftime("%H:%M")} time.'

client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker_ip, 1883, 60)
client.subscribe(mqtt_topic)
client.loop_start()

@app.route('/')
def index():
    return render_template('indexphase3.html', light_intensity=sensor_data['light_intensity'], status=sensor_data['status'], email_message=sensor_data['email_message'])

@app.route('/get_sensor_data')
def get_sensor_data():
    global sensor_data
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
