from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from iris.models import Topic


class TopicForm(forms.ModelForm):
    """Form for Topic"""

    class Meta:
        model = Topic
        fields = ('subject',)


class ParticipantJoinUser(forms.Form):

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
