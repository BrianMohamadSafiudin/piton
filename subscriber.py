import json
import asyncio
from typing import Final
from telegram.ext import Application

# Fungsi untuk membaca data pelanggan dari file JSON
def load_subscribers():
    with open('subscribers.json', 'r') as file:
        data = json.load(file)
    return data

# Fungsi untuk membaca hasil prediksi dari file JSON
def load_prediction():
    with open('hasilprediksi.json', 'r') as file:
        data = json.load(file)
    return data['prediction']

TOKEN: Final = "6652548059:AAHMjQxSifta_RDNP99XZe3TxOHOFh0gGwA"
BOT_USERNAME: Final = "@FallDetectionMonitorBot"

async def send_periodic_messages(app):
    while True:
        subscribers = load_subscribers()
        prediction = load_prediction()
        print("Mengecek daftar pelanggan yang berlangganan...")
        
        if subscribers:  # Hanya kirim pesan jika ada pelanggan yang berlangganan
            for subscriber_id in subscribers:
                print(f"Mengirim pesan periodik ke {subscriber_id}")
                await app.bot.send_message(subscriber_id, f"Hasil prediksi terbaru: {prediction}")
        else:
            print("Tidak ada pelanggan yang berlangganan.")

        await asyncio.sleep(6)

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Mulai mengirim pesan periodik
    asyncio.run(send_periodic_messages(app))
    print('Menjalankan send_periodic_messages()')
