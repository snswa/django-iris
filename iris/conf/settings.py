from django.conf import settings
from django.utils.importlib import import_module


# The order in which "add item" forms appear in the UI.
# Each item is in the the form of "module.name.ClassName"
# e.g. "iris.plugins.ParticipantJoinPlugin"
ITEM_TYPE_PLUGINS = getattr(settings, 'IRIS_ITEM_TYPE_PLUGINS', ())


# Now load all of the plugins.
ITEM_TYPE_PLUGINS_BY_NAME = {
    # plugin_class.name: plugin_class,
}
_ITEM_TYPE_PLUGINS = []
for name in ITEM_TYPE_PLUGINS:
    modname, classname = name.rsplit('.', 1)
    module = import_module(modname)
    plugin_class = getattr(module, classname)
    plugin = plugin_class()
    ITEM_TYPE_PLUGINS_BY_NAME[plugin.name] = plugin
    _ITEM_TYPE_PLUGINS.append(plugin)
ITEM_TYPE_PLUGINS = tuple(_ITEM_TYPE_PLUGINS)
del _ITEM_TYPE_PLUGINS
