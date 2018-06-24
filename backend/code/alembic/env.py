# flake8: noqa
from sapp.plugins.sqlalchemy.alembic import AlembicScript

from PROJECT import app
from PROJECT.application.model import Model

# import or define all models here to ensure they are attached to the
# Model.metadata prior to any initialization routines

import PROJECT.auth.models

AlembicScript(app, Model, 'dbsession').run()
