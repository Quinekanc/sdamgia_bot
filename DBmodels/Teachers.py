import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Teacher(SqlAlchemyBase):
    __tablename__ = 'Teachers'

    Id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("ClassTeacher.TeacherId"))

    teacher = orm.relation("Teacher")
