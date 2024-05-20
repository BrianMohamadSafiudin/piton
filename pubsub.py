import json
import os
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuration for MQTT
broker_address = "34.101.62.111"
port = 1883
topic = "esp/mpu6050/sensors"

# Initialize or open data file
if not os.path.exists('sensordata.json'):
    with open('sensordata.json', 'w') as file:
        json.dump([], file)

# Function to load data from JSON file
def load_data():
    if os.path.exists('sensordata.json'):
        with open('sensordata.json', 'r') as json_file:
            # Read the file contents
            data = json_file.read()
            # If the file is not empty, load the JSON
            if data:
                return json.loads(data)
            else:
                return []
    else:
        return []

# Buffer for sensor data
sensordata = load_data()

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    data_str = msg.payload.decode('utf-8')
    data_parts = data_str.split(',')
    device_id = data_parts[0]
    timestamp = datetime.now().isoformat()
    accel_values = [float(i) for i in data_parts[1:4]]
    gyro_values = [float(i) for i in data_parts[4:7]]
    temp_value = float(data_parts[7])

    sensor_entry = {
        "timestamp": timestamp,
        "device_id": device_id,
        "acceleration.x": accel_values[0],
        "acceleration.y": accel_values[1],
        "acceleration.z": accel_values[2],
        "gyroscope.x": gyro_values[0],
        "gyroscope.y": gyro_values[1],
        "gyroscope.z": gyro_values[2],
        "temperature": temp_value
    }

    sensordata.append(sensor_entry)

    # Overwrite the file every 30 objects
    if len(sensordata) >= 600:
        with open('sensordata.json', 'w') as json_file:
            json.dump(sensordata, json_file, indent=4)
        sensordata.clear()

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=port)
client.loop_forever()
