import json
import os
import paho.mqtt.client as mqtt
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

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

# Firebase configuration
cred = credentials.Certificate('falldetectionk4-07f9faa580c1.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://falldetectionk4-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Reference to the Firebase Realtime Database
db_ref = db.reference('sensor_data')

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    try:
        data_str = msg.payload.decode('utf-8')
        data_parts = data_str.split(',')

        # Validate that the data_parts have exactly 8 elements
        if len(data_parts) == 8:
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

            # Append the new sensor entry
            sensordata.append(sensor_entry)

            # Maintain only the last 30 entries
            if len(sensordata) > 30:
                sensordata.pop(0)

            # Overwrite the JSON file with the updated sensor data
            with open('sensordata.json', 'w') as json_file:
                json.dump(sensordata, json_file, indent=4)

            # Push sensor data to Firebase Realtime Database
            db_ref.push(sensor_entry)

        else:
            print("Invalid data format received: ", data_parts)
    except Exception as e:
        print("Error processing message: ", e)

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=port)
client.loop_forever()
