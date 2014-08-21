import RPi.GPIO as G
import time
from gps_threaded import GpsPoller
import os
from datetime import datetime
from sqlalchemy import create_engine
from droneos_ui.models import Route, Point
from sqlalchemy.orm import sessionmaker
from math import *


PIN_HOLD = 22     # Hover
PIN_BACK = 15     # South
PIN_LEFT = 13     # West
PIN_RIGHT = 11    # East
PIN_FRONT = 7     # North
PIN_REACHED = 18  # Destination

def take_picture(last_pic_time, point):
    time_difference = datetime.now() - last_pic_time
    if point.surveil == 'image' and (time_difference.total_seconds() >= point.interval):
        image = '/home/pi/image/"' + str(datetime.now()) + '.jpg"'
        #print(image)
        cmd = 'fswebcam -r 1200*720 -F2 ' + image
        os.system(cmd)
        print(cmd)
        return True
    else:
        return False
    #check if we need to take a picture
    # surveilence = image etc.
    #if picture taken then return True
    #else return False

all_pins = (PIN_HOLD, PIN_BACK, PIN_LEFT, PIN_RIGHT, PIN_FRONT, PIN_REACHED)

if '__main__' == __name__:
    
    G.cleanup()
    G.setmode(G.BOARD)

    for pin in all_pins:
        G.setup(pin, G.OUT)

    # turn all LEDs on for 2 seconds for diagnostics
    for pin in all_pins:
        G.output(pin, 1)

    time.sleep(2)

    for pin in all_pins:
        G.output(pin, 0)

    gpsp = GpsPoller()
    gpsp.start()
    
    # path to database
    engine = create_engine('sqlite:///../droneos_ui/droneos_ui.db')

    #connecting to database
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    #fetching the route that is active
    route = session.query(Route).filter_by(active=True).first()
    #target_points = session.query(Point).filter(Point.route_id == route.id).all()
    target_points = session.query(Point).filter_by(route_id=route.id).order_by(Point.idx).all()
    #target_points = [Point(33.63594, 73.05825), Point(33.63583, 73.05820), Point(33.63589, 73.05811)]
    last_pic_taken_at = datetime.now()
    i = 0
    
    for point in target_points:
        destination = point
        print(destination)
        i = i + 1
        target = False
        ## gpsp now polls every .2 seconds for new data, storing it in self.current_value
        while target == False:
            ## In the main thread, every 5 seconds print the current value
            time.sleep(1)
                ##print gpsp.get_current_value()
            try:
                coords = gpsp.get_current_value()
                current_point = Point(lat=round(coords['lat'], 5), lng=round(coords['lon'], 5))
                print("Target Point: " + str(destination))
                print("Current Point: " + str(current_point))
                print("Lat: {0}, Lng: {1}, Alt: {2}".format(round(coords['lat'], 5), round(coords['lon'], 5), coords['alt']))
                dict1 = current_point.directions_to(destination)
                print(dict1)
                distance = dict1['distance']
                bearing = dict1['direction']
                for pin in all_pins:
                        G.output(pin, 0)                
                if (bearing >= 350 and bearing <= 360) or (bearing >= 0 and bearing <= 10):
                    #G.output(PIN_FRONT, 1)
                    print 'North'
                elif bearing > 10 and bearing < 80:
                    #G.output(PIN_FRONT, 1)
                    #G.output(PIN_RIGHT, 1)
                    print 'North East'
                elif bearing >= 80 and bearing <= 100:
                    #G.output(PIN_RIGHT, 1)
                    print 'East'
                elif bearing > 100 and bearing < 170:
                    #G.output(PIN_RIGHT, 1)
                    #G.output(PIN_BACK, 1)
                    print 'South East'
                elif bearing >= 170 and bearing <= 190:
                    #G.output(PIN_BACK, 1)
                    print 'South'
                elif bearing > 190 and bearing < 260:
                    #G.output(PIN_BACK, 1)
                    #G.output(PIN_LEFT, 1)
                    print 'South West'
                elif bearing >= 260 and bearing <= 280:
                    #G.output(PIN_LEFT, 1)
                    print 'West'
                elif bearing > 280 and bearing < 350:
                    #G.output(PIN_FRONT, 1)
                    #G.output(PIN_LEFT, 1)
                    print 'North West'
                if point.continue_till_next:
                    if take_picture(last_pic_taken_at, point):
                        last_pic_taken_at = datetime.now()
                if distance <= 0.003:
                    print("!!! %d DESTINATION !!!" % i)
                    #for pin in all_pins:
                    #    G.output(pin, 1)
                    #time_in_hover = 0
                    #while time_in_hover < point.hover:
                    #    #for pin in all_pins:
                    #    #    G.output(pin, 0)
                    #    #G.output(PIN_HOLD, 1)
                    #    if take_picture(last_pic_taken_at, point):
                    #        last_pic_taken_at = datetime.now()
                    #    time.sleep(1)
                    #    time_in_hover += 1
                    #if take_picture(last_pic_taken_at, point):
                    #    last_pic_taken_at = datetime.now()
                    target = True
            except KeyError:
                print("GPS cannot get enough signals")
            except Exception, exp:
                print("%r" % exp)
                print(coords)
    G.output(PIN_REACHED, 1)
