from datetime import datetime, timedelta

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy_serializer.serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from data.users import User
from data.categories import Category
from data.db_session import create_session


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    job = Column(sqlalchemy.String)
    work_size = Column(sqlalchemy.Integer)
    collaborators = Column(sqlalchemy.String)
    category = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
    start_date = Column(sqlalchemy.DateTime, default=datetime.now)
    end_date = Column(sqlalchemy.DateTime, default=lambda: datetime.now() + timedelta(days=1))
    is_finished = Column(sqlalchemy.Boolean, default=False)

    def values(self):
        session = create_session()

        leader = session.query(User).filter(User.id == self.team_leader)[0]
        leader = leader.surname + ' ' + leader.name + ' (' + leader.position + ')'

        work_size = str(self.work_size) + [' hours', ' hour'][self.work_size == 1]

        collaborators = []
        for collaborator in self.collaborators.split(','):
            collaborators.append(session.query(User).filter(User.id == collaborator).first().fio())

        category = session.query(Category).filter(Category.id == self.category).first().name

        is_finished = ["Is not finished", "Is finished"][self.is_finished]

        return [self, self.job, leader, work_size, ', '.join(map(str, collaborators)), category, is_finished]

    def __repr__(self):
        return f'<Job #{self.id}> {self.job} {self.team_leader}'
