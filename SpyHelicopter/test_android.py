import gps
import android, time
from math import radians, cos, sin, asin, sqrt

def calculate_distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6371 * c
    km=km *1000
    return km
 
#finding directions
def find_directions(lon1, lat1, lon2, lat2):
    lat1=float(lat1)
    lat2=float(lat2)
    lon1=float(lon1)
    lon2=float(lon2)
   
    vertical_dist=calculate_distance(lon1,lat1,lon2,lat1)
    if (lat2>lat1):
       direct="go %d meters forward" % (vertical_dist)
    else:
       direct="go %d meters backward" % vertical_dist
   
    horizontal_dist=calculate_distance(lon1,lat1,lon1,lat2)
    if (lon2>lon1):
       direct2="turn %d meters right" % horizontal_dist
    else: 
       direct2="turn %d meters left" % horizontal_dist
       
    return direct,direct2


class Point(object):
    lat =0
    lon =0
        
    #constructor that initializes the para,eters
    def __init__(self, lat, lon):
        self.lat= lat
	self.lon= lon
    
    #checks if reached destination
    def on_point(self, target_point, threshold=0):
       if (target_point.lat - self.lat <= threshold) and (target_point.lon - self.lon <= threshold):
      # distance=directions.calculate_distance(self.lon,self.lat,target_point.lon, target_point.lat)
       #if (distance <= threshold):
	      return True
       else:
	      return False

    #guides towards destination
    def guides_towards(self, target_point):
	distance=directions.calculate_distance(self.lon,self.lat,target_point.lon, target_point.lat)
	vert_dir,hor_dir=directions.find_directions(self.lon,self.lat,target_point.lon, target_point.lat)
	return distance,vert_dir,hor_dir
	

if '__main__' == __name__:
    count = 0
    targ_point=point.Point( 33.658520,73.029851)
   # targ_point.lat=round(targ_point.lat,4)
    #targ_point.lon=round(targ_point.lon,4)
    lat=0.0
    lon=0.0
    droid = android.Android()
    droid.startLocating()
    time.sleep(5)
    loc = droid.readLocation().result
    if loc == {}:
      loc = getLastKnownLocation().result
    if loc != {}:
      try:
	n = loc['gps']
      except KeyError:
	n = loc['network'] 
      lat = n['latitude'] 
      lon = n['longitude']
   
   # lat = 0.0
    #lon = 0.0
    #while (lat==0.0 and lon==0.0):
     #  G.next()
      #print(G)
      # lat=G.fix.latitude
       #lon=G.fix.longitude
      #curr_point=point.Point(latitude, longitude)
      #curr_point.lat=round(curr_point.lat,4)
      #curr_point.lon=round(curr_point.lon,4)
      #print(" Current point is %s,%s" % (str(curr_point.lat ), str(curr_point.lon )))
      #targ_point.lat=round(targ_point.lat,4)
      #targ_point.lon=round(targ_point.lon,4)
      #print(" Target point is %s,%s" % (str(targ_point.lat ), str(targ_point.lon )))
      #distance, direction=currcd _point.guides_towards(targ_point)
      #print ( '%d km %s ' % (distance,direction))
      #if (lat==0.0 and lon==0.0):
	#time.sleep(0)
      #else:
    if (lat!=0.0 and lon!=0.0):
	curr_point=point.Point(lat, lon)
        count =count + 1
     #   curr_point.lat=round(curr_point.lat,4)
      #    curr_point.lon=round(curr_point.lon,4)
        while(curr_point.on_point(targ_point)== False):
	    print count
            print(" Current point is %s,%s" % (str(curr_point.lat ), str(curr_point.lon )))
            print(" Target point is %s,%s" % (str(targ_point.lat ), str(targ_point.lon )))
            distance,vert_dir,hor_dir=curr_point.guides_towards(targ_point)
            print ( '%d meters ' % (distance))
            print ('%s' % vert_dir)
            print ('%s' % hor_dir)
            time.sleep(5)
            loc = droid.readLocation().result
	    if loc == {}:
	      loc = getLastKnownLocation().result
	    if loc != {}:
	      try:
		  n = loc['gps']
	      except KeyError:
		  n = loc['network'] 
	      lat = n['latitude'] 
	      lon = n['longitude']
	      curr_point=point.Point(lat, lon)
	      count = count + 1
           #curr_point.lat=round(curr_point.lat,4)
           #curr_point.lon=round(curr_point.lon,4)
        if(curr_point.on_point(targ_point)):
	     print "destination reached"
	     break
	  
       
      
         