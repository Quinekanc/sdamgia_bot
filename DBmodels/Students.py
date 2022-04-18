import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Students(SqlAlchemyBase):
    __tablename__ = 'Students'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    class_name = sqlalchemy.Column(sqlalchemy.String)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Teachers.Id"))
    student_id = sqlalchemy.Column(sqlalchemy.Integer)
