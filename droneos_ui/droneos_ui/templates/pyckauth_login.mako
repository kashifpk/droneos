<%inherit file="base.mako"/>

<%def name="title()">
droneos_ui - Login
</%def>

<%def name="header()">
  <div id="top" style="text-align: center">
    <br /><br />
    <img src="${request.static_url('droneos_ui:static/pyck-admin.png')}"  alt="pyck"/>
  </div>
</%def>

<%def name="main_menu()"></%def>
<%def name="footer()"></%def>

<%def name="body_class()">login_page</%def>

<br />
<div class="row">
  <div class="col-md-4 col-lg-4 col-xs-1 col-sm-2"></div>
  <div class="col-md-4 col-xs-11 col-sm-11 col-lg-4">
      
    <form action="${request.route_url('pyckauth_login')}" method="POST" class="form-horizontal" role="form">
    
      <div class="input-group input-group-lg">
        <span class="input-group-addon glyphicon glyphicon-user"></span>
        <input type="text" name="user_id" class="form-control" placeholder="Username" />
      </div>
      <br />
      <div class="input-group input-group-lg">
        <span class="input-group-addon glyphicon glyphicon-random"></span>
        <input type="password" name="password" class="form-control" placeholder="Password" />
      </div>
      <br />
      <button type="submit" name="form.submitted" class="btn btn-success btn-lg btn-block">Login</button>
    
    </form>
      
  </div>
  <div class="col-md-4 col-lg-4 col-xs-1 col-sm-2"></div>
  
</div>
