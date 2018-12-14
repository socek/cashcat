from datetime import date
from uuid import uuid4

from pytest import fixture
from pytest import raises

from cashcat.application.drivers.query import NoResultFound
from cashcat.application.testing import IntegrationFixture
from cashcat.bill.models import Bill
from cashcat.bill.models import BillItem


class TestBillDriver(IntegrationFixture):
    @fixture
    def bill(self, wallet, group, bill_command):
        uid = uuid4()
        bill = Bill(
            uid, place="lidl", billed_at=date(2018, 1, 1), wallet_uid=wallet.uid
        )
        bill.add_item(uuid4(), name="cola", quantity=1, value=10, group_uid=group.uid)
        bill.add_item(
            uuid4(), name="celery", quantity=1.25, value=10, group_uid=group.uid
        )
        bill_command.create(bill)
        yield bill
        bill_command.force_delete(uid)

    def test_list_for_wallet(
        self, wallet, second_wallet, bill_query, bill_command, group
    ):
        """
        .list_for_wallet should return only list of bill for that wallet
        """
        bills = [
            Bill(
                uuid4(), place="lidl", billed_at=date(2018, 1, 2), wallet_uid=wallet.uid
            ),
            Bill(
                uuid4(),
                place="biedronka",
                billed_at=date(2018, 1, 3),
                wallet_uid=wallet.uid,
            ),
            Bill(
                uuid4(),
                place="tesco",
                billed_at=date(2018, 1, 4),
                wallet_uid=second_wallet.uid,
            ),
        ]
        for bill in bills:
            bill_command.create(bill)

        try:
            result = set(
                [bill.place for bill in bill_query.list_for_wallet(wallet.uid)]
            )
            assert result == set(["lidl", "biedronka"])

            result = set(
                [bill.place for bill in bill_query.list_for_wallet(second_wallet.uid)]
            )
            assert result == set(["tesco"])
        finally:
            for bill in bills:
                bill_command.force_delete(bill.uid)

    def test_list_for_wallet_summary(
        self, wallet, second_wallet, bill_query, bill_command, group
    ):
        """
        .list_for_wallet should compute total for each bill
        """
        first = Bill(
            uuid4(), place="lidl", billed_at=date(2018, 1, 2), wallet_uid=wallet.uid
        )
        first.add_item(uuid4(), name="cola", quantity=1, value=10, group_uid=group.uid)
        first.add_item(uuid4(), name="fanta", quantity=2, value=5, group_uid=group.uid)

        second = Bill(
            uuid4(),
            place="biedronka",
            billed_at=date(2018, 1, 3),
            wallet_uid=wallet.uid,
        )
        second.add_item(uuid4(), name="beer", quantity=6, value=1, group_uid=group.uid)
        second.add_item(
            uuid4(), name="wine", quantity=1, value=100, group_uid=group.uid
        )

        bills = [first, second]
        for bill in bills:
            bill_command.create(bill)

        try:
            result = {
                bill.place: bill for bill in bill_query.list_for_wallet(wallet.uid)
            }
            assert result["lidl"].total == 20
            assert result["biedronka"].total == 106
        finally:
            for bill in bills:
                bill_command.force_delete(bill.uid)

    def test_updating_total(
        self, wallet, second_wallet, bill_query, bill_command, group, dbsession
    ):
        """
        Updating items should update total values as well
        """
        update_item_uid = uuid4()
        remove_item_uid = uuid4()
        first = Bill(
            uuid4(), place="lidl", billed_at=date(2018, 1, 2), wallet_uid=wallet.uid
        )
        first.add_item(
            update_item_uid, name="cola", quantity=1, value=10, group_uid=group.uid
        )
        first.add_item(uuid4(), name="fanta", quantity=2, value=5, group_uid=group.uid)

        second = Bill(
            uuid4(),
            place="biedronka",
            billed_at=date(2018, 1, 3),
            wallet_uid=wallet.uid,
        )
        second.add_item(uuid4(), name="beer", quantity=6, value=1, group_uid=group.uid)
        second.add_item(
            remove_item_uid, name="wine", quantity=1, value=100, group_uid=group.uid
        )

        bills = [first, second]
        for bill in bills:
            bill_command.create(bill)

        bill_command.patch_by_uid(
            first.uid,
            create_items=[
                BillItem(
                    uid=uuid4(),
                    name="green up",
                    quantity=1,
                    value=5,
                    group_uid=group.uid,
                )
            ],
            items_update={update_item_uid: {"quantity": 2}},
        )

        bill_command.patch_by_uid(second.uid, remove_items=[remove_item_uid])

        dbsession.flush()

        try:
            result = {
                bill.place: bill for bill in bill_query.list_for_wallet(wallet.uid)
            }
            assert result["biedronka"].total == 6
            assert result["lidl"].total == 35
        finally:
            for bill in bills:
                bill_command.force_delete(bill.uid)

    def test_get_active_by_uid_after_delete(
        self, wallet, bill_query, bill_command, bill
    ):
        """
        .get_active_by_uid should return only not deleted object
        """
        assert bill_query.get_active_by_uid(bill.uid)

        bill_command.delete(bill.uid)

        with raises(NoResultFound):
            bill_query.get_active_by_uid(bill.uid)

    def test_get_active_by_uid_with_wrong_owner(
        self, wallet, second_wallet, bill_query, bill_command
    ):
        """
        .get_active_by_uid should return object only for wallet
        """
        uid = uuid4()
        bill = Bill(
            uid, place="lidl", billed_at=date(2018, 1, 2), wallet_uid=wallet.uid
        )
        bill_command.create(bill)

        try:
            assert bill_query.get_active_by_uid(uid, wallet.uid)

            bill_command.delete(uid)

            with raises(NoResultFound):
                bill_query.get_active_by_uid(uid, second_wallet.uid)
        finally:
            bill_command.force_delete(uid)

    def test_creating_with_items(self, wallet, bill_query, bill_command, group):
        """
        query and command should operate on bill items.
        """
        uid = uuid4()
        bill = Bill(
            uid, place="lidl", billed_at=date(2018, 1, 2), wallet_uid=wallet.uid
        )
        bill.add_item(uuid4(), name="cola", quantity=1, value=10, group_uid=group.uid)
        bill.add_item(
            uuid4(), name="celery", quantity=1.25, value=10, group_uid=group.uid
        )
        bill_command.create(bill)

        try:
            bill = bill_query.get_active_by_uid(
                uid, wallet_uid=wallet.uid, with_items=True
            )

            assert bill.place == "lidl"
            item_names = set([item.name for item in bill.items])
            assert set(["cola", "celery"]) == item_names
        finally:
            bill_command.force_delete(uid)

    def test_patch_by_uid_when_nothing(self, bill_command):
        """
        .patch_by_uid should raise an error when trying nothing to do
        """
        uid = uuid4()
        with raises(RuntimeError):
            bill_command.patch_by_uid(uid)

    def test_patch_by_uid(self, wallet, bill_query, bill_command, bill, group):
        """
        .patch_by_uid should update bill and items.
        """
        bill_update = {"place": "new place", "billed_at": date(2018, 2, 1)}
        create_items = [
            BillItem(None, name="sprite", quantity=2, value=3, group_uid=group.uid)
        ]
        remove_item_uid = bill.items[0].uid
        remove_items = [remove_item_uid]
        old_item_uid = bill.items[1].uid
        items_update = {old_item_uid: {"name": "fanta", "quantity": 2.25, "value": 100}}

        bill_command.patch_by_uid(
            bill.uid, bill_update, create_items, remove_items, items_update
        )

        bill = bill_query.get_active_by_uid(bill.uid, with_items=True)
        assert bill.place == "new place"
        assert bill.billed_at == "2018-02-01"
        assert len(bill.items) == 2
        items = {item.uid: item for item in bill.items}
        assert remove_item_uid not in items
        assert items[old_item_uid].name == "fanta"
        assert items[old_item_uid].quantity == 2.25
        assert items[old_item_uid].value == 100
        keys = list(items.keys())
        keys.remove(old_item_uid)
        new_item_uid = keys[0]
        assert items[new_item_uid].name == "sprite"
        assert items[new_item_uid].quantity == 2
        assert items[new_item_uid].value == 3

    def test_patch_by_uid_only_bill(self, wallet, bill_query, bill_command, bill):
        """
        .patch_by_uid should update bill and items.
        """
        bill_update = {"place": "new place", "billed_at": date(2018, 2, 1)}
        bill_command.patch_by_uid(bill.uid, bill_update)
        bill = bill_query.get_active_by_uid(bill.uid, with_items=True)
        assert bill.place == "new place"
        assert bill.billed_at == "2018-02-01"

    def test_patch_by_uid_only_bill_item(self, wallet, bill_query, bill_command, bill):
        """
        .patch_by_uid should update bill and items.
        """
        old_item_uid = bill.items[1].uid
        items_update = {old_item_uid: {"name": "fanta", "quantity": 2.25, "value": 100}}
        bill_command.patch_by_uid(bill.uid, items_update=items_update)

        bill = bill_query.get_active_by_uid(bill.uid, with_items=True)
        items = {item.uid: item for item in bill.items}
        assert items[old_item_uid].name == "fanta"
        assert items[old_item_uid].quantity == 2.25
        assert items[old_item_uid].value == 100
