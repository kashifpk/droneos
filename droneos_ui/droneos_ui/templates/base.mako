<%!
from droneos_ui.auth import is_allowed

auth_links = [('home', 'Home'), ('add_route', 'Add Route'), ('view_routes', 'View Routes'),
              ('admin.admin_index', 'Admin Section'), ('pyckauth_manager', 'Auth Manager')]

%>

<!DOCTYPE html>
<html>
<head>
  
  <title>${self.title()}</title>
  ${self.meta()}
  
  <link rel="shortcut icon" href="${request.static_url('droneos_ui:static/favicon.ico')}" />
  <!-- Bootstrap -->
  <link rel="stylesheet" href="${request.static_url('droneos_ui:static/bootstrap/css/bootstrap.min.css')}">
  <link rel="stylesheet" href="${request.static_url('droneos_ui:static/bootstrap/css/bootstrap-theme.min.css')}">
  
  <!-- Custom CSS -->
  <link rel="stylesheet" href="${request.static_url('droneos_ui:static/pyck.css')}" type="text/css" media="screen" charset="utf-8" />
  
  <!-- Dojo -->
  <link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/dojo/1.8.3/dojo/resources/dojo.css" type="text/css" charset="utf-8" />
  <link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/dojo/1.8.3/dijit//themes/claro/claro.css" type="text/css" charset="utf-8" />
  <script src="//ajax.googleapis.com/ajax/libs/dojo/1.8.3/dojo/dojo.js" data-dojo-config="isDebug: true, async: true, parseOnLoad: true"></script>
  <script type="text/javascript">
        require(['dojo/parser', 'dojo/domReady'],function(parser,ready){ready(function(){
          parser.parse();
          });});
  </script>
  ${self.js()}
</head>

<body class="${self.body_class()}" ${self.body_attrs()}>
   <div class="container">
	<div class="row">
		<div class="col-md-12">
			${self.header()}
		</div>
	</div>
    ${self.content_wrapper()}
	<div class="row">
		<div class="col-md-12">${self.footer()}</div>
	</div>
  </div>
</body>
</html>

<%def name="js()"></%def>

<%def name="title()">The PyCK Web Application Development Framework</%def>

<%def name="meta()">
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="PyCK web application" />
</%def>

<%def name="body_class()">
claro
</%def>
<%def name="body_attrs()">
</%def>
<%def name="header()">
  <div>
    ${self.main_menu()}
  </div>
</%def>
  
<%def name="content_wrapper()">
  <div id="content">
    
    <% flash_msgs = request.session.pop_flash() %>
    
    %for flash_msg in flash_msgs:
      <div class="alert alert-info">
        ${flash_msg}
      </div>
    %endfor
    
  ${self.body()}
  </div>
</%def>
    
<%def name="main_menu()">
<nav class="navbar navbar-inverse" role="navigation">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="${request.route_url('home')}"><img src="${request.static_url('droneos_ui:static/DroneOS-small.png')}"  alt="pyck" /></a>
    </div>

    
    
    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        %for routename, desc in auth_links:
          <%
          row_class = ""
          if request.route_url(routename) == request.current_route_url():
              row_class = "active"
          %>
          
          %if is_allowed(request, routename):
            <li class="${row_class}"><a href="${request.route_url(routename)}">${desc}</a></li>
          %endif
        %endfor
      </ul>
      <!--<form class="navbar-form navbar-left" role="search">
        <div class="form-group">
          <input type="text" class="form-control" placeholder="Search">
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
      </form>-->
      <ul class="nav navbar-nav navbar-right">
        <li>
        %if request.session.get('logged_in_user', None):
        <form style="display: inline" action="${request.route_url('pyckauth_logout')}" method="get">
          <button class="btn btn-danger">Logout</button>
        </form>
        %else:
        <form style="display: inline" action="${request.route_url('pyckauth_login')}" method="get">
          <a href="${request.static_url('droneos_ui:static/full final.html')}" class="btn btn-success">User Manual</a>
        </form>
        %endif
        </li>
        
      </ul>
    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>

  
  
  
  
  

</%def>
<%def name="footer()"></%def>

