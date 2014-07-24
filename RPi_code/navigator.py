import RPi.GPIO as GPIO
import sys
import time
import logging
from math import radians
from gps_threaded import Point, GpsPoller
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, Unicode, UnicodeText, Float, Boolean

Base = declarative_base()

THRESHOLD = 0.00003

log = logging.getLogger(__name__)

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
        elif abs(self.lat - other.lat) < THRESHOLD and abs(self.lng - other.lng) < THRESHOLD:
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


class Navigator(object):
    "Navigator class for providing directions based on GPS coordinates"

    PIN_HOLD = 22
    PIN_BACK = 15     # South
    PIN_LEFT = 13     # West
    PIN_RIGHT = 11    # East
    PIN_FRONT = 7     # North

    all_pins = (PIN_HOLD, PIN_BACK, PIN_LEFT, PIN_RIGHT, PIN_FRONT)

    def __init__(self):
        "Setup GPIO and other stuff etc"

        self.gps = GpsPoller()
        self.gps.start()
        
        self.gpio_setup()

    def gpio_setup(self):

        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        for pin in self.all_pins:
            GPIO.setup(pin, GPIO.OUT)

    def blink(self):
        "turn all LEDs on for 2 seconds for diagnostics"

        for pin in self.all_pins:
            GPIO.output(pin, 1)

        time.sleep(2)

        for pin in self.all_pins:
            GPIO.output(pin, 0)

    def navigate_to(self, target_point):
        "Navigates to the target point"

        target_reached = False
        while not target_reached:
            try:
                time.sleep(2)
                coords = self.gps.get_current_value()
                if 'lat' not in coords:
                    log.info("No GPS fix yet! waiting")
                    continue

                current_point = Point(lat=round(coords['lat'], 5), lon=round(coords['lon'], 5))
                print(current_point)
                print(current_point.directions_to(target_point))
                if current_point == target_point:
                    print("*** Target Point Reached")
                    #GPIO.output(PIN_HOLD, 1)

            except Exception, exp:
                log.error("Error fetching GPS coordinates")
                #print("%r" % exp)
                #print(coords)
    

# This list is used when the script is executed with "test" argument.
TEST_POINTS = [
    Point(idx=1, lat=37.12345, lng=73.12321,
          alt=200.0, surveil='image', hovertime=0,
          interval=3, continue_till_next=True),
    Point(idx=2, lat=37.12345, lng=73.12321,
          alt=200.0, surveil='image', hovertime=0,
          interval=3, continue_till_next=True),
    Point(idx=3, lat=37.12345, lng=73.12321,
          alt=200.0, surveil='image', hovertime=0,
          interval=3, continue_till_next=True),
]


if '__main__' == __name__:

    guide = Navigator(gpsp)
    #guide.blink()

    target_points = []

    if len(sys.argv) > 1 and 'test' == sys.argv[1]:
        target_points = TEST_POINTS
    else:
        # path to database
        engine = create_engine('sqlite:///../droneos_ui/droneos_ui.db')

        #connecting to database
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        #fetching the route that is active
        route = session.query(Route).filter_by(active= True).first()
        if not route:
            print("ERROR: No active routes found!")
            sys.exit(1)

        target_points = session.query(Point).filter_by(route_id=route.id).order_by(Point.idx).all()

    for point in target_points:
        guide.navigate_to(point)

    print("!!! FINAL DESTINATION !!!")
