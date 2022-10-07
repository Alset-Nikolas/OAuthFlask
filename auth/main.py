from flask import Flask, render_template, request, redirect, session
import typing
from auth.models import UserModel

from multiple_oauth.oauth import OAuthSignIn
from multiple_oauth.auth_vk import VkSignIn
from multiple_oauth.auth_github import GithubSignIn
from multiple_oauth.auth_yandex import YandexSignIn
from multiple_oauth.auth_tel import get_token, SMSTransport, TSMSResponse

from db import init_db
import models.users as model_users
import schemas.user as schemas_user

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


# --------------- TELEPHONE api ------------------
@app.route("/send_sms", methods=["GET", "POST"])
def send_sms():
    code: str = get_token()
    tel: str = request.form.get("phone")
    session["tel"] = tel
    sms: SMSTransport = SMSTransport(app.config["TOKEN_TEL"])
    result: TSMSResponse = sms.send(tel, code)
    return redirect("/check_tel")


@app.route("/check_tel", methods=["GET", "POST"])
def registration_tel():
    code: str = get_token()
    if request.method == "POST":
        if request.form.get("token") == code:
            model_users.update_user({"tel": session["tel"]}, "tel")
            return "OK"
        return render_template(f"auth_tel/check_token.html", er="Неправильный токен")
    return render_template(f"auth_tel/check_token.html")


@app.route("/authorize/<provider>")
def oauth_authorize(provider):
    oauth: TYPE_OAUTH = OAuthSignIn.get_provider(provider)
    return oauth.authorize(), 301


@app.route("/callback/<provider>")
def oauth_callback(provider):
    oauth: TYPE_OAUTH = OAuthSignIn.get_provider(provider)
    user_data: typing.Dict = oauth.callback()
    if user_data:
        session["user_id"]: int = model_users.update_user(user_data, provider)
        return render_template(f"{provider}_auth.html", userData=user_data)
    return redirect(f"/authorize/{provider}")


@app.route("/api/user/get/<int:id>")
def get_user(id):
    user: UserModel = model_users.get_user_by_id(id)
    schema: schemas_user.UserSchema = schemas_user.UserSchema()
    if user:
        return schema.dump(user), 200
    return {"code": 404, "message": "User not found"}, 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
