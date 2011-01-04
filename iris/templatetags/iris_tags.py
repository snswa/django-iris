from django.template import Library


register = Library()


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
def hasjoinedtopic(user, topic):
    """Return True if the user participates in the topic.

    Example::

        {% if user|hasjoinedtopic:topic %}
            <a href="...">Leave topic</a>
        {% endif %}
    """
    return topic.has_participant(user)
