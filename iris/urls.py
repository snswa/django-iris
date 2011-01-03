from django.conf.urls.defaults import *


urlpatterns = patterns('iris.views',
    url(
        name='iris_topics',
        regex=r'^$',
        view='topics',
        kwargs={},
    ),
    url(
        name='iris_topic_create',
        regex=r'^create/$',
        view='topic_create',
        kwargs={},
    ),
    url(
        name='iris_topic',
        regex=r'^(?P<topic_id>\d+)/$',
        view='topic',
        kwargs={},
    ),
    url(
        name='iris_topic_slug',
        regex=r'^(?P<topic_id>\d+)/(?P<slug>[\w_-]+)/$',
        view='topic',
        kwargs={},
    ),
)
