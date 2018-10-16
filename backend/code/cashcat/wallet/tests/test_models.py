from uuid import uuid4

from pytest import mark

from cashcat.wallet.models import Wallet


class TestWallet(object):
    @mark.parametrize(
        "type, valid", (("private", True), ("vat", True), ("normal", False))
    )
    def test_wallet_type_validation(self, type, valid):
        try:
            Wallet(uuid4(), name="name", type=type, owner_uid=uuid4())
            assert valid is True
        except RuntimeError:
            assert valid is False
