from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from math import degrees, atan2
from decimal import *
import math
import string
import urllib
import re

from ..models import (
    DBSession,
    path,
    coordinates,
    )

from ..forms import ContactForm




def calculate_distance(latitude1, latitude2, longitude1, longitude2):
      
    
     
    # HAVERSINE FORMULA: 
      R = 6371; 
      latitude1 = math.radians(latitude1);
      latitude2= math.radians(latitude2);
      longitude1 = math.radians(longitude1);
      longitude2 = math.radians(longitude2);
      #angle = math.atan2(longitude2 - longitude1, latitude2 - latitude1) * 180/3.14159265;
      dLat = (latitude2-latitude1);
      dLon = (longitude2-longitude1);
      latt1 = latitude1;
      latt2 = latitude2;
      arr = math.sin(dLat/2) * math.sin(dLat/2) +math.sin(dLon/2) * math.sin(dLon/2) * math.cos(latt1) * math.cos(latt2);
      c = 2 * atan2(math.sqrt(arr), math.sqrt(1-arr)); 
      d = float(R * c);
      return d;


def calculate_angle(latitude1, latitude2, longitude1, longitude2):
   R = 6371; 
   latitude1 = math.radians(latitude1);
   latitude2= math.radians(latitude2);
   longitude1 = math.radians(longitude1);
   longitude2 = math.radians(longitude2); 
   dLat = (latitude2-latitude1);
   dLon = (longitude2-longitude1);
   lat1 = latitude1;
   lat2 = latitude2;

   y = math.sin(dLon) * math.cos(lat2);
   x = math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(dLon);
   brng = degrees(math.atan2(y,x));
   return brng;




@view_config(route_name='hello', renderer='hello.mako')
def say_hello(request):
  file1=request.POST['formvar'];
  file2=request.POST['formvar'];
  pathname=request.POST['path_name'];
  pathdesc=request.POST['path_desc'];
  alt=request.POST['alt'];
  
  results1=[]
  results2=[]
  results3=[]
 # results4=[]
  
  file2=str(file2);
  file1=str(file1);
  pathname=str(pathname);
  pathdesc=str(pathdesc);
  alt=str(alt);
  # To get latitudes in a list
  
  start_index=file1.find("(")
  while -1!= start_index:
    end_index=file1.find(",", start_index)
    if -1!= end_index:
      testing=file1[start_index+1:end_index]
      results1.append(testing)
    start_index=file1.find("(", end_index)
   
   
  # to get longitude in a list 
   
  index_1=file2.find(" ")
  while -1!= index_1:
    index_2=file2.find(")", index_1)
    if -1!= index_2:
      testing2=file2[index_1+1:index_2]
      results2.append(testing2)
    index_1=file2.find(" ", index_2)

  
  path1=path(name=pathname, desc=pathdesc)
  DBSession.add(path1)
  a = DBSession.query(path.id).order_by(path.id.desc()).first()
  index=0;
  lat1=results1[index]
  long1=results2[index]

  
  
  for index in range(len(results1)):
    # Code for retrieving points at index2
    lt2=results1[index+1:]
    lg2=results2[index+1:]
    for l2 in lt2:
      lat2=l2;
      break;
    for ln2 in lg2:
      long2=ln2;
      break;
      
  #evaluating direction for points
  
    lat1=float(lat1)
    lat2=float(lat2)
    long1=float(long1)
    long2=float(long2)
  
    if (lat1 < lat2 and long1 < long2):
	direct="Towards North East"
    elif (lat1 > lat2 and long1 < long2):
	direct="Towards South East"
    elif (lat1 > lat2 and long1 > long2):
	direct="Towards South West"
    elif (lat1 < lat2 and long1 > long2):
	direct="Towards North West"
    else:
	direct="Moving in right direction"
	
    latitude1=lat1;
    latitude2=lat2;
    longitude1=long1;
    longitude2=long2;
    # Code for calculating angle
    #dx=lat2-lat1
    #dy=long2-long1
    #angle = degrees(atan2(dy, dx))
  #  angle=calculate_angle(latitude1, latitude2, longitude1, longitude2);
    
    
    # Conversion form decimal fraction to DMS-Format
  #  deg = int(angle)
   #temp = 60 * (angle - deg)
    #minut = int(temp)
    #sec = 60 * (temp - minut)
    
    # Rounds seconds
    #sec=int(sec * 10) / 10.0
    
    
    
    
    
   
    
    
    
    #for calculating distance between ponits:  
      
    d=calculate_distance(latitude1, latitude2, longitude1, longitude2);
    # Code for database insertion 
    results3.append(direct)
    #results4.append(dist)
    lat1=lat2
    long1=long2
    coordinate1= coordinates(cordi_num="P_"+str(index+1), latitude= float(results1[index]), longitude=float(results2[index]), altitude=alt, path_id=a.id, direction=results3[index], distcalc=d)
    DBSession.add(coordinate1)

    
    #distance=results4[index]
  acc2 = DBSession.query(coordinates).all()
  return {'acc2':acc2}  
 
  
@view_config(route_name='savings', renderer='savings.mako')   
def my_savings(request):
    acc2 = DBSession.query(coordinates).all()
    
    return {'acc2':acc2}  
    
    
    
@view_config(route_name='compare', renderer='compare.mako')   
def my_compare(request):
    
    
    return {}    
    
    
    
@view_config(route_name='plot', renderer='plot.mako')
def my_plot(request):
  variable1=request.POST['check'];
  variable1=str(variable1);
  variable1=int(variable1);
  e=DBSession.query(coordinates).filter(coordinates.path_id==variable1).all()
  return {'e': e}
  

    
    
    
@view_config(route_name='map', renderer='map.mako')   
def my_map(request):
  
  
    
    
  return {}  
    
    
    
@view_config(route_name='test', renderer='test.mako')   
def test(request):
  R=6371;
  latitude1= 33.6623534223548;
  latitude2= 33.5977488143793;
  longitude1=73.1740951538086;
  longitude2=73.0522155761719;
  latitude1 = math.radians(latitude1);
  latitude2= math.radians(latitude2);
  longitude1 = math.radians(longitude1);
  longitude2 = math.radians(longitude2);
  angle = math.atan2(longitude2 - longitude1, latitude2 - latitude1) * 180/3.14159265;
  dLat = (latitude2-latitude1);
  dLon = (longitude2-longitude1);
  latt1 = latitude1;
  latt2 = latitude2;
  arr = math.sin(dLat/2) * math.sin(dLat/2) +math.sin(dLon/2) * math.sin(dLon/2) * math.cos(latt1) * math.cos(latt2);
  c = 2 * atan2(math.sqrt(arr), math.sqrt(1-arr)); 
  d = float(R * c);
  
  return {'angle':angle}
  
    
    
    
    
    
    
@view_config(route_name='savings1', renderer='savings1.mako')   
def my_savings1(request):
    acc2 = DBSession.query(path).all()
    
    return {'acc2':acc2}      
    
  
  

@view_config(route_name='home', renderer='home.mako')
def my_view(request):
    one = None
    return {'one': one, 'project': 'spycar'}


@view_config(route_name='contact', renderer="contact.mako")
def contact_form(request):

    f = ContactForm(request.POST)   # empty form initializes if not a POST request

    if 'POST' == request.method and 'form.submitted' in request.params:
        if f.validate():
            #TODO: Do email sending here.

            request.session.flash("Your message has been sent!")
            return HTTPFound(location=request.route_url('home'))

    return {'contact_form': f}
