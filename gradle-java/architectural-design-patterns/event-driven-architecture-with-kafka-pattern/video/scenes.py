"""Scene definitions for the Event-Driven Architecture with Kafka teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Event-Driven Architecture with Kafka',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Event-Driven '
            'Architecture pattern with Apache Kafka, in Java, and it is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] It '
            'is the framework version of the Event-Driven Architecture '
            'video. That one showed services that write facts to an '
            'append only log, and read it at their own pace. It showed a '
            'service that is down catching up, a new reader replaying '
            'history, briefly wrong stock, and a duplicate delivery '
            'absorbed by a check. This one shows the same idea inside '
            'Apache Kafka. [[slnc 350]] The plain definition, in short: '
            'with Kafka, the log is a topic on a broker, and each service '
            'reads it as a consumer group that the broker remembers. '
            '[[slnc 300]] By the end you will see an order lost because '
            'shipping was down, see the order service send to a real '
            'broker, see a service catch up from its remembered offset, '
            'see a new reader replay history, see the system briefly '
            'inconsistent, and see the bill, which is duplicates and a '
            'broker to run.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Event-Driven Architecture, the', 'hand-built video, writes facts to', 'a log.', '', 'It shows readers at their own', 'pace, and a reader that catches', 'up.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video assumes the Event-Driven Architecture video. If '
            'you have not seen it, start there. It writes facts to a log, '
            'and shows readers at their own pace, a reader that was down '
            'catching up, and a new reader replaying history. [[slnc '
            '300]] This one uses the same example. It does not teach the '
            'pattern again. It shows what Apache Kafka does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: Kafka, and', 'Docker to run it.', '', 'You need Docker running. Without', 'it the demo says so and stops.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before the first line of code, what Apache Kafka is. Kafka '
            'is a system that keeps a log of events on a server, called a '
            'broker. Producers add events to a topic. Consumers read the '
            'topic, and the broker remembers how far each group of '
            'consumers has read. [[slnc 300]] And a promise: skipping '
            'this video loses none of the pattern. The hand-built one '
            'teaches all of it.'
        ),
    ),
    dict(
        key='04-direct', kind='console', title='Calling And Waiting',
        body="""ONE. Calling each other.
  the order service calls
  shipping and waits.
  shipping is down.
  order accepted: false.

  a customer lost an order.""",
        narration=(
            'First, calling each other. The order service calls shipping, '
            'and waits. Shipping is down. The order is not accepted. A '
            'customer lost an order because a service they never see was '
            'down.'
        ),
    ),
    dict(
        key='05-log', kind='console', title='Telling The Log',
        body="""TWO. Telling the log.
  the order service sends the
  event to Kafka: offset 0.
  it has no reference to inventory
  or shipping.

  both read the topic, and act.""",
        narration=(
            'Second, telling the log. The order service sends the event '
            'to Kafka, which gives it offset zero, and it finishes. It '
            'has no reference to inventory or shipping. Both read the '
            'topic, and both see the order.'
        ),
    ),
    dict(
        key='06-down', kind='console', title='A Service That Is Down',
        body="""THREE. A service is down.
  shipping read ORD-1, went down.
  3 more orders accepted.
  the broker counts lag 3.

  shipping is back, and catches up
  from where it stopped:
  4 planned, lag 0.""",
        narration=(
            'Third, a service that is down. Shipping read the first '
            'order, and then went down. Three more orders were accepted. '
            'Shipping is three events behind, as the broker counts it. '
            'Shipping came back and caught up, from where it stopped. It '
            'has now planned four orders, and is none behind.'
        ),
    ),
    dict(
        key='07-new', kind='console', title='A New Reader',
        body="""FOUR. A new reader.
  analytics added after 2 orders.
  it reads the topic from the
  start: ORD-1, ORD-2.

  the order service is untouched.""",
        narration=(
            'Fourth, a new reader. Analytics is added after two orders. '
            'It reads the topic from the start, and sees both. The order '
            'service was not touched. Kafka keeps the events, so a new '
            'service can be built from history.'
        ),
    ),
    dict(
        key='08-late', kind='console', title='Not The Same Instant',
        body="""FIVE. Not the same instant.
  order accepted; stock: 10.
  it should be 9.
  after inventory reads: 9.

  for a moment they disagree.
  eventually consistent.""",
        narration=(
            'Fifth, not the same instant. The order is accepted, and '
            'stock in the warehouse is still ten. It should be nine. '
            'After inventory reads the topic, it is nine. For a moment, '
            'the two disagree. The system is eventually consistent, not '
            'consistent at every instant.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  the same event, delivered twice.
  no duplicate check: stock 8.
  with one: 9. right.

  the flow is spread over services:
  read the topic to see it.

  and a broker is another system
  to run.""",
        narration=(
            'Last, the bill. The same event is delivered twice, as Kafka '
            'may after a missed commit. Without a duplicate check, stock '
            'is eight. With one, it is nine, which is right. The flow of '
            'an order is now spread over several services, so to see it, '
            'you read the topic, not one piece of code. And a broker is '
            'another system to run.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['A group for each service.', '', 'Expect readers to be behind.', '', 'Make readers safe to repeat.', '', 'Watch the lag.'],
        narration=(
            'My verdict, plainly. Use a broker when services must not '
            'depend on each other being up, and when new services will '
            'come. Give each service its own group. Expect readers to be '
            'behind, and design for it. Make every reader safe to repeat. '
            'And watch the lag.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['`KafkaProducer` and', '`KafkaConsumer`, or', '`@KafkaListener`.', '', 'A `group.id` for each service.', '', 'Lag dashboards, and `kafka-', 'consumer-groups.sh`.'],
        narration=(
            'How do you recognise this in code you did not write? '
            'KafkaProducer and KafkaConsumer, or @KafkaListener. A '
            'group.id for each service. Lag dashboards, and '
            'kafka-consumer-groups.sh.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Most large event-driven systems:', 'order pipelines, activity feeds', 'and change data capture.'],
        narration=(
            'You have met this in most large event-driven systems: order '
            'pipelines, activity feeds and change data capture.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Apache Kafka 4.3.1.', '', 'Docker 24 or later.'],
        narration=(
            'For the record. Apache Kafka, 4.3.1. Docker, 24 or later.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real broker', 'in a container, real offsets, and', 'real consumer groups.', '', 'Each act uses its own one-', 'partition topic, so the counts are', 'exact.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: a real broker in a container, real '
            'offsets, and real consumer groups. Each act uses its own one '
            'partition topic, so the counts are exact.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a small system where all parts', 'are always up together, a direct', 'call is simpler. A broker is a', 'system to run, and to understand.'],
        narration=(
            'So when is it too much? For a small system where all parts '
            'are always up together, a direct call is simpler. A broker '
            'is a system to run, and to understand.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a third reader for a loyalty service, and read the topic from the start..'],
        narration=(
            "That's Event-Driven Architecture with Kafka. [[slnc 250]] If "
            'you take one sentence away, take this one: Kafka keeps the '
            "log and each service's place in it, and the price is a "
            'broker to run, and readers that may see an event twice. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, add a '
            'third reader for a loyalty service, and read the topic from '
            'the start. [[slnc 300]] If this helped, a like genuinely '
            'does help other people find it, and subscribe if you would '
            'like the rest of the series. [[slnc 250]] Thanks for '
            'watching.'
        ),
    ),
]
