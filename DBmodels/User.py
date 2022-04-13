import sqlalchemy
from sqlalchemy import orm

from .DbConnection import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'Users'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    If_Teacher = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    Tasks = orm.relation("Task", back_populates='User')
