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
        
        var path = line.getPath();
        %for point in route.points:
        path.push(new google.maps.LatLng(${point.lat}, ${point.lng}));
        %endfor
        
        line.setMap(map);
      
    }
    
    google.maps.event.addDomListener(window, 'load', initialize);
    
</script>
</%def>

<div>
<h1>Viewing Route  : <b> ${route.name} </b></h1>
<p>${route.description}</p>

<form action="${request.route_url('update_route', rname=route.name)}" method="POST" role="form" class="form-horizontal">
   <table class="table table-striped table-hover">
    <thead>
        <tr>
            <th><b>Index</b></th>
            <th><b>Latitude</b></th>
            <th><b>Longitude</b></th>
            <th><b>Altitude</b></th>
            <th><b>Surveillance</b></th>
            <th><b>Hover</b></th>
            <th><b>Interval</b></th>
            <th><b>Till Next</b></th>
        </tr>
    </thead>
    <tbody>
        %for P in route.points:
        <tr>
            <td>${P.idx}</td>
            <td>${P.lat}</td>
            <td>${P.lng}</td>
            <td><input class="form-control" name="alt_${P.idx}" value="${P.alt}" /></td>
            <td>
            <select name="type_${P.idx}">
                %for value in ['none', 'audio', 'image', 'video']:
                    <option value="${value}"
                            %if P.surveil == value:
                            selected
                            %endif
                            >${value.title()}</option>
                %endfor
            </select>
            </td>
            <td><input class="form-control" name="hover_${P.idx}" value="${P.hover_time}" /></td>
            <td><input class="form-control" name="interval_${P.idx}" value="${P.interval}" /></td>
            <td><input type="checkbox" name="continue_${P.idx}" value="yes"
                       %if P.continue_till_next:
                       checked="true"
                       %endif
                       ></td>
            
        </tr>
        %endfor
    </tbody>
    
   </table>
  
  
  <button type="submit" class="btn btn-success">Update</button
  
    
</form>
</br>
<div id="map-canvas" style="width:100%;height:650px;"></div>
 

</div>