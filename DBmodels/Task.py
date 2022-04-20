import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Task(SqlAlchemyBase):
    __tablename__ = 'Tasks'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    TaskId = sqlalchemy.Column(sqlalchemy.Integer)
    Topic = sqlalchemy.Column(sqlalchemy.Integer)
    StudentId = sqlalchemy.Column(sqlalchemy.Integer)
    SubjectName = sqlalchemy.Column(sqlalchemy.String)
    ClassTaskId = sqlalchemy.Column(sqlalchemy.Integer)
    Result = sqlalchemy.Column(sqlalchemy.Integer)

    Task = orm.relation("Task")
