import vk_api
import json
from vk_api import longpoll
from config import bot_token
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload

session = vk_api.VkApi(token=bot_token)

#Вывод сообщения
def send_message(user_id, message, keyboard=None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0,
    }

    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    else:
        post = post

    session.method("messages.send", post)

for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id

        print(user_id,':', text)

        if text == "Start":
            keyboard = VkKeyboard()

            buttons = ["Главная", "Профиль", "Инфо"]
            button_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE]

            for btn, btn_color in zip(buttons, button_colors):
                keyboard.add_button(btn, btn_color)

            send_message(user_id, "Привет!")
    

        if text == "Главная":
            keyboard = VkKeyboard()

            buttons = ["Главная", "Профиль", "Инфо"]
            button_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE]

            for btn, btn_color in zip(buttons, button_colors):
                keyboard.add_button(btn, btn_color)

            send_message(user_id, "👋🏻 Привет, \nя игровой бот Apxidea!", keyboard)

            # if buttons[0] == "Главная":
            #     send_message(user_id, "👋🏻 Привет, я игровой бот Apxidea,\n 👮‍ скорее нажимай на кнопку Старт и начинай играть!", keyboard)