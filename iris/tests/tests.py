from operator import attrgetter

from django.contrib.auth.models import User
from django.test import TestCase

from iris.models import ParticipantJoin, Topic


class IrisTest(TestCase):
    """Tests for django-iris."""

    def setUp(self):
        self.alice, created = User.objects.get_or_create(username='alice')
        if created:
            self.alice.save()
        self.bob, created = User.objects.get_or_create(username='bob')
        if created:
            self.bob.save()

    def tearDown(self):
        del self.alice
        del self.bob

    def test_create_topic(self):
        # alice starts a topic with a subject
        subject = 'Aardvarks'
        topic = Topic(
            subject=subject,
            creator=self.alice,
        )
        topic.save()
        assert topic.subject == subject
        assert topic.creator == self.alice
        topic.add_participant(
            creator=self.alice,
            obj=self.alice,
        )
        #
        # - topic has one item, "alice joined"
        #     - the item's creator was alice
        #     - the item's content is a "topic join" object
        #     - the item is rendered as "alice: alice joined"
        assert topic.items.count() == 1
        first_item = topic.items.all()[0]
        assert first_item.creator == self.alice
        assert isinstance(first_item.content, ParticipantJoin)
        assert unicode(first_item) == u'alice: alice joined'
        #
        assert topic.created != first_item.created
        assert topic.modified == first_item.created
        #
        assert topic.has_participant(self.alice)
        assert not topic.has_participant(self.bob)
        #
        assert topic.item_last_read_by(self.alice) == None
        #
        # - alice is in the participant list for this topic
        assert self.alice in map(attrgetter('content'), topic.participants.all())
        assert self.bob not in map(attrgetter('content'), topic.participants.all())

    def test_add_other_participant(self):
        # - alice starts a topic with a subject
        subject = 'Antelopes'
        topic = Topic(
            subject=subject,
            creator=self.alice,
        )
        topic.save()
        topic.add_participant(
            creator=self.alice,
            obj=self.alice,
        )
        #
        # - alice adds bob to the topic
        topic.add_participant(
            creator=self.alice,
            obj=self.bob,
        )
        # - topic has two items, latest is "alice added bob"
        #     - the item's creator was alice
        #     - the item's content is a "topic join" object
        #     - the item is rendered as "alice: added bob"
        assert topic.items.count() == 2
        latest_item = topic.items.latest('created')
        assert latest_item.creator == self.alice
        assert isinstance(latest_item.content, ParticipantJoin)
        assert unicode(latest_item) == u'alice: bob joined'
        #
        assert topic.modified == latest_item.created
        #
        assert topic.has_participant(self.alice)
        assert topic.has_participant(self.bob)
        #
        assert topic.item_last_read_by(self.bob) == None
