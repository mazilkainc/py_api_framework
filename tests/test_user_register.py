import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import random
import string


class TestUserRegister(BaseCase):
    def setup(self):
        self.base_part = "learnqa"
        self.domain = "example.com"
        self.random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{self.base_part}{self.random_part}@{self.domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

#       Создание пользователя с некорректным email - без символа @
    def test_create_user_with_email_without_at(self):
        email = f"{self.base_part}{self.random_part}{self.domain}"
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_decode(response, "Invalid email format")

#       Создание пользователя без указания одного из полей - с помощью @parametrize необходимо проверить, что отсутствие любого параметра не дает зарегистрировать пользователя
    exclude_params = [
        ("no_password"),
        ("no_username"),
        ("no_firstName"),
        ("no_lastName"),
        ("no_email")
    ]

    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_without_param(self, condition):
        data = {
            'password': '123',
            'username': f"learnqa{self.random_part}",
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        if condition == "no_password":
            data.pop("password")
            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
            Assertions.assert_code_status(response, 400)
            Assertions.assert_content_decode(response, "The following required params are missed: password")

        elif condition == "no_username":
            data.pop("username")
            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
            Assertions.assert_code_status(response, 400)
            Assertions.assert_content_decode(response, "The following required params are missed: username")

        elif condition == "no_firstName":
            data.pop("firstName")
            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
            Assertions.assert_code_status(response, 400)
            Assertions.assert_content_decode(response, "The following required params are missed: firstName")

        elif condition == "no_lastName":
            data.pop("lastName")
            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
            Assertions.assert_code_status(response, 400)
            Assertions.assert_content_decode(response, "The following required params are missed: lastName")

        elif condition == "no_email":
            data.pop("email")
            response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
            Assertions.assert_code_status(response, 400)
            Assertions.assert_content_decode(response, "The following required params are missed: email")

#       Создание пользователя с очень коротким именем в один символ

    def test_create_user_with_short_name(self):
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(1))
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_decode(response, "The value of 'username' field is too short")

#       Создание пользователя с очень длинным именем - длиннее 250 символов
    def test_create_user_with_long_name(self):
        username = ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for _ in range(251))
        data = {
                'password': '123',
                'username': username,
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content_decode(response, "The value of 'username' field is too long")




