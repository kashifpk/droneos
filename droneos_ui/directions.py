#! /usr/bin/python

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
  
  #  if (lat1 < lat2 and lon1 < lon2):
#	direct="Towards North East"
 #   elif (lat1 > lat2 and lon1 < lon2):
        #direct="Towards South East"
  #  elif (lat1 > lat2 and lon1 > lon2):
#	direct="Towards South West"
 #   elif (lat1 < lat2 and lon1 > lon2):
#	direct="Towards North West"
 #   else:
#	direct="Moving in right direction"
 #   return direct
    


if '__main__' == __name__:
    d = calculate_distance(73.058289012,33.6360666,73.058086667,33.635958833)
    direct,direct2 = find_directions(73.058289012,33.6360666,73.058086667,33.635958833)
    print "\n Distance:\n"
    print d
    print direct
    print direct2