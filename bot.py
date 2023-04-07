#Cообщение приветствия:
#"Привет, комбезник!


import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


vk_session = vk_api.VkApi(
    token = "TOKEN_GROUP"
    )
vk = vk_session.get_api()

def send_message(user_id, message, keyboard = None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0,
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    
    vk_session.method("messages.send", post)

def send_photo(peer_id, photo, keyboard = None):
    a = vk_session.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open(photo, 'rb')}).json()
    c = vk_session.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    d = "photo{}_{}".format(c["owner_id"], c["id"])
    post = {
        "peer_id": peer_id,
        "message": "Держи",
        "attachment": d,
        "random_id": 0,
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    
    vk_session.method("messages.send", post)

longpoll = VkLongPoll(vk_session)
index_msg = 0
courses = ["1", "2", "3", "4", "5", "6"]
user_course = ""
choice_command = 0

keyboard_start = VkKeyboard(True)
keyboard_start.add_button("Начать", VkKeyboardColor.POSITIVE.value)

keyboard_commands = VkKeyboard(True)
keyboard_commands.add_button("Расписание", VkKeyboardColor.POSITIVE.value)
keyboard_commands.add_line()
keyboard_commands.add_button("Предметы на курсе", VkKeyboardColor.SECONDARY.value)
keyboard_commands.add_line()
keyboard_commands.add_button("Закончить сессию", VkKeyboardColor.NEGATIVE.value)

keyboard_back = VkKeyboard(True)
keyboard_back.add_button("Назад", VkKeyboardColor.PRIMARY.value)

keyboard_courses = VkKeyboard(True)
keyboard_courses.add_button("1", VkKeyboardColor.POSITIVE.value)
keyboard_courses.add_button("2", VkKeyboardColor.PRIMARY.value)
keyboard_courses.add_button("3", VkKeyboardColor.POSITIVE.value)
keyboard_courses.add_line()
keyboard_courses.add_button("4", VkKeyboardColor.PRIMARY.value)
keyboard_courses.add_button("5", VkKeyboardColor.POSITIVE.value)
keyboard_courses.add_button("6", VkKeyboardColor.PRIMARY.value)
keyboard_courses.add_line()
keyboard_courses.add_button("Назад", VkKeyboardColor.NEGATIVE.value)

f_course_subs = ("Алгебра\nДискретная математика\nИностранный язык\nИнформатикa\n" 
                "Физ-ра\nМат. анализ\nВведение в математику\nИстория\n" 
                "Введение в специальность\nГеометрия")
s_course_subs = ("Алгебра\nАлгоритмы кодирования и сжатия информации\nТеория вероятности\n" 
                "Аппаратные средства вычислительной техники\nДискретная математика\n"
                "Иностранный язык\nМетоды программирования\nФиз-ра\nЯзыки программирования\n"
                 "Мат. анализ\nАлгебра\nВведение в специальность")
t_course_subs = ("Теория автоматов\nКомпьютерные сети\nМат. логика\n"
                 "Технический английский\nСистемы управления базами данных\nФиз-ра\nФизика\n"
                 "Мат. стат.\nТеоретико-числовые методы в криптографии\nЯзыки программирования\n"
                 "Теория чисел\nФилософия\nНИР")
fo_course_subs = ("Комбинаторика\nКриптографические методы защиты информации\nМетоды компиляции\n"
                  "Операционные системы\nКомпьютерные сети\nПравоведение\nТЧМК\n"
                  "Теория информации\nФизика\nБЖД\nБулевы функции в криптографии\nБазы данных\n"
                  "Соц.Инженерия\nТеория кодирования и сжатия информации\n"
                  "Электроника и схемотехника\nНИР")
fi_course_subs = ("Аппаратная реализация криптоалгоритмов\nБезопасность веб-приложений\nЗПД\n"
                  "КриптоПротоколы\nМетоды верификации\nМодели безопасности компьютерных систем\n"
                  "Психология\nСети и системы передачи информации\nТехническая защита информации\n"
                  "Экономика\nАнализ уязвимостей ПО\nЗащита в операционных системах\n"
                  "Основы управленческой деятельности\nОблачные вычисления\n"
                  "Производственная практика")
six_course_subs = ("Организационное и правовое обеспечение информационной безопасности\n"
                   "Основы информационной безопасности\nВКР")

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        text = event.text
        user_id = event.user_id
        peer_id = event.peer_id
        #Слушаем longpoll, если пришло сообщение то:	
        if text.lower() == "начать":
            index_msg = 1
            message = "Привет, комбезник, чем я могу тебе помочь?"
            send_message(user_id, message, keyboard_commands)
            continue

        elif index_msg == 0:
            message = "Нажми кнопку 'Начать', и мы приступим"
            send_message(user_id, message, keyboard_start)
        
        elif index_msg == 1:
            if text.lower() == "расписание":
                index_msg += 1
                choice_command = 1
                message = "Выберите курс (1-6)"
                send_message(user_id, message, keyboard_courses)
            
            elif text.lower() == "предметы на курсе":
                index_msg += 1
                choice_command = 2
                message = "Выберите курс (1-6)"
                send_message(user_id, message, keyboard_courses)
                        
            elif text.lower() == "закончить сессию":
                index_msg -= 1
                message = "Нажмите кнопку 'Начать', и мы приступим"
                send_message(user_id, message, keyboard_start)
            else:
                message = "Я пока не знаю такие команды"
                send_message(user_id, message, keyboard_commands)
        elif index_msg == 2: 
            if text in courses:
                user_course = text
                if choice_command == 1:
                    index_msg += 1
                    message = "Укажите свою группу"
                    keyboard_groups = VkKeyboard()
                    keyboard_groups.add_button("Назад")
                    if text == "1":
                        keyboard_groups.add_button("932223")
                        keyboard_groups.add_button("932224")
                        send_message(user_id, message, keyboard_groups)
                    elif text == "2":
                        keyboard_groups.add_button("932124")
                        keyboard_groups.add_button("932125")
                        send_message(user_id, message, keyboard_groups)
                    elif text == "3":
                        keyboard_groups.add_button("932024")
                        keyboard_groups.add_button("932025")
                        send_message(user_id, message, keyboard_groups)
                    elif text == "4":
                        keyboard_groups.add_button("931924")
                        keyboard_groups.add_button("931925")
                        send_message(user_id, message, keyboard_groups)
                    elif text == "5":
                        keyboard_groups.add_button("931824/25")
                        send_message(user_id, message, keyboard_groups)
                    else:
                        keyboard_groups.add_button("931723/24")
                        send_message(user_id, message, keyboard_groups)
                else:
                    if text == "1":
                        message = f_course_subs
                        send_message(user_id, message, keyboard_courses)
                    elif text == "2":
                        message = s_course_subs
                        send_message(user_id, message, keyboard_courses)
                    elif text == "3":
                        message = t_course_subs
                        send_message(user_id, message, keyboard_courses)
                    elif text == "4":
                        message = fo_course_subs
                        send_message(user_id, message, keyboard_courses)
                    elif text == "5":
                        message = fi_course_subs
                        send_message(user_id, message, keyboard_courses)
                    else:
                        message = six_course_subs
                        send_message(user_id, message, keyboard_courses)

            elif text.lower() == "назад":
                index_msg -= 1
                choice_command = 0
                message = "Выберите действие"
                send_message(user_id, message, keyboard_commands)

            else:
                message = "Напиши номер курса: 1-6"
                send_message(user_id, message, keyboard_courses)

        elif index_msg == 3: 
            if text == "931824/25" and user_course == "5":
                photo = "Расписание/931825.jpg"
                send_photo(peer_id, photo)

            elif text == "931925" and user_course == "4":
                photo = "Расписание/931925.jpg"
                send_photo(peer_id, photo)

            elif text == "931924" and user_course == "4":
                photo = "Расписание/931924.jpg"
                send_photo(peer_id, photo)

            elif text == "932024" and user_course == "3":
                photo = "Расписание/932024.jpg"
                send_photo(peer_id, photo)

            elif text == "932025" and user_course == "3":
                photo = "Расписание/932025.jpg"
                send_photo(peer_id, photo)

            elif text == "932125" and user_course == "2":
                photo = "Расписание/932125.jpg"
                send_photo(peer_id, photo)

            elif text == "932124" and user_course == "2":
                photo = "Расписание/932124.jpg"
                send_photo(peer_id, photo)

            elif text == "932223" and user_course == "1":
                photo = "Расписание/932223.jpg"
                send_photo(peer_id, photo)

            elif text == "932224" and user_course == "1":
                photo = "Расписание/932224.jpg"
                send_photo(peer_id, photo)
            
            elif text == "931723/24" and user_course == "6":
                message = "Поздравляю с окончанием учёбы!"
                send_message(user_id, message)

            elif text.lower() == "назад":
                index_msg -= 1
                user_course = ""
                message = "Напиши свой курс (1-6)"
                send_message(user_id, message, keyboard_courses)

            else:
                message = ("Группа не соответствует курсу")
                send_message(user_id, message)


