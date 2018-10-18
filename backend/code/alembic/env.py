# flake8: noqa
from sapp.plugins.sqlalchemy.alembic import AlembicScript

from cashcat import app
from cashcat.application.drivers.dbmodel import SqlDataModel

# import or define all models here to ensure they are attached to the
# Model.metadata prior to any initialization routines

import cashcat.auth.drivers.dbmodels
import cashcat.wallet.drivers.dbmodels
import cashcat.bill.drivers.dbmodels

AlembicScript(app, SqlDataModel, "dbsession").run()
