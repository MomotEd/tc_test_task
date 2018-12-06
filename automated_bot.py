import random


from config.bot_config import (NUMBER_OF_USERS, MAX_POSTS_PER_USER,
                               MAX_LIKES_PER_USER, HOST, USER_DATA,
                               POST_MESSAGE, STRART_MSG)
import requests


class AutomatedBot:
    def __init__(self, user_data: list, users_amount, max_posts, max_likes,
                 host="localhost:8000", login="admin", password="admin",
                 email="admin@admin.com"):

        self.users_amount = users_amount
        self.user_data = user_data
        self.max_posts = max_posts
        self.max_likes = max_likes
        self.bot_jwt_token = None
        self.current_jwt_token = None
        self.host = host
        self.bot_login = login
        self.bot_password = password
        self.bot_email = email

    def retrieve_password_from_data(self, email):
        return next(iter([data["password"] for data
                          in self.user_data if data["email"] == email]), "")

    def get_token(self, email, password):
        token = None
        _ = None
        response = requests.post("{}/api/token/obtain/".format(self.host),
                                 {"email": email,
                                  "password": password})

        if response.status_code == 200:
            data = response.json()
            token = data['token']
        return _, token

    def refresh_token(self, jwt_token):
        response = requests.post("{}/api/token/refresh/".format(self.host),
                                 {"token": jwt_token})

        if response.status_code == 200:
            data = response.json()
            return data['token']

    def register_user(self, login="", password="", email=""):
        token = None
        data = {
            "username": login,
            "password": password,
            "email": email,
        }
        response = requests.post("{}/api/user/sign_up/".format(self.host), data=data)
        if response.status_code == 201:
            _, token = self.get_token(email, password)
        return response, token

    def authenticate(self, email, username, password):
        _, token_to_set = self.get_token(email, password)
        if token_to_set:
            return _, token_to_set
        print("Unable to get token. Trying to register {}".format(email))
        response, token_to_set = self.register_user(username, password, email)
        if token_to_set:
            return response, token_to_set
        print("Unable to register {}".format(email))
        return None, None

    def create_posts(self):
        print("------------------Start creating new posts--------------------")
        for user in self.user_data[:self.users_amount]:
            self.current_jwt_token = None
            email = user["email"]
            password = user["password"]
            username = user["username"]
            response, self.current_jwt_token = self.authenticate(email, username, password)

            if self.current_jwt_token:
                if not response:
                    print("User {} has beed registred, posts already made".format(email))
                    continue

                user_data = response.json()
                posts_amount = random.randint(1, self.max_posts)

                for post in range(0, posts_amount):
                    body = POST_MESSAGE
                    user_id = user_data.get('id')
                    user_url = "{}/api/user/{}/".format(self.host, user_id)
                    title = "{} made a new post".format(username)
                    data = {
                        "user": user_url,
                        "text": body,
                        "title": title
                    }
                    response = requests.post("{}/api/post/".format(self.host),
                                             data=data,
                                             headers={
                                                 "Authorization": "JWT {}".format(
                                                  self.current_jwt_token)})
                    if response.status_code != 201:
                        print('Unable to create a post for user {}'.format(username))
                        break
                    print('{}'.format(title))
            else:
                print('Unable to create user {}'.format(email))

    def do_like_activity(self):
        print("------------------Start creating new likes--------------------")
        user_activity_url = "{}/api/user/get_users_activity/?max_likes={}".format(self.host,
                                                                               self.max_likes)
        response = requests.get(user_activity_url,
                                headers={"Authorization": "JWT {}".format(self.bot_jwt_token)})
        if response.status_code == 200:
            for user in response.json():
                email = user['email']
                password = self.retrieve_password_from_data(email)
                _, self.current_jwt_token = self.get_token(email, password)

                for i in range(0, self.max_likes - user['likes_count']):
                    response = requests.post(
                        "{}/api/user/make_like/".format(self.host),
                        data={'id': user['id']},
                        headers={"Authorization": "JWT {}".format(self.current_jwt_token)})
                    if response.status_code == 200:
                        result = response.json()
                        print("Post with id {} has been liked".format(result['updated']))
                    elif response.status_code == 304:
                        print('No more posts left')
                        exit(0)
                    else:
                        raise Exception(
                            'User{} unavailable for like activity'.format(user['username']))
        else:
            print('Unable to get users activity')

    def run(self):
        print(STRART_MSG.format(self.host, self.users_amount, self.max_posts,
                                self.max_likes))

        if self.users_amount > len(self.user_data):
            print("User data is to small. Set up user amount to". format(
                len(self.user_data)))
            self.users_amount = len(self.user_data)

        _, self.bot_jwt_token = self.authenticate(self.bot_email, self.bot_login,
                                                  self.bot_password)
        if self.bot_jwt_token:
            self.create_posts()
            self.do_like_activity()


bot = AutomatedBot(USER_DATA, NUMBER_OF_USERS, MAX_POSTS_PER_USER,
                   MAX_LIKES_PER_USER, HOST)
bot.run()