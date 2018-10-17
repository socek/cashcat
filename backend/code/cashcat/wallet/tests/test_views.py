from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPNotFound
from pytest import fixture
from pytest import mark
from pytest import raises

from cashcat.application.drivers.query import NoResultFound
from cashcat.application.testing import ViewFixture
from cashcat.wallet.models import Wallet
from cashcat.wallet.views import WalletView
from cashcat.wallet.views import WalletsView


class Fixtures(ViewFixture):
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


class TestWalletsView(Fixtures):
    @fixture
    def view(self, mroot_factory, mrequest):
        return WalletsView(mroot_factory, mrequest)

    def test_get(self, view, mquery, mget_user):
        """
        .get should return list of wallets
        """
        wallet = MagicMock()
        wallet.uid = uuid4()
        wallet.owner_uid = uuid4()
        mquery.list_for_owner.return_value = [wallet]
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


class TestWalletView(Fixtures):
    @fixture
    def view(self, mroot_factory, mrequest):
        return WalletView(mroot_factory, mrequest)

    @fixture
    def mget_wallet(self, view):
        with patch.object(view, "_get_wallet") as mock:
            yield mock

    def test_validate_when_wallet_is_not_accessible_by_user(
        self, view, mget_user, mget_wallet
    ):
        """
        .validate should raise HTTPNotFound when wallet is not accessible by the
        current logged in user
        """
        mget_wallet.return_value.is_accessible_by.return_value = False

        with raises(HTTPNotFound):
            view.validate()

    def test_validate(self, view, mget_user, mget_wallet):
        """
        .validate should do nothing when everything is ok
        """
        assert view.validate() is None

    def test_get(self, view, mget_wallet):
        """
        .get should return serialized wallet data
        """
        wallet = Wallet(uid=uuid4(), name="my name", type="private", owner_uid=uuid4())
        mget_wallet.return_value = wallet

        assert view.get() == {
            "uid": str(wallet.uid),
            "name": "my name",
            "type": "private",
            "owner_uid": str(wallet.owner_uid),
        }

    def test_patch(self, view, mget_wallet, mrequest, mcommand):
        """
        .patch should update wallet data
        """
        uid = str(uuid4())
        mrequest.json_body = {"name": "new name"}
        mrequest.matchdict = {"wallet_uid": uid}

        view.patch()

        mcommand.update_by_uid.assert_called_once_with(uid, {"name": "new name"})

    def test_get_wallet(self, view, mquery, mrequest):
        """
        ._get_wallet should return wallet object found by uid from url
        """
        uid = str(uuid4())
        mrequest.matchdict = {"wallet_uid": uid}

        assert view._get_wallet() == mquery.get_by_uid.return_value
        mquery.get_by_uid.assert_called_once_with(uid)

    def test_get_wallet_when_not_found(self, view, mquery, mrequest):
        """
        ._get_wallet should raise HTTPNotFound when query raises NoResultFound
        """
        uid = str(uuid4())
        mrequest.matchdict = {"wallet_uid": uid}
        mquery.get_by_uid.side_effect = NoResultFound()

        with raises(HTTPNotFound):
            view._get_wallet()

        mquery.get_by_uid.assert_called_once_with(uid)
