from marshmallow import Schema, fields, pprint
from models import UserModel


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
