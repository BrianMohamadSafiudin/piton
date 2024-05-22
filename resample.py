import json
import time
from datetime import datetime, timedelta

# Fungsi untuk melakukan interpolasi data antara dua titik data
def interpolate_data(data1, data2, num_points):
    interpolated_data = []
    
    # Konversi timestamp ke objek datetime
    ts1 = datetime.fromisoformat(data1["timestamp"])
    ts2 = datetime.fromisoformat(data2["timestamp"])
    
    # Hitung langkah waktu (delta)
    delta = (ts2 - ts1) / (num_points + 1)
    
    # Interpolasi titik data
    for i in range(1, num_points + 1):
        timestamp = (ts1 + i * delta).isoformat()
        interpolated_point = {
            "timestamp": timestamp,
            "device_id": data1["device_id"],
            "acceleration.x": round(linear_interpolate(data1["acceleration.x"], data2["acceleration.x"], num_points + 1, i), 3),
            "acceleration.y": round(linear_interpolate(data1["acceleration.y"], data2["acceleration.y"], num_points + 1, i), 3),
            "acceleration.z": round(linear_interpolate(data1["acceleration.z"], data2["acceleration.z"], num_points + 1, i), 3),
            "gyroscope.x": round(linear_interpolate(data1["gyroscope.x"], data2["gyroscope.x"], num_points + 1, i), 7),
            "gyroscope.y": round(linear_interpolate(data1["gyroscope.y"], data2["gyroscope.y"], num_points + 1, i), 7),
            "gyroscope.z": round(linear_interpolate(data1["gyroscope.z"], data2["gyroscope.z"], num_points + 1, i), 7),
            "temperature": round(linear_interpolate(data1["temperature"], data2["temperature"], num_points + 1, i), 2),
        }
        interpolated_data.append(interpolated_point)
    
    return interpolated_data

# Fungsi interpolasi linear
def linear_interpolate(start, end, steps, current_step):
    return start + (end - start) * current_step / steps

# Fungsi untuk melakukan resampling dan menyimpan data
def perform_resampling():
    # Baca data dari sensordata.json
    with open('sensordata.json', 'r') as f:
        sensor_data = json.load(f)

    # Inisialisasi data hasil resampling
    resampled_data = []

    # Jumlah interpolasi antara dua titik data
    num_interpolations = 29

    # Lakukan interpolasi untuk setiap pasangan titik data berurutan
    for i in range(len(sensor_data) - 1):
        resampled_data.append(sensor_data[i])  # Tambahkan titik data asli

        # Interpolasi antara titik data saat ini dan titik data berikutnya
        interpolated = interpolate_data(sensor_data[i], sensor_data[i + 1], num_interpolations)
        resampled_data.extend(interpolated)

    resampled_data.append(sensor_data[-1])  # Tambahkan titik data terakhir

    # Simpan data hasil resampling ke resample_sensordata.json
    with open('resampled_sensordata.json', 'w') as f:
        json.dump(resampled_data, f, indent=4)

    print("Data telah diresample dan disimpan di resample_sensordata.json.")

# Jalankan fungsi perform_resampling()
while True:
    perform_resampling()
    time.sleep(0.1)
