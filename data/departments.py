import sqlalchemy
from sqlalchemy import Column
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer.serializer import SerializerMixin
from data.users import User
from data.db_session import create_session


class Department(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'departments'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = Column(sqlalchemy.String)
    chief = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    members = Column(sqlalchemy.String)
    email = Column(sqlalchemy.String, unique=True)

    def __repr__(self):
        return f'<Department> {self.id} {self.title}'

    def values(self):
        session = create_session()
        chief = session.query(User).filter(User.id == self.chief)[0]
        chief = chief.surname + ' ' + chief.name + ' (' + chief.position + ')'
        members = []
        for member in self.members.split(','):
            members.append(session.query(User).filter(User.id == member).first().fio())

        return [self, self.title, chief, self.email, ', '.join(map(str, members))][:]
