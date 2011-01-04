from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(
        regex=r'^$',
        view=redirect_to,
        kwargs=dict(
            url='/iris/',
        ),
    ),
    url(
        regex=r'^admin/',
        view=include(admin.site.urls),
    ),
    url(
        regex=r'^iris/',
        view=include('iris.urls'),
    ),
)

urlpatterns = urlpatterns + patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    ) if settings.DEBUG else urlpatterson

