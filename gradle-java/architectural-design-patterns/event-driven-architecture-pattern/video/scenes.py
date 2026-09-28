"""Scene definitions for the Event-Driven Architecture teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Event-Driven Architecture',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Event-Driven Architecture pattern, in Java. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] In an event-driven '
            'system, services do not call each other. [[slnc 300]] '
            'Instead, each one writes facts, called events, to a shared '
            'log. [[slnc 300]] And each one reads that log at its own '
            'pace. [[slnc 600]] Think of a kitchen with a ticket rail. '
            '[[slnc 300]] The waiter clips an order ticket to the rail, '
            'and walks away. [[slnc 300]] The grill cook and the salad '
            'cook each read the tickets when they are ready. [[slnc 300]] '
            'The waiter never waits for a cook. [[slnc 700]] In our '
            'online store, three services must work together: orders, '
            'inventory, and shipping. [[slnc 300]] And any of them may be '
            'down at any moment. [[slnc 500]] In this video, we will lose '
            'an order the old way, then fix it with a log. [[slnc 300]] '
            'We will watch a service catch up after being down, add a '
            'brand new reader, and then look at the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order is placed:', '', 'inventory reserves stock,', 'shipping plans a delivery.', '', 'Either may be down right now.', '', 'Should the order wait?'],
        narration=(
            'Here is the scenario. [[slnc 400]] A customer places an '
            'order. [[slnc 300]] Inventory must reserve the stock. [[slnc '
            '300]] Shipping must plan a delivery. [[slnc 400]] But either '
            'of those services might be down right now. [[slnc 500]] So '
            "here is the question. [[slnc 300]] Should the customer's "
            'order have to wait for them?'
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
            'First, the old way: services calling each other. [[slnc '
            '400]] The order service calls shipping, and waits for an '
            'answer. [[slnc 300]] But shipping is down. [[slnc 400]] So '
            'the order is not accepted. [[slnc 500]] A customer just lost '
            'their order, because of a service they never even see.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Services do not call each other.', '', 'They write facts to a log,', 'and read the log at their', 'own pace.', '', 'Each remembers how far', 'it has read.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Services do not call each '
            'other. [[slnc 300]] They write facts to a log. [[slnc 300]] '
            'And each service reads the log at its own pace. [[slnc 400]] '
            'Each one also remembers how far it has read, like a bookmark '
            'in a book.'
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
            'Second demo: telling the log. [[slnc 400]] The order service '
            'adds an event to the log, at position zero. [[slnc 300]] '
            'Then it is finished. [[slnc 400]] It knows nothing about '
            'inventory or shipping. [[slnc 300]] It does not even hold a '
            'reference to them. [[slnc 400]] Inventory reads the event, '
            'and acts. [[slnc 300]] Shipping reads the same event, and '
            'acts too.'
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
            'Third demo: a service that is down. [[slnc 400]] Shipping is '
            'switched off. [[slnc 300]] Three orders arrive, and all '
            'three are accepted anyway. [[slnc 400]] Shipping has planned '
            'nothing yet. [[slnc 300]] It is three events behind. [[slnc '
            '500]] Then shipping comes back. [[slnc 300]] It opens the '
            'log at its bookmark, and reads on. [[slnc 300]] It catches '
            'up, and plans all three deliveries. [[slnc 300]] Now it is '
            'zero behind.'
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
            'Fourth demo: a new reader. [[slnc 400]] After two orders '
            'have been placed, we add a brand new service: analytics. '
            '[[slnc 400]] It reads the log from the very beginning. '
            '[[slnc 300]] So it sees both earlier orders. [[slnc 400]] '
            'And the order service was not changed at all. [[slnc 400]] '
            'Because the log is kept, a new service can be built from '
            'history.'
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
            'Fifth demo: things do not happen at the same instant. [[slnc '
            '400]] An order is accepted. [[slnc 300]] But the stock count '
            'still says ten. [[slnc 300]] It should say nine. [[slnc '
            '400]] A moment later, inventory reads the event, and the '
            'count becomes nine. [[slnc 500]] For that short moment, the '
            'two services disagree. [[slnc 300]] This is called eventual '
            'consistency. [[slnc 300]] The system becomes correct, but '
            'not at every single instant.'
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
            'Finally, the cost. [[slnc 400]] Sometimes the same event is '
            'delivered twice. [[slnc 400]] Without a duplicate check, the '
            'stock drops twice, to eight. [[slnc 300]] That is wrong. '
            '[[slnc 300]] With a duplicate check, it stays at nine, which '
            'is right. [[slnc 500]] There is a second cost. [[slnc 300]] '
            'The journey of one order is now spread across several '
            'services. [[slnc 300]] To follow it, you have to read the '
            'log, not one piece of code.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Kafka, Pulsar, Kinesis or a', 'similar log at the centre of a', '', 'Services whose only link is a', 'topic name.', '', 'Event sourcing, and CQRS read', 'models built by reading events.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a log at the centre of the system, '
            'such as Kafka, Pulsar, or Kinesis. [[slnc 300]] Look for '
            'services whose only connection is the name of a topic. '
            '[[slnc 300]] Look for event sourcing, or read models built '
            'by reading events. [[slnc 300]] And look for readers that '
            'track an offset, or report how far behind they are.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use events when services should', 'not depend on each other being up,', 'and when new services will come.', 'Keep the log. Expect eventual', 'consistency, and design for it.', 'Make every reader safe to repeat.', 'And keep a way to see the whole', 'flow, because no single piece of', 'code shows it.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use events when '
            'services should not depend on each other being up. [[slnc '
            '300]] And when you expect new services to join later. [[slnc '
            '500]] Then follow four rules. [[slnc 300]] One. [[slnc 200]] '
            'Keep the log. [[slnc 300]] Two. [[slnc 200]] Expect eventual '
            'consistency, and design for it. [[slnc 300]] Three. [[slnc '
            '200]] Make every reader safe to run twice on the same event. '
            '[[slnc 300]] And four. [[slnc 200]] Keep a way to see the '
            'whole flow, because no single piece of code shows it.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a small system where all parts', 'are always up together, a direct', 'call is simpler and easier to', 'follow. Events pay off when parts', 'fail or change on their own.'],
        narration=(
            'So, when is this too much? [[slnc 400]] In a small system '
            'where every part is always up together, a direct call is '
            'simpler, and easier to follow. [[slnc 400]] Events pay off '
            'when the parts fail, or change, on their own.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Event-Driven Architecture. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] '
            'Event-driven architecture lets services work without waiting '
            'for each other, and the price is that nothing is instant, '
            'and the flow is harder to see. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Add a shipping reader that fails on one '
            'event. [[slnc 300]] Then decide what the reader should do '
            'with it. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
