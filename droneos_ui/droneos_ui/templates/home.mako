<%inherit file="base.mako"/>

<%def name="title()">
PyCK Web Development Framework
</%def>

<%def name="header()">
  <div id="top" style="text-align: center">
    <br /><br />
    <img src="${request.static_url('droneos_ui:static/pyck-admin.png')}"  alt="pyck"/>
  </div>
  ${self.main_menu()}
</%def>
  
  <div class="row">
    <div class="col-md-12">
        <p class="text-center">
          Welcome to <span class="app-name">${project}</span>, an application generated by<br/>
          the PyCK web application development framework.
        </p>
    </div>
  </div>
  <div class="row">
    <div class="col-sm-6 text-right">
      <h2>Search documentation</h2>
      <form class="search" action="http://pythonhosted.org/PyCK/search.html" method="get">
        <input type="text" name="q" />
        <input type="submit" value="Go" />
        <input type="hidden" name="check_keywords" value="yes" />
        <input type="hidden" name="area" value="default" />
      </form>
    </div>
    <div class="col-sm-6 text-left">
      <h2>PyCK links</h2>
      <ul class="links">
        <li>
          <a href="http://pyck.compulife.com.pk">PyCK Website</a>
        </li>
        <li>
          <a href="http://packages.python.org/PyCK/">Documentation</a>
        </li>
        <li>
          <a href="http://pypi.python.org/pypi/PyCK">PyCK at PyPi</a>
        </li>
        <li>
          <a href="irc://irc.freenode.net#pyck">IRC Channel</a>
        </li>
      </ul>
    </div>
  </div>  
