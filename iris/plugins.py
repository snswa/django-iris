from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms


class ItemTypePlugin(object):

    label = None
    name = None
    form_class = None

    @classmethod
    def css_class(cls):
        return cls.name.replace('.', '-')

    @classmethod
    def add_template(cls):
        return 'iris/items/{0}.html'.format(cls.name)


class ParticipantAddUserForm(forms.Form):

    username = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data['username']
        username = username.strip()
        if User.objects.filter(username=username).count() == 0:
            raise ValidationError('Could not find user by that name.')
        return username

    def save(self, request, topic):
        user = request.user
        other_user = User.objects.get(username=self.cleaned_data['username'])
        if not topic.has_participant(other_user):
            return topic.add_participant(
                creator=user,
                obj=other_user,
            )


class ParticipantAddUserPlugin(ItemTypePlugin):

    label = u'participant'
    name = 'iris.participantjoin.add.user'
    form_class = ParticipantAddUserForm
