import random

import mysql
import telebot
from telebot import types
import time
import mysql.connector as sql

conn = sql.connect(host="localhost", user="root", password="mySQL2341m", database="mydb",
                   auth_plugin='caching_sha2_password')

cursor = conn.cursor()

cardslist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
             '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
             '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
             '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
             '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
             '51', '52', '53', '54']
globalid = 0
gameid = ''
status = ''
admin = ''
players = []
playerstext = ''
queueu = ''
playerq = ''
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
        if message.text == 'Предмет 1':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("❌ Отменить")
            markup.add(btn1)
            deletem.append(bot.send_message(message.from_user.id, f"Напишите дз", reply_markup=markup))
            work = '1'
            bot.register_next_step_handler(message, adddz, work)

        elif message.text == 'Предмет 2':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("❌ Отменить")
            markup.add(btn1)
            deletem.append(bot.send_message(message.from_user.id, f"Напишите дз", reply_markup=markup))
            work = '2'
            bot.register_next_step_handler(message, adddz, work)

        elif message.text == 'Предмет 3':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("❌ Отменить")
            markup.add(btn1)
            deletem.append(bot.send_message(message.from_user.id, f"Напишите дз", reply_markup=markup))
            work = '3'
            bot.register_next_step_handler(message, adddz, work)

        elif message.text != 'Предмет 3':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Предмет 1")
            btn2 = types.KeyboardButton("Предмет 2")
            btn3 = types.KeyboardButton("Предмет 3")
            markup.add(btn1, btn2, btn3)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))

            conn.commit()

    elif status == '3':
        if message.text == 'АНГЛ ЯЗ':
            switch(message, '1 ГРУППА', '2 ГРУППА')

        elif message.text == 'Предмет 2':
            watch(message, '2')

        elif message.text == 'Предмет 3':
            watch(message, '3')

        elif message.text != 'Предмет 3':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Предмет 1")
            btn2 = types.KeyboardButton("Предмет 2")
            btn3 = types.KeyboardButton("Предмет 3")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup)

            conn.commit()

    elif status == '1':

        if message.text == "✏ Добавить дз":

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Предмет 1")
            btn2 = types.KeyboardButton("Предмет 2")
            btn3 = types.KeyboardButton("Предмет 3")
            markup.add(btn1, btn2, btn3)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))

            cursor.execute(f"""UPDATE `mydb`.`status` SET `status` = '2' WHERE (`id` = {message.from_user.id})""")
            conn.commit()

        elif message.text == '🔴 Посмотреть дз':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Предмет 1")
            btn2 = types.KeyboardButton("Предмет 2")
            btn3 = types.KeyboardButton("Предмет 3")
            markup.add(btn1, btn2, btn3)
            deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))

            cursor.execute(f"""UPDATE `mydb`.`status` SET `status` = '3' WHERE (`id` = {message.from_user.id})""")
            conn.commit()

        elif message.text == '/start':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("✏ Добавить дз")
            btn2 = types.KeyboardButton('🔴 Посмотреть дз')
            btn3 = types.KeyboardButton('❔ как работает бот?')
            markup.add(btn1, btn2, btn3)
            deletem.append(bot.send_message(message.from_user.id, f"Выберите опцию", reply_markup=markup))
        elif message.text == '❔ как работает бот?':
            bot.send_message(message.from_user.id, f"Бот работает очень просто. Если вы хотите добавить домашнее "
                                                   f"задание, то нажмите '✏ Добавить дз'. Далее выберите предмет "
                                                   f"по которому вы хотите написать дз. Далее вы должны написать дз "
                                                   f"(оно не должно иметь кавычки или быть слишком длинным) или "
                                                   f"отменить.")

            bot.send_message(message.from_user.id, f"Для просмотра уже записанного дз нужно нажать кнопку"
                                                   f"'🔴 Посмотреть дз' и выбрать нужный предмет. Выведутся три "
                                                   f"последнее записанное дз.")

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("✏ Добавить дз")
            btn2 = types.KeyboardButton('🔴 Посмотреть дз')
            btn3 = types.KeyboardButton('❔ как работает бот?')
            markup.add(btn1, btn2, btn3)
            deletem.append(bot.send_message(message.from_user.id, f"Выберите опцию", reply_markup=markup))
        else:

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("✏ Добавить дз")
            btn2 = types.KeyboardButton('🔴 Посмотреть дз')
            btn3 = types.KeyboardButton('❔ как работает бот?')
            markup.add(btn1, btn2, btn3)
            deletem.append(bot.send_message(message.from_user.id, f"Выберите опцию", reply_markup=markup))

def switch(message, one, two, ,):
    pass


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
                print(str(row)[2:len(row) - 4])
                print(row)
                cursor.execute(f"""DELETE From `mydb`.`student` WHERE (`homework` = '{str(row)[2:len(row) - 4]}');""")
                break

        cursor.execute(f"""UPDATE `mydb`.`status` SET `status` = '1' WHERE (`id` = {message.from_user.id})""")
        conn.commit()

def watch(message, work):
    cursor.execute(f"""SELECT homework From `mydb`.`student` WHERE (`predmet` = '{work}');""")

    i = 0

    rows = cursor.fetchall()
    for row in rows:
        print(str(row)[2:len(row) - 4])
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
    btn3 = types.KeyboardButton('❔ как работает бот?')
    markup.add(btn1, btn2, btn3)
    deletem.append(bot.send_message(message.from_user.id, f"Выберите опцию", reply_markup=markup))

    conn.commit()

conn.commit()
bot.polling(none_stop=True, interval=0)
