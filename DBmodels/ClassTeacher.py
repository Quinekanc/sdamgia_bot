import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class ClassTeacher(SqlAlchemyBase):
    __tablename__ = 'ClassTeachers'
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    ClassId = sqlalchemy.Column(sqlalchemy.Integer)
    TeacherId = sqlalchemy.Column(sqlalchemy.Integer)
