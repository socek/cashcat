from pytest import fixture

from cashcat.application.testing import IntegrationFixture
from cashcat.auth.drivers import UserCommand
from cashcat.auth.drivers import UserQuery


class TestBaseDrivers(IntegrationFixture):
    """
    In order to test base drivers, we need to use any drivers that inherits
    from normal Query and Command class. User should be good enought.
    """
    @fixture
    def query(self, app):
        return UserQuery(app.dbsession)

    @fixture
    def command(self, app):
        return UserCommand(app.dbsession)

