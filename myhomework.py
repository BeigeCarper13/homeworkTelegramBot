import mysql
import telebot
from telebot import types
import time
import mysql.connector as sql

maindb = 'heroku_a5b02c6d58c3d21'
deletem = []
text = ''
status = ''
isadmin = ''
conn = sql.connect(host="eu-cdbr-west-03.cleardb.net", user="b8660ea738335d", password="99f21639",
                   database="heroku_a5b02c6d58c3d21", port="3306")
cursor = conn.cursor()
subobjlist = {'АНГЛ ЯЗ': 'Лабаченя;Хадарович', 'РУСС': 'РУСС ЯЗ;РУСС ЛИТ', 'БЕЛ': 'БЕЛ ЯЗ;БЕЛ ЛИТ',
              'ИНФОРМ': 'Ковалевская;Боркун', 'ИСТОРИЯ': 'БЕЛАРУСИ;ВСЕМИРНАЯ', 'МАТЕМ': 'ГЕОМЕТРИЯ;АЛБЕБРА'}
curicurral = {'1': 'АНГЛ ЯЗ;ВСЕМИРНАЯ;РУСС ЛИТ;ТРУД ОБУЧ;ИСКУССТВО;БИОЛОГ;',
              '2': 'БЕЛ ЯЗ;БИОЛОГ;РУСС ЯЗ;ГЕОМЕТРИЯ;ГЕОМЕТРИЯ;АНГЛ ЯЗ;ГЕОГРАФ;',
              '3': 'ФИЗРА;ХИМИЯ;ФИЗИК;ФИЗИК;ГЕОМЕТРИЯ;БЕЛ ЯЗ;РУСС ЯЗ;',
              '4': 'ХИМИЯ;ФИЗРА;ФИЗИК;АЛБЕБРА;АНГЛ ЯЗ;БЕЛ ЛИТ;',
              '5': 'ГЕОГРАФ;БЕЛАРУСИ;ФИЗРА;БЕЛ ЛИТ;АЛБЕБРА;АЛБЕБРА;ИНФОРМ;'}

bot = telebot.TeleBot('1876503650:AAH_sMeqFTVZx5PkW6dktrLKKJtIsPYkNck')


@bot.message_handler(content_types=['text'])
def start(message):
    conn = sql.connect(host="eu-cdbr-west-03.cleardb.net", user="b8660ea738335d", password="99f21639",
                       database="heroku_a5b02c6d58c3d21", port="3306")
    cursor = conn.cursor()
    print(f"Пользователь: {message.from_user.id}, id: {message.chat.id}, username: @{message.from_user.username}, "
          f"Текст: {message.text}, name: {message.from_user.first_name}.\n")

    global status, isadmin
    try:
        cursor.execute(f"""INSERT ignore `{maindb}`.`student`(`id`,`status`,`admin`)VALUES('{message.from_user.id}', 'mainmenu', 'noadmin')""")
    except mysql.connector.errors.OperationalError:
        print("mysql не работает")

    cursor.execute(f"""SELECT status From `{maindb}`.`student` WHERE (`id` = {message.from_user.id});""")
    check = cursor.fetchall()
    for check0 in check:
        status = str(check0)[2:len(check0) - 4]

    cursor.execute(f"""SELECT admin From `{maindb}`.`student` WHERE (`id` = {message.from_user.id});""")
    check = cursor.fetchall()
    for check0 in check:
        isadmin = str(check0)[2:len(check0) - 4]
    conn.commit()
    if status == 'banned':
        bot.send_message(message.from_user.id, f"Женя, иди отсюда")
    if status == 'mainmenu' and isadmin == 'noadmin':
        if message.text == '/admin':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("❌ Отменить")
            markup.add(btn1)
            deletem.append(bot.send_message(message.from_user.id, f"Напишите пароль: ", reply_markup=markup))
            bot.register_next_step_handler(message, admincheck, )

        elif message.text == '🗓 ВСЁ ДЗ':
            cursor.execute(
                f"""select search from `heroku_a5b02c6d58c3d21`.`student` where id = {message.from_user.id};""")
            check = cursor.fetchall()
            for check0 in check:
                if str(check0)[1:len(check0) - 3] == '1':
                    bot.send_message(message.from_user.id, f"Запрос обрабатывается...")
                else:
                    homework(message, isadmin)
        elif message.text == '📋 РАСПИСАНИЕ' or message.text == '/homework' or message.text == '/homework@Misca8bot':
            lessonslist(message, isadmin)
        elif message.text == '/basemenu':
            basemenu(message)

    if status == 'mainmenu' and isadmin == 'yesadmin':
        if message.text == '✏ ДОБАВИТЬ':
            cursor.execute(f"""UPDATE `{maindb}`.`student` SET `status` = 'adding' WHERE (`id` = {message.from_user.id})""")
            conn.commit()
            lessons(message)
        if message.text == '🗓 ВСЁ ДЗ':
            cursor.execute(f"""select search from `heroku_a5b02c6d58c3d21`.`student` where id = {message.from_user.id};""")
            check = cursor.fetchall()
            for check0 in check:
                if str(check0)[1:len(check0) - 3] == '1':
                    bot.send_message(message.from_user.id, f"Запрос обрабатывается...")
                else:
                    homework(message, isadmin)
        if message.text == '📋 РАСПИСАНИЕ' or message.text == '/homework' or message.text == '/homework@Misca8bot':
            lessonslist(message, isadmin)
        if message.text == '🔧 ПОМЕНЯТЬ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("❌ Отменить")
            markup.add(btn1)
            deletem.append(bot.send_message(message.from_user.id, f"Впишите день недели", reply_markup=markup))
            bot.register_next_step_handler(message, change)
        if message.text == '/basemenu':
            adminmenu(message)

    if status == 'adding' and isadmin == 'yesadmin':
        if message.text == 'АНГЛ ЯЗ' or message.text == 'РУСС' or message.text == 'БЕЛ' or message.text == 'ИНФОРМ' \
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
                f"""UPDATE `{maindb}`.`student` SET `status` = 'mainmenu' WHERE (`id` = {message.from_user.id})""")
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


