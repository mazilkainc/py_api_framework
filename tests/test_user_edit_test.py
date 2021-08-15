import requests
import json
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.fun import MyFun
import time

class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
#       Look at lib/fun.py
        MyFun.register(self)

        MyFun.login(self, self.email, self.password)

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

#   Попытаемся изменить данные пользователя, будучи неавторизованными
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

    def test_test(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email_1 = register_data['email']
        first_name_1 = register_data['firstName']
        password_1 = register_data['password']
        user_id_1 = self.get_json_value(response1, "id")

        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email_2 = register_data['email']
        first_name_2 = register_data['firstName']
        password_2 = register_data['password']
        user_id_2 = self.get_json_value(response1, "id")

        print(user_id_1, user_id_2)





