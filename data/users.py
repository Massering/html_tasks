from werkzeug.security import generate_password_hash, check_password_hash

import datetime
import sqlalchemy
from sqlalchemy_serializer.serializer import SerializerMixin
from flask_login import UserMixin
from sqlalchemy import Column
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = Column(sqlalchemy.String)
    name = Column(sqlalchemy.String)
    age = Column(sqlalchemy.Integer)
    position = Column(sqlalchemy.String)
    speciality = Column(sqlalchemy.String)
    address = Column(sqlalchemy.String)
    city_from = Column(sqlalchemy.String)
    email = Column(sqlalchemy.String, unique=True)
    hashed_password = Column(sqlalchemy.String)
    modified_date = Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<Colonist> {self.id} {self.surname} {self.name}'

    def fio(self):
        return self.surname + ' ' + self.name

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
