from uuid import uuid4

from pytest import raises

from cashcat.application.drivers.query import NoResultFound
from cashcat.application.testing import IntegrationFixture
from cashcat.group.models import Group


class TestGroupDriver(IntegrationFixture):
    def test_list_for_owner(self, wallet, second_wallet, group_query, group_command):
        """
        .list_for_owner should return only list of wallet for that wallet
        """
        groups = [
            Group(uuid4(), name="my wallet1", wallet_uid=wallet.uid),
            Group(uuid4(), name="my wallet2", wallet_uid=wallet.uid),
            Group(
                uuid4(), name="my wallet3", wallet_uid=second_wallet.uid
            ),
        ]
        for group in groups:
            group_command.create(group)

        try:
            result = set([group.name for group in group_query.list_for_wallet(wallet)])
            assert result == set(["my wallet1", "my wallet2"])

            result = set(
                [group.name for group in group_query.list_for_wallet(second_wallet)]
            )
            assert result == set(["my wallet3"])
        finally:
            for group in groups:
                group_command.force_delete(group.uid)

    def test_get_active_by_uid_after_delete(self, wallet, group_query, group_command):
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

    def test_get_active_by_uid_with_wrong_owner(
        self, wallet, second_wallet, group_query, group_command
    ):
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
