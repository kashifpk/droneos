from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, Unicode, UnicodeText, Float

from . import db, Base


class Route(Base):

    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    description = Column(UnicodeText)


class Point(Base):

    __tablename__ = 'points'

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey(Route.id))
    idx = Column(Integer, nullable=False)    # Point number (1, 2, 3 etc)
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(Float, default=200.0)

    route = relationship(Route, backref="points")
