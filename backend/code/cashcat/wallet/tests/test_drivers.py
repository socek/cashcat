from uuid import uuid4

from pytest import raises

from cashcat.application.drivers.query import NoResultFound
from cashcat.application.testing import IntegrationFixture
from cashcat.wallet.models import Wallet


class TestWalletDriver(IntegrationFixture):
    def test_list_for_owner(self, user, second_user, wallet_query, wallet_command):
        """
        .list_for_owner should return only list of wallet for that user
        """
        wallets = [
            Wallet(uuid4(), name="my wallet1", type="private", owner_uid=user.uid),
            Wallet(uuid4(), name="my wallet2", type="private", owner_uid=user.uid),
            Wallet(
                uuid4(), name="my wallet3", type="private", owner_uid=second_user.uid
            ),
        ]
        for wallet in wallets:
            wallet_command.create(wallet)

        try:
            result = set([wallet.name for wallet in wallet_query.list_for_owner(user)])
            assert result == set(["my wallet1", "my wallet2"])

            result = set(
                [wallet.name for wallet in wallet_query.list_for_owner(second_user)]
            )
            assert result == set(["my wallet3"])
        finally:
            for wallet in wallets:
                wallet_command.force_delete(wallet.uid)

    def test_get_active_by_uid_after_delete(self, user, wallet_query, wallet_command):
        """
        .get_active_by_uid should return only not deleted object
        """
        uid = uuid4()
        wallet = Wallet(uid, name="my wallet1", type="private", owner_uid=user.uid)
        wallet_command.create(wallet)

        try:
            assert wallet_query.get_active_by_uid(uid)

            wallet_command.delete(uid)

            with raises(NoResultFound):
                wallet_query.get_active_by_uid(uid)
        finally:
            wallet_command.force_delete(uid)

    def test_get_active_by_uid_with_wrong_owner(
        self, user, second_user, wallet_query, wallet_command
    ):
        """
        .get_active_by_uid should return object only for owner
        """
        uid = uuid4()
        wallet = Wallet(uid, name="my wallet1", type="private", owner_uid=user.uid)
        wallet_command.create(wallet)

        try:
            assert wallet_query.get_active_by_uid(uid, user.uid)

            wallet_command.delete(uid)

            with raises(NoResultFound):
                wallet_query.get_active_by_uid(uid, second_user.uid)
        finally:
            wallet_command.force_delete(uid)
