import telebot
from telebot import types
from test_response import *
from get_stat import get_response_stat

bot = telebot.TeleBot('6985148923:AAHwmhG0KogYrTRho9A6gWCtHTT30AsXGag')

user_inputs = {}


def send_routes(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='/sendmsg', callback_data='/sendmsg')
    keyboard.add(key_1)
    key_2 = types.InlineKeyboardButton(text='/healthcheck', callback_data='/healthcheck')
    keyboard.add(key_2)
    key_3 = types.InlineKeyboardButton(text='/training_model', callback_data='/training_model')
    keyboard.add(key_3)
    key_4 = types.InlineKeyboardButton(text='/get_stat', callback_data='/get_stat')
    keyboard.add(key_4)
    bot.send_message(chat_id, 'Роуты', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def services(message):
    send_routes(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == '/sendmsg':
        bot.send_message(call.message.chat.id, sendmsg())
        send_routes(call.message.chat.id)

    elif call.data == '/healthcheck':
        bot.send_message(call.message.chat.id, healthcheck())
        send_routes(call.message.chat.id)

    elif call.data == '/training_model':
        bot.send_message(call.message.chat.id, training_model())
        send_routes(call.message.chat.id)

    elif call.data == '/get_stat':
        bot.send_message(call.message.chat.id, 'Введи hash_id')
        bot.register_next_step_handler(call.message, process_hash_input)


def process_hash_input(message):
    hash_id = message.text
    result = get_response_stat(hash_id)
    bot.send_message(message.chat.id, result)

    send_routes(message.chat.id)


bot.polling(none_stop=True, interval=0)
