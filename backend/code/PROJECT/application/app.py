from sapp.plugins.logging import LoggingPlugin
from sapp.plugins.pyramid.configurator import ConfiguratorWithPyramid
from sapp.plugins.pyramid.plugins import RoutingPlugin
from sapp.plugins.settings import SettingsPlugin
from sapp.plugins.sqlalchemy.plugin import DatabasePlugin

from PROJECT.application.plugins.json import JsonPlugin
from PROJECT.application.plugins.redis import RedisPlugin
from PROJECT.application.plugins.routing import CROJECTRouting


class CROJECTConfigurator(ConfiguratorWithPyramid):
    def append_plugins(self):
        self.add_plugin(SettingsPlugin('PROJECT.application.settings'))
        self.add_plugin(LoggingPlugin())
        self.add_plugin(DatabasePlugin('dbsession'))
        self.add_plugin(RoutingPlugin(CROJECTRouting))
        self.add_plugin(RedisPlugin())
        self.add_plugin(JsonPlugin())
