from uuid import uuid4

from cashcat.application.testing import IntegrationFixture
from cashcat.wallet.models import Wallet


class TestWalletDriver(IntegrationFixture):
    def test_list_for_owner(self, user, second_user, wallet_query, wallet_command):
        """
        .list_for_owner should return only list of wallet for that user
        """
        wallets = [
            Wallet(uuid4(), name="my wallet1", type="normal", owner_uid=user.uid),
            Wallet(uuid4(), name="my wallet2", type="normal", owner_uid=user.uid),
            Wallet(uuid4(), name="my wallet3", type="normal", owner_uid=second_user.uid),
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
