import vk_api
import json
import requests
from vk_api import longpoll
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload

bot_token = '36e1e01db40c2317b3afa628c3d3fc94fda70e1d12a9a72b7b44359d003abcd2c500bc35a503ff9d62e9f'

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
        text = event.text
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
                
            url = 'https://min-api.cryptocompare.com/data/price?fsym=' + \
                text.upper() + '&tsyms=BTC,USD,EUR,RUB'
            resp = requests.get(url)

            json_resp = json.loads(resp.text)

            # if json_resp[text]["BTC"] == json_resp[text]['BTC']:
            #     print("BTC:", str(json_resp[text]['BTC']))
            #     print("USD:", str(json_resp[text]['USD']))
            #     print("EUR:", str(json_resp[text]['EUR']))
            #     print("RUB:", str(json_resp[text]['RUB']))
            # else:
            #     print(user_id, 'Криптовалюта не найдена!', keyboard)

            try:
                print("BTC:", str(json_resp['BTC']))
                print("USD:", str(json_resp['USD']))
                print("EUR:", str(json_resp['EUR']))
                print("RUB:", str(json_resp['RUB']))

                # Сообщение в Вк
                send_message(user_id, 'BTC: ' +
                        str(json_resp['BTC']), keyboard)
                send_message(user_id, 'USD: ' +
                            str(json_resp['USD']), keyboard)
                send_message(user_id, 'EUR: ' +
                            str(json_resp['EUR']), keyboard)
                send_message(user_id, 'RUB: ' +
                            str(json_resp['RUB']), keyboard)
            except:
                print(user_id, text, 'Криптовалюта не найдена!')

                # Сообщение в Вк
                send_message(user_id, 'Криптовалюта не найдена!', keyboard)
