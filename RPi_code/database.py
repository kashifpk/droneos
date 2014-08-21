from sqlalchemy import create_engine
from droneos_ui.models import Route, Point
from sqlalchemy.orm import sessionmaker
from point import Points

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

#fetching the points on the active route
point = session.query(Point).filter(Point.route_id == r_id).all()
for P in point:
    lat = P.lat
    lng = P.lng
    #print lat
    #print lng
    targ_point = Points(lat, lng)
    print targ_point.lat
    print targ_point.lon

