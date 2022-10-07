from rauth import OAuth2Service
from flask import request, redirect
from multiple_oauth.oauth import OAuthSignIn
import json


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__("yandex")
        self.service = OAuth2Service(
            name="yandex",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://oauth.yandex.ru/authorize",
            access_token_url="https://oauth.yandex.ru/token",
            base_url="https://login.yandex.ru/info",
        )

    def authorize(self):
        return redirect(
            self.service.get_authorize_url(
                response_type="code",
                client_id=self.service.client_id,
            )
        )

    def callback(self):
        def parse_args(s):
            return json.loads(s)

        if "code" not in request.args:
            return None

        data = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": self.get_callback_url(),
        }

        oauth_session = self.service.get_auth_session(data=data, decoder=parse_args)

        user_info = oauth_session.get(
            self.service.base_url, params={"FieldNames": ["Login"]}
        ).json()
        return user_info
