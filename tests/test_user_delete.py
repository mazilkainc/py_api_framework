import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from datetime import datetime
import random
import string
import allure


class TestUserDelete(BaseCase):

    exclude_params = [
        ("user_id_2"),
        ("created_user_positive"),
        ("creared_user_from_another_negative")
    ]

    def setup(self):
        data = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id = self.get_json_value(response1, "user_id")

        self.base_part = "learnqa"
        self.domain = "example.com"
        self.random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{self.base_part}{self.random_part}@{self.domain}"



    @allure.description("This test delete user as user who can't be deleted, as the same user, as another user")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_delete_user(self, condition):



        response2 = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        if condition == "user_id_2":

            response5 = MyRequests.delete(f"/user/{self.user_id}",
                                    headers={"x-csrf-token": self.token},
                                    cookies={"auth_sid": self.auth_sid}
            )
            Assertions.assert_code_status(response5, 400)
            Assertions.assert_content_decode(response5, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

        elif condition == "created_user_positive":
            data = {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': self.email
            }
            response = MyRequests.post("/user/", data=data)
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

            response1 = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id = self.get_json_value(response1, "user_id")

            response5 = MyRequests.delete(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
            )
            Assertions.assert_code_status(response5, 200)
            Assertions.assert_content_decode(response5, "")

            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": self.token},
                cookies={"auth_sid": self.auth_sid}
            )
            Assertions.assert_code_status(response4, 404)
            Assertions.assert_content_decode(response4, "User not found")

        elif condition == "creared_user_from_another_negative":
            data = {
                'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': self.email
            }
            response = MyRequests.post("/user/", data=data)
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

            response2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token},
                cookies={"auth_sid": self.auth_sid}
            )
            # auth_sid = self.get_cookie(response, "auth_sid")
            # token = self.get_header(response1, "x-csrf-token")
            user_id = self.get_json_value(response2, "user_id")

            response5 = MyRequests.delete(f"/user/{user_id}",
                                    headers={"x-csrf-token": self.token},
                                    cookies={"auth_sid": self.auth_sid}
            )


            Assertions.assert_code_status(response5, 400)
            Assertions.assert_content_decode(response5, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")
#       Метод пытается удалить юзера, который залогинен



