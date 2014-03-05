<%inherit file="pyckauth_base.mako"/>


<div>
<h1>spycar - Authentication Manager</h1>
    
    <br />
    <div id="authmanager_statistics">
    <table style="width: 60%; margin: auto; font-size: large; font-weight: bold;">
        <tr class="tr_heading">
            <th colspan="2">Authentication Manager - Statistics</th>
        </tr>
        <tr class="oddrow">
            <td>Total Users</td>
            <td style="text-align: right">${user_count}</td>
        </tr>
        <tr class="evenrow">
            <td>Total Permissions (Roles)</td>
            <td style="text-align: right">${permission_count}</td>
        </tr>
        <tr class="oddrow">
            <td>Total Routes</td>
            <td style="text-align: right">${route_count}</td>
        </tr>
    </table>
    
    </div>  
</div>