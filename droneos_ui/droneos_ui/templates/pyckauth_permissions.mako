<%inherit file="pyckauth_base.mako"/>


<div>
<h1>droneos_ui - Authentication Manager - Permissions</h1>
%if "edit"==action:
<form action="${request.current_route_url()}?action=edit&id=${permission.permission}" method="post">
%else:
<form action="${request.current_route_url()}" method="post">
%endif

<table style="margin: auto;">
    ${permission_form.as_table() | n}
    
    <tr>
        <td style="text-align: right">
            <input type="submit" value="${action.title()} Permission" class="button green" />
        </td>
    </tr>
</table>
</form>

<br /><br />

<table style="margin: auto;">
    <tr class="tr_heading">
        <th>Permission</th>
        <th>Description</th>
        <th></th>   
    </tr>
    
    %for P in permissions:
    
    <tr class="${loop.cycle('oddrow', 'evenrow')}">
        <td>${P.permission}</td>
        <td>${P.description}</td>
        <td>
            <a href="${request.current_route_url()}?action=edit&id=${P.permission}">Edit</a>
            <a href="${request.current_route_url()}?action=delete&id=${P.permission}">Delete</a> 
        </td>
    </tr>
    
    %endfor
</table>


</div>

