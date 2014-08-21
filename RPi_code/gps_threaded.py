import threading
import time
from math import *
from gps import gps, WATCH_ENABLE

THREASHOLD = 0

class Point(object):

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

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




class GpsPoller(threading.Thread):

   def __init__(self):
       threading.Thread.__init__(self)
       self.session = gps(mode=WATCH_ENABLE)
       self.current_value = None

   def get_current_value(self):
       return self.current_value

   def run(self):
       try:
            while True:
                self.current_value = self.session.next()
                time.sleep(0.2) # tune this, you might not get values that quickly
       except StopIteration:
            pass

if __name__ == '__main__':

    destination = Point(33.63593, 73.05824)
    gpsp = GpsPoller()
    gpsp.start()
    # gpsp now polls every .2 seconds for new data, storing it in self.current_value
    while 1:
        # In the main thread, every 5 seconds print the current value
        time.sleep(2)
        #print gpsp.get_current_value()
        try:
            coords = gpsp.get_current_value()
            current_point = Point(round(coords['lat'], 5), round(coords['lon'], 5))
            print("Tajairget Point: " + str(destination))
            print("Current Point: " + str(current_point))
            print("Lat: {0}, Lng: {1}, Alt: {2}".format(round(coords['lat'], 5), round(coords['lon'], 5), coords['alt']))
            dict1 = current_point.directions_to(destination)
            print(dict1)
            distance = dict1.itervalues().next()
            if distance <= 0.003:
                print("!!! FINAL DESTINATION !!!")
        except Exception, exp:
            print("%r" % exp)
            print(coords)
