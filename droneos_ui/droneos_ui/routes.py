"""
Project routes
"""


def application_routes(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('contact', '/contact')
    config.add_route('add_route', '/routes/add')
    config.add_route('view_routes', '/routes/view')
    config.add_route('view_route', '/routes/view/{rname}')
    config.add_route('update_route', '/routes/update/{rname}')
    config.add_route('set_active', '/routes/setactive/{rname}')

    config.add_route('pyckauth_login', '/login')
    config.add_route('pyckauth_logout', '/logout')
    config.add_route('pyckauth_manager', '/auth')
    config.add_route('pyckauth_users', '/auth/users')
    config.add_route('pyckauth_permissions', '/auth/permissions')
    config.add_route('pyckauth_routes', '/auth/routes')
