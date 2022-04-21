import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm
from .User import User


class ClassTeacher(SqlAlchemyBase):
    __tablename__ = 'ClassTeachers'
    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    ClassId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Classes.Id"))

    TeacherId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Users.Id"))
    Teacher: User = orm.relationship("User", back_populates="classes")
