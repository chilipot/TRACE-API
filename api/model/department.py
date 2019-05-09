from sqlalchemy import Column, Integer, Unicode

from api.model.mixins import DepartmentSearchable, Base, Dictable


class Department(Base, Dictable, DepartmentSearchable):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    code = Column(Unicode(10))
    title = Column(Unicode(100))
