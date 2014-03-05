<%inherit file="base.mako"/>

<%def name="title()">
spycar - Login
</%def>

<%def name="header()">
  <div id="top" style="text-align: center">
    <br /><br />
    <img src="${request.static_url('spycar:static/pyck-admin.png')}"  alt="pyck"/>
  </div>
</%def>

<%def name="main_menu()"></%def>
<%def name="footer()"></%def>

<%def name="body_class()">login_page</%def>

<br />
<center>
    <div class="loginbox">
        <div class="loginbox_inner">
            <form action="${request.route_url('pyckauth_login')}" method="POST">
            <div class="loginbox_content">
                <input type="text" name="user_id" class="username" />
                <input type="password" name="password" class="password" />
                <button type="submit" name="form.submitted">Login</button>
            </div>
            </form>
        </div>
    </div>
</center>
