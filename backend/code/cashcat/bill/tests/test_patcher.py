from uuid import uuid4

from datetime import date
from pytest import fixture

from cashcat.bill.models import Bill
from cashcat.bill.patcher import BillPatcher


class TestPatcher(object):
    @fixture
    def bill_uid(self):
        return uuid4()

    @fixture
    def first_item_uid(self):
        return uuid4()

    @fixture
    def second_item_uid(self):
        return uuid4()

    @fixture
    def third_item_uid(self):
        return uuid4()

    @fixture
    def old_bill(self, bill_uid, first_item_uid, second_item_uid, third_item_uid):
        bill = Bill(uid=bill_uid, place="place", billed_at="2018-01-01")
        bill.add_item(first_item_uid, "red", 1.0, 2.0)
        bill.add_item(second_item_uid, "green", 2.0, 4.0)
        bill.add_item(third_item_uid, "blue", 3.0, 6.0)
        return bill

    @fixture
    def new_bill(self, bill_uid, first_item_uid, second_item_uid, third_item_uid):
        bill = Bill(uid=bill_uid, place="place", billed_at=date(2018, 1, 1))
        bill.add_item(first_item_uid, "red", 1.0, 2.0)
        bill.add_item(second_item_uid, "green", 2.0, 4.0)
        bill.add_item(third_item_uid, "blue", 3.0, 6.0)
        return bill

    @fixture
    def patcher(self, old_bill, new_bill):
        return BillPatcher(old_bill, new_bill)

    def test_no_changes(self, patcher):
        """
        Patcher should return empty lists when no changes found.
        """
        assert patcher.make() == ({}, [], [], {})

    def test_bill_changes(self, patcher, new_bill):
        """
        Patcher should create diff for bill when there are changes.
        """
        new_bill.place = "another place"
        new_bill.billed_at = date(2018, 1, 2)

        assert patcher.make() == (
            {"place": "another place", "billed_at": date(2018, 1, 2)},
            [],
            [],
            {},
        )

    def test_new_bill_items(self, patcher, new_bill):
        """
        Patcher should create list of newly created bill items.
        """
        item = new_bill.add_item(None, "yellow", 4.0, 8.0)

        assert patcher.make() == ({}, [item], [], {})

    def test_removing_bill_items(self, patcher, new_bill):
        """
        Patcher should create list of removed bill items uids.
        """
        item = new_bill.items.pop(2)

        assert patcher.make() == ({}, [], [item.uid], {})

    def test_changing_bill_items(self, patcher, new_bill):
        """
        Patcher should create dict of diffs of changes for bill items.
        """
        item = new_bill.items[2]
        item.name = "new"
        item.quantity = 10
        item.value = 20

        assert patcher.make() == (
            {},
            [],
            [],
            {item.uid: {"name": "new", "quantity": 10, "value": 20}},
        )
