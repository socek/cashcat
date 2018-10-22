from copy import deepcopy
from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

from pyramid.httpexceptions import HTTPBadRequest
# from pyramid.httpexceptions import HTTPNotFound
from pytest import fixture
from pytest import mark
from pytest import raises

# from cashcat.application.drivers.query import NoResultFound
from cashcat.application.testing import ViewFixture
# from cashcat.bill.models import Bill
# from cashcat.bill.views import BillView
from cashcat.bill.views import BillsView


class Fixtures(ViewFixture):
    @fixture
    def mquery(self, view):
        with patch.object(view, "bill_query") as mock:
            yield mock.return_value

    @fixture
    def mcommand(self, view):
        with patch.object(view, "bill_command") as mock:
            yield mock.return_value

    @fixture
    def mbill_query(self):
        with patch("cashcat.bill.views.BillQuery") as mock:
            yield mock

    @fixture
    def mbill_command(self):
        with patch("cashcat.bill.views.BillCommand") as mock:
            yield mock

    @fixture
    def mget_wallet(self, view):
        with patch.object(view, "_get_wallet") as mock:
            yield mock


class TestBillsView(Fixtures):

    bill_data = {
        "place": "Lidl",
        "billed_at": date(2018, 1, 2).isoformat(),
        "wallet_uid": str(uuid4()),
        "items": [
            {
                "name": "coke",
                "uid": str(uuid4()),
                "quantity": 1.14,
                "value": 1.15,
            }
        ]
    }

    @fixture
    def view(self, mroot_factory, mrequest):
        return BillsView(mroot_factory, mrequest)

    def test_get(self, view, mquery, mget_user, mget_wallet):
        """
        .get should return list of bills
        """
        bill_item = MagicMock()
        bill_item.uid = uuid4()
        bill_item.quantity = 1.4
        bill_item.value = 1.5
        bill_item.bill_uid = uuid4()
        bill = MagicMock()
        bill.uid = uuid4()
        bill.wallet_uid = uuid4()
        bill.items = [bill_item]
        mquery.list_for_wallet.return_value = [bill]
        assert view.get() == [
            {
                "uid": str(bill.uid),
                "place": str(bill.place),
                "billed_at": bill.billed_at.isoformat.return_value,
                "items": [
                    {
                        "uid": str(bill_item.uid),
                        "name": str(bill_item.name),
                        "quantity": Decimal("1.40"),
                        "value": Decimal("1.50"),
                    }
                ],
                "wallet_uid": str(bill.wallet_uid),
            }
        ]
        mquery.list_for_wallet.assert_called_once_with(mget_wallet.return_value)

    @mark.parametrize("key, value", (
        ["place", ""],
        ["place", None],
        ["billed_at", ""],
        ["billed_at", None],
    ))
    def test_put_empty(self, view, mget_user, mrequest, value, key):
        """
        .put should validate data from user and raise bad request on error
        """
        mrequest.json_body = deepcopy(self.bill_data)
        mrequest.json_body[key] = value

        with raises(HTTPBadRequest):
            view.put()

    @mark.parametrize("key", ["place", "billed_at"])
    def test_put_missing(self, view, mget_user, mrequest, key):
        """
        .put should validate data from user and raise bad request on error
        """
        mrequest.json_body = deepcopy(self.bill_data)
        del mrequest.json_body[key]

        with raises(HTTPBadRequest):
            view.put()

    @mark.parametrize("key, value", (
        ["name", ""],
        ["name", None],
        ["quantity", ""],
        ["quantity", None],
        ["quantity", "a"],
        ["value", ""],
        ["value", None],
        ["value", "a"],
    ))
    def test_put_empty_in_items(self, view, mget_user, mrequest, value, key):
        """
        .put should validate data from user and raise bad request on error
        """
        mrequest.json_body = deepcopy(self.bill_data)
        mrequest.json_body['items'][0][key] = value

        with raises(HTTPBadRequest):
            view.put()

    @mark.parametrize("key", ["name", "quantity", "value"])
    def test_put_missing_in_items(self, view, mget_user, mrequest, key):
        """
        .put should validate data from user and raise bad request on error
        """
        mrequest.json_body = deepcopy(self.bill_data)
        del mrequest.json_body['items'][0][key]

        with raises(HTTPBadRequest):
            view.put()

    def test_put(self, view, mcommand, mget_user, mrequest, mget_wallet):
        """
        .put should validate data from user and create new wallet
        """
        mget_wallet.return_value.uid = uuid4()
        mrequest.json_body = deepcopy(self.bill_data)
        print(mrequest.json_body)
        result = view.put()
        assert result["uid"]
        assert result["place"] == "Lidl"
        assert result["billed_at"] == "2018-01-02"
        assert result["wallet_uid"] == str(mget_wallet.return_value.uid)
        assert result["items"][0]["name"] == "coke"
