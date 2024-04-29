import json
from typing import Final
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Application, filters, ContextTypes
import openai

# Telegram Bot Token
TOKEN: Final = "6652548059:AAHMjQxSifta_RDNP99XZe3TxOHOFh0gGwA"
BOT_USERNAME: Final = "@FallDetectionMonitorBot"

# OpenAI API Key
OPENAI_API_KEY: Final = ""
# OPENAI_API_KEY: Final = "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"

# Initialize the OpenAI API client
openai.api_key = OPENAI_API_KEY

# Membuat variabel untuk menyimpan daftar pengguna yang berlangganan
subscribers = set()

# Function to generate response using GPT
def generate_response(text):
    prompt_text = "The following is a conversation with a friendly AI named ChatGPT. " \
                  "The AI is helpful, clever, and very friendly.\n\nUser: " + text + "\nAI:"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt_text,
        max_tokens=100
    )
    return response.choices[0].text.strip()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Halo! Saya bot dari alat deteksi jatuh!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ada yang bisa saya bantu?')

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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text = str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:   
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = generate_response(new_text)
        else:
            return
    else:
        response: str = generate_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Tambahkan handler command
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("subscribe", subscribe_command))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    
    # Message handler untuk semua pesan teks
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
  
    # Handler untuk error
    app.add_error_handler(error)
    
    # Mulai polling
    print('Polling...')
    app.run_polling(poll_interval=5)
