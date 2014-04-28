<%inherit file="pyckauth_base.mako"/>


<div class="panel panel-primary">
  <div class="panel-heading">droneos_ui - Authentication Manager</div>
  <div class="panel-body">
    <table class="table table-striped table-hover">
        <thead>
        <tr class="info">
            <th colspan="2">Authentication Manager - Statistics</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>Total Users</td>
            <td style="text-align: right">${user_count}</td>
        </tr>
        <tr>
            <td>Total Permissions (Roles)</td>
            <td style="text-align: right">${permission_count}</td>
        </tr>
        <tr>
            <td>Total Routes</td>
            <td style="text-align: right">${route_count}</td>
        </tr>
        </tbody>
    </table>
  </div>
</div>