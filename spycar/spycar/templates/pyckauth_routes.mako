<%inherit file="pyckauth_base.mako"/>

<style>
    li {display: inline; list-style: none;}
</style>

<div>
<h1>spycar - Authentication Manager - Route Permissions</h1>

<form action="${request.current_route_url()}" method="post">

<table style="margin: auto;">
    ${route_permissions_form.as_table() | n}
    
    <tr>
        <td style="text-align: right" colspan="2">
            <input type="submit" value="${action.title()} Route Permission" class="button green" />
        </td>
    </tr>
</table>
</form>

<br /><br />

<table style="margin: auto;">
    <tr class="tr_heading">
        <th>Route Name</th>
        <th>Permission</th>
        <th>Request Method</th>
        <th></th>   
    </tr>
    
    %for RP in route_permissions:
    
    <tr class="${loop.cycle('oddrow', 'evenrow')}">
        <td>${RP.route_name}</td>
        <td>${RP.permission}</td>
        <td>${RP.method}</td>
        
        <td>
            <a href="${request.current_route_url()}?action=delete&r=${RP.route_name}&p=${RP.permission}&m=${RP.method}"">Delete</a>
        </td>
    </tr>
    
    %endfor
</table>


</div>'

