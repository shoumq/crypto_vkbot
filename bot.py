import vk_api
import json
import requests
from vk_api import longpoll
from config import bot_token
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload

session = vk_api.VkApi(token=bot_token)


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
        text = event.text.upper()
        user_id = event.user_id

        print(user_id, ':', text)

        if text == "Старт":
            keyboard = VkKeyboard()

            buttons = ["Узнать курс популярных криптовалют"]
            button_colors = [VkKeyboardColor.PRIMARY]

            for btn, btn_color in zip(buttons, button_colors):
                keyboard.add_button(btn, btn_color)

            send_message(user_id, "Привет!")

        if text != "Старт":
            keyboard = VkKeyboard()

            buttons = ["Узнать курс популярных криптовалют"]
            button_colors = [VkKeyboardColor.PRIMARY]

            for btn, btn_color in zip(buttons, button_colors):
                keyboard.add_button(btn, btn_color)

            url = f'https://min-api.cryptocompare.com/data/pricemulti?fsyms=' + text + \
                '&tsyms=BTC,USD,EUR,RUB&api_key=416db249c44d22c2be9e0f207eb26c3da07383c4b2134c41470ff46d6cc1daef'
            resp = requests.get(url)

            json_resp = json.loads(resp.text)

            if json_resp[text]["BTC"] != '-1':
                print("BTC:", str(json_resp[text]['BTC']))
                print("USD:", str(json_resp[text]['USD']))
                print("EUR:", str(json_resp[text]['EUR']))
                print("RUB:", str(json_resp[text]['RUB']))
            elif json_resp["Response"] == "Error":
                send_message(user_id, 'Криптовалюта не найдена!', keyboard)

            # Отправка сообщений
            if json_resp[text]["BTC"] != '-1':
                send_message(user_id, 'BTC: ' +
                             str(json_resp[text]['BTC']), keyboard)
                send_message(user_id, 'USD: ' +
                             str(json_resp[text]['USD']), keyboard)
                send_message(user_id, 'EUR: ' +
                             str(json_resp[text]['EUR']), keyboard)
                send_message(user_id, 'RUB: ' +
                             str(json_resp[text]['RUB']), keyboard)

            elif json_resp["Response"] == "Error":
                send_message(user_id, 'Криптовалюта не найдена!', keyboard)
