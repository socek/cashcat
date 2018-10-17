from unittest.mock import MagicMock
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

    def test_is_accessible_by(self):
        """
        .is_accessible_by should return True if the uid of the user and .owner_uid does match
        """
        user = MagicMock()
        user.uid = uuid4()
        wallet = Wallet(uuid4(), name="name", type="private", owner_uid=user.uid)
        assert wallet.is_accessible_by(user) is True

    def test_is_accessible_by_when_failed(self):
        """
        .is_accessible_by should return False if the uid of the user and .owner_uid does not match
        """
        user = MagicMock()
        user.uid = uuid4()
        wallet = Wallet(uuid4(), name="name", type="private", owner_uid=uuid4())
        assert wallet.is_accessible_by(user) is False
