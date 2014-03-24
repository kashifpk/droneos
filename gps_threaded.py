import threading
import time
from gps import gps, WATCH_ENABLE

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

   gpsp = GpsPoller()
   gpsp.start()
   # gpsp now polls every .2 seconds for new data, storing it in self.current_value
   while 1:
       # In the main thread, every 5 seconds print the current value
       time.sleep(5)
<<<<<<< HEAD
       #print gpsp.get_current_value.latitude
       print gpsp.get_current_value()
=======
       print gpsp.get_current_value()
       #print gpsp.get_current_value()
>>>>>>> f9329e6af1115d32ace3f6262a5cc39085906b66
