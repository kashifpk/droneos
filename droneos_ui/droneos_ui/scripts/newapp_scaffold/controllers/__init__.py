from .. import APP_NAME, PROJECT_NAME, APP_BASE

from pyramid.events import subscriber
from pyramid.events import BeforeRender

#@subscriber(BeforeRender)
#def add_global(event):
#    event['PROJECT_NAME'] = PROJECT_NAME
#    event['APP_NAME'] = APP_NAME
#    event['APP_BASE'] = APP_BASE
