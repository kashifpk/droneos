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
    db,
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
    db.configure(bind=engine)
    db.autoflush = True
    Base.metadata.create_all(engine)
    with transaction.manager:

        #Authentication related basic user and permission setup
        if 0 == db.query(User).count():
            db.add(User('admin', hashlib.sha1('admin').hexdigest()))
            db.flush()

        if 0 == db.query(Permission).count():
            db.add(Permission('admin', 'Manage administrative section'))
            db.flush()

        if 0 == db.query(UserPermission).count():
            db.add(UserPermission('admin', 'admin'))
            db.flush()

        if 0 == db.query(RoutePermission).count():
            db.add(RoutePermission('pyckauth_manager', 'ALL', 'admin'))
            db.flush()

    #populate application models
    for app_name in enabled_apps:

        app_module = importlib.import_module("apps.%s.scripts.populate" % app_name)
        #print("App Module: %s\n" % app_module.__name__)

        try:
            app_module.populate_app(engine, db)
        except Exception, e:
            print(repr(e))
