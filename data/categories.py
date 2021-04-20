import sqlalchemy
from sqlalchemy import Column
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer.serializer import SerializerMixin


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'categories'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = Column(sqlalchemy.String, unique=True)

    def __repr__(self):
        return f'<Category #{self.id}> {self.name}'
