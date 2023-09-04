import random

import mysql
import telebot
from telebot import types
import time
import mysql.connector as sql

conn = sql.connect(host="localhost", user="root", password="mySQL2341m", database="mydb",
                   auth_plugin='caching_sha2_password')

cursor = conn.cursor()

lessonslist = [{'ГЕОГРАФ':'geogr'},{'БИОЛОГ':'biolog'},{'ФИЗИК':'phisic'},{'ХИМИЯ':'xim'},{'ТРУД':'trud'},
               {'ИСКУССТВ':'isk'}]



deletem = []

bot = telebot.TeleBot('1876503650:AAH_sMeqFTVZx5PkW6dktrLKKJtIsPYkNck')


@bot.message_handler(content_types=['text'])
def start(message):
    global status

    cursor.execute(f"""INSERT ignore `mydb`.`status`(`id`,`status`)VALUES({message.from_user.id}, {1})""")

    cursor.execute(f"""SELECT status From`mydb`.`status` WHERE (`id` = {message.from_user.id});""")

    rows1 = cursor.fetchall()
    for row1 in rows1:
        status = str(row1)[2:len(row1) - 4]

    if status == '2':
        if message.text == 'АНГЛ ЯЗ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("1 Группа")
            btn2 = types.KeyboardButton("2 Группа")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchadd, 'eng1', 'eng2', '1 Группа', '2 Группа')

        elif message.text == 'РУСС':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("ЛИТРА")
            btn2 = types.KeyboardButton("ЯЗЫК")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchadd, 'rusl', 'rusy', 'ЛИТРА', 'ЯЗЫК')

        elif message.text == 'БЕЛ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("ЛИТРА")
            btn2 = types.KeyboardButton("ЯЗЫК")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchadd, 'bell', 'bely', "ЛИТРА", 'ЯЗЫК')

        elif message.text == 'МАТЕМ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("АЛГЕБР")
            btn2 = types.KeyboardButton("ГЕОМЕТР")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchadd, 'algebr', 'geom', "АЛГЕБР", 'ГЕОМЕТР')

        elif message.text == 'ИНФОРМ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("1 ГРУППA")
            btn2 = types.KeyboardButton("2 ГРУППA")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchadd, '1g', '2g', "1 ГРУППA", '2 ГРУППA')

        elif message.text == 'ИСТОРИЯ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("ВСЕМИР")
            btn2 = types.KeyboardButton("БЕЛ")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchadd, 'vsem', 'bel', "ВСЕМИР", 'БЕЛ')

        elif message.text == 'ФИЗРА':
            bot.send_message(message.from_user.id, "Если ты серьёзно хочешь написать дз по физре, то ты реал сумашедший")

        elif message.text == 'ГЕОГРАФ' or message.text == 'БИОЛОГ' or message.text == 'ФИЗИК' or \
                message.text == 'ХИМИЯ' or message.text == 'ТРУД' or message.text == 'ИСКУССТВ':
            for i in lessonslist:
                if str(message.text) == str(i.keys())[12:len(i.keys()) - 4]:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = types.KeyboardButton("❌ Отменить")
                    markup.add(btn1)
                    deletem.append(bot.send_message(message.from_user.id, f"Напишите дз", reply_markup=markup))
                    bot.register_next_step_handler(message, adddz, i[str(message.text)])

        elif message.text != 'Предмет 3':
            lessons(message)
            conn.commit()

    elif status == '3':
        if message.text == 'АНГЛ ЯЗ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("1 Группа")
            btn2 = types.KeyboardButton("2 Группа")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchwatch, 'eng1', 'eng2', '1 Группа', '2 Группа')

        elif message.text == 'РУСС':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("ЛИТРА")
            btn2 = types.KeyboardButton("ЯЗЫК")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchwatch, 'rusl', 'rusy', 'ЛИТРА', 'ЯЗЫК')

        elif message.text == 'БЕЛ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("ЛИТРА")
            btn2 = types.KeyboardButton("ЯЗЫК")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchwatch, 'bell', 'bely', "ЛИТРА", 'ЯЗЫК')

        elif message.text == 'МАТЕМ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("АЛГЕБР")
            btn2 = types.KeyboardButton("ГЕОМЕТР")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchwatch, 'algebr', 'geom', "АЛГЕБР", 'ГЕОМЕТР')

        elif message.text == 'ИНФОРМ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("1 ГРУППA")
            btn2 = types.KeyboardButton("2 ГРУППA")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchwatch, '1g', '2g', "1 ГРУППA", '2 ГРУППA')

        elif message.text == 'ИСТОРИЯ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("ВСЕМИР")
            btn2 = types.KeyboardButton("БЕЛ")
            markup.add(btn1, btn2)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))
            bot.register_next_step_handler(message, switchwatch, 'vsem', 'bel', "ВСЕМИР", 'БЕЛ')

        elif message.text == 'ФИЗРА':
            bot.send_message(message.from_user.id, "Если ты серьёзно ищешь дз по физре, то ты реал сумашедший")

        elif message.text == 'ГЕОГРАФ' or message.text == 'БИОЛОГ' or message.text == 'ФИЗИК' or \
                message.text == 'ХИМИЯ' or message.text == 'ТРУД' or message.text == 'ИСКУССТВ':
            for i in lessonslist:
                if str(message.text) == str(i.keys())[12:len(i.keys()) - 4]:
                    watch(message, i[str(message.text)])

        elif message.text != 'Предмет 3':
            lessons(message)
            conn.commit()

    elif status == '1':

        if message.text == "✏ Добавить дз":

            lessons(message)

            cursor.execute(f"""UPDATE `mydb`.`status` SET `status` = '2' WHERE (`id` = {message.from_user.id})""")
            conn.commit()

        elif message.text == '🔴 Посмотреть дз':

            lessons(message)

            cursor.execute(f"""UPDATE `mydb`.`status` SET `status` = '3' WHERE (`id` = {message.from_user.id})""")
            conn.commit()

        elif message.text == '/start':
            basemenu(message)

        elif message.text == '❔ как работает бот?':
            bot.send_message(message.from_user.id, f"Бот работает очень просто. Если вы хотите добавить домашнее "
                                                   f"задание, то нажмите '✏ Добавить дз'. Далее выберите предмет "
                                                   f"по которому вы хотите написать дз. Далее вы должны написать дз "
                                                   f"(оно не должно иметь кавычки или быть слишком длинным) или "
                                                   f"отменить.")

            bot.send_message(message.from_user.id, f"Для просмотра уже записанного дз нужно нажать кнопку"
                                                   f"'🔴 Посмотреть дз' и выбрать нужный предмет. Выведутся три "
                                                   f"последнее записанное дз.")
            basemenu(message)
        else:
            basemenu(message)

