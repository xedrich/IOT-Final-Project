from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import DHT11
import RPi.GPIO as GPIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import email
import requests

app = Flask(__name__)

# GPIO Configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
led_pin = 12
photoresistor_pin = 0  # Assuming you connected the photoresistor to analog pin 0
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)

# App Configuration
latest_sensor_data = {'temperature': 'N/A', 'humidity': 'N/A', 'light_intensity': 'N/A'}
fan_status = 'OFF'
led_status = 'OFF'

# Email Configuration
email_address = "bedabeda.beda21@gmail.com"
email_password = "naef inep pcbi aaek"
email_recipient = "bedabeda.beda21@gmail.com"

def update_sensor_data():
    with app.app_context():
        temperature, humidity = DHT11.read_sensor_data()
        light_intensity = read_photoresistor_data()
        latest_sensor_data.update({'temperature': temperature, 'humidity': humidity, 'light_intensity': light_intensity})

        if temperature > 21 and fan_status == 'OFF':
            send_email(email_recipient, "Temperature Alert", f"The current temperature is {temperature}°C. Would you like to turn on the fan?")

def read_photoresistor_data():
    try:
        response = requests.get('http://192.168.0.114/get_light_intensity')
        return response.json().get('light_intensity', 'N/A')
    except Exception as e:
        print(f"Failed to read photoresistor data: {e}")
        return 'N/A'

def send_email(recipient, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, recipient, msg.as_string())

        print('Successfully sent the email')
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_email():
    try:
        with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
            mail.login(email_address, email_password)
            mail.select("inbox")

            result, data = mail.search(None, "ALL")
            ids = data[0]
            id_list = ids.split()
            latest_email_id = id_list[-1]

            result, data = mail.fetch(latest_email_id, "(RFC822)")
            raw_email = data[0][1]

            msg = email.message_from_bytes(raw_email)
            subject = msg['subject']
            if "YES" in subject.upper():
                global fan_status
                fan_status = 'ON'

    except Exception as e:
        print(f"Failed to check email: {e}")

# Schedule periodic tasks
scheduler = BackgroundScheduler()
scheduler.add_job(update_sensor_data, 'interval', seconds=2)
scheduler.add_job(check_email, 'interval', seconds=2)
scheduler.start()

# Routes
@app.route('/')
def index():
    led_state = GPIO.input(led_pin)
    return render_template('index.html', **latest_sensor_data, fan_status=fan_status, led_state=led_state)

@app.route('/get_sensor_data')
def get_sensor_data():
    temperature, humidity = DHT11.read_sensor_data()
    latest_sensor_data.update({'temperature': temperature, 'humidity': humidity})
    return jsonify(**latest_sensor_data, fan_status=fan_status, led_status=led_status)

@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    led_state = GPIO.input(led_pin)
    GPIO.output(led_pin, not led_state)
    global led_status
    led_status = 'ON' if not led_state else 'OFF'
    return jsonify({'led_state': GPIO.input(led_pin)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
