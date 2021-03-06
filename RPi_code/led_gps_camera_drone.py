import RPi.GPIO as G
import time
from gps_threaded import Point, GpsPoller
from sqlalchemy import create_engine
from droneos_ui.models import Route, Point
from sqlalchemy.orm import sessionmaker
from point import Points

PIN_HOLD = 22
PIN_BACK = 15     # South
PIN_LEFT = 13     # West
PIN_RIGHT = 11    # East
PIN_FRONT = 7     # North

all_pins = (PIN_HOLD, PIN_BACK, PIN_LEFT, PIN_RIGHT, PIN_FRONT)

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
    route = session.query(Route).filter(Route.active == True).all()
    for R in route:
	r_id = R.id
	print r_id
    
    target_points = session.query(Point).filter(Point.route_id == r_id).order_by(Point.id).all()
    
    for point in target_points:
        pass
        #destination = Point(33.63388,73.04414)
        
        ## gpsp now polls every .2 seconds for new data, storing it in self.current_value
        #while 1:
            ## In the main thread, every 5 seconds print the current value
            #time.sleep(2)
            ##print gpsp.get_current_value()
            #try:
                #coords = gpsp.get_current_value()
                #current_point = Point(round(coords['lat'], 5), round(coords['lon'], 5))
                #print("Lat: {0}, Lng: {1}, Alt: {2}".format(round(coords['lat'], 5), round(coords['lon'], 5), coords['alt']))
                #print(current_point.directions_to(destination))
                #if current_point == destination:
                    #print("!!! FINAL DESTINATION !!!")
                    #G.output(PIN_HOLD, 1)
            #except Exception, exp:
                #print("%r" % exp)
                #print(coords)
