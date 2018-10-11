from uuid import uuid4

from pytest import fixture
from pytest import raises
from sqlalchemy.orm.exc import NoResultFound

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

    # def test_get_by_id_when_not_exists(self, query):
    #     """
    #     .get_by_id should reaise NoResultFound when object with provided id
    #     does not exists
    #     """
    #     with raises(NoResultFound):
    #         query.get_by_id(uuid4())

    # def test_get_by_id_when_exists(self, query):
    #     """
    #     .get_by_id should return proper object, if object with provided id
    #     exists.
    #     """
    #     assert query.get_by_id(user.id).id == user.id
