import RPi.GPIO as GPIO
import sys
import time
import logging
from math import *
from gps_threaded import GpsPoller
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, Unicode, UnicodeText, Float, Boolean
import os
from datetime import datetime

Base = declarative_base()

THRESHOLD = 0.003

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

    #IMAGE_BASE = '/home/amber/droneos/RPi_code/image/'
    IMAGE_BASE = '/home/pi/droneos/RPi_code/image/'


    PIN_HOLD = 22
    PIN_BACK = 15     # South
    PIN_LEFT = 13     # West
    PIN_RIGHT = 11    # East
    PIN_FRONT = 7     # North
    PIN_REACHED = 18

    all_pins = (PIN_HOLD, PIN_BACK, PIN_LEFT, PIN_RIGHT, PIN_FRONT, PIN_REACHED)
    last_pic_time = None

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
                time.sleep(1)
                coords = self.gps.get_current_value()
                #print(coords)
                if 'lat' not in coords:
                    print(coords)
                    for pin in self.all_pins:
                        GPIO.output(pin, 0)
                    GPIO.output(self.PIN_FRONT, 1)
                    GPIO.output(self.PIN_BACK, 1)
                    print("No GPS fix yet! waiting")
                    continue

                if 'image' == target_point.surveil and target_point.continue_till_next:
                    if not self.last_pic_time:
                        self.take_picture()
                    else:
                        time_diff = datetime.now() - self.last_pic_time
                        if time_diff.total_seconds() >= target_point.interval:
                
                            self.take_picture()

                current_point = Point(lat=round(coords['lat'], 5), lng=round(coords['lon'], 5))
                print('Current Point : %s ' % str(current_point))
                print ('Target Point : %s' % str(target_point))
                dict1 = current_point.directions_to(target_point)
                print(dict1)
                distance = dict1['distance']
                bearing = dict1['direction']
                for pin in self.all_pins:
                    GPIO.output(pin, 0)
                if (bearing >= 350 and bearing <= 360) or (bearing >= 0 and bearing <= 10):
                    GPIO.output(self.PIN_FRONT, 1)
                    print 'North'
                elif bearing > 10 and bearing < 80:
                    GPIO.output(self.PIN_FRONT, 1)
                    GPIO.output(self.PIN_RIGHT, 1)
                    print 'North East'
                elif bearing >= 80 and bearing <= 100:
                    GPIO.output(self.PIN_RIGHT, 1)
                    print 'East'
                elif bearing > 100 and bearing < 170:
                    GPIO.output(self.PIN_RIGHT, 1)
                    GPIO.output(self.PIN_BACK, 1)
                    print 'South East'
                elif bearing >= 170 and bearing <= 190:
                    GPIO.output(self.PIN_BACK, 1)
                    print 'South'
                elif bearing > 190 and bearing < 260:
                    GPIO.output(self.PIN_BACK, 1)
                    GPIO.output(self.PIN_LEFT, 1)
                    print 'South West'
                elif bearing >= 260 and bearing <= 280:
                    GPIO.output(self.PIN_LEFT, 1)
                    print 'West'
                elif bearing > 280 and bearing < 350:
                    GPIO.output(self.PIN_FRONT, 1)
                    GPIO.output(self.PIN_LEFT, 1)
                    print 'North West'
                if distance <= THRESHOLD:
                    print("*** Target Point Reached")
                    target_reached = True

                    # hover logic comes here
                    if target_point.hover_time > 0:
                        hover_start = datetime.now()
                        time_diff = datetime.now() - hover_start
                        while (time_diff.total_seconds() < target_point.hover_time):
                            print 'Wait. . . Please'
                            for pin in self.all_pins:
                                GPIO.output(pin, 0)
                            GPIO.output(self.PIN_HOLD, 1)
                            self.take_picture()
                            time.sleep(target_point.interval)
                            time_diff = datetime.now() - hover_start
                    return
            except Exception, exp:
                print("Error fetching GPS coordinates")
                print("%r" % exp)
                #print(coords)

    # For capturing and saving images
    def take_picture(self):
        image = self.IMAGE_BASE + '"' + str(datetime.now()) + '.jpg"'
        #print(image)
        cmd = 'fswebcam -d /dev/video0 -r 1200*720 -F2 ' + image
        print(cmd)
        os.system(cmd)
        print 'Picture Taken'
        self.last_pic_time = datetime.now()


# This list is used when the script is executed with "test" argument.
TEST_POINTS = [
    Point(idx=1, lat=33.65795, lng=73.03,
          alt=200.0, surveil='image', hover_time=5,
          interval=2, continue_till_next=True),
    Point(idx=2, lat=33.6582, lng=73.03022,
          alt=200.0, surveil='image', hover_time=6,
          interval=1, continue_till_next=False),
    Point(idx=3, lat=33.65851, lng=73.03015,
          alt=200.0, surveil='image', hover_time=7,
          interval=1, continue_till_next=True),
    Point(idx=4, lat=33.65795, lng=73.03,
          alt=200.0, surveil='image', hover_time=8,
          interval=1, continue_till_next=False)
]
#TEST_POINTS = [
#    Point(idx=1, lat=33.63383, lng=73.04409,
#          alt=200.0, surveil='image', hover_time=10,
#          interval=2, continue_till_next=True),
#    Point(idx=2, lat=33.63387, lng=73.04422,
#          alt=200.0, surveil='image', hover_time=10,
#          interval=2, continue_till_next=True),
#    Point(idx=3, lat=33.63382, lng=73.04412,
#          alt=200.0, surveil='image', hover_time=10,
#          interval=2, continue_till_next=True)

#TEST_POINTS = [
#    Point(idx=1, lat=33.63594, lng=73.05825,
#          alt=200.0, surveil='image', hover_time=10,
#          interval=2, continue_till_next=True),
#    Point(idx=2, lat=33.63583, lng=73.0582,
#          alt=200.0, surveil='image', hover_time=5,
#          interval=1, continue_till_next=False),
#    Point(idx=3, lat=33.63589, lng=73.05811,
#          alt=200.0, surveil='image', hover_time=10,
#          interval=2, continue_till_next=False),
#    Point(idx=4, lat=33.63594, lng=73.05825,
#          alt=200.0, surveil='image', hover_time=5,
#          interval=1, continue_till_next=False)
#]


if '__main__' == __name__:

    guide = Navigator()
    guide.blink()

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
        print(point)
        guide.navigate_to(point)
    print("!!! FINAL DESTINATION !!!")
    for pin in guide.all_pins:
            GPIO.output(pin, 0)
    GPIO.output(guide.PIN_REACHED, 1)
    sys.exit()
