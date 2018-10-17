from sapp.decorators import WithContext

from cashcat import app


def driver(drv):
    @WithContext(app, args=["dbsession"])
    def make(self=None, dbsession=None):
        return drv(dbsession)

    return make
