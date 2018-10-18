from cashcat.application.drivers import Command

from .dbmodels import BillData
from .query import BillQuery


class BillCommand(Command):
    model = BillData
    _query = BillQuery

