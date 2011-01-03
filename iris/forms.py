from django import forms

from iris import api


class TopicCreateForm(forms.Form):
    """Form to create a new iris topic."""

    subject = forms.CharField()

    def save(self, request):
        topic = api.create_topic(
            creator=request.user,
            subject=self.cleaned_data['subject'],
        )
        return topic
