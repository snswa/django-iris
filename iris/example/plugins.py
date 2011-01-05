from django import forms

from iris.base import ModelPluginForm
from iris.base import ItemTypePlugin

from iris.example.models import Note, OneLiner


class NoteForm(ModelPluginForm):

    class Meta:
        model = Note


class NoteAddPlugin(ItemTypePlugin):

    label = u'note'
    name = u'example.note.add'
    form_class = NoteForm


class OneLinerForm(ModelPluginForm):

    class Meta:
        model = OneLiner


class OneLinerAddPlugin(ItemTypePlugin):

    label = u'quip'
    name = u'example.oneliner.add'
    form_class = OneLinerForm
