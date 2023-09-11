import random

import mysql
import telebot
from telebot import types
import time
import mysql.connector as sql

conn = sql.connect(host="localhost", user="root", password="mySQL2341m", database="mydb",
                   auth_plugin='caching_sha2_password')

cursor = conn.cursor()

deletem = []
text = ''
status = ''
isadmin = ''
subobjlist = {'АНГЛ ЯЗ': 'Лабаченя;Хадарович', 'РУСС': 'РУСС ЯЗ;РУСС ЛИТ', 'БЕЛ': 'БЕЛ ЯЗ;БЕЛ ЛИТ',
              'ИНФОРМ':'Ковалевская;Боркун', 'ИСТОРИЯ':'БЕЛАРУСИ;ВСЕМИРНАЯ', 'МАТЕМ':'ГЕОМЕТРИЯ;АЛБЕБРА'}

bot = telebot.TeleBot('1876503650:AAH_sMeqFTVZx5PkW6dktrLKKJtIsPYkNck')


@bot.message_handler(content_types=['text'])
def start(message):
    global status, isadmin

    cursor.execute(f"""INSERT ignore `mydb`.`student`(`id`,`status`,`admin`)VALUES('{message.from_user.id}', 'mainmenu', 
    'noadmin')""")

    cursor.execute(f"""SELECT status From `mydb`.`student` WHERE (`id` = {message.from_user.id});""")
    check = cursor.fetchall()
    for check0 in check:
        status = str(check0)[2:len(check0) - 4]
    conn.commit()

    cursor.execute(f"""SELECT admin From `mydb`.`student` WHERE (`id` = {message.from_user.id});""")
    check = cursor.fetchall()
    for check0 in check:
        isadmin = str(check0)[2:len(check0) - 4]
    conn.commit()

    if status == 'mainmenu' and isadmin == 'noadmin':
        if message.text == '/admin':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("❌ Отменить")
            markup.add(btn1)
            deletem.append(bot.send_message(message.from_user.id, f"Напишите пароль: ", reply_markup=markup))
            bot.register_next_step_handler(message, admincheck)

        if message.text == '🗓 ВСЁ ДЗ':
            homework(message, isadmin)
        elif message.text != '/admin':
            basemenu(message)

    if status == 'mainmenu' and isadmin == 'yesadmin':
        if message.text == '✏ ДОБАВИТЬ':
            cursor.execute(
                f"""UPDATE `mydb`.`student` SET `status` = 'adding' WHERE (`id` = {message.from_user.id})""")
            conn.commit()
            lessons(message)
        if message.text == '🗓 ВСЁ ДЗ':
            homework(message, isadmin)
        elif message.text != '/admin':
            adminmenu(message)

    if status == 'adding' and isadmin == 'yesadmin':
        if message.text == 'АНГЛ ЯЗ' or message.text == 'РУСС' or message.text == 'БЕЛ' or message.text == 'ИНФОРМ'\
                or message.text == 'ИСТОРИЯ' or message.text == 'МАТЕМ':
            a = 0
            keyword1 = ''
            keyword2 = ''
            for i in subobjlist[message.text]:
                if i == ';':
                    a = 1
                if a == 1:
                    keyword2 += i
                if a == 0:
                    keyword1 += i
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(f'1️⃣ {keyword1}')
            btn2 = types.KeyboardButton(f'2️⃣ {keyword2[1:len(keyword2)]}')
            btn3 = types.KeyboardButton("❌ Отменить")
            markup.add(btn1, btn2, btn3)
            deletem.append(bot.send_message(message.from_user.id, f"Выберите:", reply_markup=markup))
            bot.register_next_step_handler(message, subgroups, f'1️⃣ {keyword1}', f'2️⃣ {keyword2[1:len(keyword2)]}')
        elif message.text == '❌ВЫЙТИ':
            cursor.execute(
                f"""UPDATE `mydb`.`student` SET `status` = 'mainmenu' WHERE (`id` = {message.from_user.id})""")
            conn.commit()
            adminmenu(message)
        elif message.text == 'ГЕОГРАФ' or message.text == 'БИОЛОГ' or message.text == 'ФИЗИК' or message.text == 'ХИМИЯ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("❌ Отменить")
            markup.add(btn1)
            deletem.append(bot.send_message(message.from_user.id, f"Напишите дз: ", reply_markup=markup))
            bot.register_next_step_handler(message, write, message.text)
        else:
            lessons(message)


