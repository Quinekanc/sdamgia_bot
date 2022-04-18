import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Class(SqlAlchemyBase):
    __tablename__ = 'Classes'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    class_num = sqlalchemy.Column(sqlalchemy.Integer)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Teachers.Id"))
    task_for_class = sqlalchemy.Column(sqlalchemy.String)
