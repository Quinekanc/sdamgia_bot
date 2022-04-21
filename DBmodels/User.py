import sqlalchemy
from sqlalchemy import orm

from .DbConnection import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'Users'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    IsTeacher = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    ClassId = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
