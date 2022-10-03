from crypt import methods
from flask import Flask, render_template, request, redirect
from oauth import OAuthSignIn
from auth_vk import VkSignIn
from auth_github import GithubSignIn
from auth_yandex import YandexSignIn
import typing
from auth_tel import get_token, SMSTransport, TSMSResponse


app = Flask(__name__)
app.config["SECRET_KEY"] = "top secret!"
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
app.config["TOKEN_TEL"] = "E021CCF2-76F5-08B8-FD88-1D7FE93C87C6"
TYPE_OAUTH = typing.Union[YandexSignIn, VkSignIn, GithubSignIn]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send_sms", methods=["GET", "POST"])
def send_sms():
    code: str = get_token()
    tel: str = request.form.get("phone")
    sms: SMSTransport = SMSTransport(app.config["TOKEN_TEL"])
    result: TSMSResponse = sms.send(tel, code)
    return redirect("/check_tel")


@app.route("/check_tel", methods=["GET", "POST"])
def registration_tel():
    code: str = get_token()
    if request.method == "POST":
        if request.form.get("token") == code:
            return "OK"
        return render_template(f"auth_tel/check_token.html", er="Неправильный токен")
    return render_template(f"auth_tel/check_token.html")


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
