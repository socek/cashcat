from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture

from cashcat.application.plugins.routing import CashcatRouting


class TestCashcatRouting(object):
    @fixture
    def madd(self):
        with patch.object(CashcatRouting, 'add') as mock:
            yield mock

    @fixture
    def mpyramid(self):
        return MagicMock()

    def test_routing(self, madd, mpyramid):
        """
        This is syntax check of the routing.
        """
        CashcatRouting(mpyramid).make()

        madd.assert_called()
