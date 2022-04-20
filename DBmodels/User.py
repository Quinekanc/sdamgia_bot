import sqlalchemy
from sqlalchemy import orm

from .DbConnection import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'Users'

    Id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Student.Id"), primary_key=True)

    user = orm.relation("User")
