import json
from typing import Final
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Application, filters, ContextTypes

TOKEN: Final = "6652548059:AAHMjQxSifta_RDNP99XZe3TxOHOFh0gGwA"
BOT_USERNAME: Final = "@FallDetectionMonitorBot"

# Membuat variabel untuk menyimpan daftar pengguna yang berlangganan
subscribers = set()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Halo! Saya bot dari alat deteksi jatuh!')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Status pengguna saat ini')
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
        print("Anda Belum Subscribe!!!")

async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Menambahkan pengguna ke daftar pelanggan...")
    subscribers.add(update.message.chat.id)
    await update.message.reply_text('Anda telah berhasil berlangganan untuk mendapatkan notifikasi jatuh.')
    print("Daftar Pelanggan yang Berlangganan:")
    for subscriber_id in subscribers:
        print(subscriber_id)
    # Data yang akan disimpan
    data = list(subscribers)
    # Simpan data ke dalam file JSON
    with open('subscribers.json', 'w') as file:
        json.dump(data, file)

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Menghapus pengguna dari daftar pelanggan
    subscribers.discard(update.message.chat.id)
    await update.message.reply_text('Anda telah berhasil berhenti berlangganan untuk mendapatkan notifikasi jatuh.')
    print("Daftar Pelanggan yang Berlangganan:")
    for subscriber_id in subscribers:
        print(subscriber_id)
    # Data yang akan disimpan
    data = list(subscribers)
    # Simpan data ke dalam file JSON
    with open('subscribers.json', 'w') as file:
        json.dump(data, file)

def handle_response(text: str) -> str:
    text = text.lower()

    if "hi" in text:
        return "Hey there!"

    elif "how are you" in text:
        return "I am good."

    else:
        return "I do not understand what you wrote."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text = str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:   
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response)
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text = str = update.message.text
    chat_id = update.message.chat.id

    print(f'User ({chat_id}) in {message_type}: "{text}"')

    # Create a set to store chat IDs of users who have already been replied to
    replied_users = set()

    if chat_id not in replied_users:
        # If the user has not been replied to yet, handle the message
        response = handle_response(text)

        # Add the chat ID to the set to prevent future replies
        replied_users.add(chat_id)

        # Send the response to the user
        await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Tambahkan handler command
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("subscribe", subscribe_command))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    
    # Message handler untuk semua pesan teks
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
  
    # Handler untuk error
    app.add_error_handler(error)
    
    # Mulai polling
    print('Polling...')
    app.run_polling(poll_interval=5)
