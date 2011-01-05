from django.db import models
from django.utils.translation import ugettext_lazy as _


class Note(models.Model):

    text = models.TextField()

    class Meta:
        pass

    def __unicode__(self):
        return u'Note'


class OneLiner(models.Model):

    quip = models.CharField(max_length=160)

    class Meta:
        pass

    def __unicode__(self):
        return u'OneLiner'
