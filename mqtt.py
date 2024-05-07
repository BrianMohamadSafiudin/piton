import json
import os
import paho.mqtt.client as mqtt

# Konfigurasi broker MQTT
broker_address = "34.128.88.34"
port = 1883
topics = ["esp/mpu6050/acceleration", "esp/mpu6050/gyroscope", "esp/mpu6050/temperature"]

# Fungsi untuk memuat data dari file JSON
def load_data():
    if os.path.exists('sensor_data.json'):
        with open('sensor_data.json', 'r') as json_file:
            return json.load(json_file)
    else:
        return {"gyro": None, "acceleration": None, "temperature": None}

# Data sensor global
sensor_data = load_data()

# Fungsi callback yang dipanggil ketika klien menerima pesan CONNACK dari server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in topics:
        client.subscribe(topic)

# Fungsi callback yang dipanggil ketika pesan diterima dari server
def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    data_str = msg.payload.decode('utf-8')
    data_values = [float(i) for i in data_str.split(',')]

    # Update data tergantung pada topik
    if msg.topic == "esp/mpu6050/acceleration":
        sensor_data['acceleration'] = {"x": data_values[0], "y": data_values[1], "z": data_values[2]}
    elif msg.topic == "esp/mpu6050/gyroscope":
        sensor_data['gyro'] = {"x": data_values[0], "y": data_values[1], "z": data_values[2]}
    elif msg.topic == "esp/mpu6050/temperature":
        sensor_data['temperature'] = data_values[0]

    # Simpan data yang diperbarui ke file JSON
    with open('sensor_data.json', 'w') as json_file:
        json.dump(sensor_data, json_file, indent=4)

# Membuat objek klien MQTT
client = mqtt.Client()

# Menetapkan fungsi callback
client.on_connect = on_connect
client.on_message = on_message

# Menghubungkan ke broker
client.connect(broker_address, port=port)

# Loop selamanya
client.loop_forever()
