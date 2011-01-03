import iris.models as m


def create_topic(creator, subject):
    """Return a newly-created topic."""
    topic = m.Topic(
        subject=subject,
        creator=creator,
    )
    topic.save()
    participant = m.Participant(
        topic=topic,
        content=creator,
    )
    participant.save()
    joined = m.ParticipantJoined(
        participant=participant,
    )
    joined.save()
    item = m.Item(
        topic=topic,
        participant=participant,
        content=joined,
    )
    item.created = topic.created
    item.save()
    return topic
