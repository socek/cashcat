from unittest.mock import MagicMock
from unittest.mock import patch

from pytest import fixture

from PROJECT.application.plugins.routing import CROJECTRouting


class TestCROJECTRouting(object):
    @fixture
    def madd(self):
        with patch.object(CROJECTRouting, 'add') as mock:
            yield mock

    @fixture
    def mpyramid(self):
        return MagicMock()

    def test_routing(self, madd, mpyramid):
        """
        This is syntax check of the routing.
        """
        CROJECTRouting(mpyramid).make()

        madd.assert_called()
