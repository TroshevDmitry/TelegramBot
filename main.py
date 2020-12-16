import telebot
from telebot import types
from telegram.ext import CommandHandler

import requests

url = 'asd'
CHECK = 0
SEARCH = 0
NAME = ''

bot = telebot.TeleBot("1417060824:AAFcN5o04OVuT2RkVEpMPgSR-l9Y2fJwKUQ")

@bot.message_handler(content_types=["text"])
def any_msg(message):
    global CHECK, SEARCH, NAME
    # Создаем клавиатуру и каждую из кнопок (по 2 в ряд)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    url_button = types.InlineKeyboardButton(text="URL api", url="https://pokeapi.co/")
    callback_button = types.InlineKeyboardButton(text="Посмотреть на пикачу", callback_data="photo")
    callback_button1 = types.InlineKeyboardButton(text="Почитать про абилки пикачу", callback_data="ability")
    callback_button2 = types.InlineKeyboardButton(text="Найти покемона", callback_data="search")
    keyboard.add(url_button, callback_button, callback_button1, callback_button2)
    if (message.text[-1]=='!'):
        bot.send_message(chat_id=message.chat.id, text="Погнали!😎😎😎", reply_markup=keyboard)
    else:
        if (SEARCH):
            SEARCH = 0
            wtf = 0
            #вывод картинки
            print('searching...')
            NAME = message.text
            print(NAME)
            try:
                url = 'https://pokeapi.co/api/v2/pokemon/' + NAME.lower()
                contests = requests.get(url).json()
                id = contests['id']
                wtf += 1
            except Exception as e:
                print('ошибка в url \n' + str(e))
                bot.send_message(chat_id=message.chat.id, text="Похоже,такого покемона нет... "
                                                           "Попробуй еще раз👻👻👻", reply_markup=keyboard)
            print('id' + str(id))
            url1 = 'https://pokeres.bastionbot.org/images/pokemon/' + str(id) + '.png'
            info = url1
            print('info:'+info)
            bot.send_message(chat_id=message.chat.id, text="Так вот же он ⚡️⚡️⚡️")
            bot.send_photo(chat_id=message.chat.id, photo=info)


            #вывод абилок
            url2 = 'https://pokeapi.co/api/v2/pokemon/' + str(id)
            contests = requests.get(url2).json()
            abilities = contests['abilities']
            info = ''
            counter = 1
            try:
                for ability in abilities:
                    info += 'способность  № ' + str(counter) + '  ' + ability['ability']['name'] + '\n'
                    counter += 1
            except Exception as e:
                print(e)
            print(info)
            bot.send_message(chat_id=message.chat.id, text="Держи абилки👀")
            bot.send_message(chat_id=message.chat.id, text=info, reply_markup=keyboard)


        else:
            if (CHECK == 0):
                bot.send_message(message.chat.id, "Привет, {} ! "
                                              "О каком покемоне ты хочешь узнать сегодня?"
                                              "\n⬇️⬇️⬇️    Тыкай на кнопочки⬇️⬇️⬇️   ".format(message.chat.first_name),
                      reply_markup=keyboard)
                CHECK += 1
            elif (CHECK != 0):
                bot.send_message(message.chat.id,
                         "Слушай, {} , попробуй лучше нажимать на эти кнопки, текст я не воспринимаю".format(message.chat.first_name))
                bot.send_message(message.chat.id, '⬇️⬇️⬇️   Вот эти   ⬇️⬇️⬇️  ', reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global SEARCH
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "photo":
            #Вывод фото пикачу
            # Уведомление в верхней части экрана
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Нашел фото!")
            print('get_image_url1')
            url = 'https://pokeres.bastionbot.org/images/pokemon/25.png'
            print(url)
            bot.send_message(chat_id=call.message.chat.id, text="Вот он ⭐️⭐️⭐️")
            bot.send_photo(chat_id=call.message.chat.id, photo=url)
            bot.send_message(chat_id=call.message.chat.id, text="Хочешь я тебе еще что-нибудь покажу?\n"
                                                                "Напиши < еще! >, но "
                                                                "не забудь поставить < ! >\n"
                                                                "покажи мне энергию ⚡️⚡️⚡️")
        elif call.data == 'ability':
            #Вывод абилок пикачу
            #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ну держи ⚡️⚡️⚡️")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Нашел абилки!")
            contests = requests.get('https://pokeapi.co/api/v2/pokemon/pikachu').json()
            abilities = contests['abilities']
            info = ''
            counter = 1
            try:
                for ability in abilities:
                    info += 'способность  № ' + str(counter) + '  ' + ability['ability']['name'] + '\n'
                    counter += 1
            except Exception as e:
                print(e)
            print(info)
            bot.send_message(chat_id=call.message.chat.id, text="Ну держи👀")
            bot.send_message(chat_id=call.message.chat.id, text=info)
            bot.send_message(chat_id=call.message.chat.id, text="Хочешь я тебе еще что-нибудь покажу?\n"
                                                                "Напиши < еще! >, но "
                                                                "не забудь поставить < ! >\n"
                                                                "покажи мне энергию ⚡️⚡️⚡️")
        elif call.data == 'search':
            if (SEARCH==0):
                bot.send_message(chat_id=call.message.chat.id, text="напиши имя покемона на АНГЛИЙСКОМ языке\n"
                                                                "тогда я покажу тебе магию  💫💫💫 ")
            SEARCH =+ 1

if __name__ == '__main__':
    bot.infinity_polling()
