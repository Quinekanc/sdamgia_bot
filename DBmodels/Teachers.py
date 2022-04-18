import sqlalchemy
from .DbConnection import SqlAlchemyBase
from sqlalchemy import orm


class Teachers(SqlAlchemyBase):
    __tablename__ = 'Teachers'

    Id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    class_num = sqlalchemy.Column(sqlalchemy.Integer)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer)
