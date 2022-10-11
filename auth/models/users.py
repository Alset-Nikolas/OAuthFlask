import typing
from models import UserModel, session
from log import logger
from dataclass.user import UserInfo


def get_user_by_phone(tel: str) -> typing.Optional[UserModel]:
    return session.query(UserModel).filter(UserModel.phone == tel).first()


def get_user_by_id(id: int) -> typing.Optional[UserModel]:
    return session.query(UserModel).filter(UserModel.id == id).first()


def update_user(user_data: UserInfo, provider: str) -> int:
    logger.info(f"update_user user={user_data}, provider={provider}")
    user_db = get_user_by_phone(user_data.phone)
    if user_db:
        user_db.email = user_data.email or user_db.email
        user_db.login = user_data.login or user_db.login
        user_db.first_name = user_data.first_name or user_db.first_name
        user_db.last_name = user_data.last_name or user_db.last_name
    else:
        user_db = UserModel(
            email=user_data.email,
            phone=user_data.phone,
            login=user_data.login,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
    session.add(user_db)
    session.commit()
    return user_db.id
