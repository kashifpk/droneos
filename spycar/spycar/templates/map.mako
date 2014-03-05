<!DOCTYPE html>
<html>
<body>
   <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAXMKZ6a4ICAcuCqs8PVa3z3Ar9AF0nthY&sensor=false">
    </script>
    <script>


var str1;
var line;
var arr = new Array();
var a=0;
function initialize() {
  var mapDiv = document.getElementById('map-canvas');
  var map = new google.maps.Map(mapDiv, {
    center: new google.maps.LatLng(33.6667,73.1667),
    zoom: 12,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  
  line = new google.maps.Polyline({
    strokeColor: '#ff0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });

  line.setMap(map);

  google.maps.event.addListener(map, 'click', addNewPoint);
}
function addNewPoint(e) {
  var path = line.getPath();
  path.push(e.latLng);


arr[a]=(e.latLng);
a++;
str1=arr.toString();
//str1 = str1.replace(/[,]/g,")(");
document.myform3.formvar.value = str1;
}


google.maps.event.addDomListener(window, 'load', initialize);



function validateForm()
{
var x=document.forms["myform3"]["path_name"].value;
if (x==null || x=="")
  {
  alert("You must enter a path name");
  return false;
  }
var y=document.forms["myform3"]["formvar"].value;
if (y==null || y=="")
  {
  alert("You have not defined any path");
  return false;
  }
  
  var z=document.forms["myform3"]["path_desc"].value;
if (z==null || z=="")
  {
  alert("You have not described your path");
  return false;
  }
}

</script>

  


<div id="map-canvas" style="width:1200px;height:650px;"></div>

<form name="myform3" action="http://0.0.0.0:6543/hello" onsubmit="return validateForm()"  method="POST">
		
		<input type="hidden" name="formvar" value="">
<p><b>PATH INFORMATION</b><br><br>

Name: <input type="text" name="path_name"><br>
Description: <input type="text" name="path_desc"><br>
Altitude: <input type="text" name="alt" value="200"><br>
</p>
<input type="submit" value="Done" />
	</form>

	</body>
</html> 
