from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy import Column as Col
from data.db_session import SqlAlchemyBase, create_session
from data.users import User


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = Col(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = Col(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    job = Col(sqlalchemy.String)
    work_size = Col(sqlalchemy.Integer)
    collaborators = Col(sqlalchemy.String)
    start_date = Col(sqlalchemy.DateTime, default=datetime.now)
    end_date = Col(sqlalchemy.DateTime, default=lambda: datetime.now() + timedelta(days=1))
    is_finished = Col(sqlalchemy.Boolean)

    def values(self, session):
        leader = session.query(User).filter(User.id == self.team_leader)[0]
        leader = leader.surname + ' ' + leader.name + ' (' + leader.position + ')'
        work_size = str(self.work_size) + [' hours', ' hour'][self.work_size == 1]
        is_finished = ["Is not finished", "Is finished"][self.is_finished]

        return [self.job, leader, work_size, self.collaborators, is_finished][:]

    def __repr__(self):
        return f'<Job #{self.id}> {self.job}'
