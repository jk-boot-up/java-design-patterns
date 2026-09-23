"""Scene definitions for the Event Bus with NATS teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Event Bus with NATS',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Event Bus '
            'pattern with NATS, in Java, and it is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] The plain definition, in '
            'short: an event bus is one meeting place. You publish to it, '
            'you subscribe to it, and you never hold a reference to '
            'whoever is on the other side. [[slnc 300]] Here is the '
            'everyday version. Think of a tannoy in a warehouse. Somebody '
            'picks up the microphone and announces that an order is ready '
            'to pack. Everybody standing in the room at that moment hears '
            'it. The person on the microphone does not know who is in the '
            'room, does not wait for anybody, and is never told whether '
            'anybody acted on it. And somebody who walks in a second '
            'later hears nothing, because there is no recording. [[slnc '
            '350]] Now the same thing in an online store. Checkout '
            'announces that an order has been placed. The email service, '
            'the warehouse and the analytics tally each listen for what '
            'they care about. Checkout holds no reference to any of them. '
            '[[slnc 300]] The difference in this video is that the '
            'meeting place is now a real server, in a container, on the '
            'network. And it keeps nothing.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['The Event Bus video builds the', 'same bus by hand, inside one', 'program.', '', 'It teaches the pattern. If you', 'have not seen it, start there.', '', 'This one shows what changes when', 'the bus is a separate server.'],
        narration=(
            'This video has a partner. The Event Bus video builds the '
            'same bus by hand, inside one program, in plain Java with '
            'nothing installed. If you have not seen it, start there, '
            'because it teaches the pattern. [[slnc 300]] This video does '
            'not teach it again. It uses the same online store, and it '
            'shows what changes when the meeting place stops being an '
            'object in your program and becomes a separate server on the '
            'network.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['NATS is a message bus that runs', 'as a program of its own.', '', 'It stores nothing and remembers', 'nobody.', '', 'You need a container runtime.', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before the first line of code, what NATS is. NATS is a '
            'message bus that runs as a program of its own. A service '
            'publishes an event under a name, and returns straight away. '
            'Another service subscribes to a name, and from that moment '
            'the server sends it every event published under that name. '
            '[[slnc 300]] NATS calls that name a subject. The important '
            'part is what NATS does not do. It stores nothing. It '
            'remembers nobody. An event goes to whoever is listening at '
            'that instant, and then it is gone. [[slnc 300]] You will '
            'need a container runtime running, such as Docker. Without '
            'one the demo prints a single sentence saying so, and stops. '
            'And skipping this video loses none of the pattern.'
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
            'First, the store before there is a bus. Five services that '
            'each tell the other four when an order is placed need twenty '
            'wires between them, because each pair needs one in each '
            'direction. [[slnc 250]] And now that these are separate '
            'programs, every one of those wires is a network address that '
            'somebody has to be told about, that can be typed wrong, and '
            'that can point at something which is not running. Add a '
            'sixth service and it needs ten more.'
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
            'Second, everyone knows the bus. Checkout publishes an order '
            'placed event under the name store dot orders dot placed, and '
            'returns immediately. It is told nothing at all about who was '
            'listening. [[slnc 250]] The email service saw the order. The '
            'warehouse saw the order. The analytics tally saw the order. '
            'Each of them has its own connection to the server, and none '
            'of them knows about the others. Five services, one '
            'connection each: five wires, not twenty.'
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
            'Third, subscribing by name. The hand-built bus let a '
            'subscriber ask for a type of event. NATS has no types. It '
            'has names, written in dotted parts, like store dot orders '
            'dot placed. [[slnc 250]] Checkout publishes four events: an '
            'order placed, that order cancelled, a payment taken, and '
            'stock running low. A listener that asks for the exact name '
            'store dot orders dot placed receives one event. [[slnc 200]] '
            'A listener can also ask for a family. A star stands for one '
            'part of the name, so store dot orders dot star receives two: '
            'the placed and the cancelled. An arrow stands for the whole '
            'rest of the name, so store dot arrow receives all four.'
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
            'Fourth, one failing subscriber. The email service throws: '
            'the mail server timed out. The warehouse, on a connection of '
            'its own, still reserves the stock for that order. [[slnc '
            '250]] In the hand-built bus that isolation had to be '
            'written, by catching the failure so one bad subscriber could '
            'not stop the rest. Here it is free, because the two '
            'subscribers are not even in the same program. And checkout '
            'was never told, because publishing had already returned '
            'before either of them ran.'
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
            'Fifth, and this is the act the whole video exists for: an '
            'event nobody hears. [[slnc 250]] Nobody is listening. '
            'Checkout publishes an order placed event for order ORD one. '
            'The call returns without an error, and the bus drops the '
            'event. There is no error, no record, and nowhere to read it '
            'back from. The hand-built bus noticed this and turned the '
            'event into a dead event that something could watch for. NATS '
            'has no such hook. [[slnc 350]] Then the warehouse starts '
            'listening, and checkout publishes order ORD two. The first '
            'event the warehouse ever receives is ORD two. [[slnc 250]] '
            'Pause on why that matters. You cannot prove a miss by '
            'waiting and seeing nothing, because you never know how long '
            'to wait. But this bus delivers one name in the order it was '
            'published. So once the second order has arrived, the first '
            'one cannot still be on its way. It was never coming. Two '
            'orders published, one received.'
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
            'There is one way out, and it is worth knowing. Telling this '
            'bus is never confirmed. Asking is. [[slnc 250]] A request is '
            'a question with a reply address attached to it. When you '
            'send a request under a name that nobody is listening to, the '
            'server does not leave you waiting. It answers immediately, '
            'and it says there are no responders. That is the only moment '
            'on this bus where a publisher ever learns that its words '
            'went nowhere.'
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
            'Last, the bill. Who reacts to an order being placed? Nothing '
            'in checkout says, and checkout genuinely cannot find out. '
            'The hand-built bus was an object you could ask. This one is '
            'a separate program, and only it knows, so it has to be asked '
            'on a second port that exists for that. It reports three '
            'listeners for store events. [[slnc 300]] Analytics then '
            'stops listening while keeping its connection open: two. Then '
            'all three services close their connections: none, because '
            'closing a connection takes every listener on it at once. '
            '[[slnc 300]] And the bus is now a program of its own to run, '
            'to watch and to keep up. This demo needed one container. '
            'And it keeps nothing, so a subscriber that is down when an '
            'event is published has missed it for good.'
        ),
    ),
    dict(
        key='11-contrast', kind='bullets', title='The Opposite Trade',
        body=['A durable log keeps events, so a', 'service that was down catches up', 'later.', '', 'Its price: storage, tracking every', 'reader, and the same event', 'possibly arriving twice.', '', 'NATS chooses the other side of', 'every one of those.'],
        narration=(
            'It is worth knowing what the other choice looks like, '
            'because this course covers both. A durable log keeps every '
            'event it is given. A service that was down comes back and '
            'reads everything it missed, and a brand new service can be '
            'built from the whole history. [[slnc 300]] The price is '
            'real: the server stores the events, it tracks how far every '
            'reader has got, and it may hand the same event over twice, '
            'so every reader has to be safe to repeat. [[slnc 300]] NATS '
            'chooses the other side of every one of those. Neither is '
            'right in general. Pick the one that matches what a missed '
            'event would actually cost you.'
        ),
    ),
    dict(
        key='12-verdict', kind='bullets', title='The Verdict',
        body=['Use it for announcements, not for', 'anything you cannot lose.', '', 'Name subjects for facts in the', 'past tense, and agree them as a', 'team.', '', 'Wait for the server to confirm a', 'subscription before publishing.'],
        narration=(
            'My verdict, plainly. Use this kind of bus for announcements: '
            'cache invalidations, live dashboards, telemetry, anything '
            'where the next event makes the last one irrelevant. [[slnc '
            '250]] Name your subjects for facts in the past tense, and '
            'agree the naming as a team, because the names are the '
            'contract and nothing checks them for you. [[slnc 250]] '
            'Always wait for the server to confirm a subscription before '
            'you publish something you want that subscriber to hear. And '
            'when an event genuinely must not be lost, do not reach for a '
            'longer timeout. Reach for a durable log, or ask instead of '
            'telling.'
        ),
    ),
    dict(
        key='13-recognise', kind='bullets', title='How To Recognise It',
        body=['Publish and subscribe taking a', 'dotted string.', '', 'Subject names with a star or an', 'arrow in them.', '', 'A flush before a publish: that is', 'somebody who has been bitten.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'connection object with publish and subscribe on it, both '
            'taking a dotted string rather than a class. [[slnc 200]] '
            'Subject names with a star or an arrow in them. A dispatcher, '
            'which is just a subscription with a handler attached instead '
            'of a loop. [[slnc 200]] And a flush call right before a '
            'publish. That one is somebody who has already been bitten by '
            'publishing before the server had agreed to the subscription.'
        ),
    ),
    dict(
        key='14-versions', kind='bullets', title='What Was Used',
        body=['NATS server 2.15.0, in a', 'container.', '', 'The NATS Java client, 2.26.3.', '', 'Testcontainers 2.0.5, which', 'starts and stops the container.', '', 'Java 21, and Docker 24 or later.'],
        narration=(
            'For the record. The NATS server, version 2 point 15 point '
            'zero, running in a container. The official NATS client for '
            'Java, version 2 point 26 point 3. Testcontainers, version 2 '
            'point zero point 5, which starts the container and stops it '
            'again. Java 21, and Docker 24 or later.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real server', 'in a container, real subjects,', 'real dropped events.', '', 'No test sleeps. Every wait has a', 'deadline and fails rather than', 'hangs.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything here is real: a real NATS server in a container, '
            'real subjects, and events that are really dropped. [[slnc '
            '250]] And no test anywhere in this project sleeps for a '
            'fixed time. Every wait has a deadline, and when the deadline '
            'passes the test fails and says who was waiting for what, '
            'rather than hanging.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try adding a loyalty service that', 'listens for payments, and watch it hear nothing else.'],
        narration=(
            "That's the Event Bus pattern with NATS. [[slnc 250]] If you "
            'take one sentence away, take this one: on this bus, '
            'publishing always succeeds, and succeeding means nothing. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough you can step through '
            'are all in the repository. [[slnc 300]] If you try one '
            'exercise, add a loyalty service that listens for payments '
            'taken, and watch it hear the payment and nothing else. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
