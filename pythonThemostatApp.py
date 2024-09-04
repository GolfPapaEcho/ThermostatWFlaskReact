RPi Thermostat

sudo pip3 install flask flask-cors w1thermsensor RPi.GPIO psutil
ON Pi


app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
import psutil

# Setup GPIO
GPIO.setmode(GPIO.BCM)
HEATER_PIN = 17
GPIO.setup(HEATER_PIN, GPIO.OUT)

# Initialize the DS18B20 sensor
sensor = W1ThermSensor()

app = Flask(__name__)
CORS(app)

# Global variable to hold the setpoint temperature
setpoint_temp = 25.0  # Default setpoint

def read_temp():
    try:
        return sensor.get_temperature()
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

def is_solenoid_running():
    for proc in psutil.process_iter(['name', 'cmdline']):
        if 'Solenoid.py' in proc.info['cmdline']:
            return True
    return False

def control_heater():
    current_temp = read_temp()
    if current_temp is not None:
        if current_temp <= setpoint_temp:
            GPIO.output(HEATER_PIN, GPIO.HIGH)
        else:
            GPIO.output(HEATER_PIN, GPIO.LOW)
    return current_temp

@app.route('/api/temperature', methods=['GET'])
def get_temperature():
    current_temp = control_heater()
    return jsonify({'current_temperature': current_temp, 'setpoint': setpoint_temp})

@app.route('/api/setpoint', methods=['POST'])
def set_setpoint():
    global setpoint_temp
    data = request.json
    if 'setpoint' in data:
        setpoint_temp = float(data['setpoint'])
        return jsonify({'message': 'Setpoint updated', 'setpoint': setpoint_temp})
    else:
        return jsonify({'error': 'Setpoint not provided'}), 400

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Program interrupted. Checking for running Solenoid.py.")
    finally:
        if not is_solenoid_running():
            GPIO.cleanup()
            print("GPIO cleaned up.")
        else:
            print("Solenoid.py is running. Skipping GPIO cleanup.")

