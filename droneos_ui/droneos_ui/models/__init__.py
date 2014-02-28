from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

#from models import your_model_names_here
from auth import Permission, User, UserPermission, RoutePermission

# Place additional model names here for ease of importing.
__all__ = ['DBSession', 'Base', 'Permission', 'User', 'UserPermission', 'RoutePermission']
