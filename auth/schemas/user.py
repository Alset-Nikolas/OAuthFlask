from marshmallow import Schema, pre_load, post_load
from models import UserModel
from dataclass.user import UserInfo


class UserSchema(Schema):
    class Meta:
        model = UserModel
        # Fields to expose
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "login",
            "date_login",
        )

    @pre_load
    def create_user_info(self, all_info_user: dict, **kwargs):
        info_user = dict()
        info_user["email"] = all_info_user["default_email"]
        info_user["login"] = all_info_user["login"]
        info_user["phone"] = all_info_user["default_phone"]["number"]
        info_user["first_name"] = all_info_user["first_name"]
        info_user["last_name"] = all_info_user["last_name"]
        return info_user

    @post_load
    def get_user_info(self, info_user, **kwargs):
        return UserInfo.get_user_obj_for_dict(info_user)
