import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Students(SqlAlchemyBase):
    __tablename__ = 'Students'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    class_num = sqlalchemy.Column(sqlalchemy.Integer)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Teachers.Id"))
    student_id = sqlalchemy.Column(sqlalchemy.Integer)
