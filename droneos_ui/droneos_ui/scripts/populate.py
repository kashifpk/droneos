import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

import importlib
import hashlib
from ..apps import enabled_apps
from .. import load_project_settings

from ..models import (
    DBSession,
    User,
    Permission,
    RoutePermission,
    UserPermission,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)

    load_project_settings()

    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    DBSession.autoflush = True
    Base.metadata.create_all(engine)
    with transaction.manager:

        #Authentication related basic user and permission setup
        if 0 == DBSession.query(User).count():
            DBSession.add(User('admin', hashlib.sha1('admin').hexdigest()))
            DBSession.flush()

        if 0 == DBSession.query(Permission).count():
            DBSession.add(Permission('admin', 'Manage administrative section'))
            DBSession.flush()

        if 0 == DBSession.query(UserPermission).count():
            DBSession.add(UserPermission('admin', 'admin'))
            DBSession.flush()

        if 0 == DBSession.query(RoutePermission).count():
            DBSession.add(RoutePermission('pyckauth_manager', 'ALL', 'admin'))
            DBSession.flush()

    #populate application models
    for app_name in enabled_apps:

        app_module = importlib.import_module("apps.%s.scripts.populate" % app_name)
        #print("App Module: %s\n" % app_module.__name__)

        try:
            app_module.populate_app(engine, DBSession)
        except Exception, e:
            print(repr(e))
