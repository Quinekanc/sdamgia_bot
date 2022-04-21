import sqlalchemy
from sqlalchemy import orm

from .DbConnection import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'Users'

    Id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Students.Id"), primary_key=True)

    teachers = orm.relationship("Teacher")
    students = orm.relationship("Student")
