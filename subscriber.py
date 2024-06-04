import json
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Final
from telegram.ext import Application

# Initialize Firebase Admin application
cred = credentials.Certificate('falldetectionk4-07f9faa580c1.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to read subscriber data from JSON file
def load_subscribers():
    with open('subscribers.json', 'r') as file:
        data = json.load(file)
    return data

# Function to read prediction data from JSON file
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
        print("Checking the list of subscribed customers...")

        if subscribers:  # Only send messages if there are subscribers
            for subscriber_id in subscribers:
                print(f"Sending periodic message to {subscriber_id}")
                await app.bot.send_message(subscriber_id, f"Latest prediction result: {prediction}")
                # Send prediction result to Firebase
                doc_ref = db.collection('predictions').document(str(subscriber_id))
                doc_ref.set({
                    'prediction': prediction
                })
        else:
            print("No subscribed customers.")

        await asyncio.sleep(6)

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Start sending periodic messages
    asyncio.run(send_periodic_messages(app))
    print('Running send_periodic_messages()')
