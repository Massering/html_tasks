from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy import Column, orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer.serializer import SerializerMixin
from data.users import User


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    job = Column(sqlalchemy.String)
    work_size = Column(sqlalchemy.Integer)
    collaborators = Column(sqlalchemy.String)
    start_date = Column(sqlalchemy.DateTime, default=datetime.now)
    end_date = Column(sqlalchemy.DateTime, default=lambda: datetime.now() + timedelta(days=1))
    is_finished = Column(sqlalchemy.Boolean, default=False)

    def values(self, session):
        leader = session.query(User).filter(User.id == self.team_leader)[0]
        leader = leader.surname + ' ' + leader.name + ' (' + leader.position + ')'
        work_size = str(self.work_size) + [' hours', ' hour'][self.work_size == 1]
        is_finished = ["Is not finished", "Is finished"][self.is_finished]

        return [self.job, leader, work_size, self.collaborators, is_finished][:]

    def __repr__(self):
        return f'<Job #{self.id}> {self.job}'
