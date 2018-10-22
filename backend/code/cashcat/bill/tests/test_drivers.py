from datetime import datetime
from uuid import uuid4

from pytest import raises

from cashcat.application.drivers.query import NoResultFound
from cashcat.application.testing import IntegrationFixture
from cashcat.bill.models import Bill


class TestBillDriver(IntegrationFixture):
    def test_list_for_wallet(self, wallet, second_wallet, bill_query, bill_command):
        """
        .list_for_wallet should return only list of bill for that wallet
        """
        bills = [
            Bill(
                uuid4(),
                place="lidl",
                billed_at=datetime.utcnow(),
                wallet_uid=wallet.uid,
            ),
            Bill(
                uuid4(),
                place="biedronka",
                billed_at=datetime.utcnow(),
                wallet_uid=wallet.uid,
            ),
            Bill(
                uuid4(),
                place="tesco",
                billed_at=datetime.utcnow(),
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

    def test_get_active_by_uid_after_delete(self, wallet, bill_query, bill_command):
        """
        .get_active_by_uid should return only not deleted object
        """
        uid = uuid4()
        bill = Bill(
            uid, place="lidl", billed_at=datetime.utcnow(), wallet_uid=wallet.uid
        )
        bill_command.create(bill)

        try:
            assert bill_query.get_active_by_uid(uid)

            bill_command.delete(uid)

            with raises(NoResultFound):
                bill_query.get_active_by_uid(uid)
        finally:
            bill_command.force_delete(uid)

    def test_get_active_by_uid_with_wrong_owner(
        self, wallet, second_wallet, bill_query, bill_command
    ):
        """
        .get_active_by_uid should return object only for wallet
        """
        uid = uuid4()
        bill = Bill(
            uid, place="lidl", billed_at=datetime.utcnow(), wallet_uid=wallet.uid
        )
        bill_command.create(bill)

        try:
            assert bill_query.get_active_by_uid(uid, wallet.uid)

            bill_command.delete(uid)

            with raises(NoResultFound):
                bill_query.get_active_by_uid(uid, second_wallet.uid)
        finally:
            bill_command.force_delete(uid)

    def test_creating_with_items(self, wallet, bill_query, bill_command):
        """
        query and command should operate on bill items.
        """
        uid = uuid4()
        bill = Bill(
            uid, place="lidl", billed_at=datetime.utcnow(), wallet_uid=wallet.uid
        )
        bill.add_item(uuid4(), name="cola", quantity=1, value=10)
        bill.add_item(uuid4(), name="celery", quantity=1.25, value=10)
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
