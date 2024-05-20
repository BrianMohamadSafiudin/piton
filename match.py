import json
import numpy as np
from tensorflow.keras.models import load_model
import time

# Fungsi untuk memproses JSON menjadi array fitur
def process_json(data_json):
    data = json.loads(data_json)
    gyro_x = [float(item["gyroscope.x"]) for item in data]
    gyro_y = [float(item["gyroscope.y"]) for item in data]
    gyro_z = [float(item["gyroscope.z"]) for item in data]
    
    # Gabungkan data gyroscope menjadi satu array
    gyro_data = np.array([gyro_x, gyro_y, gyro_z]).T
    return gyro_data

# Muat model AI yang telah dilatih menggunakan Keras
model_path = 'fall-detection-model.h5'
model = load_model(model_path)

# Label kelas sesuai dengan model
class_labels = [
    "Stand for 30 seconds (D01/01)",
    "Walk normally and turn for 4m (D06/06)",
    "Forward fall when trying to sit down (F01/20)",
    "Backward fall when trying to sit down (F02/21)",
    "Lateral fall when trying to sit down (F03/22)"
]

def predict_and_save():
    # Muat data JSON dari file
    with open('resampled_sensordata.json', 'r') as f:
        data_json = f.read()

    # Proses JSON untuk mendapatkan data gyroscope
    gyro_data = process_json(data_json)

    # Pastikan data memiliki panjang yang sesuai dengan padding atau trimming
    n_timesteps = 600
    n_features = 3  # gyroscope x, y, z

    if gyro_data.shape[0] < n_timesteps:
        # Padding dengan nilai nol jika data kurang dari 600 titik
        padding = np.zeros((n_timesteps - gyro_data.shape[0], n_features))
        gyro_data = np.vstack((gyro_data, padding))
    elif gyro_data.shape[0] > n_timesteps:
        # Trim data jika lebih dari 600 titik
        gyro_data = gyro_data[:n_timesteps, :]

    # Buat prediksi menggunakan model
    gyro_data_reshaped = gyro_data.reshape(1, n_timesteps, n_features)
    prediction = model.predict(gyro_data_reshaped)

    # Tentukan kelas dengan probabilitas tertinggi
    predicted_class = np.argmax(prediction)
    status = class_labels[predicted_class]

    # Simpan hasil prediksi ke file hasilprediksi.json
    with open('hasilprediksi.json', 'w') as outfile:
        json.dump({'prediction': status}, outfile)

    print(f'Hasil Prediksi: {status}')

# Jalankan kode setiap 6 detik
while True:
    predict_and_save()
    time.sleep(6)
