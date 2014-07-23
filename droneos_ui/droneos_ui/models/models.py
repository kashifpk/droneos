from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, Unicode, UnicodeText, Float, Boolean
from math import radians

from . import db, Base


class Route(Base):

    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    description = Column(UnicodeText)
    active = Column(Boolean, default=False)


class Point(Base):

    __tablename__ = 'points'

    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey(Route.id))
    idx = Column(Integer, nullable=False)    # Point number (1, 2, 3 etc)
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(Float, default=200.0)
    surveil = Column(Unicode(200))
    hover_time = Column(Integer, default=0)
    interval = Column(Integer, default=0)
    continue_till_next = Column(Boolean, default=False)

    route = relationship(Route, backref="points")

    def __str__(self):
        return "Point({0}, {1})".format(self.lat, self.lng)

    def __eq__(self, other):
        if self.lat == other.lat and self.lng == other.lng:
            return True
        elif abs(self.lat - other.lat) < THREASHOLD and abs(self.lng - other.lng) < THREASHOLD:
            return True
        else:
            return False

    def directions_to(self, P2):
        """
        Tells bearing (angle) and distance to P2
        """
        lat1 = self.lat
        lon1 = self.lng
        lat2 = P2.lat
        lon2 = P2.lng

        #Haversine Formuala to find vertical angle and distance
        lon1, lat1, lon2, lat2 = map(float, [lon1, lat1, lon2, lat2])
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        base = 6371 * c
        base = round(base, 4)

        #Horizontal Bearing
        def calc_bearing(lat1, lon1, lat2, lon2):
            dLon = lon2 - lon1
            y = sin(dLon) * cos(lat2)
            x = cos(lat1) * sin(lat2) \
                - sin(lat1) * cos(lat2) * cos(dLon)
            return atan2(y, x)

        bearing = calc_bearing(lat1, lon1, lat2, lon2)
        bearing = degrees(bearing)
        if (bearing < 0):
            bearing = 360 + bearing

        ##Output the data
        #print("---------------------------------------")
        #print(":::::Auto Aim Directional Anntenna:::::")
        #print("---------------------------------------")
        #print("Horizontial Distance:", base,"km")
        #print(" Horizontial Bearing:",bearing)
        #print("---------------------------------------")
        return dict(distance=base, direction=bearing)

