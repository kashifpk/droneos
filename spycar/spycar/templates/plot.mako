%for category in e:
 
<h3>${category.path_id}</h3>
%endfor

<!DOCTYPE html>
<html>
  <head>
 <script src="https://maps.googleapis.com/maps/api/js?libraries=geometry&key=AIzaSyAXMKZ6a4ICAcuCqs8PVa3z3Ar9AF0nthY&sensor=false">
    </script>
    <script>





function initialize() {
  var myLatLng = new google.maps.LatLng(33.6667,73.1667);
  var mapOptions = {
    zoom: 12,
    center: myLatLng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };  
 
 var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
%for cat in e:
var startLL = new google.maps.LatLng(33.7200563373881,73.0759048461914);
var endLL = new google.maps.geometry.spherical.computeOffset(startLL, 7.52789734622327*1000, 113.064855886194);
 var coordinates = [startLL, endLL];


  var flightPlanCoordinates = [
      new google.maps.LatLng(33.7200563373881,73.0759048461914),
      new google.maps.LatLng(33.6892100935496, 73.1483459472656),
      new google.maps.LatLng(${cat.latitude}, ${cat.longitude}),
      
      
  ];
%endfor


 var flightPath = new google.maps.Polyline({
    path:coordinates ,
    strokeColor: '#00FF00',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });

  flightPath.setMap(map);



var flightPat = new google.maps.Polyline({
    path:flightPlanCoordinates ,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });
flightPat.setMap(map);
}

  
google.maps.event.addDomListener(window, 'load', initialize);

</script>
  </head>

<body>
<div id="map-canvas" style="width:1400px;height:793px;"></div>

</body>
</html>

