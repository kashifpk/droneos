from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension
from .. import project_package, APP_NAME

DBSession = project_package.models.DBSession


class RenameTables(DeclarativeMeta): 
    def __init__(cls, classname, bases, dict_): 
        if '__tablename__' in dict_: 
            cls.__tablename__ = dict_['__tablename__'] = APP_NAME + "_" + cls.__tablename__ 

        return DeclarativeMeta.__init__(cls, classname, bases, dict_)

Base = declarative_base(metaclass=RenameTables)


#from models import MyModel

__all__ = ['DBSession', 'Base',
           #'MyModel'
           ]


