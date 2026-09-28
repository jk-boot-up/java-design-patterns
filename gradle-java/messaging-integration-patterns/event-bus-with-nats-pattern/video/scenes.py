"""Scene definitions for the Event Bus with NATS teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Event Bus with NATS',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Event Bus pattern, in Java, using NATS. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] An event bus is one '
            'meeting place. [[slnc 300]] You publish to it, you subscribe '
            'to it, and you never hold a reference to whoever is on the '
            'other side. [[slnc 600]] Think of a loudspeaker in a '
            'warehouse. [[slnc 300]] Someone announces that an order is '
            'ready to pack. [[slnc 300]] Everyone in the room at that '
            'moment hears it. [[slnc 300]] The announcer does not know '
            'who is listening, and is never told whether anyone acted. '
            '[[slnc 300]] And someone who walks in a second later hears '
            'nothing, because there is no recording. [[slnc 700]] In our '
            'online store, checkout announces that an order has been '
            'placed. [[slnc 300]] The email service, the warehouse, and '
            'analytics each listen for what they care about. [[slnc 500]] '
            'What is new here is that the meeting place is a real server, '
            'on the network. [[slnc 300]] And it keeps nothing.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['The Event Bus video builds the', 'same bus by hand, inside one', 'program.', '', 'It teaches the pattern. If you', 'have not seen it, start there.', '', 'This one shows what changes when', 'the bus is a separate server.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Event Bus video. [[slnc 400]] That '
            'one builds the bus by hand, inside one program, in plain '
            'Java. [[slnc 300]] If you are new to the pattern, watch that '
            'one first. [[slnc 500]] Here, we keep the same online store. '
            '[[slnc 300]] And we hear what changes when the meeting place '
            'becomes a separate server.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['NATS is a message bus that runs', 'as a program of its own.', '', 'It stores nothing and remembers', 'nobody.', '', 'You need a container runtime.', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'First, what is NATS? [[slnc 400]] NATS is a message bus that '
            'runs as a program of its own. [[slnc 500]] A service '
            'publishes an event under a name, and returns straight away. '
            '[[slnc 300]] Another service subscribes to a name. [[slnc '
            '300]] From then on, the server sends it every event '
            'published under that name. [[slnc 300]] NATS calls that name '
            'a subject. [[slnc 500]] The important part is what NATS does '
            'not do. [[slnc 300]] It stores nothing. [[slnc 300]] It '
            'remembers nobody. [[slnc 300]] An event goes to whoever is '
            'listening at that instant, and then it is gone. [[slnc 500]] '
            'You need Docker running. [[slnc 300]] And one promise: if '
            'you skip this video, you lose none of the pattern.'
        ),
    ),
    dict(
        key='04-direct', kind='console', title='Everyone Knows Everyone',
        body="""ONE. Everyone knows everyone.
  5 services that each tell the
  other four: 20 wires.

  every wire is an address that
  can be wrong or down.

  add a sixth: 10 more.""",
        narration=(
            'First demo: the store before there is a bus. [[slnc 400]] '
            'Five services, each telling the other four when an order is '
            'placed. [[slnc 300]] That needs twenty connections between '
            'them. [[slnc 500]] And these are now separate programs. '
            '[[slnc 300]] So every connection is a network address, which '
            'someone must be told about. [[slnc 300]] Which can be typed '
            'wrong. [[slnc 300]] And which can point at something that is '
            'not running. [[slnc 500]] Add a sixth service, and it needs '
            'ten more.'
        ),
    ),
    dict(
        key='05-bus', kind='console', title='Everyone Knows The Bus',
        body="""TWO. Everyone knows the bus.
  checkout published
  OrderPlaced ORD-1 and returned.

  email saw it. the warehouse saw
  it. analytics saw it.

  5 wires, not 20.""",
        narration=(
            'Second demo: everyone knows the bus. [[slnc 400]] Checkout '
            'publishes an order placed event, under the subject store dot '
            'orders dot placed. [[slnc 300]] And it returns immediately. '
            '[[slnc 300]] It is told nothing about who was listening. '
            '[[slnc 500]] The email service receives the order. [[slnc '
            '300]] The warehouse receives it. [[slnc 300]] Analytics '
            'receives it. [[slnc 500]] Each has its own connection to the '
            'server, and none knows about the others. [[slnc 300]] Five '
            'services, one connection each: five, not twenty.'
        ),
    ),
    dict(
        key='06-names', kind='console', title='Subscribing By Name',
        body="""THREE. By name.
  four events published: order
  placed, order cancelled,
  payment taken, stock low.

  store.orders.placed -> 1
  store.orders.*      -> 2
  store.>             -> 4""",
        narration=(
            'Third demo: subscribing by name. [[slnc 400]] NATS has no '
            'event types. [[slnc 300]] It has names made of dotted parts, '
            'like store dot orders dot placed. [[slnc 500]] Checkout '
            'publishes four events. [[slnc 300]] An order placed. [[slnc '
            '200]] That order cancelled. [[slnc 200]] A payment taken. '
            '[[slnc 200]] And stock running low. [[slnc 500]] A listener '
            'for the exact name, order placed, receives one event. [[slnc '
            '500]] A listener can also ask for a family. [[slnc 300]] A '
            'star stands for one part of the name. [[slnc 300]] So store '
            'dot orders dot star receives two: placed, and cancelled. '
            '[[slnc 300]] An arrow stands for everything after it. [[slnc '
            '300]] So store dot arrow receives all four.'
        ),
    ),
    dict(
        key='07-failure', kind='console', title='One Failing Subscriber',
        body="""FOUR. One failing subscriber.
  email's handler threw:
  mail server timed out.

  the warehouse still reserved
  the stock for ORD-1.

  checkout was never told.""",
        narration=(
            'Fourth demo: one failing subscriber. [[slnc 400]] The email '
            'service fails: the mail server timed out. [[slnc 300]] But '
            'the warehouse, on its own connection, still reserves the '
            'stock. [[slnc 500]] In the hand-built bus, that protection '
            'had to be written by hand. [[slnc 300]] Here it comes free, '
            'because the two subscribers are not even in the same '
            'program. [[slnc 500]] And checkout was never told, because '
            'it had already moved on.'
        ),
    ),
    dict(
        key='08-missed', kind='console', title='An Event Nobody Hears',
        body="""FIVE. An event nobody hears.
  nobody listening. ORD-1 was
  published, and dropped.
  no error. no record. no log.

  warehouse starts listening.
  ORD-2 published.
  its first ever event: ORD-2.

  2 published, 1 received.""",
        narration=(
            'Fifth demo, and the heart of this video: an event nobody '
            'hears. [[slnc 500]] Nobody is listening. [[slnc 300]] '
            'Checkout publishes an order placed event, for order one. '
            '[[slnc 300]] The call returns with no error. [[slnc 300]] '
            'And the bus drops the event. [[slnc 500]] There is no error, '
            'no record, and nowhere to read it back from. [[slnc 300]] '
            'The hand-built bus turned unheard events into dead events '
            'you could watch for. [[slnc 300]] NATS has no such thing. '
            '[[slnc 600]] Then the warehouse starts listening. [[slnc '
            '300]] And checkout publishes order two. [[slnc 300]] The '
            'very first event the warehouse ever receives is order two. '
            '[[slnc 500]] Why does that prove order one was lost? [[slnc '
            '300]] Because this bus delivers events for one name in the '
            'order they were published. [[slnc 300]] So once order two '
            'has arrived, order one can no longer be on its way. [[slnc '
            '300]] It was never coming. [[slnc 300]] Two orders '
            'published, and one received.'
        ),
    ),
    dict(
        key='09-ask', kind='console', title='Ask, Do Not Tell',
        body="""  telling this bus is never
  confirmed.

  asking is: a request with
  nobody listening came back
  at once, saying:

    no responders""",
        narration=(
            'There is one way out, and it is worth knowing. [[slnc 400]] '
            'Telling this bus is never confirmed. [[slnc 300]] But asking '
            'is. [[slnc 500]] A request is a question, with a reply '
            'address attached. [[slnc 300]] Send a request under a name '
            'that nobody is listening to. [[slnc 300]] And the server '
            'answers at once, saying: no responders. [[slnc 500]] That is '
            'the only moment on this bus when a publisher learns its '
            'words went nowhere.'
        ),
    ),
    dict(
        key='10-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  who reacts to an order?
  only the server knows. ask it
  on a second port: 3 listeners.

  analytics stops listening: 2.
  connections closed: 0.

  1 container to run and watch.""",
        narration=(
            'Finally, the costs. [[slnc 400]] Who reacts to an order '
            'being placed? [[slnc 300]] Nothing in checkout says, and '
            'checkout cannot find out. [[slnc 300]] Only the server '
            'knows. [[slnc 300]] So you must ask the server, on a '
            'separate monitoring port. [[slnc 500]] It reports three '
            'listeners for store events. [[slnc 300]] Analytics stops '
            'listening: two. [[slnc 300]] All three services disconnect: '
            'none. [[slnc 500]] And the bus is now a program of its own, '
            'to run, watch, and maintain. [[slnc 300]] Most importantly, '
            'it keeps nothing. [[slnc 300]] A subscriber that is down '
            'when an event is published has missed it for good.'
        ),
    ),
    dict(
        key='11-contrast', kind='bullets', title='The Opposite Trade',
        body=['A durable log keeps events, so a', 'service that was down catches up', 'later.', '', 'Its price: storage, tracking every', 'reader, and the same event', 'possibly arriving twice.', '', 'NATS chooses the other side of', 'every one of those.'],
        narration=(
            'It is worth knowing the opposite choice, because this series '
            'covers both. [[slnc 500]] A durable log keeps every event it '
            'is given. [[slnc 300]] A service that was down comes back, '
            'and reads everything it missed. [[slnc 300]] And a brand new '
            'service can be built from the whole history. [[slnc 500]] '
            'The price is real. [[slnc 300]] The server stores the '
            'events, tracks how far each reader has got, and may deliver '
            'the same event twice. [[slnc 300]] So every reader must be '
            'safe to run twice. [[slnc 500]] NATS makes the opposite '
            'choice on every one of those. [[slnc 300]] Neither is right '
            'in general. [[slnc 300]] Choose based on what a missed event '
            'would really cost you.'
        ),
    ),
    dict(
        key='12-verdict', kind='bullets', title='The Verdict',
        body=['Use it for announcements, not for', 'anything you cannot lose.', '', 'Name subjects for facts in the', 'past tense, and agree them as a', 'team.', '', 'Wait for the server to confirm a', 'subscription before publishing.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use this kind of bus '
            'for announcements, where the next event makes the last one '
            'irrelevant. [[slnc 300]] Clearing caches, live dashboards, '
            'and system measurements. [[slnc 500]] Name your subjects as '
            'facts in the past tense, and agree the names as a team. '
            '[[slnc 300]] Because the names are the contract, and nothing '
            'checks them for you. [[slnc 500]] Always wait for the server '
            'to confirm a subscription before publishing something that '
            'subscriber must hear. [[slnc 500]] And when an event must '
            'never be lost, use a durable log, or ask instead of telling.'
        ),
    ),
    dict(
        key='13-recognise', kind='bullets', title='How To Recognise It',
        body=['Publish and subscribe taking a', 'dotted string.', '', 'Subject names with a star or an', 'arrow in them.', '', 'A flush before a publish: that is', 'somebody who has been bitten.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a connection with publish and subscribe '
            'methods, taking a dotted name, not a class. [[slnc 300]] '
            'Look for subject names containing a star, or an arrow. '
            '[[slnc 300]] And look for a flush call, just before a '
            'publish. [[slnc 300]] That is someone who has already been '
            'caught out, by publishing before the server confirmed a '
            'subscription.'
        ),
    ),
    dict(
        key='14-versions', kind='bullets', title='What Was Used',
        body=['NATS server 2.15.0, in a', 'container.', '', 'The NATS Java client, 2.26.3.', '', 'Testcontainers 2.0.5, which', 'starts and stops the container.', '', 'Java 21, and Docker 24 or later.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] The NATS '
            'server, version two point fifteen, in a container. [[slnc '
            '300]] The NATS Java client, version two point twenty-six '
            'point three. [[slnc 300]] Testcontainers two point zero '
            'point five, which starts and stops the container. [[slnc '
            '300]] Java twenty-one, and Docker twenty-four or later.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real server', 'in a container, real subjects,', 'real dropped events.', '', 'No test sleeps. Every wait has a', 'deadline and fails rather than', 'hangs.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] '
            'Everything here is real. [[slnc 300]] A real NATS server in '
            'a container, real subjects, and events that are really '
            'dropped. [[slnc 500]] And no test ever just sleeps for a '
            'fixed time. [[slnc 300]] Every wait has a deadline. [[slnc '
            '300]] If the deadline passes, the test fails, and says what '
            'it was waiting for, instead of hanging.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try adding a loyalty service that', 'listens for payments, and watch it hear nothing else.'],
        narration=(
            "That's the Event Bus pattern, with NATS. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] On '
            'this bus, publishing always succeeds, and succeeding means '
            'nothing. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add a loyalty service that listens only for payments '
            'taken. [[slnc 300]] And check that it hears the payment, and '
            'nothing else. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
