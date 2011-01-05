from django import forms

from iris.plugins import ItemTypePlugin

from iris.example.models import Note, OneLiner


class _BaseForm(forms.ModelForm):

    def save(self, request, topic, *args, **kwargs):
        obj = super(_BaseForm, self).save(*args, **kwargs)
        return topic.add_item(
            creator=request.user,
            obj=obj,
        )


class NoteForm(_BaseForm):

    class Meta:
        model = Note


class NoteAddPlugin(ItemTypePlugin):

    label = u'note'
    name = u'example.note.add'
    form_class = NoteForm
    add_template = 'iris/items/generic.add.html'


class OneLinerForm(_BaseForm):

    class Meta:
        model = OneLiner


class OneLinerAddPlugin(ItemTypePlugin):

    label = u'quip'
    name = u'example.oneliner.add'
    form_class = OneLinerForm
    add_template = 'iris/items/generic.add.html'
