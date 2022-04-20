import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Subject(SqlAlchemyBase):
    __tablename__ = 'Subjects'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    Name = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("Task.Subject"))
