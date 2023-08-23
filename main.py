from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import mysql.connector

# Ganti dengan token bot Anda
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Ganti dengan informasi koneksi MySQL Anda
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_NAME = 'your_database_name'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Halo! Saya adalah bot pencari data. Gunakan perintah /searchname, /searchid, atau /searchphone untuk mencari berdasarkan nama, ID, atau nomor telepon.')

def search_name(update: Update, context: CallbackContext) -> None:
    query = " ".join(context.args)
    search_data("name", query, update)

def search_id(update: Update, context: CallbackContext) -> None:
    query = context.args[0] if context.args else None
    search_data("id", query, update)

def search_phone(update: Update, context: CallbackContext) -> None:
    query = context.args[0] if context.args else None
    search_data("phone", query, update)

def search_data(search_type, query, update):
    if search_type == "name":
        condition = "name LIKE %s"
        search_term = f"%{query}%"
    elif search_type == "id":
        condition = "id = %s"
        search_term = query
    elif search_type == "phone":
        condition = "phone LIKE %s"
        search_term = f"%{query}%"
    else:
        return

    conn = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    query = f'SELECT * FROM data WHERE {condition}'
    cursor.execute(query, (search_term,))
    results = cursor.fetchall()
    
    conn.close()
    
    if results:
        response = f"Hasil pencarian {search_type}:\n"
        for result in results:
            response += str(result) + "\n"
    else:
        response = f"Maaf, {search_type} tidak ditemukan dalam database."
    
    update.message.reply_text(response)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("searchname", search_name))
    dispatcher.add_handler(CommandHandler("searchid", search_id))
    dispatcher.add_handler(CommandHandler("searchphone", search_phone))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
