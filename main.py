from pprint import pprint
import requests
import json

from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests

token_group = 'vk1.a.55tbxDi-xjofojgSy6jkWiwZctH2ldZCefwcXnNlehSa5oNp4F_DhezNJMRnByTFS-xNi5pjyytOPrnUzzrpe7nA9ZAiiHPUqwMzB32FYNthGzS2KfLPoH729kKrDLdVsIDUVd6F755qRsLw1ZvGy8gAC6ijeU8ruuDTr-aK-LPTBdNVRwbzXERUTqqFiwUmt8WeChT4Kg-gRagKRknX6g'
id_application = '51777292'
access_token = 'vk1.a.H4rT3vDtnn44d-T3fkblYwD50amI56vxbtsM1vVc48klUUIjdL_M1Xk_n9c-6dnR8Be1dA5tUT1Xf7v3TC5mOosg8MQNlik80ogc_qOnTGAT2KWgHo0SxZsD8wBBUtIdmZV8c-NR1JBu7IFBKqD5sQYPJL74IrYl8XMLKQJ_E6ud-LwODtuM8qZmDcnow9cAEV3CYogEzLdlrpi9nMWTFQ'
user_id = '205203687'


class VKinder:

    def __init__(self, access_token, user_id, group_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.group_id = group_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def user_all_info(self):
        url = 'https://api.vk.com/method/groups.getMembers'
        params = {'access_token': self.token, 'group_id': self.group_id, 'fields': 'bdate, city, domain, sex',
                  'v': self.version}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photos_info(self):
        url = 'https://api.vk.com/method/photos.get/'
        private_account_photo = []
        for account in self.user_all_info()['response']['items']:
            account = account['id']
            params = {'access_token': self.token, 'user_id': account, 'album_id': 'profile', 'extended': '1',
                      'v': self.version}
            access_photos = requests.get(url, params=params).json()
            private_account_photo.append(access_photos)
        return private_account_photo

    def get_id(self):
        id_users = []
        name_users = []
        for id_user in self.user_all_info()['response']['items']:
            print(id_user['first_name'])
            name_users.append(id_user['first_name'])
            id_users.append(id_user['id'])
        dict_id = dict(zip(id_users, name_users))
        return dict_id

    def get_all_photos(self):
        dict_p = []
        for get_info_p in self.get_photos_info():
            inform = get_info_p['response']['items']
            lik = []
            url_photos = []
            for uni in inform:
                likes = uni['likes']['count']
                lik.append(likes)
                size = uni['sizes'][-1]
                photo = size['url']
                url_photos.append(photo)
            dict_photo = dict(zip(lik, url_photos))
            dict_p.append(dict_photo)
        return dict_p

    def three_photos(self):
        result_dict = []
        for photo_list in self.get_all_photos():
            likes_and_urls = {likes: url for likes, url in photo_list.items()}
            sorted_likes_and_urls = {k: likes_and_urls[k] for k in sorted(likes_and_urls, reverse=True)}
            top_3_photos = dict(list(sorted_likes_and_urls.items())[:3])
            result_dict.append(top_3_photos)
        combined_data = list(zip(self.get_id().keys(), result_dict))
        combined_dict = dict(combined_data)

        return combined_dict

access_token = access_token
user_id = user_id
group_id = 223096214
vk = VKinder(access_token, user_id, group_id)
pprint(vk.user_all_info())
name_id = vk.get_id()

import bd


vk_session = vk_api.VkApi(token=token_group)
vk = vk_session.get_api()
longpol = VkLongPoll(vk_session)

def write_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), 'keyboard': keyboard})

def get_but(message, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{message}"
        },
        "color": f"{color}"
    }

keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('Найди пару', 'negative'), get_but('Next', 'negative')],
        [get_but('Не ищи пару', 'positive'), get_but('Удачи', 'positive')]
    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


for event in longpol.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.lower()
            if request == "привет":
                write_msg(event.user_id, f"Хай, {name_id[event.user_id] if event.user_id in name_id.keys() else 'такого имени нет'}!")
                # print(name_id.values(), event.user_id)
            if request == "найди пару":
                write_msg(event.user_id, f'{bd.(функция / метод для поиска фаворитов по айди )}')
            if request == "слудующий":
                write_msg(event.user_id, f"{bd.(функция / метод для следующего фаворита)}")
            if request == "удачи":
                write_msg(event.user_id, f"спасибо")




