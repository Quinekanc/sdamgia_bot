import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Class(SqlAlchemyBase):
    __tablename__ = 'Classes'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    class_name = sqlalchemy.Column(sqlalchemy.String)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Teachers.Id"), nullable=True)
    task_for_class = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    main_class = orm.relation("Class")
