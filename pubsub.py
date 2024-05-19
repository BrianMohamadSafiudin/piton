import json
import os
import paho.mqtt.client as mqtt
from datetime import datetime

# Konfigurasi broker MQTT
broker_address = "34.101.62.111"
port = 1883
topics = ["esp/mpu6050/acceleration", "esp/mpu6050/gyroscope", "esp/mpu6050/temperature"]

# Membuat atau membuka file data
if not os.path.exists('sensor_data.json'):
    with open('sensor_data.json', 'w') as file:
        json.dump([], file)  # Inisialisasi file sebagai array JSON

# Fungsi untuk memuat data dari file JSON
def load_data():
    with open('sensor_data.json', 'r') as json_file:
        return json.load(json_file)

# Buffer data sensor dan counter
sensor_data_buffer = []
data_count = 0

# Fungsi callback yang dipanggil ketika klien menerima pesan CONNACK dari server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in topics:
        client.subscribe(topic)

# Fungsi callback yang dipanggil ketika pesan diterima dari server
def on_message(client, userdata, msg):
    global data_count
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    data_str = msg.payload.decode('utf-8')
    data_parts = data_str.split(',')
    device_id = data_parts[0]
    
    try:
        data_values = [float(i) for i in data_parts[1:]]  # Convert the rest of the parts to float
    except ValueError as e:
        print(f"Error converting data to float. Data received: {data_parts[1:]}")
        return  # Early exit if data conversion fails
    
    timestamp = datetime.now().isoformat()
    sensor_type = msg.topic.split('/')[-1]

    # Create dictionary based on sensor type
    data_entry = {
        "timestamp": timestamp,
        "device_id": device_id
    }
    
    # Add sensor-specific data
    if sensor_type == "acceleration" or sensor_type == "gyroscope":
        if len(data_values) == 3:
            data_entry[sensor_type] = {"x": data_values[0], "y": data_values[1], "z": data_values[2]}
        else:
            print(f"Insufficient data for {sensor_type}. Expected 3 values, got {len(data_values)}")
            return
    elif sensor_type == "temperature":
        if len(data_values) == 1:
            data_entry[sensor_type] = data_values[0]
        else:
            print(f"Unexpected data count for temperature. Expected 1 value, got {len(data_values)}")
            return
    
    sensor_data_buffer.append(data_entry)
    data_count += 1

    # Save to JSON file every 100 messages
    if data_count >= 100:
        existing_data = load_data()
        updated_data = existing_data + sensor_data_buffer
        with open('sensordata.json', 'w') as json_file:
            json.dump(updated_data, json_file, indent=4)
        sensor_data_buffer.clear()
        data_count = 0

# Membuat objek klien MQTT
client = mqtt.Client()

# Menetapkan fungsi callback
client.on_connect = on_connect
client.on_message = on_message

# Menghubungkan ke broker
client.connect(broker_address, port=port)

# Loop selamanya
client.loop_forever()
