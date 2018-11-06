from cashcat.application.drivers import Command

from .dbmodels import GroupData
from .query import GroupQuery


class GroupCommand(Command):
    model = GroupData
    _query = GroupQuery
