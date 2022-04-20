import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class ClassTeachers(SqlAlchemyBase):
    __tablename__ = 'Tasks'

    ClassId = sqlalchemy.Column(sqlalchemy.Integer)
    TeacherId = sqlalchemy.Column(sqlalchemy.Integer)

    class_teacher = orm.relation("ClassTeacher")
