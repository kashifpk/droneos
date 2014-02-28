# This list contains all the enabled apps for the project, when you add a new app, add it to this list
# to make it accessible by the project.

import importlib

enabled_apps = []
PROJECT_NAME = 'droneos_ui'
project_package = importlib.import_module("droneos_ui")
