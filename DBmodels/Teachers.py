import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Teacher(SqlAlchemyBase):
    __tablename__ = 'Teachers'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer)
    teacher = orm.relation("Teacher", back_populates="Class")
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Classes.Id"), nullable=True)
