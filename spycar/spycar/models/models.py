from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey
    )

from . import DBSession, Base


# Create your models here.

class path(Base):
  __tablename__='Path'
  id=Column(Integer, primary_key=True)
  name=Column(Unicode(200))
  #descr=Column(Unicode(200))
  children = relationship("coordinates", backref="Path")
  

  
class coordinates(Base):
  __tablename__= 'Coordinates'
  cordi_num=Column(Unicode(200), primary_key=True)
  path_id=Column(Integer, ForeignKey('Path.id'))
  #Point=Column(Unicode(200))
  latitude=Column(Unicode(200))
  longitude=Column(Unicode(200))
  altitude=Column(Unicode(200), default="200")
  direction=Column(Unicode(200))
  #distance=Column(Unicode(200))
 # decimal_degree=Column(Unicode(200))
  #degrees=Column(Unicode(200))
  #minutes=Column(Unicode(200))
  #seconds=Column(Unicode(200))
  distcalc=Column(Unicode(200))
  
  #paths=relationship(path, backref=backref("Coordinates"))
  