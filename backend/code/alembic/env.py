# flake8: noqa
from sapp.plugins.sqlalchemy.alembic import AlembicScript

from cashcat import app
from cashcat.application.model import Model

# import or define all models here to ensure they are attached to the
# Model.metadata prior to any initialization routines

import cashcat.auth.models

AlembicScript(app, Model, 'dbsession').run()
