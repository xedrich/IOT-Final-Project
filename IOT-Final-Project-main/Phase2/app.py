from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import DHT11
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import email
import time

app = Flask(__name__)

# Define initial fan status
latest_sensor_data = {'temperature': 'N/A', 'humidity': 'N/A'}
fan_status = 'OFF'

# Email configuration
email_address = "GMAIL@gmail.com"
email_password = "APP PASSWORD"
email_recipient = "GMAIL@gmail.com"

def update_sensor_data():
    with app.app_context():
        temperature, humidity = DHT11.read_sensor_data()
        latest_sensor_data['temperature'] = temperature
        latest_sensor_data['humidity'] = humidity

        # Check temperature and send email
        if temperature > 24 and fan_status == 'OFF':
            email_body = f"The current temperature is {temperature}°C. Would you like to turn on the fan?"
            send_email(email_recipient, "Temperature Alert", email_body)

def send_email(recipient, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, recipient, msg.as_string())
        server.close()
        print('Successfully sent the email')
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_email():
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
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
        mail.logout()
    except Exception as e:
        print(f"Failed to check email: {e}")

# Schedule periodic tasks
scheduler = BackgroundScheduler()
scheduler.add_job(update_sensor_data, 'interval', seconds=2)
scheduler.add_job(check_email, 'interval', seconds=2)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html', temperature=latest_sensor_data['temperature'], humidity=latest_sensor_data['humidity'], fan_status=fan_status)

@app.route('/get_sensor_data')
def get_sensor_data():
    temperature, humidity = DHT11.read_sensor_data()
    latest_sensor_data['temperature'] = temperature
    latest_sensor_data['humidity'] = humidity
    return jsonify(temperature=temperature, humidity=humidity, fan_status=fan_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)