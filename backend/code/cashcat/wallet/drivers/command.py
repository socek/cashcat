from cashcat.application.drivers import Command

from .dbmodels import WalletData
from .query import WalletQuery


class WalletCommand(Command):
    model = WalletData
    _query = WalletQuery
