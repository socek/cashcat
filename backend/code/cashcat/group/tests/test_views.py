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
from cashcat.group.models import Group
from cashcat.group.views import GroupView
from cashcat.group.views import GroupsView


class Fixtures(ViewFixture):
    @fixture
    def mquery(self, view):
        with patch.object(view, "group_query") as mock:
            yield mock.return_value

    @fixture
    def mcommand(self, view):
        with patch.object(view, "group_command") as mock:
            yield mock.return_value

    @fixture
    def mgroup_query(self):
        with patch("cashcat.group.views.GroupQuery") as mock:
            yield mock

    @fixture
    def mgroup_command(self):
        with patch("cashcat.group.views.GroupCommand") as mock:
            yield mock

    @fixture
    def mget_wallet(self, view):
        with patch.object(view, "_get_wallet") as mock:
            mock.return_value.uid = uuid4()
            yield mock


class TestGroupsView(Fixtures):
    @fixture
    def view(self, mroot_factory, mrequest):
        return GroupsView(mroot_factory, mrequest)

    def test_get(self, view, mquery, mget_wallet):
        """
        .get should return list of groups
        """
        group = MagicMock()
        group.uid = uuid4()
        group.wallet_uid = uuid4()
        mquery.list_for_wallet.return_value = [group]
        assert view.get() == [
            {
                "name": str(group.name),
                "uid": str(group.uid),
                "wallet_uid": str(group.wallet_uid),
            }
        ]

    @mark.parametrize("value", ["", None])
    def test_put_empty(self, view, mget_wallet, mrequest, value):
        """
        .put should validate data from user and raise bad request on error
        """
        mrequest.json_body = {"name": value}

        with raises(HTTPBadRequest):
            view.put()

    def test_put_missing(self, view, mget_wallet, mrequest):
        """
        .put should validate data from user and raise bad request on error
        """
        mrequest.json_body = {}

        with raises(HTTPBadRequest):
            view.put()

    def test_put(self, view, mcommand, mget_wallet, mrequest):
        """
        .put should validate data from user and create new group
        """
        mrequest.json_body = {"name": "myname"}
        result = view.put()
        assert result["uid"]
        assert result["name"] == "myname"
        assert result["wallet_uid"] == str(mget_wallet.return_value.uid)


class TestGroupView(Fixtures):
    @fixture
    def view(self, mroot_factory, mrequest):
        return GroupView(mroot_factory, mrequest)

    @fixture
    def mget_group(self, view):
        with patch.object(view, "_get_group") as mock:
            yield mock

    def test_validate(self, view, mget_user, mget_wallet, mget_group):
        """
        .validate should do nothing when everything is ok
        """
        assert view.validate() is None

    def test_get(self, view, mget_group):
        """
        .get should return serialized group data
        """
        group = Group(uid=uuid4(), name="my name", wallet_uid=uuid4())
        mget_group.return_value = group

        assert view.get() == {
            "uid": str(group.uid),
            "name": "my name",
            "wallet_uid": str(group.wallet_uid),
        }

    def test_patch(self, view, mget_group, mrequest, mcommand):
        """
        .patch should update group data
        """
        uid = str(uuid4())
        wallet_uid = str(uuid4())
        mrequest.json_body = {"name": "new name"}
        mrequest.matchdict = {"group_uid": uid, "wallet_uid": wallet_uid}

        view.patch()

        mcommand.update_by_uid.assert_called_once_with(uid, {"name": "new name"})

    def test_get_group(self, view, mquery, mrequest, mget_wallet):
        """
        ._get_group should return group object found by uid from url
        """
        uid = str(uuid4())
        wallet_uid = str(mget_wallet.return_value.uid)
        mrequest.matchdict = {"group_uid": uid, "wallet_uid": wallet_uid}

        assert view._get_group() == mquery.get_active_by_uid.return_value
        mquery.get_active_by_uid.assert_called_once_with(
            uid, str(mget_wallet.return_value.uid)
        )

    def test_get_group_when_not_found(self, view, mquery, mrequest, mget_wallet):
        """
        ._get_group should raise HTTPNotFound when query raises NoResultFound
        """
        uid = str(uuid4())
        wallet_uid = str(mget_wallet.return_value.uid)
        mrequest.matchdict = {"group_uid": uid, "wallet_uid": wallet_uid}
        mquery.get_active_by_uid.side_effect = NoResultFound()

        with raises(HTTPNotFound):
            view._get_group()

        mquery.get_active_by_uid.assert_called_once_with(
            uid, str(mget_wallet.return_value.uid)
        )
