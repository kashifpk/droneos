<%inherit file="base.mako"/>

<%def name="title()">
DroneOS - Add Route
</%def>

<%def name="js()">
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAXMKZ6a4ICAcuCqs8PVa3z3Ar9AF0nthY&sensor=false"></script>
<script>
    var str1;
    var line;
    var arr = new Array();
    var a=0;

    function initialize() {        

        var iiui = new google.maps.LatLng(33.658638, 73.029095);

        var mapDiv = document.getElementById('map-canvas');
        var map = new google.maps.Map(mapDiv, {
            center: iiui,
            zoom: 14,
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
</%def>

<div>
<h1>Add a Route</h1>

<form name="myform3" action="${request.route_url('add_route')}" method="POST" role="form" class="form-horizontal">
  <input type="hidden" name="formvar" value="" />
  <div class="form-group">
    <label for="route_name">Route Name</label>
    <input class="form-control" id="route_name" name="route_name" placeholder="Route name">
  </div>
  <div class="form-groupyckp">
    <label for="route_desc">Route Description</label>
    <textarea class="form-control" id="route_desc" name="route_desc" placeholder="Route description"></textarea>
  </div>
  
  <div id="map-canvas" style="width:100%;height:650px;"></div>
  <br />
  <button type="submit" class="btn btn-success">Add Route</button>
    
</form>
<br /><br /><br /><br /><br /><br />
</div>