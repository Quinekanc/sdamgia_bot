import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Class(SqlAlchemyBase):
    __tablename__ = 'Classes'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    ClassName = sqlalchemy.Column(sqlalchemy.String)
    Tasks = orm.relationship("ClassTasks")
