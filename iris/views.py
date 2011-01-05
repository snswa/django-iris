from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from iris.forms import TopicForm
from iris.models import Topic


def topic(request, topic_id, slug=None, template_name="iris/topic.html", extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    topic = get_object_or_404(Topic, pk=topic_id)
    if not request.user.has_perm('iris.view_topic', topic):
        raise PermissionDenied()
    template_context = dict(
        extra_context,
        topic=topic,
    )
    return render_to_response(template_name, template_context, RequestContext(request))


def topic_create(request, form_class=TopicForm, template_name="iris/topic_create.html", extra_context=None, *args, **kwargs):
    if not request.user.has_perm('iris.add_topic'):
        raise PermissionDenied()
    extra_context = extra_context or {}
    if request.method == 'POST':
        topic_create_form = form_class(request.POST)
        if topic_create_form.is_valid():
            topic = topic_create_form.save(commit=False)
            topic.creator = request.user
            topic.save()
            topic.add_participant(request.user, request.user)
            return redirect(topic)
    else:
        topic_create_form = form_class()
    template_context = dict(
        extra_context,
        topic_create_form=topic_create_form,
    )
    return render_to_response(template_name, template_context, RequestContext(request))


def topic_join(request, topic_id, *args, **kwargs):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        if not request.user.has_perm('iris.join_topic', topic):
            raise PermissionDenied()
        if not topic.has_participant(request.user):
            topic.add_participant(request.user, request.user)
    return redirect(topic)


def topics(request, template_name="iris/topics.html", form_class=TopicForm, extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    topic_list = Topic.objects.order_by('modified')
    topic_create_form = form_class()
    template_context = dict(
        extra_context,
        topic_list=topic_list,
        topic_create_form=topic_create_form,
    )
    return render_to_response(template_name, template_context, RequestContext(request))
