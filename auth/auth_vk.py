from rauth import OAuth2Service
from flask import request, redirect
from oauth import OAuthSignIn
import json
import requests
import typing


class VkSignIn(OAuthSignIn):
    def __init__(self):
        super(VkSignIn, self).__init__("vk")
        self.service = OAuth2Service(
            name="vk",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://oauth.vk.com/authorize",
            access_token_url="https://oauth.vk.com/access_token",
            base_url="https://api.vk.com/method/users.get",
        )

    def authorize(self):
        """
        Запрос к сервису для авторизации пользователя
        """
        return redirect(
            self.service.get_authorize_url(
                scope="email",
                response_type="code",
                redirect_uri=self.get_callback_url(),
            )
        )

    def callback(self) -> typing.Optional[typing.Dict]:
        """
        Запрос к API сервиса о информации про пользователя
        """

        if "code" not in request.args:
            return

        data: typing.Dict = self.get_access_token(code=request.args["code"])

        if "access_token" not in data:
            return
        try:
            user_info: typing.Dict = self.vk_auth(data["access_token"])
            return user_info
        except BaseException:
            return

    def get_access_token(self, code: str) -> requests.Response:
        get_token = "https://oauth.vk.com/access_token"
        token_param = {
            "client_id": self.service.client_id,
            "client_secret": self.service.client_secret,
            "redirect_uri": self.get_callback_url(),
            "code": code,
        }
        request = requests.post(url=get_token, data=token_param)
        if request.status_code != 200:
            return {}

        response = json.loads(request.text.replace("\\", ""))
        return response

    def vk_auth(self, access_token: str) -> typing.Dict:
        auth = "https://api.vk.com/method/users.get"
        auth_param = {
            "fields": "uid,login,first_name,last_name,screen_name,has_mobile,bdate,photo_max_orig,mail,email",
            "access_token": access_token,
            "scope": "email,offline",
            "v": 5.124,
        }
        response = requests.post(url=auth, data=auth_param)
        s = json.loads(response.content)
        data = s["response"][0]
        return data


#
