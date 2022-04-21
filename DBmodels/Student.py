import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Student(SqlAlchemyBase):
    __tablename__ = 'Students'

    Id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Users.Id"),
                           primary_key=True)
    ClassId = sqlalchemy.Column(sqlalchemy.Integer)

    user = orm.relationship("User", back_populates="students")
