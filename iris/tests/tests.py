from operator import attrgetter

from django.contrib.auth.models import User
from django.test import TestCase

from iris import api
from iris.models import ParticipantJoined


class IrisTest(TestCase):
    """Tests for django-iris

    Scratchpad:

    - alice adds bob to an empty topic
        - topic has one item, "alice added bob"
            - the item's creator was alice
            - the item's content is a "topic join" object
            - the item is rendered as "alice: added bob"
        - the topic's modified stamp is same as item's stamp
        - bob is an active participant
        - bob's last-viewed time is the topic's creation time
        - alice's last-viewed time is the item's stamp
    """

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
        topic = api.create_topic(
            subject=subject,
            creator=self.alice,
        )
        assert topic.subject == subject
        assert topic.creator == self.alice
        #
        # - topic has one item, "alice joined"
        #     - the item's creator was alice
        #     - the item's content is a "topic join" object
        #     - the item is rendered as "alice: alice joined"
        assert topic.items.count() == 1
        first_item = topic.items.all()[0]
        assert first_item.participant.content == self.alice
        assert isinstance(first_item.content, ParticipantJoined)
        assert unicode(first_item) == u'alice: alice joined'
        #
        # - the topic's creation stamp is the same as the item's stamp
        assert topic.created == first_item.created
        #
        # - the topic's modified stamp is the same as the item's stamp
        assert topic.modified == first_item.created
        #
        # - alice is a participant of this topic, bob is not
        assert topic.has_participant(self.alice)
        assert not topic.has_participant(self.bob)
        #
        # - alice's last-viewed time is the creation time
        assert topic.last_read_by(self.alice) == topic.created
        #
        # - alice is in the participant list for this topic
        assert self.alice in map(attrgetter('content'), topic.participants.all())
        assert self.bob not in map(attrgetter('content'), topic.participants.all())
