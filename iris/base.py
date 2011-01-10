from django import forms


class ItemTypePlugin(object):

    label = None
    name = None
    form_class = None

    @property
    def action_label(self):
        # Set this as an attribute of a subclass to turn off this behavior.
        return u'Add a {0}'.format(self.label)

    @property
    def css_class(self):
        return self.name.replace('.', '-')

    @property
    def add_template(self):
        return 'iris/items/{0}.html'.format(self.name)


class PluginForm(forms.Form):
    """Base class for Form classes used by ItemTypePlugin.

    The return type of save() is not the model that the form is based on.
    Rather, it returns a saved Item that attaches the object to the Topic.
    """

    def __init__(self, *args, **kwargs):
        self._request = kwargs.pop('request', None)
        self._topic = kwargs.pop('topic', None)
        super(PluginForm, self).__init__(*args, **kwargs)


class ModelPluginForm(forms.ModelForm):
    """Base class for ModelForm classes used by ItemTypePlugin.

    The return type of save() is not the model that the form is based on.
    Rather, it returns a saved Item that attaches the object to the Topic.
    """

    class Meta:
        model = None

    def __init__(self, *args, **kwargs):
        self._request = kwargs.pop('request', None)
        self._topic = kwargs.pop('topic', None)
        super(ModelPluginForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        obj = super(ModelPluginForm, self).save(*args, **kwargs)
        return self._topic.add_item(
            creator=self._request.user,
            obj=obj,
        )
