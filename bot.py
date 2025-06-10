import telebot
from telebot import types
import os
from flask import Flask, request

API_TOKEN = '7964885596:AAHfeyL1T6xpSKGZ1MT-tOLDQ79Fu4Qntlc'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

user_data = {}

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add("Узнать цену", "Узнать причину цены")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Что тебе нужно?", reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: message.text == "Узнать цену")
def ask_questionnaire(message):
    msg = bot.send_message(message.chat.id, "Заполни анкету:\n1. Имя и фамилия игрока\n2. Возраст\n3. Позиция\n4. Клуб\n5. Нынешняя статистика\n6. Прошлая статистика\n7. Номинации\n8. Место на ЗМ\n9. Трофеи")
    bot.register_next_step_handler(msg, process_questionnaire)

def process_questionnaire(message):
    user_data[message.chat.id] = {'price': message.text}
    bot.send_message(message.chat.id, "Анкета сохранена!")

@bot.message_handler(func=lambda message: message.text == "Узнать причину цены")
def ask_reason(message):
    msg = bot.send_message(message.chat.id, "Заполни:\n1. Имя и фамилия игрока\n2. Цена\n3. Причина")
    bot.register_next_step_handler(msg, process_reason)

def process_reason(message):
    user_data[message.chat.id] = {'reason': message.text}
    bot.send_message(message.chat.id, "Спасибо! Причина записана.")

@app.route(f'/{API_TOKEN}', methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook():
    return "Bot is working!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url='https://YOUR-RAILWAY-APP.up.railway.app/' + API_TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
