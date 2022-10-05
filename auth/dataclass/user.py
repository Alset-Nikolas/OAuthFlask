from dataclasses import dataclass
import typing

@dataclass
class UserInfo:
    login: typing.Optional[str]
    phone: str
    email: typing.Optional[str]

    @classmethod
    def get_user_obj_for_row(cls, row):
        return cls(row[0], row[1], row[2])

    def __str__(self):
        return f'<UserInfo: login: {self.login}, phone:{self.phone}, email:{self.email}>'