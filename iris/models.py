import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


class Topic(models.Model):
    """A topic of conversation."""

    subject = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True, db_index=True)

    creator_content_type = models.ForeignKey(ContentType, blank=True, null=True)
    creator_object_id = models.PositiveIntegerField(blank=True, null=True)
    creator = generic.GenericForeignKey("creator_content_type", "creator_object_id")

    class Meta:
        pass

    def __unicode__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('iris_topic_slug', kwargs=dict(
            topic_id=self.id,
            slug=slugify(self.subject),
        ))

    def add_participant(self, creator, content):
        participant = Participant(
            topic=self,
            content=content,
        )
        participant.save()
        joined = ParticipantJoined(
            participant=participant,
        )
        joined.save()
        item = Item(
            topic=self,
            creator=creator,
            content=joined,
        )
        item.save()

    def get_participant(self, content):
        """Get participation information for the given content."""
        content_type = ContentType.objects.get_for_model(content)
        try:
            return Participant.objects.get(
                topic=self,
                content_type__pk=content_type.id,
                object_id=content.id,
            )
        except Participant.DoesNotExist:
            return None

    def has_participant(self, content):
        participant = self.get_participant(content)
        return participant is not None

    def item_last_read_by(self, content):
        content_type = ContentType.objects.get_for_model(content)
        participant = Participant.objects.get(
            topic=self,
            content_type__pk=content_type.id,
            object_id=content.id,
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

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        topic = self.topic
        topic.modified = self.created
        topic.save()

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


class ParticipantJoined(models.Model):
    """Information about someone joining a conversation."""

    participant = models.ForeignKey('Participant', related_name='+')

    class Meta:
        pass

    def __unicode__(self):
        return u"{0} joined".format(self.participant)
