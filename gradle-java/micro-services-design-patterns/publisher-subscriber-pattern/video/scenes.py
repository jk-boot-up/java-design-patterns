"""Scene definitions for the Publisher-Subscriber teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Publisher-Subscriber',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the '
            'Publisher-Subscriber pattern in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] The plain '
            'definition: publisher subscriber lets a service announce an '
            'event once, to a topic, and lets any number of other '
            'services listen, without the publisher knowing who they are. '
            '[[slnc 350]] This is another project in the microservices '
            'category, whose subject is how many small services stay '
            'reliable when they talk to each other. In our online store, '
            'one thing happens, an order is placed, and several services '
            'care. [[slnc 300]] By the end you will see an order service '
            'that calls three others by name, see it publish once '
            'instead, see subscribers go at their own pace and take only '
            'what they want, see a late subscriber miss history unless '
            'the log is kept, and see the bill, which is that the '
            'publisher never knows who got the event.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order is placed:', '', 'inventory reserves stock,', 'email sends a confirmation,', 'analytics counts it.', '', 'Next month, loyalty points want', 'to know too.', '', 'Who calls whom?'],
        narration=(
            'Here is the scenario. When an order is placed in the online '
            'store, inventory must reserve stock, email must send a '
            'confirmation, and analytics must count it. Next month, '
            'loyalty points want to know as well. [[slnc 300]] The '
            'question: who calls whom?'
        ),
    ),
    dict(
        key='03-direct', kind='console', title='The Order Service Calls Each One',
        body="""ONE. Calls each one.
  inventory, email, analytics.

  the order service knows 3
  services by name.

  a fourth means editing it.""",
        narration=(
            'First, the order service calls each one. Inventory, email, '
            'analytics. It works. But the order service knows three other '
            'services by name, and when loyalty points want to know, '
            'someone must edit the order service.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['The publisher appends an event', 'to a topic.', '', 'Subscribers read the topic, each', 'at its own position.', '', 'The publisher does not know who', 'is listening.'],
        narration=(
            'The pattern. The publisher appends an event to a topic. '
            'Subscribers read the topic, each at its own position and its '
            'own pace. And the publisher does not know who is listening.'
        ),
    ),
    dict(
        key='05-pub', kind='console', title='The Order Service Only Publishes',
        body="""TWO. Publish once.
  three subscribers each get
  the event.

  loyalty is added: it gets it.
  the order service was not
  changed.""",
        narration=(
            'Second, the order service only publishes. It publishes the '
            'event once. Inventory, email and analytics each get it. Then '
            'a fourth subscriber, loyalty points, is added, and gets it '
            'too. The order service was not changed.'
        ),
    ),
    dict(
        key='06-pace', kind='console', title='Each At Its Own Pace',
        body="""THREE. Own pace.
  5 orders published.
  email: handled 5.
  analytics: handled 1,
  backlog 4.

  it catches up later.""",
        narration=(
            'Third, each at its own pace. Five orders are published. '
            'Email handles all five. Analytics handles one, and has a '
            'backlog of four. Later, analytics catches up. A slow '
            'subscriber held up neither the fast one, nor the publisher.'
        ),
    ),
    dict(
        key='07-filter', kind='console', title='Each Takes What It Wants',
        body="""FOUR. A filter.
  email: placed orders only.
  analytics: everything.

  each subscriber says what it
  wants.""",
        narration=(
            'Fourth, each takes what it wants. Email asks only for placed '
            'orders, and gets one. Analytics asks for everything, and '
            'gets a placed and a cancelled event. Each subscriber says '
            'what it wants. The publisher publishes one stream.'
        ),
    ),
    dict(
        key='08-late', kind='console', title='A Subscriber That Arrives Late',
        body="""FIVE. Late.
  3 published before, 1 after.
  a live subscriber: ORD-4.
  from the start: ORD-1 to 4.

  the log had to be kept.""",
        narration=(
            'Fifth, a subscriber that arrives late. Three orders were '
            'published before loyalty was added, and one after. A '
            'subscriber that joins live sees only the last one. One that '
            'reads from the start sees all four, because the log was '
            'kept. Keeping the log is what makes a late subscriber '
            'possible, and it has to be kept somewhere.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill: Nobody Knows Who Got It',
        body="""SIX. The bill.
  email is down. the publisher
  is told nothing.
  back: it catches up.

  the publisher cannot ask
  whether the email went out.""",
        narration=(
            'Last, the bill. Email is down when the order is placed, and '
            'the publisher is told nothing. When email comes back, it '
            'catches up, because its place in the log was kept. But the '
            'publisher still cannot ask whether the email went out. It '
            'published, and it does not know who listened.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A publish call with a topic name', 'and no reference to any consumer.', '', 'Kafka topics and consumer groups,', 'SNS topics, Google Pub/Sub,', '', 'ApplicationEventPublisher and', '@EventListener in Spring, inside'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'publish call with a topic name and no reference to any '
            'consumer. Kafka topics and consumer groups, SNS topics, '
            'Google Pub/Sub, RabbitMQ fanout exchanges. '
            'ApplicationEventPublisher and @EventListener in Spring, '
            'inside one process. A subscription with a filter or a '
            'routing key.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use publish and subscribe when one', 'thing happens and several', 'independent parties care, and when', 'new parties will come along. Keep', 'the events small and named for', 'what happened. Keep the log long', 'enough for a late or absent', 'subscriber. Make every subscriber', 'safe to run twice. Do not use it'],
        narration=(
            'Here is my verdict, plainly. Use publish and subscribe when '
            'one thing happens and several independent parties care, and '
            'when new parties will come along. Keep the events small and '
            'named for what happened. Keep the log long enough for a late '
            'or absent subscriber. Make every subscriber safe to run '
            'twice. Do not use it when the publisher needs an answer.'
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
        body=['If one known service needs the', 'result, a direct call is clearer.', 'A topic is for facts that many may', 'want, and that you do not want to', 'track.'],
        narration=(
            'So when is it too much? If one known service needs the '
            'result, a direct call is clearer. A topic is for facts that '
            'many may want, and that you do not want to track.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Publisher-Subscriber. [[slnc 250]] If you take one "
            'sentence away, take this one: publish-subscribe lets a '
            'service say what happened without knowing who cares, and the '
            'price is that it never learns who acted. [[slnc 350]] The '
            'full source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, add a subscriber that only wants '
            'cancelled orders, and see whether the publisher changes. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
