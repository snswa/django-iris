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


class ModelPluginForm(forms.ModelForm):
    """Base class for ModelForms used by ItemTypePlugin.

    The return type of save() is not the model that the form is based on.
    Rather, it returns a saved Item that attaches the object to the Topic.
    """

    class Meta:
        model = None

    def save(self, request, topic, *args, **kwargs):
        obj = super(ModelPluginForm, self).save(*args, **kwargs)
        return topic.add_item(
            creator=request.user,
            obj=obj,
        )
