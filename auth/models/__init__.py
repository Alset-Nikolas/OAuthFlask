from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Integer, Column, create_engine, String, DateTime, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.operators import op
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import composite, relationship
import datetime
import uuid

DATABASE = {
    "drivername": "postgresql",
    # "host": "postgres",
    "host": "localhost",
    "port": "5432",
    "username": "postgres",
    "password": "qwerty",
    "database": "oauth_users",
}
Base = declarative_base()
engine = create_engine(
    f'postgresql+psycopg2://{DATABASE["username"]}:{DATABASE["password"]}@{DATABASE["host"]}:{DATABASE["port"]}/{DATABASE["database"]}'
)


session = Session(bind=engine)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)

    email = Column(EmailType)
    phone = Column(String, nullable=False)
    login = Column(String)
    date_login = Column(DateTime, default=datetime.datetime.utcnow)
    tokens = relationship("TokenModel", back_populates="user")


class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    domain_name = Column(String(80))
    domain_key = Column(String(80))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="tokens")

    def __init__(self, domain_name, user_id, domain_key=None):
        self.domain_name = domain_name
        self.user_id = user_id
        self.domain_key = domain_key or uuid.uuid4().hex

    def __str__(self) -> str:
        return f"<TokenModel id={self.id}, domain_name={self.domain_name}>"

    def json(self):
        return {
            "domain_name": self.domain_name,
            "domain_key": self.domain_key,
            "user_id": self.user_id,
        }

    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()
