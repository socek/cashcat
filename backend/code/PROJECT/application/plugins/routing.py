from sapp.plugins.pyramid.routing import Routing

from PROJECT.auth.routing import auth_routing


class CROJECTRouting(Routing):
    def make(self):
        auth_routing(self)
