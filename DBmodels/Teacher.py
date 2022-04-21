import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Teacher(SqlAlchemyBase):
    __tablename__ = 'Teachers'

    Id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Users.Id"), primary_key=True)

    user = orm.relationship("User", back_populates="teachers")