def subgroups(message, keyword1, keyword2):
    if message.text == '❌ Отменить':
        bot.send_message(message.from_user.id, f"Действие было отменено")
        lessons(message)
    elif message.text == keyword1 or message.text == keyword2:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("❌ Отменить")
        markup.add(btn1)
        deletem.append(bot.send_message(message.from_user.id, f"Напишите дз: ", reply_markup=markup))
        bot.register_next_step_handler(message, write, message.text[4:len(message.text)])
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(f'{keyword1}')
        btn2 = types.KeyboardButton(f'2️⃣  {keyword2[4:len(keyword2)]}')
        btn3 = types.KeyboardButton("❌ Отменить")
        markup.add(btn1, btn2, btn3)
        deletem.append(bot.send_message(message.from_user.id, f"Вы ввели какюую-то херню. Введите нормально: ", reply_markup=markup))
        bot.register_next_step_handler(message, subgroups, f'{keyword1}', f'{keyword2}')


def write(message, hitler):
    if message.text == '❌ Отменить':
        bot.send_message(message.from_user.id, f"Действие было отменено")
        lessons(message)
    else:
        cursor.execute(
            f"""Delete from mydb.object where object = '{hitler}'""")
        cursor.execute(
            f"""INSERT ignore `mydb`.`object`(`object`,`text`)VALUES('{hitler}','{message.text}')""")
        conn.commit()
        bot.send_message(message.from_user.id, f"Спасибо за ввод дз!")
        adminmenu(message)


def lessons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('АНГЛ ЯЗ')
    btn2 = types.KeyboardButton("РУСС")
    btn3 = types.KeyboardButton("БЕЛ")
    btn4 = types.KeyboardButton("ИНФОРМ")
    btn5 = types.KeyboardButton("ИСТОРИЯ")
    btn6 = types.KeyboardButton("МАТЕМ")
    btn8 = types.KeyboardButton("ГЕОГРАФ")
    btn9 = types.KeyboardButton("БИОЛОГ")
    btn10 = types.KeyboardButton("ФИЗИК")
    btn11 = types.KeyboardButton("ХИМИЯ")
    btn15 = types.KeyboardButton("❌ВЫЙТИ")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn8, btn9, btn10, btn11, btn15)
    deletem.append(bot.send_message(message.from_user.id, "Выберите предмет", reply_markup=markup))


def homework(message, isitadmin):
    cursor.execute(f"""SELECT object From `mydb`.`object`""")
    obj = cursor.fetchall()
    for obj0 in obj:
        format = "'%M %D %Y, %H %M %S'"
        cursor.execute(f"""SELECT DATE_FORMAT(datatime, '%M %D %Y, %H:%m:%s') From `mydb`.`object` where object = '{str(obj0)[2:len(str(obj0))-3].upper()}'""")

        datet = cursor.fetchall()
        for datet0 in datet:

            cursor.execute(f"""SELECT text From `mydb`.`object` where object = '{str(obj0)[2:len(str(obj0)) - 3].upper()}'""")
            textt = cursor.fetchall()
            for textt0 in textt:
                bot.send_message(message.from_user.id,
                                 f"{str(obj0)[2:len(str(obj0))-3]}: {str(textt0)[2:len(str(textt0))-3]} \n-обновленно в {str(datet0)[2:len(str(datet0))-3]}-\n\n")
#                text += f"{str(obj0)[2:len(str(obj0))-3]}: {text0} \n-обновленно в {datet0}-\n\n"
#    bot.send_message(message.from_user.id, text)
    if isitadmin == 'yesadmin':
        adminmenu(message)
    if isitadmin == 'noadmin':
        basemenu(message)


def basemenu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🗓 ВСЁ ДЗ')
    markup.add(btn1)
    bot.send_message(message.from_user.id, f"Выберите опцию", reply_markup=markup)


def adminmenu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🗓 ВСЁ ДЗ')
    btn2 = types.KeyboardButton('✏ ДОБАВИТЬ')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, f"Выберите опцию для администатора", reply_markup=markup)


def admincheck(message):
    if message.text == '❌ Отменить':
        bot.send_message(message.from_user.id, f"Действие было отменено")
        basemenu(message)

    elif message.text == 'Десятка домой':
        cursor.execute(f"""UPDATE `mydb`.`student` SET `admin` = 'yesadmin' WHERE (`id` = {message.from_user.id})""")
        conn.commit()
        bot.send_message(message.from_user.id, f"Поздравляю! Вы стали администратором в боте!")
        adminmenu(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("❌ Отменить")
        markup.add(btn1)
        deletem.append(bot.send_message(message.from_user.id, f"Ваш пароль недействителен. Повторите попытку: ",
                                        reply_markup=markup))
        bot.register_next_step_handler(message, admincheck)


conn.commit()
bot.polling(none_stop=True, interval=0)
