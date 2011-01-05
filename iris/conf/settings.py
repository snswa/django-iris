from django.conf import settings


# The order in which "add item" forms appear in the UI.
# Each item is in the the form of "appname.modelname", e.g.
# same as the contenttypes framework.
ADD_ITEM_TYPE_ORDER = getattr(settings, 'IRIS_ADD_ITEM_TYPE_ORDER', (
    'iris.participantjoin',
))
