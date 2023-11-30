import RPi.GPIO as GPIO
from flask import Flask, render_template, redirect, url_for

GPIO.setwarnings(False)  # Disable warnings
GPIO.setmode(GPIO.BCM)

# GPIO pin connected to the LED
led_pin = 18
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)  # Initially turn off the LED

app = Flask(__name__)

@app.route('/')
def index():
    led_state = GPIO.input(led_pin)
    if led_state:
        return render_template('LEDon.html')
    else:
        return render_template('LEDoff.html')

@app.route('/toggle', methods=['POST'])
def toggle_led():
    led_state = GPIO.input(led_pin)
    GPIO.output(led_pin, not led_state)  # Toggle the LED state
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
