#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
 
import os
from gps import *
from time import *
import time
import threading

 
gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  import point
  targ_point=point.Point(33.635910833,73.0580735)
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      os.system('clear')
 
      
      latitude=gpsd.fix.latitude
      longitude=gpsd.fix.longitude
      curr_point=point.Point(latitude, longitude)
      curr_point.lat=round(curr_point.lat,4)
      curr_point.lon=round(curr_point.lon,4)
      print curr_point.lat
      print curr_point.lon
      print round(targ_point.lat,4)
      print round(targ_point.lon,4)
      distance, direction=curr_point.guides_towards(targ_point)
      print ( '%d meters %s ' % (distance,direction))
 
    #  time.sleep(5) #set to whatever
      if curr_point.on_point(targ_point):
	 print "Destination reached. . ."
	 print "\nKilling Thread..."
	 gpsp.running = False
	 gpsp.join()
      else:
	 time.sleep(5) #set to whatever
	 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."