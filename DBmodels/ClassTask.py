import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class ClassTask(SqlAlchemyBase):
    __tablename__ = 'ClassTasks'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    ClassId = sqlalchemy.Column(sqlalchemy.Integer)
    TeacherId = sqlalchemy.Column(sqlalchemy.Integer)
    TaskId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Tasks.ClassTaskId"))
