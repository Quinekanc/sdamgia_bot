import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class ClassTask(SqlAlchemyBase):
    __tablename__ = 'ClassTasks'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    ClassId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Classes.Id"))

    TeacherId = sqlalchemy.Column(sqlalchemy.Integer)
    TaskId = sqlalchemy.Column(sqlalchemy.Integer)

    SubjectId = sqlalchemy.Column(sqlalchemy.String)
