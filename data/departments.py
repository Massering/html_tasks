import sqlalchemy
from sqlalchemy import Column, orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer.serializer import SerializerMixin


class Department(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'departments'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = Column(sqlalchemy.String)
    chief = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    members = Column(sqlalchemy.String)
    email = Column(sqlalchemy.String, unique=True)

    def __repr__(self):
        return f'<Department> {self.id} {self.title}'