def lessonslist(message, isitadmin):
    cursor.execute(f"""SELECT day From `{maindb}`.`list` WHERE (`number` = '0')""")
    check = cursor.fetchall()

    alllessons = []
    onelesson = ''
    a = 1

    for check0 in check:

        for i in curicurral[str(int(str(check0)[2:len(str(check0)) - 3]))]:
            if i == ';':
                alllessons.append(onelesson)
                onelesson = ''
            else:
                onelesson += i
    onelesson = 'ДЗ НА ЗАВТРА:\n'

    for i in alllessons:
        if i == 'АНГЛ ЯЗ':
            cursor.execute(f"""SELECT text From `{maindb}`.`object` WHERE (`object` = 'Лабаченя')""")
            obj = cursor.fetchall()
            for obj0 in obj:
                onelesson += f'*{a}) АНГЛ ЯЗ(Лабаченя) -*  {str(obj0)[2:len(str(obj0)) - 3]}\n'
            cursor.execute(f"""SELECT text From `{maindb}`.`object` WHERE (`object` = 'ХАДАРОВИЧ')""")
            obj = cursor.fetchall()
            for obj0 in obj:
                onelesson += f'*{a}) АНГЛ ЯЗ(ХАДАРОВИЧ) -*  {str(obj0)[2:len(str(obj0)) - 3]}\n-\n'
                a += 1
        elif i == 'БЕЛАРУСИ':
            cursor.execute(f"""SELECT text From `{maindb}`.`object` WHERE (`object` = 'БЕЛАРУСИ')""")
            obj = cursor.fetchall()
            for obj0 in obj:
                onelesson += f'*{a}) ИСТОРИЯ БЕЛАРУСИ -*  {str(obj0)[2:len(str(obj0)) - 3]}\n-\n'
            a += 1
        elif i == 'ВСЕМИРНАЯ':
            cursor.execute(f"""SELECT text From `{maindb}`.`object` WHERE (`object` = 'ВСЕМИРНАЯ')""")
            obj = cursor.fetchall()
            for obj0 in obj:
                onelesson += f'*{a}) ВСЕМИРНАЯ ИСТОРИЯ -*  {str(obj0)[2:len(str(obj0)) - 3]}\n-\n'
            a += 1
        elif i == 'ИНФОРМ':
            cursor.execute(f"""SELECT text From `{maindb}`.`object` WHERE (`object` = 'Ковалевская')""")
            obj = cursor.fetchall()
            for obj0 in obj:
                onelesson += f'*{a}) ИНФОРМ(Ковалевская) -*  {str(obj0)[2:len(str(obj0)) - 3]}\n'
            cursor.execute(f"""SELECT text From `{maindb}`.`object` WHERE (`object` = 'Боркун')""")
            obj = cursor.fetchall()
            for obj0 in obj:
                onelesson += f'*{a}) ИНФОРМ(Боркун) -*  {str(obj0)[2:len(str(obj0)) - 3]}\n-\n'
                a += 1
        else:
            cursor.execute(f"""SELECT text From `{maindb}`.`object` WHERE (`object` = '{i}')""")
            obj = cursor.fetchall()

            for obj0 in obj:
                onelesson += f'*{a}) {i} -*  {str(obj0)[2:len(str(obj0)) - 3]}\n-\n'
                a += 1
    bot.send_message(message.chat.id, f"{onelesson[0:len(onelesson)-2]}", parse_mode="Markdown")

    alllessons.clear()
    if isitadmin == 'yesadmin' and message.chat.id == message.from_user.id:
        adminmenu(message)
    if isitadmin == 'noadmin' and message.chat.id == message.from_user.id:
        basemenu(message)


