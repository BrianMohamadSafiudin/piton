import os
import json
import numpy as np
from tensorflow.keras.models import load_model
import time

# Fungsi untuk memproses JSON menjadi array fitur
def process_json(data_json):
    data = json.loads(data_json)
    gyro_x = [float(item["gyroscopex"]) for item in data]
    gyro_y = [float(item["gyroscopey"]) for item in data]
    gyro_z = [float(item["gyroscopez"]) for item in data]
    # accel_x = [float(item["acceleration.x"]) for item in data]
    # accel_y = [float(item["acceleration.y"]) for item in data]
    # accel_z = [float(item["acceleration.z"]) for item in data]
    
    # Gabungkan data gyroscope dan accelerometer menjadi satu array
    combined_data = np.array([gyro_x, gyro_y, gyro_z]).T
    return combined_data

# Muat model AI yang telah dilatih menggunakan Keras tanpa optimizer
model_path = 'allnewfall-detection-model.h5'
model = load_model(model_path, compile=False)

# Label kelas sesuai dengan model
class_labels = [
    "Stand for 30 seconds (D01/01)",
    "Walk normally and turn for 4m (D06/06)",
    "Forward fall when trying to sit down (F01/20)",
    "Backward fall when trying to sit down (F02/21)",
    "Lateral fall when trying to sit down (F03/22)"
]

# class_labels = [
#     "Stand for 30 seconds (D01/01)",
#     "Stand, slowly bend the back with or without bending at knees, tie shoe lace, and get up (D02/02)",
#     "Pick up an object from the floor (D03/03)",
#     "Gently jump (try to reach an object) (D04/04)",
#     "Stand, sit to the ground, wait a moment, and get up with normal speed (D05/05)",
#     "Walk normally with turn (4m) (D06/06)",
#     "Walk quickly with turn (4m) (D07/07)",
#     "Jog normally with turn (4m) (D08/08)",
#     "Jog quickly with turn (4m) (D09/09)",
#     "Stumble while walking (D10/10)",
#     "Sit on a chair for 30 seconds (D11/11)",
#     "Sit on the sofa (back is inclined to the support) for 30 seconds (D12/12)",
#     "Sit down to a chair normally, and get up from a chair normally (D13/13)",
#     "Sit down to a chair quickly, and get up from a chair quickly (D14/14)",
#     "Sit a moment, trying to get up, and collapse into a chair (D15/15)",
#     "Stand, sit on the sofa (back is inclined to the support), and get up normally (D16/16)",
#     "Lie on the bed for 30 seconds (D17/17)",
#     "Sit a moment, lie down to the bed normally, and get up normally (D18/18)",
#     "Sit a moment, lie down to the bed quickly, and get up quickly (D19/19)",
#     "Walk upstairs and downstairs normally (5 steps) (D20/35)",
#     "Walk upstairs and downstairs quickly (5 steps) (D21/36)",
#     "Forward fall when trying to sit down (F01/20)",
#     "Backward fall when trying to sit down (F02/21)",
#     "Lateral fall when trying to sit down (F03/22)",
#     "Forward fall when trying to get up (F04/23)",
#     "Lateral fall when trying to get up (F05/24)",
#     "Forward fall while sitting, caused by fainting (F06/25)",
#     "Lateral fall while sitting, caused by fainting (F07/26)",
#     "Backward fall while sitting, caused by fainting (F08/27)",
#     "Vertical (forward) fall while walking caused by fainting (F09/28)",
#     "Fall while walking, use of hands to dampen fall, caused by fainting (F10/29)",
#     "Forward fall while walking caused by a trip (F11/30)",
#     "Forward fall while jogging caused by a trip (F12/31)",
#     "Forward fall while walking caused by a slip (F13/32)",
#     "Lateral fall while walking caused by a slip (F14/33)",
#     "Backward fall while walking caused by a slip (F15/34)"
# ]

def predict_and_save():
    # Muat data JSON dari file
    with open('sensordata.json', 'r') as f:
        data_json = f.read()

    # Proses JSON untuk mendapatkan data gyroscope dan accelerometer
    sensor_data = process_json(data_json)

    # Pastikan hanya melakukan prediksi jika ada tepat 600 objek
    n_timesteps = 25
    n_features = 3  # gyroscope x, y, z dan acceleration x, y, z

    if sensor_data.shape[0] < n_timesteps:
        print(f'Data tidak cukup: hanya {sensor_data.shape[0]} objek, menunggu sampai ada 25 objek.')
        return
    elif sensor_data.shape[0] > n_timesteps:
        # Trim data jika lebih dari 25 titik
        sensor_data = sensor_data[:n_timesteps, :]

    # Pertukarkan sumbu untuk menyesuaikan dengan bentuk input model (6, 25)
    sensor_data = np.swapaxes(sensor_data, 0, 1)

    # Ubah bentuk input sesuai dengan yang diharapkan oleh model
    sensor_data_reshaped = sensor_data.reshape(1, n_features, n_timesteps, 1)

    prediction = model.predict(sensor_data_reshaped)

    # Tentukan kelas dengan probabilitas tertinggi
    predicted_class = np.argmax(prediction)
    status = class_labels[predicted_class]

    # Simpan hasil prediksi ke file hasilprediksi.json
    with open('hasilprediksi.json', 'w') as outfile:
        json.dump({'prediction': status}, outfile)

    print(f'Hasil Prediksi: {status}')
    print(prediction)
    print(prediction.shape)
    
# Jalankan kode setiap 1 detik
while True:
    predict_and_save()
    time.sleep(2.5)
