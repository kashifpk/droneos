<%inherit file="base.mako"/>

<%!
auth_links = [('pyckauth_manager', 'Auth Home'), ('pyckauth_users', 'Users'),
              ('pyckauth_permissions', 'Permissions'), ('pyckauth_routes', 'Routes')]
%>

<%def name="title()">
droneos_ui - Authentication Manager
</%def>

<%def name="content_wrapper()">
  <div class="row">
      <div class="col-md-3">${self.side_menu()}</div>
      <div class="col-md-9">
        <div id="content">
          
          <% flash_msgs = request.session.pop_flash() %>
          
          %for flash_msg in flash_msgs:
            <div class="alert alert-info">
              ${flash_msg}
            </div>
          %endfor
          
          ${self.body()}      
        </div>
      </div>
  </div>
  
</%def>
  
<%def name="side_menu()">
<ul class="nav nav-pills nav-stacked">
	%for routename, desc in auth_links:
      <%
      row_class = ""
      if request.route_url(routename) == request.current_route_url():
          row_class = "active"
      %>
	  <li class="${row_class}"><a href="${request.route_url(routename)}">${desc}</a></li>	
	%endfor	
</ul>

</%def>




<%def name="footer()">
  
</%def>