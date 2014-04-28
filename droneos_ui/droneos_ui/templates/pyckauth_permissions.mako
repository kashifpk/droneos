<%inherit file="pyckauth_base.mako"/>

<div class="panel panel-primary">
  <div class="panel-heading">droneos_ui - Authentication Manager - Permissions</div>
  <div class="panel-body">

    %if "edit"==action:
    <form action="${request.current_route_url()}?action=edit&id=${permission.permission}" method="post" role="form" class="form-horizontal">
    %else:
    <form action="${request.current_route_url()}" method="post" role="form" class="form-horizontal">
    %endif


    ${permission_form.as_div() | n}
    
    <div class="form-group">
        <div class="col-md-offset-3 col-md-9">
          <button type="submit" class="btn btn-success">${action.title()} Permission</button>
        </div>
    </div>
</form>
</div>
  
<div class="panel-heading">Existing Permissions</div>
<div class="panel-body">
  <table class="table table-striped table-hover">
    <thead>
        <tr style="font-weight: bold; font-size: larger;">
        <th>Permission</th>
        <th>Description</th>
        <th></th>   
        </tr>
    </thead>
    <tbody>
    
    %for P in permissions:
    
    <tr>
        <td>${P.permission}</td>
        <td>${P.description}</td>
        <td>
            <a href="${request.current_route_url()}?action=edit&id=${P.permission}">Edit</a>
            <a href="${request.current_route_url()}?action=delete&id=${P.permission}">Delete</a> 
        </td>
    </tr>
    
    %endfor
    </tbody>
</table>


</div>

