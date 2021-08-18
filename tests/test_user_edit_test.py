import requests
import pytest
import json
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.fun import MyFun
import time
import random
import string
import allure

@allure.epic("User edit cases")
class TestUserEdit(BaseCase):
    exclude_params = [
        ("change_name"),
        ("change_name_to_1_char")
    ]
    TEST_CASE_LINK = 'https://www.gurock.com/testrail/'

#   Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем (positive)
#   Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем,
    #   на очень короткое значение в один символ (negative)
    @allure.title(f"Parameterized test title: adding {exclude_params}")
    @allure.description(f"This test change just created user first name to new name or to 1 char name")
    @allure.testcase(TEST_CASE_LINK, 'Test case title')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('condition', exclude_params)
    def test_edit_just_created_user(self, condition):
#       Look at lib/fun.py
        MyFun.register(self)

        MyFun.login(self, self.email, self.password)

        if condition == "change_name":
            new_name = "Changed Name"
            MyFun.edit(self, new_name, self.user_id, self.auth_sid, self.token)
            Assertions.assert_code_status(self.response3, 200)

            MyFun.get_user(self, self.user_id, self.auth_sid, self.token)
            Assertions.assert_json_value_by_name(
                self.response4,
                "firstName",
                new_name,
                "Wrong name of the user after edit"
            )
        elif condition == "change_name_to_1_char":
            new_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(1))

            MyFun.edit(self, new_name, self.user_id, self.auth_sid, self.token)
            Assertions.assert_code_status(self.response3, 400)
            expected_content={"error":"Too short value for field firstName"}
            Assertions.assert_decode_as_json(self.response3, "error", expected_content, f"No {expected_content} in response")

            MyFun.get_user(self, self.user_id, self.auth_sid, self.token)
            Assertions.assert_json_value_by_name(
                self.response4,
                "firstName",
                self.first_name,
                "Wrong name of the user after edit"
            )



#   Попытаемся изменить данные пользователя, будучи неавторизованными
    @allure.description(f"This test change just created user first name without auth")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user_no_auth(self):
        MyFun.register(self)

        new_name = "Changed Name"
        MyFun.edit(self, new_name, self.user_id, "", "")
        Assertions.assert_code_status(self.response3, 400)

        MyFun.login(self, self.email, self.password)
        MyFun.get_user(self, self.user_id, self.auth_sid, self.token)
        expected_content={"id":f"{self.user_id}","username":"learnqa","email":f"{self.email}","firstName":"learnqa","lastName":"learnqa"}
        obj_json = json.loads(self.response4.content.decode("utf-8"))
        assert obj_json == expected_content, f"Request decoded JSON is not the same with expected_content. There is {obj_json}"

#    Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    @allure.description(f"This test change just created user first name from another user")
    @pytest.mark.xfail(condition=lambda: True, reason='Expected no one changes his name')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user_as_another_user(self):
        MyFun.register(self)
        email_1 = self.email
        first_name_1 = self.first_name
        password_1 = self.password
        user_id_1 = self.user_id

        time.sleep(3)

        MyFun.register(self)
        email_2 = self.email
        first_name_2 = self.first_name
        password_2 = self.password
        user_id_2 = self.user_id

        MyFun.login(self, email_1, password_1)
        auth_sid_1 = self.auth_sid
        token_1 = self.token

        new_name = "Changed Name"
        MyFun.edit(self, new_name, user_id_2, auth_sid_1, token_1)
        Assertions.assert_code_status(self.response3, 200)

        MyFun.get_user(self, user_id_1, auth_sid_1, token_1)
        expected_content = {"id": f"{user_id_1}", "username": "learnqa", "email": f"{email_1}",
                            "firstName": f"{new_name}", "lastName": "learnqa"}
        Assertions.assert_decode_as_json(self.response4, "firstName", expected_content,
                                         f"Request decoded JSON is not the same with expected_content.")

        MyFun.login(self, email_2, password_2)
        auth_sid_2 = self.auth_sid
        token_2 = self.token

        MyFun.get_user(self, user_id_2, auth_sid_2, token_2)
        expected_content = {"id": f"{user_id_2}", "username": "learnqa", "email": f"{email_2}",
                            "firstName": "learnqa", "lastName": "learnqa"}
        Assertions.assert_decode_as_json(self.response4, "firstName", expected_content, f"Request decoded JSON is not the same with expected_content.")

#       Name changes for first

    @allure.description(f"This test change just created user email to email without '@'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_just_created_user_as_same_user_without_at(self):

        MyFun.register(self)
        email_1 = self.email

        MyFun.login(self, self.email, self.password)

        new_email= email_1.replace('@', '')
        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_content_decode(response3, "Invalid email format")

        MyFun.get_user(self, self.user_id, self.auth_sid, self.token)
        expected_content={"id":f"{self.user_id}","username":"learnqa","email":f"{email_1}","firstName":"learnqa","lastName":"learnqa"}
        obj_json = json.loads(self.response4.content.decode("utf-8"))
        assert obj_json == expected_content, f"Request decoded JSON is not the same with expected_content. There is {obj_json}"





