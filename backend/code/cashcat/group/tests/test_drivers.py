from datetime import date
from uuid import uuid4

from pytest import fixture
from pytest import raises

from cashcat.application.drivers.query import NoResultFound
from cashcat.application.testing import IntegrationFixture
from cashcat.bill.models import Bill
from cashcat.group.models import Group


class TestGroupDriver(IntegrationFixture):
    def test_list_for_owner(self, wallet, second_wallet, group_query,
                            group_command):
        """
        .list_for_owner should return only list of wallet for that wallet
        """
        groups = [
            Group(uuid4(), name="my wallet1", wallet_uid=wallet.uid),
            Group(uuid4(), name="my wallet2", wallet_uid=wallet.uid),
            Group(uuid4(), name="my wallet3", wallet_uid=second_wallet.uid),
        ]
        for group in groups:
            group_command.create(group)

        try:
            result = set(
                [group.name for group in group_query.list_for_wallet(wallet)])
            assert result == set(["my wallet1", "my wallet2"])

            result = set([
                group.name
                for group in group_query.list_for_wallet(second_wallet)
            ])
            assert result == set(["my wallet3"])
        finally:
            for group in groups:
                group_command.force_delete(group.uid)

    def test_get_active_by_uid_after_delete(self, wallet, group_query,
                                            group_command):
        """
        .get_active_by_uid should return only not deleted object
        """
        uid = uuid4()
        group = Group(uid, name="my group1", wallet_uid=wallet.uid)
        group_command.create(group)

        try:
            assert group_query.get_active_by_uid(uid)

            group_command.delete(uid)

            with raises(NoResultFound):
                group_query.get_active_by_uid(uid)
        finally:
            group_command.force_delete(uid)

    def test_get_active_by_uid_with_wrong_owner(self, wallet, second_wallet,
                                                group_query, group_command):
        """
        .get_active_by_uid should return object only for owner
        """
        uid = uuid4()
        group = Group(uid, name="my group1", wallet_uid=wallet.uid)
        group_command.create(group)

        try:
            assert group_query.get_active_by_uid(uid, wallet.uid)

            group_command.delete(uid)

            with raises(NoResultFound):
                group_query.get_active_by_uid(uid, second_wallet.uid)
        finally:
            group_command.force_delete(uid)


class TestGroupSummary(IntegrationFixture):
    @fixture(scope="class", autouse=True)
    def base(self, group, second_group, wallet, bill_command):
        uuids = []
        bill = Bill(
            uuid4(),
            place="lidl",
            billed_at=date(2018, 1, 2),
            wallet_uid=wallet.uid)
        bill.add_item(
            uuid4(), name="cola", quantity=1, value=10, group_uid=group.uid)
        bill.add_item(
            uuid4(),
            name="celery",
            quantity=1.25,
            value=10,
            group_uid=group.uid)
        bill_command.create(bill)
        uuids.append(bill.uid)

        bill = Bill(
            uuid4(),
            place="biedronka",
            billed_at=date(2018, 1, 3),
            wallet_uid=wallet.uid)
        bill.add_item(
            uuid4(), name="cola", quantity=1, value=10, group_uid=group.uid)
        bill.add_item(
            uuid4(),
            name="celery",
            quantity=1.25,
            value=10,
            group_uid=group.uid)
        bill_command.create(bill)
        uuids.append(bill.uid)

        bill = Bill(
            uuid4(),
            place="kaufland",
            billed_at=date(2018, 1, 4),
            wallet_uid=wallet.uid)
        bill.add_item(
            uuid4(),
            name="cola",
            quantity=1,
            value=10,
            group_uid=second_group.uid)
        bill.add_item(
            uuid4(),
            name="celery",
            quantity=1.25,
            value=10,
            group_uid=second_group.uid)
        bill_command.create(bill)
        uuids.append(bill.uid)

        yield uuids

        for uid in uuids:
            bill_command.force_delete(uid)

    def test_for_one_day(self, group_query, wallet):
        """
        .summary_for_period should count summary for one day if needed
        """
        result = group_query.summary_for_period(wallet.uid, date(2018, 1, 2),
                                                date(2018, 1, 2))
        assert result == [('Group1', 22.5, 2)]

    def test_for_two_days(self, group_query, wallet):
        """
        .summary_for_period should count summary for two days if needed
        """
        result = group_query.summary_for_period(wallet.uid, date(2018, 1, 2),
                                                date(2018, 1, 3))
        assert result == [('Group1', 45, 4)]

    def test_for_three_days(self, group_query, wallet):
        """
        .summary_for_period should count summary for all days if needed
        """
        result = group_query.summary_for_period(wallet.uid, date(2018, 1, 2),
                                                date(2018, 1, 4))
        assert sorted(result) == [('Group1', 45, 4), ('Group2', 22.5, 2)]

    def test_for_none_products(self, group_query, wallet):
        """
        .summary_for_period should return empty list if no bills found on the given period
        """
        result = group_query.summary_for_period(wallet.uid, date(2018, 1, 5),
                                                date(2018, 1, 10))
        assert result == []
