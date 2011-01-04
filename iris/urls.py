from django.conf.urls.defaults import *


urlpatterns = patterns('iris.views',
    url(
        name=   'iris_topics',
        regex=  r'^$',
        view=   'topics',
    ),
    url(
        name=   'iris_topic_create',
        regex=  r'^create/$',
        view=   'topic_create',
    ),
    url(
        name=   'iris_topic',
        regex=  r'^(?P<topic_id>\d+)/read/$',
        view=   'topic',
    ),
    url(
        name=   'iris_topic_join',
        regex=  r'^(?P<topic_id>\d+)/join/$',
        view=   'topic_join',
    ),
    url(
        name=   'iris_topic_slug',
        regex=  r'^(?P<topic_id>\d+)/read/(?P<slug>[\w_-]+)/$',
        view=   'topic',
    ),
)
