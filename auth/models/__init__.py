from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import (
    Integer,
    Column,
    create_engine,
    String,
    DateTime,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.operators import op
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import composite
import datetime

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
    phone = Column(String)
    login = Column(String)
    date_login = Column(DateTime, default=datetime.datetime.utcnow)
