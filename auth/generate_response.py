from log import logger


def provider_not_exist_error(provider: str, code: int):
    logger.error(f"provider '{provider}' not exist in app.config")
    return {
        "code": code,
        "message": f"provider '{provider}' not exist",
    }, code


def settings_provider_error(provider: str, code: int, er_text: str):
    logger.error(f"Problem in settings app provider '{provider}'. Detail: '{er_text}'")
    return {
        "code": code,
        "error": f"settings_provider_error",
        "provider": provider,
        "message": "Check settings yandex app: Domain URL, Callback URL, Client ID, Client secret",
    }, code


def redirect_to_authorize(provider: str, code: int, redirect_cause: str):
    logger.info(f"user redirect /authorize/{provider}: '{redirect_cause}'")
    return {
        "code": code,
        "provider": provider,
        "message": redirect_cause,
        "uri_redirect": f"/authorize/{provider}",
    }, code


def provider_access_error(provider: str, code: int, er_info_person: str):
    logger.error(
        f"User info in provider not correct: user_data. Detail: '{er_info_person}'"
    )
    return {
        "code": code,
        "error": "provider_access_error",
        "provider": provider,
        "message": "Check access settings yandex app: email, login, tel",
    }, code


def user_not_exist_error(id: int, code: int):
    logger.error(f"User not exist. id = '{id}'")
    return {
        "code": code,
        "error": "user_not_exist",
        "user_id": id,
        "message": "User not found by id",
    }, code


def not_api_key_error(code: int):
    logger.error("User not provide API key")
    return {
        "code": code,
        "error": "not_key_api",
        "message": "Please provide an API key",
    }, code


def not_valid_api_key(code: int):
    logger.error("The provided API key is not valid")
    return {
        "code": code,
        "error": "not_key_api",
        "message": "The provided API key is not valid",
    }, code


def not_param_domain_name_error(code: int):
    logger.error("lost parameter 'domain_name' - your website domain")
    return {
        "code": code,
        "error": "not_param_domain_name",
        "message": "lost parameter 'domain_name' - your website domain",
    }, code


def domain_name_error(code: int, domain_name: str):
    logger.error(f"A domain name '{domain_name}' already used")
    return {
        "code": code,
        "error": "not_param_domain_name",
        "message": f"A domain name '{domain_name}' already used.",
    }, code


def get_api_key_user(code: int, domain_key: str, domain_name: str):
    logger.error(f"token add domain '{domain_name}'")
    return {
        "code": code,
        "api_key": domain_key,
        "domain_name": domain_name,
    }, code
