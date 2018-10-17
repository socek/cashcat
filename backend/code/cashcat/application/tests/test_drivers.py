from unittest.mock import MagicMock
from unittest.mock import sentinel

from undecorated import undecorated

from cashcat.application.drivers import driver


class TestDriver(object):
    def test_driver(self):
        """
        driver function should create method which allow to init any driver.
        """
        query = MagicMock()
        result = driver(query)
        result = undecorated(result)
        assert result(sentinel.dbsession) == query.return_value
        query.assert_called_once_with(sentinel.dbsession)
