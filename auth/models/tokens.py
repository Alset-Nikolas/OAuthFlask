from models import TokenModel, UserModel, session


def create_new_device(domain_name, user_id):
    new_token = TokenModel(domain_name=domain_name, user_id=user_id)
    new_token.save_to_db()
    return new_token


def get_by_name(domain_name):
    return (
        session.query(TokenModel).filter(TokenModel.domain_name == domain_name).first()
    )


def get_by_key(api_key):
    return session.query(TokenModel).filter(TokenModel.domain_key == api_key).first()
