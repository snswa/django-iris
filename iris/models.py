import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Topic(models.Model):
    """A topic of conversation."""

    subject = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(blank=True, null=True)

    creator_content_type = models.ForeignKey(ContentType, blank=True, null=True)
    creator_object_id = models.PositiveIntegerField(blank=True, null=True)
    creator = generic.GenericForeignKey("creator_content_type", "creator_object_id")

    class Meta:
        pass

    def __unicode__(self):
        return self.subject

    def has_participant(self, content):
        content_type = ContentType.objects.get_for_model(content)
        participants = Participant.objects.filter(
            topic=self,
            content_type__pk=content_type.id,
            object_id=content.id,
        )
        return participants.count() == 1

    def last_read_by(self, content):
        content_type = ContentType.objects.get_for_model(content)
        participant = Participant.objects.get(
            topic=self,
            content_type__pk=content_type.id,
            object_id=content.id,
        )
        return participant.last_read


class Item(models.Model):
    """An item in a conversation."""

    topic = models.ForeignKey('Topic', related_name='items')
    created = models.DateTimeField(default=datetime.datetime.now) # don't use auto_now_add since we sometimes want to override this on create
    participant = models.ForeignKey('Participant', related_name='+')

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content = generic.GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return u"{0}: {1}".format(self.participant, self.content)

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        topic = self.topic
        topic.modified = self.created
        topic.save()
        participant = self.participant
        participant.last_read = self.created
        participant.save()


class Participant(models.Model):
    """A user or other object participating in a topic."""

    topic = models.ForeignKey('Topic', related_name='participants')

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content = generic.GenericForeignKey("content_type", "object_id")

    last_read = models.DateTimeField(blank=True, null=True)

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
