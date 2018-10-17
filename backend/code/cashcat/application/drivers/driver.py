from sapp.decorators import WithContext

from cashcat import app


def driver(drv):
    @WithContext(app, args=["dbsession"])
    def make(dbsession):
        return drv(dbsession)

    return make
