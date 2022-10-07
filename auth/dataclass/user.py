from dataclasses import dataclass
import typing


@dataclass
class UserInfo:
    login: typing.Optional[str]
    phone: str
    email: typing.Optional[str]
    first_name: typing.Optional[str]
    last_name: typing.Optional[str]

    @classmethod
    def get_user_obj_for_dict(cls, info: typing.DefaultDict):
        return cls(**info)

    def __str__(self):
        return (
            f"<UserInfo: login: {self.login}, phone:{self.phone}, email:{self.email}>"
        )
