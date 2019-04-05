from sqlalchemy import Column, String, Integer, Date

from base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone