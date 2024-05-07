import json
import os
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuration for MQTT
broker_address = "34.128.88.34"
port = 1883
topics = ["esp/mpu6050/acceleration", "esp/mpu6050/gyroscope", "esp/mpu6050/temperature"]

# Initialize or open data file
if not os.path.exists('sensordata.json'):
    with open('sensordata.json', 'w') as file:
        json.dump([], file)  # Initialize file as JSON array

# Function to load data from JSON file
def load_data():
    with open('sensordata.json', 'r') as json_file:
        return json.load(json_file)

# Buffer for sensor data and counter
sensordata_buffer = {}
data_count = 0

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in topics:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    global data_count
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    data_str = msg.payload.decode('utf-8')
    data_parts = data_str.split(',')
    device_id = data_parts[0]
    data_values = [float(i) for i in data_parts[1:]]
    timestamp = datetime.now().isoformat()
    sensor_type = msg.topic.split('/')[-1]

    # Initialize or update the entry
    key = (device_id, timestamp)
    if key not in sensordata_buffer:
        sensordata_buffer[key] = {"timestamp": timestamp, "device_id": device_id}
    
    if sensor_type == "acceleration" or sensor_type == "gyroscope":
        sensordata_buffer[key][sensor_type] = {"x": data_values[0], "y": data_values[1], "z": data_values[2]}
    elif sensor_type == "temperature":
        sensordata_buffer[key][sensor_type] = data_values[0]

    # Check if entry is complete
    if all(k in sensordata_buffer[key] for k in ["acceleration", "gyroscope", "temperature"]):
        data_count += 1
        if data_count >= 100:  # Adjust this as necessary
            existing_data = load_data()
            updated_data = existing_data + list(sensordata_buffer.values())
            with open('sensordata.json', 'w') as json_file:
                json.dump(updated_data, json_file, indent=4)
            sensordata_buffer.clear()
            data_count = 0

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=port)
client.loop_forever()
