<%inherit file="pyckauth_base.mako"/>
<style>
    li {display: inline;}
</style>

<div class="panel panel-primary">
  <div class="panel-heading">droneos_ui - Authentication Manager - Route Permissions</div>
  <div class="panel-body">
    
<form action="${request.current_route_url()}" method="post" role="form" class="form-horizontal">


    ${route_permissions_form.as_div() | n}
    
    <div class="form-group">
        <div class="col-md-offset-3 col-md-9">
          <button type="submit" class="btn btn-success">${action.title()} Route Permission</button>
        </div>
    </div>
    
</form>
</div>
  
<div class="panel-heading">Existing Route Permissions</div>
<div class="panel-body">
  <table class="table table-striped table-hover">
    <thead>
    <tr style="font-weight: bold; font-size: larger;">
        <th>Route Name</th>
        <th>Permission</th>
        <th>Request Method</th>
        <th></th>   
    </tr>
    </thead>
    <tbody>
    %for RP in route_permissions:
    
    <tr>
        <td>${RP.route_name}</td>
        <td>${RP.permission}</td>
        <td>${RP.method}</td>
        
        <td>
            <a href="${request.current_route_url()}?action=delete&r=${RP.route_name}&p=${RP.permission}&m=${RP.method}"">Delete</a>
        </td>
    </tr>
    
    %endfor
    </tbody>
</table>


</div>'

