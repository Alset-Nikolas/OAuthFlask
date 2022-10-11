from flask import Flask, render_template, request, session
import typing
from models import UserModel, TokenModel
from multiple_oauth.oauth import OAuthSignIn, RottenTokenError
from multiple_oauth.auth_yandex import YandexSignIn
from db import init_db
import models.users as model_users
import models.tokens as model_token
import schemas.user as schemas_user
from dataclass.user import UserInfo
import generate_response
from flask_jwt import JWT
from security import api_required

app = Flask(__name__)

app.config["SECRET_KEY"] = "top secret!"
app.config["OAUTH_CREDENTIALS"] = {
    "yandex": {
        "id": "13f79c998f1b451abfc569b829a87fe9",
        "secret": "2c06214f5d224cd48e0ff8b583ada4f9",
    },
}

TYPE_OAUTH = YandexSignIn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/authorize/<provider>")
def oauth_authorize(provider: str):
    """
    Перенапрвить пользователя авторизоваться через провайдер (например яндекс)
    """
    if provider not in app.config["OAUTH_CREDENTIALS"]:
        return generate_response.provider_not_exist_error(provider, 404)
    oauth: TYPE_OAUTH = OAuthSignIn.get_provider(provider)
    return oauth.authorize(), 301


@app.route("/callback/<provider>")
def oauth_callback(provider: str):
    """
    После авторизации (через провайдер), провайдер перенаправит пользователя на этот url
    """
    if provider not in app.config["OAUTH_CREDENTIALS"]:
        return generate_response.provider_not_exist_error(provider, 404)
    try:
        oauth: TYPE_OAUTH = OAuthSignIn.get_provider(provider)
        user_data: typing.Dict = oauth.callback()
        if not user_data:
            raise RottenTokenError("user code not exist")
    except KeyError as er_settings:
        return generate_response.settings_provider_error(provider, 501, er_settings)
    except RottenTokenError as redirect_cause:
        return generate_response.redirect_to_authorize(
            provider, 301, str(redirect_cause)
        )

    schema: schemas_user.UserSchema = schemas_user.UserSchema()
    try:
        user_info: UserInfo = schema.load(user_data)
    except KeyError as er_info_person:
        generate_response.provider_access_error(provider, 505, er_info_person)

    session["user_id"]: int = model_users.update_user(user_info, provider)
    return render_template(f"{provider}_auth.html", userData=user_info)


@app.route("/api/get/user/<int:id>")
def get_user(id):
    user: UserModel = model_users.get_user_by_id(id)
    schema: schemas_user.UserSchema = schemas_user.UserSchema()
    if not user:
        return generate_response.user_not_exist_error(id, 404)
    return schema.dump(user), 200


@app.route("/api/get/user/add-site")
def add_new_client():
    data: dict = request.args
    user_id: int = session["user_id"]
    if "domain_name" not in data:
        return generate_response.not_param_domain_name_error(401)

    domain_name: str = data["domain_name"]
    if model_token.get_by_name(domain_name):
        return generate_response.domain_name_error(402, domain_name)
    if model_users.get_user_by_id(user_id):
        new_token: TokenModel = model_token.create_new_device(domain_name, user_id)
        return generate_response.get_api_key_user(
            201, new_token.domain_key, domain_name
        )
    return generate_response.redirect_to_authorize("yandex", 301, "user not auth")


@app.route("/probe")
@api_required
def probe():
    return {"code": 200}, 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
