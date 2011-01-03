from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _

from iris.forms import TopicForm
from iris.models import Topic


def topic(request, topic_id, slug=None, template_name="iris/topic.html", extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    topic = get_object_or_404(Topic, pk=topic_id)
    template_context = dict(
        extra_context,
        topic=topic,
    )
    return render_to_response(template_name, template_context, RequestContext(request))


@login_required
def topic_create(request, form_class=TopicForm, template_name="iris/topic_create.html", extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    if request.method == 'POST':
        topic_create_form = form_class(request.POST)
        if topic_create_form.is_valid():
            topic = topic_create_form.save(commit=False)
            topic.creator = request.user
            topic.save()
            topic.add_participant(request.user, request.user)
            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        topic_create_form = form_class()
    template_context = dict(
        extra_context,
        topic_create_form=topic_create_form,
    )
    return render_to_response(template_name, template_context, RequestContext(request))


def topics(request, template_name="iris/topics.html", extra_context=None, *args, **kwargs):
    extra_context = extra_context or {}
    topic_list = Topic.objects.order_by('-modified')
    template_context = dict(
        extra_context,
        topic_list=topic_list,
    )
    return render_to_response(template_name, template_context, RequestContext(request))
