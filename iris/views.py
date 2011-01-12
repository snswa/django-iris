from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from iris.conf import settings
from iris.forms import TopicForm
from iris.models import Item, Topic


# --- TOPICS ---


def topic(request, topic_id, slug=None, template_name="iris/topic.html", extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    topic = get_object_or_404(Topic, pk=topic_id)
    if not request.user.has_perm('iris.view_topic', topic):
        raise PermissionDenied()
    item_type_list = [
        dict(
            plugin=plugin,
            form=plugin.form_class(request=request, topic=topic),
            user_has_perm=plugin.user_has_perm(request.user, topic),
        )
        for plugin in settings.ITEM_TYPE_PLUGINS
    ]
    template_context = dict(
        topic=topic,
        item_type_list=item_type_list,
    )
    template_context.update(extra_context)
    return render_to_response(template_name, template_context, RequestContext(request))


def default_post_topic_create(request, topic, *args, **kwargs):
    topic.add_participant(creator=request.user, obj=request.user)


def topic_create(request, form_class=TopicForm, post_topic_create=default_post_topic_create,
                 template_name="iris/topic_create.html", extra_context=None, *args, **kwargs):
    if not request.user.has_perm('iris.add_topic'):
        raise PermissionDenied()
    extra_context = extra_context or {}
    if request.method == 'POST':
        topic_create_form = form_class(request.POST)
        if topic_create_form.is_valid():
            topic = topic_create_form.save(commit=False)
            topic.creator = request.user
            topic.save()
            post_topic_create(request, topic, *args, **kwargs)
            # attach get params
            url = '{0}?{1}'.format(topic.get_absolute_url(), request.GET.urlencode())
            return redirect(url)
    else:
        topic_create_form = form_class()
    template_context = dict(
        topic_create_form=topic_create_form,
    )
    template_context.update(extra_context)
    return render_to_response(template_name, template_context, RequestContext(request))


def topic_join(request, topic_id, *args, **kwargs):
    topic = get_object_or_404(Topic, pk=topic_id)
    destination = topic
    if request.method == 'POST':
        if not request.user.has_perm('iris.join_topic', topic):
            raise PermissionDenied()
        if not topic.has_participant(request.user):
            destination = topic.add_participant(request.user, request.user)
    url = '{0}?{1}'.format(destination.get_absolute_url(), request.GET.urlencode())
    return redirect(url)


def topics(request, template_name="iris/topics.html", form_class=TopicForm, queryset=None, queryset_fn=None, extra_context=None, *args, **kwargs):
    """Render a list of topics.

    Set `queryset_fn` to a function that accepts ``request, queryset, *args, **kwargs``
    if you would like to select topics other than the default `queryset`
    which is all topics in last-modified order.
    """
    extra_context = extra_context or {}
    if queryset is None:
        queryset = Topic.objects.order_by('modified')
    if callable(queryset_fn):
        queryset = queryset_fn(request, queryset, *args, **kwargs)
    topic_create_form = form_class()
    template_context = dict(
        topic_list=queryset,
        topic_create_form=topic_create_form,
    )
    template_context.update(extra_context)
    return render_to_response(template_name, template_context, RequestContext(request))


# --- ITEMS ---


def item_add(request, topic_id, plugin_name, template_name="iris/item_add.html", extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    topic = get_object_or_404(Topic, pk=topic_id)
    plugin = settings.ITEM_TYPE_PLUGINS_BY_NAME[plugin_name]
    if not request.user.has_perm('iris.add_to_topic', topic):
        raise PermissionDenied()
    if not plugin.user_has_perm(request.user, topic):
        raise PermissionDenied()
    form_class = plugin.form_class
    if request.method == 'POST':
        form = form_class(request.POST, request=request, topic=topic)
        if form.is_valid():
            item = form.save()
            if request.is_ajax():
                return HttpResponse('1', 'application/json')
            else:
                if item:
                    url = '{0}?{1}'.format(item.get_absolute_url(), request.GET.urlencode())
                else:
                    # Form saved, but due to duplicate data or other circumstance,
                    # no item was generated but no error state either, so
                    # redirect to topic.
                    url = '{0}?{1}'.format(topic.get_absolute_url(), request.GET.urlencode())
                return redirect(url)
    else:
        form = form_class(request=request, topic=topic)
    template_context = dict(
        topic=topic,
        item_type=dict(
            plugin=plugin,
            form=form,
            user_has_perm=plugin.user_has_perm(request.user, topic),
        ),
    )
    template_context.update(extra_context)
    # Just return the snippet for an AJAX request.
    if request.is_ajax():
        template_name = plugin.add_template
    return render_to_response(template_name, template_context, RequestContext(request))


def items_after(request, topic_id, after_item_id, template_name="iris/items_after.html", extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    topic = get_object_or_404(Topic, pk=topic_id)
    if not request.user.has_perm('iris.view_topic', topic):
        raise PermissionDenied()
    after_item = get_object_or_404(Item, pk=after_item_id, topic=topic)
    item_list = topic.items.filter(created__gt=after_item.created)
    template_context = dict(
        after_item=after_item,
        item_list=item_list,
    )
    template_context.update(extra_context)
    if request.is_ajax():
        bits = template_name.rsplit('.', 1)
        template_name = bits[0] + '_ajax.' + bits[1]
    return render_to_response(template_name, template_context, RequestContext(request))
