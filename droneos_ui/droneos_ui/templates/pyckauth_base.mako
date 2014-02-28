<%inherit file="base.mako"/>

<%def name="title()">
droneos_ui - Authentication Manager
</%def>

<%def name="main_menu()">
<p>
  <a href="${request.route_url('pyckauth_users')}">Users</a> |
  <a href="${request.route_url('pyckauth_permissions')}">Permissions</a> |
  <a href="${request.route_url('pyckauth_routes')}">Routes</a>
</p>
</%def>

${self.body()}

<%def name="footer()">
  
</%def>