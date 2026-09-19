"""Scene definitions for the Domain Event teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Domain Event',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Domain Event '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'domain event is a record of something that has already '
            'happened in the business, named in the past tense, that '
            'never changes, so that other parts of the system can react '
            'to it without the thing that raised it knowing who they are. '
            '[[slnc 350]] This is the third project in the domain-driven '
            'design category, whose subject is writing code that says '
            'what the business says. In our online store, the thing that '
            'happens is an order being placed. [[slnc 300]] By the end '
            'you will see an order that calls three services fall into a '
            'half-done state, see the same order say what happened '
            'instead, watch a failing reaction leave the order alone and '
            'be retried, and see the gap between saving and telling, '
            'which is the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order is placed:', '', 'stock is reserved,', 'a confirmation email is sent,', 'and the sales funnel is counted.', '', 'Who calls whom?'],
        narration=(
            'Here is the scenario. When an order is placed in the online '
            'store, three things follow. Stock is reserved. A '
            'confirmation email is sent. And the sales funnel is counted. '
            '[[slnc 300]] The question: who calls whom? Should the order '
            'code know all three?'
        ),
    ),
    dict(
        key='03-calls', kind='console', title='The Order Calls Everyone',
        body="""ONE. Calls everyone.
  the mail server is down.
  the caller: mail server
  timed out.

  order saved: true.
  stock reserved.
  analytics never counted it.""",
        narration=(
            'First, the order calls everyone. It saves the order, '
            'reserves stock, and then sends the email, and the mail '
            'server is down. The caller is told that it failed. But the '
            'order is saved, and stock is reserved. And analytics never '
            'counted it, because that call was after the failure. [[slnc '
            '300]] A half done state, and the order code knows three '
            'other systems.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['The order records what happened:', 'OrderPlaced, in the past tense.', '', 'It calls nobody.', '', 'Whoever cares reacts, later,', 'and separately.', '', 'An event is a fact, and never', 'changes.'],
        narration=(
            'The pattern. The order records what happened: order placed, '
            'in the past tense. It calls nobody. Whoever cares reacts, '
            'later, and separately. And an event is a fact. It is never '
            'changed after it is recorded.'
        ),
    ),
    dict(
        key='05-says', kind='console', title='The Order Says What Happened',
        body="""TWO. It says.
  place() recorded:
  OrderPlaced for ORD-2,
  ada, 4999 pence.

  the order called nobody.
  asked again: nothing.""",
        narration=(
            'Second, the order says what happened. Placing it records one '
            'event: order placed, with the id, the customer and the '
            'total. The order called nobody. Ask for the events again, '
            'and there are none, because they have been handed over.'
        ),
    ),
    dict(
        key='06-after', kind='console', title='Delivered After The Save',
        body="""THREE. After the save.
  saved. 1 event waiting.
  reactions: 0.

  relay:
  stock reserved.
  email sent.
  analytics counted.
  0 waiting.""",
        narration=(
            'Third, delivered after the save. Saving the order keeps its '
            'event. Nothing has reacted yet. Then a relay delivers the '
            'event: stock is reserved, the email is sent, and analytics '
            'counts it. Nothing is waiting any more.'
        ),
    ),
    dict(
        key='07-fail', kind='console', title='A Failing Reaction',
        body="""FOUR. A failure.
  the mail server is down.
  email failed. stock and
  analytics ran.
  1 event still waiting.

  server back: next relay
  sends the email once.""",
        narration=(
            'Fourth, a failing reaction. The mail server is down. The '
            'email reaction fails, and the other two run. The order is '
            'safe, and one event is still waiting, for the email alone. '
            '[[slnc 300]] When the server is back, the next relay sends '
            'just that one. The email went out once, and stock was not '
            'reserved twice.'
        ),
    ),
    dict(
        key='08-facts', kind='console', title='Events Are Facts',
        body="""FIVE. Facts.
  place then cancel:
  OrderPlaced,
  OrderCancelled.

  records: data, not the
  order. a handler cannot
  reach back.""",
        narration=(
            'Fifth, events are facts. Place the order and then cancel it, '
            'and two events are recorded, in that order. Each is a '
            'record. It carries the data, and it does not carry the '
            'order. A handler that receives one cannot reach back and '
            'change the order.'
        ),
    ),
    dict(
        key='09-gap', kind='console', title='The Gap Between Saving And Telling',
        body="""SIX. The gap.
  stopped after the save,
  before the relay.
  reactions: 0. kept: 1.

  after a restart, the relay:
  reactions: 3.
  nothing lost.""",
        narration=(
            'Last, the bill. Saving the order and telling everyone are '
            'two steps, and the process can stop between them. Here it '
            'does. Nothing has reacted, but the event was saved with the '
            'order. After a restart, the relay delivers it, and nothing '
            'is lost. [[slnc 300]] Publishing straight after the save, '
            'with nothing kept, would have lost all three. That is the '
            'transactional outbox, and it is the next thing to read.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A method that records an event,', 'not one that calls a service.', '', 'Names in the past tense:', 'OrderPlaced.', '', 'A list of events on an entity,', 'collected when it is saved.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'method that records an event instead of calling a service. '
            'Event names in the past tense, like order placed, or payment '
            'received. A list of events on an entity, collected when it '
            'is saved. And in Spring, the application event publisher, '
            'and the domain events annotation.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Name it in the past tense.', '', 'Save events with the aggregate.', '', 'Deliver separately, and', 'expect repeats.', '', 'Make each handler safe to', 'run twice.', '', 'Not when the caller needs', 'the answer.'],
        narration=(
            'Here is my verdict, plainly. Raise a domain event when '
            'something happens that other parts of the business care '
            'about. Name it in the past tense, and keep it small. Save '
            'the events with the aggregate. Deliver them separately, '
            'expect a delivery to be repeated, and make each handler safe '
            'to run twice. And do not use an event where the caller needs '
            'the answer straight away.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'The mail server is a switch that', 'makes the email fail.', '', 'The relay is called by hand, so', 'the order of events is the same', 'every run.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. The mail server is a switch that '
            'makes the email fail. The relay is called by hand, so the '
            'order of events is the same every run.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['When there is one reaction and the', 'caller needs its answer, a plain', 'call is clearer.', '', 'An event is for reactions that may', 'come and go, later.'],
        narration=(
            'So when is it too much? When there is one reaction, and the '
            'caller needs its answer, a plain call is clearer. An event '
            'is for reactions that may come and go, and may happen later.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add an OrderShipped event and a', 'handler that reacts to it.'],
        narration=(
            "That's Domain Event. [[slnc 250]] If you take one sentence "
            'away, take this one: an event lets a thing say what '
            'happened, and leaves who cares to someone else, if the '
            'saving and the telling are kept together. [[slnc 350]] The '
            'full source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, add an order shipped event and a '
            'handler that reacts to it. [[slnc 300]] If this helped, a '
            'like genuinely does help other people find it, and subscribe '
            'if you would like the rest of the series. [[slnc 250]] '
            'Thanks for watching.'
        ),
    ),
]
