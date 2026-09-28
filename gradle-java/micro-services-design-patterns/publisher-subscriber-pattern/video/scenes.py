"""Scene definitions for the Publisher-Subscriber teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Publisher-Subscriber',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Publisher-Subscriber pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A service announces '
            'an event once, to a named channel called a topic. [[slnc '
            '300]] Any number of other services can listen. [[slnc 300]] '
            'And the service that announced it does not know who they '
            'are. [[slnc 600]] Think of a radio station. [[slnc 300]] It '
            'broadcasts once. [[slnc 300]] Anyone can tune in, and the '
            'station never knows who is listening. [[slnc 700]] In our '
            'online store, one thing happens, an order is placed, and '
            'several services care about it. [[slnc 500]] By the end, you '
            'will hear an order service that calls three others by name. '
            '[[slnc 300]] Then the same service publishing once instead. '
            '[[slnc 300]] Listeners working at their own pace, and taking '
            'only what they want. [[slnc 300]] A late listener missing '
            'history, unless it is kept. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order is placed:', '', 'inventory reserves stock,', 'email sends a confirmation,', 'analytics counts it.', '', 'Next month, loyalty points want', 'to know too.', '', 'Who calls whom?'],
        narration=(
            'Here is the scenario. [[slnc 400]] When an order is placed '
            'in the online store, three things must happen. [[slnc 300]] '
            'Inventory must reserve the stock. [[slnc 300]] Email must '
            'send a confirmation. [[slnc 300]] And analytics must count '
            'it. [[slnc 500]] Next month, a loyalty points service wants '
            'to know as well. [[slnc 500]] So here is the question. '
            '[[slnc 300]] Who calls whom?'
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
            'First demo: the order service calls each one. [[slnc 400]] '
            'Inventory. [[slnc 200]] Email. [[slnc 200]] Analytics. '
            '[[slnc 300]] It works. [[slnc 500]] But the order service '
            'knows three other services by name. [[slnc 300]] And when '
            'loyalty points wants to know, someone has to edit the order '
            'service.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['The publisher appends an event', 'to a topic.', '', 'Subscribers read the topic, each', 'at its own position.', '', 'The publisher does not know who', 'is listening.'],
        narration=(
            'Now, the pattern. [[slnc 400]] The publisher adds an event '
            'to the end of a topic. [[slnc 300]] The services that listen '
            'are called subscribers. [[slnc 300]] Each subscriber reads '
            'the topic from its own position, at its own pace. [[slnc '
            '500]] And the publisher does not know who is listening.'
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
            'Second demo: the order service only publishes. [[slnc 400]] '
            'It publishes the event once. [[slnc 300]] Inventory, email, '
            'and analytics each receive it. [[slnc 500]] Then a fourth '
            'subscriber is added: loyalty points. [[slnc 300]] It '
            'receives the event too. [[slnc 500]] And the order service '
            'was not changed at all.'
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
            'Third demo: each at its own pace. [[slnc 400]] Five orders '
            'are published. [[slnc 300]] Email handles all five. [[slnc '
            '300]] Analytics handles one, and has four still waiting. '
            '[[slnc 500]] Later, analytics catches up. [[slnc 300]] The '
            'slow subscriber held up neither the fast one, nor the '
            'publisher.'
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
            'Fourth demo: each takes what it wants. [[slnc 400]] Email '
            'asks only for placed orders, and gets one. [[slnc 300]] '
            'Analytics asks for everything. [[slnc 300]] So it gets both '
            'a placed order and a cancelled order. [[slnc 500]] Each '
            'subscriber says what it wants. [[slnc 300]] The publisher '
            'just publishes one stream.'
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
            'Fifth demo: a subscriber that arrives late. [[slnc 400]] '
            'Three orders were published before loyalty points was added. '
            '[[slnc 300]] And one was published after. [[slnc 500]] A '
            'subscriber that joins live only sees the last order. [[slnc '
            '300]] One that reads from the beginning sees all four. '
            '[[slnc 300]] Because the history of events was kept. [[slnc '
            '500]] Keeping that history is what makes a late subscriber '
            'possible. [[slnc 300]] And it has to be stored somewhere.'
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
            'Finally, the bill. [[slnc 400]] Email is down when an order '
            'is placed. [[slnc 300]] And the publisher is told nothing. '
            '[[slnc 500]] When email comes back, it catches up, because '
            'its place in the topic was kept. [[slnc 500]] But the '
            'publisher still cannot ask whether the email went out. '
            '[[slnc 300]] It published. [[slnc 300]] And it does not know '
            'who listened.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A publish call with a topic name', 'and no reference to any consumer.', '', 'Kafka topics and consumer groups,', 'SNS topics, Google Pub/Sub,', '', 'ApplicationEventPublisher and', '@EventListener in Spring, inside'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a publish call with a topic name, and '
            'no mention of who receives it. [[slnc 300]] Look for Kafka '
            'topics, Amazon S N S topics, Google Pub Sub, or RabbitMQ '
            'fan-out exchanges. [[slnc 300]] Inside one Spring program, '
            'look for an event publisher, and event listener annotations. '
            '[[slnc 300]] Or a subscription with a filter.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use publish and subscribe when one', 'thing happens and several', 'independent parties care, and when', 'new parties will come along. Keep', 'the events small and named for', 'what happened. Keep the log long', 'enough for a late or absent', 'subscriber. Make every subscriber', 'safe to run twice. Do not use it'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use publish and '
            'subscribe when one thing happens, and several independent '
            'services care. [[slnc 300]] Especially when new services '
            'will come along later. [[slnc 600]] Keep the events small, '
            'and name them for what happened. [[slnc 300]] Keep the '
            'history long enough for a late or absent subscriber. [[slnc '
            '300]] And make every subscriber safe to handle the same '
            'event twice. [[slnc 500]] Do not use it when the publisher '
            'needs an answer.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] "
            'Nothing depends on a real clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If one known service needs the', 'result, a direct call is clearer.', 'A topic is for facts that many may', 'want, and that you do not want to', 'track.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If only one known '
            'service needs the result, a direct call is clearer. [[slnc '
            '400]] A topic is for facts that many services may want, and '
            'that you do not want to keep track of.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Publisher-Subscriber pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] '
            'Publish and subscribe lets a service say what happened '
            'without knowing who cares, and the price is that it never '
            'learns who acted. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] Add a subscriber that '
            'only wants cancelled orders. [[slnc 300]] Then check whether '
            'the publisher had to change. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
