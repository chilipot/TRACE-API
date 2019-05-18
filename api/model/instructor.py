from sqlalchemy import Column, Integer, Unicode

from api.model.mixins import InstructorSearchable, Base, Dictable


class Instructor(Base, Dictable, InstructorSearchable):
    __tablename__ = 'instructor'

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(100))
    last_name = Column(Unicode(100))
    middle_name = Column(Unicode(100))

    @property
    def full_name(self):
        return ' '.join(filter(lambda x: x is not None and x.strip(),
                               [self.first_name, self.last_name]))
