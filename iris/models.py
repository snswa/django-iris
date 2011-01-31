import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from iris.conf import settings


class TopicManager(models.Manager):

    def with_participant(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(
            participants__content_type__pk=content_type.id,
            participants__object_id=obj.id,
            participants__is_active=True,
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
            ('add_to_topic', 'Can add items to topic(s).'),
        )

    def __unicode__(self):
        return self.subject

    def save(self, *args, **kwargs):
        self.subject = self.subject.strip()
        return super(Topic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('iris_topic_slug', kwargs=dict(
            topic_id=self.id,
            slug=slugify(self.subject),
        ))

    def add_item(self, creator, obj):
        """Add the object as an item, returning a saved item."""
        item = Item(
            topic=self,
            creator=creator,
            content=obj,
        )
        item.save()
        return item

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
        return self.add_item(creator, joined)

    def get_participant(self, obj):
        """Get participation information for the given object."""
        content_type = ContentType.objects.get_for_model(obj)
        try:
            return Participant.objects.get(
                topic=self,
                content_type=content_type,
                object_id=obj.id,
            )
        except Participant.DoesNotExist:
            return None

    def has_participant(self, obj):
        if not isinstance(obj, models.Model):
            return False
        participant = self.get_participant(obj)
        return participant is not None and participant.is_active

    def item_last_read_by(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        participant = Participant.objects.get(
            topic=self,
            content_type=content_type,
            object_id=obj.id,
        )
        return participant.item_last_read

    def participants_of_type(self, model_class):
        if isinstance(model_class, basestring):
            app_label, model = model_class.split('.', 1)
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        else:
            content_type = ContentType.objects.get_for_model(model_class)
        return self.participants.filter(content_type=content_type)


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
        get_latest_by = 'created'
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
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            ('topic', 'content_type', 'object_id'),
        )

    def __unicode__(self):
        return unicode(self.content)


class ParticipantJoin(models.Model):
    """Information about someone joining a conversation."""

    participant = models.ForeignKey('Participant', related_name='+')

    class Meta:
        pass

    def __unicode__(self):
        return u"{0} joined".format(self.participant)


class ParticipantLeave(models.Model):
    """Information about someone leaving a conversation."""

    participant = models.ForeignKey('Participant', related_name='+')

    class Meta:
        pass

    def __unicode__(self):
        return u"{0} left".format(self.participant)
