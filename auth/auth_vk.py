from rauth import OAuth2Service
from flask import request, redirect
from oauth import OAuthSignIn
import json
import requests


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
        return redirect(
            self.service.get_authorize_url(
                scope="email",
                response_type="code",
                redirect_uri=self.get_callback_url(),
            )
        )

    def callback(self):

        if "code" not in request.args:
            return None

        data = self.get_access_token(code=request.args["code"])
        user_info = self.vk_auth(data["access_token"])
        return user_info

    def get_access_token(self, code):
        get_token = "https://oauth.vk.com/access_token"
        token_param = {
            "client_id": self.service.client_id,
            "client_secret": self.service.client_secret,
            "redirect_uri": self.get_callback_url(),
            "code": code,
        }
        request = requests.post(url=get_token, data=token_param)
        response = json.loads(request.text.replace("\\", ""))
        return response

    def vk_auth(self, access_token):
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