def lessons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('АНГЛ ЯЗ')
    btn2 = types.KeyboardButton("РУСС")
    btn3 = types.KeyboardButton("БЕЛ")
    btn4 = types.KeyboardButton("ИНФОРМ")
    btn5 = types.KeyboardButton("ИСТОРИЯ")
    btn6 = types.KeyboardButton("МАТЕМ")
    btn7 = types.KeyboardButton("ИНФОРМ")
    btn8 = types.KeyboardButton("ГЕОГРАФ")
    btn9 = types.KeyboardButton("БИОЛОГ")
    btn10 = types.KeyboardButton("ФИЗИК")
    btn11 = types.KeyboardButton("ХИМИЯ")
    btn12 = types.KeyboardButton("ТРУД")
    btn13 = types.KeyboardButton("ИСКУСТВ")
    btn14 = types.KeyboardButton("ФИЗРА")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14)
    deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))

def basemenu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("✏ Добавить дз")
    btn2 = types.KeyboardButton('🔴 Посмотреть дз')
    btn3 = types.KeyboardButton('❔ как работает бот?')
    markup.add(btn1, btn2, btn3)
    deletem.append(bot.send_message(message.from_user.id, f"Выберите опцию", reply_markup=markup))
def switchwatch(message, code1, code2, keyword1, keyword2):
    if message.text == keyword1:
        watch(message, code1)
    if message.text == keyword2:
        watch(message, code2)

