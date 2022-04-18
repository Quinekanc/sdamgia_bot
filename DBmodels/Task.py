import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Task(SqlAlchemyBase):
    __tablename__ = 'Tasks'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    TaskId = sqlalchemy.Column(sqlalchemy.Integer)
    Topic = sqlalchemy.Column(sqlalchemy.Integer)
    User_Id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Users.Id"))
    Subject_Name = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("Subjects.Name"))
    User = orm.relation('User')
    Subject = orm.relation('Subject')
