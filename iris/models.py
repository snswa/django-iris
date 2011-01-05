import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from iris.conf import settings


def get_item_type_info(item_type_name, form_kwargs=None):
    if isinstance(item_type_name, ContentType):
        content_type = item_type_name
        app_label, model = content_type.app_label, content_type.model
    else:
        app_label, model = item_type_name.split('.')
        content_type = ContentType.objects.get(app_label=app_label, model=model)
    model_class = content_type.model_class()
    css_class = '{0}-{1}'.format(app_label, model)
    add_template = 'iris/items/{0}.{1}.add.html'.format(app_label, model)
    return dict(
        css_class=css_class,
        model_class=model_class,
        add_template=add_template,
        item_add_form=model_class.item_add_form_class()(form_kwargs),
    )

def get_item_type_list(form_kwargs=None):
    """Create a list of dictionaries for listed item types, each with these key/value pairs:

    - 'model_class': <model class of the item type>
    - 'css_class': <CSS class to decorate list item with>
    - 'add_template': <name of template for adding an item of this type>
    - 'item_add_form': <form instance>
    """
    L = []
    for item_type_name in settings.ADD_ITEM_TYPE_ORDER:
        L.append(get_item_type_info(item_type_name, form_kwargs))
    return L


class TopicManager(models.Manager):

    def with_participant(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(
            participants__content_type__pk=content_type.id,
            participants__object_id=obj.id,
        )


class Topic(models.Model):
    """A topic of conversation."""

    subject = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True, db_index=True)

    creator_content_type = models.ForeignKey(ContentType, blank=True, null=True)
    creator_object_id = models.PositiveIntegerField(blank=True, null=True)
    creator = generic.GenericForeignKey("creator_content_type", "creator_object_id")

    objects = TopicManager()

    class Meta:
        ordering = ('modified', )
        permissions = (
            ('view_topic', 'Can view topic(s).'),
            ('join_topic', 'Can participate in topic(s).'),
        )

    def __unicode__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('iris_topic_slug', kwargs=dict(
            topic_id=self.id,
            slug=slugify(self.subject),
        ))

    def add_participant(self, creator, obj):
        """Add the object as a participant, returning the ParticipantJoin item created."""
        participant = Participant(
            topic=self,
            content=obj,
        )
        participant.save()
        joined = ParticipantJoin(
            participant=participant,
        )
        joined.save()
        item = Item(
            topic=self,
            creator=creator,
            content=joined,
        )
        item.save()
        return item

    def get_participant(self, obj):
        """Get participation information for the given object."""
        content_type = ContentType.objects.get_for_model(obj)
        try:
            return Participant.objects.get(
                topic=self,
                content_type__pk=content_type.id,
                object_id=obj.id,
            )
        except Participant.DoesNotExist:
            return None

    def has_participant(self, obj):
        participant = self.get_participant(obj)
        return participant is not None

    def item_last_read_by(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        participant = Participant.objects.get(
            topic=self,
            content_type__pk=content_type.id,
            object_id=obj.id,
        )
        return participant.item_last_read


class Item(models.Model):
    """An item in a conversation."""

    topic = models.ForeignKey('Topic', related_name='items', db_index=True)
    created = models.DateTimeField(default=datetime.datetime.now, db_index=True) # don't use auto_now_add since we sometimes want to override this on create

    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='+')
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content = generic.GenericForeignKey("content_type", "object_id")

    creator_content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='+')
    creator_object_id = models.PositiveIntegerField(blank=True, null=True)
    creator = generic.GenericForeignKey("creator_content_type", "creator_object_id")

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return u"{0}: {1}".format(self.creator, self.content)

    def get_absolute_url(self):
        """Return the topic's absolute url with a query string and hash for this item."""
        return '{0}?i={1}#i{1}'.format(self.topic.get_absolute_url(), self.id)

    def get_items_after_url(self):
        """Return an URL that will return all of the items in the topic after this item."""
        return reverse('iris_items_after', kwargs=dict(
            topic_id=self.topic_id,
            after_item_id=self.id,
        ))

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        topic = self.topic
        topic.modified = self.created
        topic.save()

    def css_class(self):
        """Return a CSS class corresponding to this item's content type."""
        ct = self.content_type
        return '{0}-{1}'.format(ct.app_label, ct.model)

    def view_template(self):
        """Return the name of the view template according to the content type."""
        ct = self.content_type
        return 'iris/items/{0}.{1}.view.html'.format(ct.app_label, ct.model)


class Participant(models.Model):
    """A user or other object participating in a topic."""

    topic = models.ForeignKey('Topic', related_name='participants')

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content = generic.GenericForeignKey("content_type", "object_id")

    item_last_read = models.ForeignKey(Item, blank=True, null=True)

    class Meta:
        pass

    def __unicode__(self):
        return unicode(self.content)


class ParticipantJoin(models.Model):
    """Information about someone joining a conversation."""

    participant = models.ForeignKey('Participant', related_name='+')

    class Meta:
        pass

    def __unicode__(self):
        return u"{0} joined".format(self.participant)

    @staticmethod
    def item_add_form_class():
        # circular
        from iris.forms import ParticipantJoinUser
        return ParticipantJoinUser

    @staticmethod
    def item_type_label():
        return u'participant'
