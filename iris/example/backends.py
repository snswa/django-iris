from django.contrib.auth.models import User

from iris.models import Participant


class ContrivedBackend(object):
    """A contrived authentication backend."""

    supports_object_permissions = True
    supports_anonymous_user = True

    def has_perm(self, user_obj, perm, obj=None):
        # Anonymous users can view everything except for topics clara has joined.
        if not user_obj.is_authenticated():
            if perm == 'iris.view_topic':
                if obj is None:
                    return True
                else:
                    clara = User.objects.get(username='clara')
                    return not obj.has_participant(clara)