def switchadd(message, code1, code2, keyword1, keyword2):
    if message.text == keyword1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("❌ Отменить")
        markup.add(btn1)
        deletem.append(bot.send_message(message.from_user.id, f"Напишите дз", reply_markup=markup))
        bot.register_next_step_handler(message, adddz, code1)
    if message.text == keyword2:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("❌ Отменить")
        markup.add(btn1)
        deletem.append(bot.send_message(message.from_user.id, f"Напишите дз", reply_markup=markup))
        bot.register_next_step_handler(message, adddz, code2)


def adddz(message, work):
    if message.text == '❌ Отменить':

        deletem.append(bot.send_message(message.from_user.id, f"Действие было отменено"))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("✏ Добавить дз")
        btn2 = types.KeyboardButton('🔴 Посмотреть дз')
        btn3 = types.KeyboardButton('❔ как работает бот?')
        markup.add(btn1, btn2, btn3)
        deletem.append(bot.send_message(message.from_user.id, f"Выберите опцию", reply_markup=markup))

        cursor.execute(f"""UPDATE `mydb`.`status` SET `status` = '1' WHERE (`id` = {message.from_user.id})""")
        conn.commit()

    elif message.text != '❌ Отменить':
        cursor.execute(f"""INSERT ignore `mydb`.`student`(`people`,`predmet`,`homework`)VALUES('{str(message.from_user.first_name)}', '{work}', '{str(message.text)}')""")

        deletem.append(bot.send_message(message.from_user.id, f"Спасибо за помощь, {str(message.from_user.first_name)}"))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("✏ Добавить дз")
        btn2 = types.KeyboardButton('🔴 Посмотреть дз')
        btn3 = types.KeyboardButton('❔ как работает бот?')
        markup.add(btn1, btn2, btn3)
        deletem.append(bot.send_message(message.from_user.id, f"Выберите опцию", reply_markup=markup))

        i = 0
        cursor.execute(f"""SELECT homework From `mydb`.`student` WHERE (`predmet` = '{work}');""")
        rows = cursor.fetchall()
        for row in rows:
            i = i + 1
        if i >= 4:
            cursor.execute(f"""SELECT homework From `mydb`.`student` WHERE (`predmet` = '{work}');""")
            rows = cursor.fetchall()
            for row in rows:
                cursor.execute(f"""DELETE From `mydb`.`student` WHERE (`homework` = '{str(row)[2:len(row) - 4]}');""")
                break

        cursor.execute(f"""UPDATE `mydb`.`status` SET `status` = '1' WHERE (`id` = {message.from_user.id})""")
        conn.commit()

def watch(message, work):
    cursor.execute(f"""SELECT homework From `mydb`.`student` WHERE (`predmet` = '{work}');""")

    i = 0

    rows = cursor.fetchall()
    for row in rows:
        cursor.execute(f"""SELECT people From `mydb`.`student` WHERE (`homework` = '{str(row)[2:len(row) - 4]}');""")

        rows1 = cursor.fetchall()
        for row1 in rows1:
            i=1
            bot.send_message(message.from_user.id, f"--- Создано {str(row1)[2:len(row1) - 4]} ---\n"
                                                   f"{str(row)[2:len(row) - 4]}")
    if i == 0:
        bot.send_message(message.from_user.id, f"По данному предмету не было написанно дз")

    cursor.execute(f"""UPDATE `mydb`.`status` SET `status` = '1' WHERE (`id` = {message.from_user.id})""")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("✏ Добавить дз")
    btn2 = types.KeyboardButton('🔴 Посмотреть дз')
    btn3 = types.KeyboardButton('❔ Как работает бот?')
    markup.add(btn1, btn2, btn3)
    deletem.append(bot.send_message(message.from_user.id, f"Выберите опцию", reply_markup=markup))

    conn.commit()

conn.commit()
bot.polling(none_stop=True, interval=0)
