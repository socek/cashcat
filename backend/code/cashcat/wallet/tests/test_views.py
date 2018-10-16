from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

from pytest import fixture
from sapp.plugins.pyramid.testing import ViewFixtureMixin

from cashcat.wallet.views import WalletView


class TestWalletView(ViewFixtureMixin):
    @fixture
    def view(self, mroot_factory, mrequest):
        return WalletView(mroot_factory, mrequest)

    @fixture
    def mquery(self, view):
        with patch.object(view, "query") as mock:
            yield mock.return_value

    @fixture
    def mget_user(self, view):
        with patch.object(view, "get_user") as mock:
            yield mock

    @fixture
    def mwallet_query(self):
        with patch('cashcat.wallet.views.WalletQuery') as mock:
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

    def test_query(self, view, mwallet_query):
        """
        .query should return wallet query driver.
        """
        db = MagicMock()
        assert view.query(dbsession=db) == mwallet_query.return_value
        mwallet_query.assert_called_once_with(db)
