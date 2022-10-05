from flask import current_app, url_for
import typing


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name) -> None:
        self.provider_name: str = provider_name
        credentials: typing.Dict = current_app.config["OAUTH_CREDENTIALS"][
            provider_name
        ]
        self.consumer_id: str = credentials["id"]
        self.consumer_secret: str = credentials["secret"]

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self) -> str:
        return url_for("oauth_callback", provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(self, provider_name) -> "OAuthSignIn":
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]
