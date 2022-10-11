from models import TokenModel
import models.tokens as model_token
from models.users import get_user_by_id
import functools
from hmac import compare_digest
from flask import request, session
import generate_response


def is_valid(api_key):
    device: TokenModel = model_token.get_by_key(api_key)
    session["user_id"] = 1  # TODO TEST для Postman

    return (
        device
        and compare_digest(device.domain_key, api_key)
        and session["user_id"]
        and session["user_id"] == device.user_id
    )


def api_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.json:
            api_key: str = request.json.get("api_key")
        else:
            return generate_response.not_api_key_error(400)
        if is_valid(api_key):
            return func(*args, **kwargs)
        else:
            return generate_response.not_valid_api_key(403)

    return decorator
