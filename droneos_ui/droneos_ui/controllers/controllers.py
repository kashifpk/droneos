from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from ..models import db, Route, Point

from ..forms import ContactForm


@view_config(route_name='home', renderer='home.mako')
def my_view(request):
    one = None
    return {'one': one, 'project': 'droneos_ui'}


@view_config(route_name='contact', renderer="contact.mako")
def contact_form(request):

    f = ContactForm(request.POST)   # empty form initializes if not a POST request

    if 'POST' == request.method and 'form.submitted' in request.params:
        if f.validate():
            #TODO: Do email sending here.

            request.session.flash("Your message has been sent!")
            return HTTPFound(location=request.route_url('home'))

    return {'contact_form': f}


@view_config(route_name='add_route', renderer='add_route.mako')
def add_route(request):
    "Add a new route"

    if 'POST' == request.method:
        #print(request.POST)
        #MultiDict([('formvar', u'(33.66256773749932, 72.99333572387695),(33.66671105868779, 73.02286148071289),(33.654780611242245, 73.0547046661377)'), ('route_name', u'asdf'), ('route_desc', u'asdf')])
        R = Route()
        R.name = request.POST['route_name']
        R.description = request.POST['route_desc']
        db.add(R)
        db.flush()

        points_str = request.POST['formvar']
        parts = points_str.split('),(')
        idx = 1
        for part in parts:
            s = part.strip('()')
            lat, lng = s.split(',')
            P = Point()
            P.idx = idx
            P.lat = float(lat)
            P.lng = float(lng)
            P.route_id = R.id
            db.add(P)

            idx += 1

        request.session.flash("Route added!")
        return HTTPFound(location=request.route_url('home'))

    return {}


@view_config(route_name='view_routes', renderer='view_routes.mako')
def view_routes(request):

    routes = db.query(Route)

    return {'routes': routes}


@view_config(route_name='view_route', renderer='view_route.mako')
def view_route(request):

    route_name = request.matchdict['rname']

    route = db.query(Route).filter_by(name=route_name).first()
    if not route:
        return HTTPNotFound()

    return {'route': route}
