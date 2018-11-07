from sapp.plugins.pyramid.routing import Routing

from cashcat.auth.routing import auth_routing
from cashcat.bill.routing import bill_routing
from cashcat.group.routing import group_routing
from cashcat.wallet.routing import wallet_routing


class CashcatRouting(Routing):
    def make(self):
        auth_routing(self)
        wallet_routing(self)
        bill_routing(self)
        group_routing(self)
