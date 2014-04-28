<%inherit file="pyckauth_base.mako"/>

<div class="panel panel-primary">
  <div class="panel-heading">droneos_ui - Authentication Manager - Users</div>
  <div class="panel-body">
    %if "edit"==action:
    <form action="${request.current_route_url()}?action=edit&id=${user.user_id}" method="post" role="form" class="form-horizontal">
    %else:
    <form action="${request.current_route_url()}" method="post" role="form" class="form-horizontal">
    %endif
    
    ${user_form.as_div() | n}
  
    <div class="form-group">
    <div class="col-sm-3">
    <b>Permissions</b>
    </div>
    
    <div class="col-sm-9">
      %for P in permissions:
        %if 'add' == action:
        <input type="checkbox" data-dojo-type="dijit/form/CheckBox" name="chk_perm_${P.permission}" value="${P.permission}" /> ${P.permission} &nbsp;&nbsp;
        %else:
            <% checked='' %>
            %for up in user.permissions:
                %if up.permission == P.permission:
                    <% checked='checked="true"' %>
                %endif
            %endfor
            <input type="checkbox" data-dojo-type="dijit/form/CheckBox" name="chk_perm_${P.permission}" value="${P.permission}" ${checked} /> ${P.permission} &nbsp;&nbsp;
        %endif
        
        %if 0!=loop.index and 0==loop.index%8:
        <br />
        %endif
      %endfor
    </div>
    </div>
    
    <div class="form-group">
        <div class="col-md-offset-3 col-md-9">
          <button type="submit" class="btn btn-success">${action.title()} User</button>
        </div>
    </div>
    </form>
    
  </div>
  
  <div class="panel-heading">Existing Permissions</div>
  <div class="panel-body">
    <table class="table table-striped table-hover">
        <thead>
        <tr style="font-weight: bold; font-size: larger;">
            <th>User ID</th>
            <th>Permissions</th>
            <th></th>   
        </tr>
        </thead>
        <tbody>
        %for U in users:
        
        <tr>
            <td>${U.user_id}</td>
            <td>
                %for P in U.permissions:
                <span style="padding: 1px 6px; background-color: #A6DDA7;">${P.permission}</span>
                %if 0!=loop.index and 0==loop.index%8:
                <br />
                %endif
                %endfor
            </td>
            <td>
                <a href="${request.current_route_url()}?action=edit&id=${U.user_id}">Edit</a>
                <a href="${request.current_route_url()}?action=delete&id=${U.user_id}">Delete</a> 
            </td>
        </tr>
        %endfor
        </tbody>
    </table>
  </div>
</div>
