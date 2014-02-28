from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    )
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from . import DBSession, Base


# RBAC models
class Permission(Base):
    __tablename__ = 'permissions'

    permission = Column(Unicode(100), primary_key=True)
    description = Column(Unicode(250))

    def __init__(self, permission='', description=''):
        self.permission = permission
        self.description = description


class RoutePermission(Base):
    __tablename__ = 'route_permissions'

    route_name = Column(Unicode(200), primary_key=True)
    method = Column(Unicode(30), default=u'ALL', primary_key=True)
    permission = Column(Unicode(100), ForeignKey(Permission.permission), primary_key=True)

    def __init__(self, route_name='', method='', permission=''):
        self.route_name = route_name
        self.method = method
        self.permission = permission


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Unicode(100), primary_key=True)
    password = Column(Unicode(40))

    def __init__(self, user_id='', password=''):
        self.user_id = user_id
        self.password = password


class UserPermission(Base):
    __tablename__ = 'user_permissions'

    user_id = Column(Unicode(100), ForeignKey(User.user_id), primary_key=True)
    permission = Column(Unicode(100), ForeignKey(Permission.permission), primary_key=True)

    user = relationship(User, backref=backref('permissions'))

    def __init__(self, user_id='', permission=''):
        self.user_id = user_id
        self.permission = permission
