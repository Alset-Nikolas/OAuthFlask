import collections
import typing
from models import UserModel, session
import datetime
from log import logger
from dataclass.user import UserInfo


def get_user_by_phone(tel):
    return session.query(UserModel).filter(UserModel.phone == tel).first()


def get_user_by_id(id: int) -> typing.Optional[UserModel]:
    return session.query(UserModel).filter(UserModel.id == id).first()


def update_user(user_data, provider):
    logger.info(f"update_user user={user_data}, provider={provider}")
    user_info = collections.defaultdict()
    if provider == "yandex":
        user_info["email"] = user_data["default_email"]
        user_info["login"] = user_data["login"]
        user_info["phone"] = user_data["default_phone"]["number"]
        user_info["first_name"] = user_data["first_name"]
        user_info["last_name"] = user_data["last_name"]
    if provider == "tel":
        phone = user_data["tel"]

    user = UserInfo.get_user_obj_for_dict(user_info)
    user_db = get_user_by_phone(user.phone)
    if user_db:
        user_db.email = user.email or user_db.email
        user_db.login = user.login or user_db.login
        user_db.first_name = user.first_name or user_db.first_name
        user_db.last_name = user.last_name or user_db.last_name
    else:
        user_db = UserModel(
            email=user.email,
            phone=user.phone,
            login=user.login,
            first_name=user.first_name,
            last_name=user.last_name,
        )
    session.add(user_db)
    session.commit()
    return user_db.id
