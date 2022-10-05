from models import UserModel, session
import datetime
from log import logger
from dataclass.user import UserInfo


def get_user_by_phone(tel):
    return session.query(UserModel).filter(UserModel.phone==tel).first()

def update_user(user_data, provider):
    logger.info(f'update_user user={user_data}, provider={provider}')
    login, email, phone = None, None, None

    if provider == 'yandex':
        if 'default_email' in user_data:
            email = user_data['default_email']

        if 'login' in user_data:
            login = user_data['login']

        if 'default_phone' in user_data:
            phone = user_data['default_phone']['number']
        
    if provider == 'tel':
        phone = user_data['tel']

    user = UserInfo.get_user_obj_for_row([login, phone, email])
    user_db = get_user_by_phone(user.phone)
    if user_db:
        user_db.email = user.email
        user_db.login = user.login
    else:
        user_db = UserModel(
            email=user.email,
            phone=user.phone,
            login=user.login,
        )
    session.add(user_db)
    session.commit()
