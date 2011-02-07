from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template import Library

from iris.models import Item, Topic


register = Library()


@register.filter
def activeparticipants(participants_qs):
    """Filter only active participants in a queryset of participants."""
    return participants_qs.filter(is_active=True)


@register.filter
def canaddtotopic(user, topic):
    """Return true if the user can add items to the topic."""
    return user.has_perm('iris.add_to_topic', obj=topic)


@register.filter
def canviewtopic(user, topic):
    """Return true if the user can view the topic.

    Example::

        {% if user|canviewtopic:topic %}
            <li>{{ topic.subject }}</li>
        {% endif %}
    """
    return user.has_perm('iris.view_topic', obj=topic)


@register.filter
def canjointopic(user, topic):
    """Return True if the user can participate in the topic.

    Example::

        {% if user|canjointopic:topic %}
            <a href="...">Join Topic</a>
        {% endif %}
    """
    return user.has_perm('iris.join_topic', obj=topic)


@register.filter
def hasjoinedtopic(obj, topic):
    """Return True if the object participates in the topic.

    Example::

        {% if user|hasjoinedtopic:topic %}
            <a href="...">Leave topic</a>
        {% endif %}
    """
    if not isinstance(obj, models.Model):
        return False
    return topic.has_participant(obj)


@register.filter
def itemreferencedby(obj):
    """Return the iris.item instance that references the given object as its content."""
    ct = ContentType.objects.get_for_model(obj)
    item = Item.objects.get(content_type=ct, object_id=obj.id)
    return item


@register.filter
def participantsoftype(obj, content_type_name=None):
    """Return a list of participant objects for a topic where
    the content object is of a certain type.

    Example::

        {% for participant in topic|participantsoftype:"teams.team" %}
            <li>{{ participant.content }} team</li>
        {% endfor %}
    """
    if content_type_name:
        return obj.participants_of_type(content_type_name)
    else:
        return obj.participants.all


@register.filter
def topicsjoined(obj):
    """Return a queryset containing Topic instances that obj participates in.

    Example::

        {% for topic in user|topicsjoined %}
            <li>{{ topic.subject }}</li>
        {% endfor %}
    """
    return Topic.objects.with_participant(obj)
