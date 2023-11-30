import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT

DHTPin = 11  # Define the pin of DHT11

def read_sensor_data():
    dht = DHT.DHT(DHTPin)  # Create a DHT class object
    counts = 0  # Measurement counts
    while True:
        counts += 1
        for i in range(0, 15):
            chk = dht.readDHT11()  # Read DHT11 and get a return value
            if chk == dht.DHTLIB_OK:
                break
            time.sleep(0.1)
        temperature = dht.temperature
        humidity = dht.humidity
        return temperature, humidity

if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
