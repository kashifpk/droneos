import directions     
class Points(object):
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
	
