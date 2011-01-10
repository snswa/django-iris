from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from iris.base import ItemTypePlugin, PluginForm


class ParticipantAddUserForm(PluginForm):

    username = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data['username']
        username = username.strip()
        if User.objects.filter(username=username).count() == 0:
            raise ValidationError('Could not find user by that name.')
        return username

    def save(self):
        user = self._request.user
        other_user = User.objects.get(username=self.cleaned_data['username'])
        if not self._topic.has_participant(other_user):
            return self._topic.add_participant(
                creator=user,
                obj=other_user,
            )


class ParticipantAddUserPlugin(ItemTypePlugin):

    label = u'participant'
    name = 'iris.participantjoin.add.user'
    form_class = ParticipantAddUserForm
