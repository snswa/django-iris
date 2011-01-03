from django import forms

from iris.models import Topic


class TopicForm(forms.ModelForm):
    """Form for Topic"""

    class Meta:
        model = Topic
        fields = ('subject',)
