from sapp.plugins.logging import LoggingPlugin
from sapp.plugins.pyramid.configurator import ConfiguratorWithPyramid
from sapp.plugins.pyramid.plugins import RoutingPlugin
from sapp.plugins.settings import SettingsPlugin
from sapp.plugins.sqlalchemy.plugin import DatabasePlugin

from cashcat.application.plugins.json import JsonPlugin
from cashcat.application.plugins.redis import RedisPlugin
from cashcat.application.plugins.routing import CashcatRouting


class CashcatConfigurator(ConfiguratorWithPyramid):
    def append_plugins(self):
        self.add_plugin(SettingsPlugin('cashcat.application.settings'))
        self.add_plugin(LoggingPlugin())
        self.add_plugin(DatabasePlugin('dbsession'))
        self.add_plugin(RoutingPlugin(CashcatRouting))
        self.add_plugin(RedisPlugin())
        self.add_plugin(JsonPlugin())
