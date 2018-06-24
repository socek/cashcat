from PROJECT.application.settings.default import default
from PROJECT.application.settings.pyramid import pyramid_specific
from PROJECT.application.settings.tests import tests_specific


def pyramid():
    settings = default()
    pyramid_specific(settings)
    return settings


def command():
    return default()


def tests():
    settings = default()
    pyramid_specific(settings)
    tests_specific(settings)
    return settings