def change(message):
    if message.text == '❌ Отменить':
        bot.send_message(message.from_user.id, f"Действие было отменено")
        lessons(message)
    else:
        cursor.execute(
            f"""Delete from {maindb}.list where lesson = '0'""")
        cursor.execute(
            f"""INSERT ignore `{maindb}`.`list`(`number`,`day`,`lesson`)VALUES('0','{message.text}','0')""")
        conn.commit()
        bot.send_message(message.from_user.id, f"Спасибо за ввод даты!")
        adminmenu(message)


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
        deletem.append(bot.send_message(message.from_user.id, f"Вы ввели какюую-то херню. Введите нормально: ",
                                        reply_markup=markup))
        bot.register_next_step_handler(message, subgroups, f'{keyword1}', f'{keyword2}')


def write(message, hitler):
    if message.text == '❌ Отменить':
        bot.send_message(message.from_user.id, f"Действие было отменено")
        lessons(message)
    else:
        cursor.execute(
            f"""Delete from {maindb}.object where object = '{hitler}'""")
        cursor.execute(
            f"""INSERT ignore `{maindb}`.`object`(`object`,`text`)VALUES('{hitler}','{message.text}')""")
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
    a = ''
    cursor.execute(f"""UPDATE `{maindb}`.`student` SET `search` = '1' WHERE (`id` = {message.from_user.id})""")
    cursor.execute(f"""SELECT object from `{maindb}`.`object`""")
    obj = cursor.fetchall()
    for obj0 in obj:
        format = "'%M %D %Y, %H %M %S'"
        cursor.execute(
            f"""SELECT DATE_FORMAT(datatime, '%M %D %Y, %H:%m:%s') From `{maindb}`.`object` where object = '{str(obj0)[2:len(str(obj0)) - 3].upper()}'""")

        datet = cursor.fetchall()
        for datet0 in datet:

            cursor.execute(
                f"""SELECT text From `{maindb}`.`object` where object = '{str(obj0)[2:len(str(obj0)) - 3].upper()}'""")
            textt = cursor.fetchall()
            for textt0 in textt:
                a += f"*{str(obj0)[2:len(str(obj0)) - 3]} -* {str(textt0)[2:len(str(textt0)) - 3]} \n" \
                     f"-обновленно в {str(datet0)[2:len(str(datet0)) - 3]}-\n\n"
    bot.send_message(message.from_user.id, a, parse_mode="Markdown")
    cursor.execute(f"""UPDATE `{maindb}`.`student` SET `search` = '0' WHERE (`id` = {message.from_user.id})""")
    if isitadmin == 'yesadmin':
        adminmenu(message)
    if isitadmin == 'noadmin':
        basemenu(message)


def basemenu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#    btn1 = types.KeyboardButton('🗓 ВСЁ ДЗ')
    btn2 = types.KeyboardButton('📋 РАСПИСАНИЕ')
    markup.add(btn2)
    bot.send_message(message.from_user.id, f"Выберите опцию", reply_markup=markup)


def adminmenu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🗓 ВСЁ ДЗ')
    btn2 = types.KeyboardButton('✏ ДОБАВИТЬ')
    btn3 = types.KeyboardButton('📋 РАСПИСАНИЕ')
    btn4 = types.KeyboardButton('🔧 ПОМЕНЯТЬ')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, f"Выберите опцию для администатора", reply_markup=markup)


def admincheck(message):
    if message.text == '❌ Отменить':
        bot.send_message(message.from_user.id, f"Действие было отменено")
        basemenu(message)

    elif message.text == 'Десятка домой':
        cursor.execute(f"""UPDATE `{maindb}`.`student` SET `admin` = 'yesadmin' WHERE (`id` = {message.from_user.id})""")
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
