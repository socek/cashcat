from sapp.plugins.pyramid.routing import Routing

from cashcat.auth.routing import auth_routing


class CashcatRouting(Routing):
    def make(self):
        auth_routing(self)
