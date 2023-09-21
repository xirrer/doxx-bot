import logging
import csv
import telepot
from telepot.loop import MessageLoop

# Initialize the bot
bot = telepot.Bot("TOKEN")

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# States for the conversation
SEARCH, STOP = range(2)

# Function to search for matches in the database
def search_in_database(query):
    with open("database.csv", "r", encoding="utf-8") as database_file:
        reader = csv.reader(database_file)
        for row in reader:
            if query in row:
                id_tg, phone, firstname, lastname, username = row
                return f"Вот что удалось найти:\n├🏷️ id_tg: {id_tg}\n├📱 phone: {phone}\n├👤 firstname: {firstname}\n├🔰 lastname: {lastname}\n└♠️username: {username}"
    return "Ничего не найдено."

# Handler for the /start command
def on_start(msg):
    chat_id = msg['chat']['id']
    bot.sendMessage(chat_id, "i always watchin u.")
    bot.user_data[chat_id] = SEARCH

# Handler for text messages
def on_text(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        query = msg['text']
        result = search_in_database(query)
        bot.sendMessage(chat_id, result)
        bot.user_data[chat_id] = SEARCH

# Handler for the /stop command
def on_stop(msg):
    chat_id = msg['chat']['id']
    bot.sendMessage(chat_id, "Search canceled. Enter new text to search or use /start.")
    bot.user_data[chat_id] = None

# Initialize the message loop
MessageLoop(bot, {
    'chat': on_text,
    'callback_query': on_stop,
    'inline_query': on_start,
    }).run_as_thread()

# Keep the bot running
while True:
    pass
