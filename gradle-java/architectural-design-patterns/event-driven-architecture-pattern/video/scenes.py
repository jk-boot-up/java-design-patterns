"""Scene definitions for the Event-Driven Architecture teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Event-Driven Architecture',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Event-Driven '
            'Architecture pattern in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] The plain '
            'definition: event driven architecture builds a system out of '
            'services that do not call each other. Instead they write '
            'facts to a shared log, and read the log at their own pace. '
            '[[slnc 350]] This is another project in the architecture '
            'category, whose subject is how a whole application is '
            'arranged, and who may depend on whom. In our online store, '
            'the question is how the order service, inventory and '
            'shipping should work together, when any of them may be down. '
            '[[slnc 300]] By the end you will see an order lost because '
            'shipping was down, see the order service only write to a '
            'log, see a service that was down catch up, see a new service '
            'read history without any change to the writer, see the '
            'system be briefly inconsistent, and see the bill, which is '
            'duplicates and a flow nobody can see in one place.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order is placed:', '', 'inventory reserves stock,', 'shipping plans a delivery.', '', 'Either may be down right now.', '', 'Should the order wait?'],
        narration=(
            'Here is the scenario. When an order is placed in the online '
            'store, inventory must reserve stock, and shipping must plan '
            'a delivery. Either of them may be down right now. [[slnc '
            '300]] The question: should the order wait?'
        ),
    ),
    dict(
        key='03-direct', kind='console', title='Calling And Waiting',
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
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Services do not call each other.', '', 'They write facts to a log,', 'and read the log at their', 'own pace.', '', 'Each remembers how far', 'it has read.'],
        narration=(
            'The pattern. Services do not call each other. They write '
            'facts to a log, and read the log at their own pace. Each one '
            'remembers how far it has read.'
        ),
    ),
    dict(
        key='05-log', kind='console', title='Telling The Log',
        body="""TWO. Telling the log.
  the order service appends
  the event at offset 0.
  it has no reference to
  inventory or shipping.

  both read the log, and act.""",
        narration=(
            'Second, telling the log. The order service appends the '
            'event, at position zero, and finishes. It has no reference '
            'to inventory or shipping. Both of them read the log, and '
            'both act.'
        ),
    ),
    dict(
        key='06-down', kind='console', title='A Service That Is Down',
        body="""THREE. A service is down.
  shipping is down.
  3 orders accepted anyway.
  shipping is 3 behind.

  it comes back, and catches up:
  0 behind.""",
        narration=(
            'Third, a service that is down. Shipping is down. Three '
            'orders are accepted anyway. Shipping has planned nothing, '
            'and is three events behind. When it comes back, it reads the '
            'log from where it stopped, and catches up. It plans all '
            'three.'
        ),
    ),
    dict(
        key='07-new', kind='console', title='A New Reader',
        body="""FOUR. A new reader.
  analytics added after 2 orders.
  it reads the log from the
  start: ORD-1, ORD-2.

  the order service is untouched.""",
        narration=(
            'Fourth, a new reader. Analytics is added after two orders '
            'were placed. It reads the log from the start, and sees both. '
            'The order service was not touched. The log is kept, so a new '
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
            'After inventory reads the log, it is nine. For a moment, the '
            'two disagree. The system is eventually consistent, not '
            'consistent at every instant.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  the same event, delivered twice.
  no duplicate check: stock 8.
  with one: 9. right.

  and the flow is spread over
  services: read the log to see
  it.""",
        narration=(
            'Last, the bill. The same event is delivered twice. Without a '
            'duplicate check, stock is eight. With one, it is nine, which '
            'is right. And the flow of an order is now spread over '
            'several services. To see it, you read the log, not one piece '
            'of code.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Kafka, Pulsar, Kinesis or a', 'similar log at the centre of a', '', 'Services whose only link is a', 'topic name.', '', 'Event sourcing, and CQRS read', 'models built by reading events.'],
        narration=(
            'How do you recognise this in code you did not write? Kafka, '
            'Pulsar, Kinesis or a similar log at the centre of a system. '
            'Services whose only link is a topic name. Event sourcing, '
            'and CQRS read models built by reading events. Consumers with '
            'an offset or a lag metric.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use events when services should', 'not depend on each other being up,', 'and when new services will come.', 'Keep the log. Expect eventual', 'consistency, and design for it.', 'Make every reader safe to repeat.', 'And keep a way to see the whole', 'flow, because no single piece of', 'code shows it.'],
        narration=(
            'Here is my verdict, plainly. Use events when services should '
            'not depend on each other being up, and when new services '
            'will come. Keep the log. Expect eventual consistency, and '
            'design for it. Make every reader safe to repeat. And keep a '
            'way to see the whole flow, because no single piece of code '
            'shows it.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. Every number quoted comes from '
            "this program's own output. Nothing depends on a clock, so "
            'every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a small system where all parts', 'are always up together, a direct', 'call is simpler and easier to', 'follow. Events pay off when parts', 'fail or change on their own.'],
        narration=(
            'So when is it too much? For a small system where all parts '
            'are always up together, a direct call is simpler and easier '
            'to follow. Events pay off when parts fail or change on their '
            'own.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Event-Driven Architecture. [[slnc 250]] If you take "
            'one sentence away, take this one: event-driven architecture '
            'lets services work without each other, and the price is that '
            'nothing is instant, and the flow is hard to see. [[slnc '
            '350]] The full source, the written notes, the diagrams and '
            'an animated walkthrough are all in the repository, running '
            'offline with nothing installed but a Java development kit. '
            '[[slnc 300]] If you try one exercise, add a shipping reader '
            'that fails on one event, and decide what the reader should '
            'do with it. [[slnc 300]] If this helped, a like genuinely '
            'does help other people find it, and subscribe if you would '
            'like the rest of the series. [[slnc 250]] Thanks for '
            'watching.'
        ),
    ),
]
