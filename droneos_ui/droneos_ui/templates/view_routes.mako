<%inherit file="base.mako"/>

<%def name="title()">
DroneOS - Routes
</%def>

<div>
<h1>Available Routes</h1>



<table class="table table-striped table-hover">
 <thead>
     <tr>
         <th>Name</th>
         <th>Description</th>
         <th>State</th>
         <th></th>
     </tr>
 </thead>
 <tbody>
     %for R in routes:
     <tr>
         <td>${R.name}</td>
         <td>${R.description}</td>
         <td>${R.active}</td>
         <td><a href="${request.route_url('set_active', rname=R.name)}">Set Active</a></td>
         <td><a href="${request.route_url('view_route', rname=R.name)}">View Route</a></td>
     </tr>
     %endfor
 </tbody>
 
</table>
  

</div>