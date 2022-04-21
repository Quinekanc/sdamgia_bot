import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Task(SqlAlchemyBase):
    __tablename__ = 'Tasks'

    Id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    TaskId = sqlalchemy.Column(sqlalchemy.Integer)
    Topic = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    StudentId = sqlalchemy.Column(sqlalchemy.Integer)
    SubjectId = sqlalchemy.Column(sqlalchemy.String)

    ClassTaskId = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    Result = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

