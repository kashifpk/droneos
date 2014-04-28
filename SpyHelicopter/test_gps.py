import gps
import time
import point

if '__main__' == __name__:
    count = 0
    targ_point=point.Point( 33.658520,73.029851)
   # targ_point.lat=round(targ_point.lat,4)
    #targ_point.lon=round(targ_point.lon,4)
    G = gps.gps(mode=gps.WATCH_ENABLE)
    lat = 0.0
    lon = 0.0
    while (lat==0.0 and lon==0.0):
       G.next()
      #print(G)
       lat=G.fix.latitude
       lon=G.fix.longitude
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
            G.next()
            lat=G.fix.latitude
            lon=G.fix.longitude
            curr_point=point.Point(lat, lon)
            count = count + 1
           #curr_point.lat=round(curr_point.lat,4)
           #curr_point.lon=round(curr_point.lon,4)
          if(curr_point.on_point(targ_point)):
	     print "destination reached"
	     break
	  
       
      
         