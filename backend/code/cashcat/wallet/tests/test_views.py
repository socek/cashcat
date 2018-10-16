from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

from pyramid.httpexceptions import HTTPBadRequest
from pytest import fixture
from pytest import mark
from pytest import raises
from undecorated import undecorated

from cashcat.application.testing import ViewFixture
from cashcat.wallet.views import WalletView


class TestWalletView(ViewFixture):
    @fixture
    def view(self, mroot_factory, mrequest):
        return WalletView(mroot_factory, mrequest)

    @fixture
    def mquery(self, view):
        with patch.object(view, "query") as mock:
            yield mock.return_value

    @fixture
    def mcommand(self, view):
        with patch.object(view, "command") as mock:
            yield mock.return_value

    @fixture
    def mwallet_query(self):
        with patch("cashcat.wallet.views.WalletQuery") as mock:
            yield mock

    @fixture
    def mwallet_command(self):
        with patch("cashcat.wallet.views.WalletCommand") as mock:
            yield mock

    def test_get(self, view, mquery, mget_user):
        """
        .get should return list of wallets
        """
        wallet = MagicMock()
        wallet.uid = uuid4()
        wallet.owner_uid = uuid4()
        mquery.list_for_user.return_value = [wallet]
        assert view.get() == [
            {
                "name": str(wallet.name),
                "type": str(wallet.type),
                "uid": str(wallet.uid),
                "owner_uid": str(wallet.owner_uid),
            }
        ]

    @mark.parametrize("value", ["", None])
    def test_put_empty(self, view, mget_user, mrequest, value):
        """
        .put should validate data from user and raise bad request on error
        """
        mrequest.json_body = {"name": value}

        with raises(HTTPBadRequest):
            view.put()

    def test_put_missing(self, view, mget_user, mrequest):
        """
        .put should validate data from user and raise bad request on error
        """
        mrequest.json_body = {}

        with raises(HTTPBadRequest):
            view.put()

    def test_put(self, view, mcommand, mget_user, mrequest):
        """
        .put should validate data from user and create new wallet
        """
        mrequest.json_body = {"name": "myname"}
        result = view.put()
        assert result["uid"]
        assert result["name"] == "myname"
        assert result["type"] == "private"
        assert result["owner_uid"] == str(mget_user.return_value.uid)

    def test_query(self, view, mwallet_query, mwallet_command):
        """
        .query should return wallet query driver.
        """
        query = undecorated(view.query)
        db = MagicMock()
        assert query(None, dbsession=db) == mwallet_query.return_value
        mwallet_query.assert_called_once_with(db)

    def test_command(self, view, mwallet_command):
        """
        .command should return wallet command driver.
        """
        command = undecorated(view.command)
        db = MagicMock()
        assert command(None, dbsession=db) == mwallet_command.return_value
        mwallet_command.assert_called_once_with(db)
