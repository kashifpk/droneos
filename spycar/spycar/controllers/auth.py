import hashlib
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ..models import DBSession, Permission, User, UserPermission, RoutePermission

from ..forms import LoginForm, UserForm, PermissionForm, RoutePermissionForm
from sqlalchemy import func


@view_config(route_name='pyckauth_manager', renderer='pyckauth_manager.mako')
def auth_manager(request):
    user_count = DBSession.query(func.count(User.user_id)).scalar()
    permission_count = DBSession.query(func.count(Permission.permission)).scalar()
    route_count = len(request.registry.introspector.get_category('routes'))

    return dict(user_count=user_count, permission_count=permission_count, route_count=route_count)


@view_config(route_name='pyckauth_users', renderer='pyckauth_users.mako')
def auth_users(request):

    action = request.GET.get('action', 'add')

    U = None
    if 'delete' == action:
        DBSession.query(UserPermission).filter_by(user_id=request.GET['id']).delete()
        DBSession.query(User).filter_by(user_id=request.GET['id']).delete()

        request.session.flash("User deleted!")
        return HTTPFound(location=request.current_route_url())

    if 'edit' == action:
        U = DBSession.query(User).filter_by(user_id=request.GET['id']).first()

    f = UserForm(request.POST, U)

    if 'POST' == request.method:
        if f.validate():
            if 'add' == action:
                U = User()
                f.populate_obj(U)
                U.password = hashlib.sha1(f.password.data).hexdigest()
                DBSession.add(U)

                # Add user permissions here.
                for key in request.POST.keys():
                    if key.startswith('chk_perm_'):
                        permission = request.POST[key]
                        UP = UserPermission(f.user_id.data, permission)
                        DBSession.add(UP)

                request.session.flash("User created!")
                return HTTPFound(location=request.current_route_url())

            elif 'edit' == action:
                DBSession.query(UserPermission).filter_by(user_id=request.GET['id']).delete()
                for key in request.POST.keys():
                    if key.startswith('chk_perm_'):
                        permission = request.POST[key]
                        UP = UserPermission(f.user_id.data, permission)
                        DBSession.add(UP)

                f.populate_obj(U)
                U.password = hashlib.sha1(f.password.data).hexdigest()
                request.session.flash("User updated!")
                return HTTPFound(location=request.current_route_url())

    permissions = DBSession.query(Permission).order_by('permission')
    users = DBSession.query(User).order_by('user_id')

    return dict(action=action, user_form=f, permissions=permissions, users=users, user=U)


@view_config(route_name='pyckauth_permissions', renderer='pyckauth_permissions.mako')
def auth_permissions(request):

    action = request.GET.get('action', 'add')

    P = None
    if 'delete' == action:
        DBSession.query(UserPermission).filter_by(permission=request.GET['id']).delete()
        DBSession.query(RoutePermission).filter_by(permission=request.GET['id']).delete()
        DBSession.query(Permission).filter_by(permission=request.GET['id']).delete()

        request.session.flash("Permission deleted!")
        return HTTPFound(location=request.current_route_url())

    if 'edit' == action:
        P = DBSession.query(Permission).filter_by(permission=request.GET['id']).first()

    f = PermissionForm(request.POST, P)

    if 'POST' == request.method:
        if f.validate():
            if 'add' == action:
                P = Permission()
                f.populate_obj(P)
                DBSession.add(P)

                request.session.flash("Permission created!")
                return HTTPFound(location=request.current_route_url())

            elif 'edit' == action:
                if f.permission.data != P.permission:
                    # Need to update permission in UserPermission and RoutePermission records too
                    user_permissions = DBSession.query(UserPermission).filter_by(permission=request.GET['id'])
                    for up in user_permissions:
                        up.permission = f.permission.data

                    route_permissions = DBSession.query(RoutePermission).filter_by(permission=request.GET['id'])
                    for rp in route_permissions:
                        rp.permission = f.permission.data

                f.populate_obj(P)
                request.session.flash("Permission updated!")
                return HTTPFound(location=request.current_route_url())

    permissions = DBSession.query(Permission).order_by('permission')

    return dict(action=action, permission_form=f, permissions=permissions, permission=P)


@view_config(route_name='pyckauth_routes', renderer='pyckauth_routes.mako')
def auth_routes(request):
    action = request.GET.get('action', 'add')

    if 'delete' == action:
        DBSession.query(RoutePermission).filter_by(
                route_name=request.GET['r'], method=request.GET['m'],
                permission=request.GET['p']).delete()

        request.session.flash("Route permission deleted!")
        return HTTPFound(location=request.current_route_url())

    # **** Code for setting up route permission form
    f = RoutePermissionForm(request.POST)

    routes = []
    for r in request.registry.introspector.get_category('routes'):
        route = r['introspectable']
        #print(R['name'] + ':' + R['pattern'])
        routes.append((route['name'], route['name'] + '(' + route['pattern'] + ')'))

    f.route_name.choices = routes

    permissions = []
    Ps = DBSession.query(Permission).order_by('permission')
    for P in Ps:
        permissions.append((P.permission, P.permission))

    f.permissions.choices = permissions
    # *************************************************

    if 'POST' == request.method:
        if f.validate():
            if 'add' == action:
                for P in f.permissions.data:
                    for M in f.request_methods.data:
                        RP = RoutePermission(route_name=f.route_name.data, method=M, permission=P)
                        DBSession.add(RP)

                request.session.flash("Route permissions created!")
                return HTTPFound(location=request.current_route_url())

    route_permissions = DBSession.query(RoutePermission).order_by(RoutePermission.route_name,
                                                                  RoutePermission.permission, RoutePermission.method)

    return dict(action=action, route_permissions=route_permissions, route_permissions_form=f)


@view_config(route_name='pyckauth_login', renderer='pyckauth_login.mako')
def login(request):

    login_form = LoginForm(request.POST)

    if 'POST' == request.method and login_form.validate():
        U = DBSession.query(User).filter_by(user_id=login_form.user_id.data).first()

        if hashlib.sha1(login_form.password.data).hexdigest() == U.password:

            request.session['logged_in_user'] = U.user_id

            #Get user permissions and store them into request.session['auth_user_permissions']
            user_permissions = []
            UPs = DBSession.query(UserPermission.permission).filter_by(user_id=U.user_id).all()
            for UP in UPs:
                user_permissions.append(UP[0])

            request.session['auth_user_permissions'] = user_permissions

            if request.session.get('came_from', None):
                return HTTPFound(location=request.session.get('came_from'))
            else:
                try:
                    return HTTPFound(location=request.route_url('adminadmin_index'))
                except Exception:
                    return HTTPFound(location=request.route_url('home'))
        else:
            request.session.flash("Authentication Failed! Invalid user ID or password")

    return dict(login_form=login_form)


@view_config(route_name='pyckauth_logout')
def logout(request):
    del request.session['logged_in_user']
    del request.session['auth_user_permissions']

    return HTTPFound(location=request.route_url('home'))
