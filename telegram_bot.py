import telebot
from telebot import types
from test_response import *

bot = telebot.TeleBot('6985148923:AAHwmhG0KogYrTRho9A6gWCtHTT30AsXGag')


def send_routes(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='/sendmsg', callback_data='/sendmsg')
    keyboard.add(key_1)
    key_2 = types.InlineKeyboardButton(text='/healthcheck', callback_data='/healthcheck')
    keyboard.add(key_2)
    key_3 = types.InlineKeyboardButton(text='/training_model', callback_data='/training_model')
    keyboard.add(key_3)
    bot.send_message(chat_id, 'Роуты', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def services(message):
    send_routes(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == '/sendmsg':
        bot.send_message(call.message.chat.id, sendmsg())
    elif call.data == '/healthcheck':
        bot.send_message(call.message.chat.id, healthcheck())
    elif call.data == '/training_model':
        bot.send_message(call.message.chat.id, training_model())

    send_routes(call.message.chat.id)


bot.polling(none_stop=True, interval=0)
