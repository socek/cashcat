from cashcat.application.drivers import Command

from .dbmodels import UserData
from .query import UserQuery


class UserCommand(Command):
    model = UserData
    _query = UserQuery
