import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Students(SqlAlchemyBase):
    __tablename__ = 'Students'

    Id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Task.StudentId"))
    ClassId = sqlalchemy.Column(sqlalchemy.Integer)

    student = orm.relation("Student")
