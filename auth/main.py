from flask import Flask, render_template, request
from oauth import OAuthSignIn
from auth_vk import VkSignIn
from auth_github import GithubSignIn
from auth_yandex import YandexSignIn
import typing

app = Flask(__name__)
app.config["SECRET_KEY"] = "top secret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["OAUTH_CREDENTIALS"] = {
    "github": {
        "id": "d0219664ea47d1e305f7",
        "secret": "4ca8560f15a17a3b2cffe809d4e8ead67f9e7df9",
    },
    "vk": {"id": "51438467", "secret": "lv0J9qcamPfHKZqBbu1v"},
    "yandex": {
        "id": "45f35df07eac4dcdb497852a0c101588",
        "secret": "3323a7456028481c9babb644928c6186",
    },
}

TYPE_OAUTH = typing.Union[YandexSignIn, VkSignIn, GithubSignIn]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/authorize/<provider>")
def oauth_authorize(provider):
    oauth: TYPE_OAUTH = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route("/callback/<provider>")
def oauth_callback(provider):
    oauth: TYPE_OAUTH = OAuthSignIn.get_provider(provider)
    userData: typing.Dict = oauth.callback()
    return render_template(f"{provider}_auth.html", userData=userData)


if __name__ == "__main__":
    app.run(debug=True)
