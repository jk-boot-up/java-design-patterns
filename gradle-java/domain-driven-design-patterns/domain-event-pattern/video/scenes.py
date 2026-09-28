"""Scene definitions for the Domain Event teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Domain Event',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Domain Event pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A domain event is a record '
            'of something that has already happened in the business. '
            '[[slnc 300]] It is named in the past tense, and it never '
            'changes. [[slnc 300]] Other parts of the system can react to '
            'it, without the thing that raised it knowing who they are. '
            '[[slnc 600]] Think of a birth announcement in a newspaper. '
            '[[slnc 300]] It states a fact that has already happened. '
            '[[slnc 300]] Whoever reads it decides what to do: send a '
            'card, visit, or nothing. [[slnc 700]] In our online store, '
            'the thing that happens is an order being placed. [[slnc '
            '500]] In this video, an order that calls three services '
            'falls into a half-done state. [[slnc 300]] Then the same '
            'order simply says what happened. [[slnc 300]] We will hear a '
            'failing reaction retried safely, and the gap between saving '
            'and telling, which is the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order is placed:', '', 'stock is reserved,', 'a confirmation email is sent,', 'and the sales funnel is counted.', '', 'Who calls whom?'],
        narration=(
            'Here is the scenario. [[slnc 400]] When an order is placed '
            'in our online store, three things must follow. [[slnc 300]] '
            'Stock is reserved. [[slnc 200]] A confirmation email is '
            'sent. [[slnc 200]] And the sale is counted for the sales '
            'report. [[slnc 500]] So here is the question. [[slnc 300]] '
            'Who calls whom? [[slnc 300]] Should the order code know '
            'about all three?'
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
            'First, the naive way: the order calls everyone. [[slnc 400]] '
            'It saves the order, reserves the stock, and then sends the '
            'email. [[slnc 300]] But the mail server is down. [[slnc '
            '500]] The caller is told that placing the order failed. '
            '[[slnc 300]] Yet the order is saved, and the stock is '
            'reserved. [[slnc 300]] And the sales report never counted '
            'it, because that step came after the failure. [[slnc 500]] A '
            'half-done state. [[slnc 300]] And the order code knows three '
            'other systems.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['The order records what happened:', 'OrderPlaced, in the past tense.', '', 'It calls nobody.', '', 'Whoever cares reacts, later,', 'and separately.', '', 'An event is a fact, and never', 'changes.'],
        narration=(
            'Now, the pattern. [[slnc 400]] The order records what '
            'happened: order placed, in the past tense. [[slnc 300]] It '
            'calls nobody. [[slnc 500]] Whoever cares reacts, later, and '
            'separately. [[slnc 500]] And an event is a fact. [[slnc '
            '300]] Once recorded, it never changes.'
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
            'Second demo: the order says what happened. [[slnc 400]] '
            'Placing order two records one event: order placed. [[slnc '
            '300]] It holds the order I D, the customer, Ada, and the '
            'total, forty-nine pounds ninety-nine. [[slnc 500]] The order '
            'called nobody. [[slnc 300]] Ask for its events again, and '
            'there are none. [[slnc 300]] Because they have already been '
            'handed over.'
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
            'Third demo: delivered after the save. [[slnc 400]] Saving '
            'the order also keeps its event. [[slnc 300]] At this point, '
            'nothing has reacted yet. [[slnc 500]] Then a relay delivers '
            'the event. [[slnc 300]] Stock is reserved. [[slnc 200]] The '
            'email is sent. [[slnc 200]] And the sales report counts it. '
            '[[slnc 300]] Nothing is waiting any more.'
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
            'Fourth demo: a failing reaction. [[slnc 400]] The mail '
            'server is down. [[slnc 300]] The email reaction fails. '
            '[[slnc 300]] The other two reactions still run. [[slnc 500]] '
            'The order is safe. [[slnc 300]] And one event is still '
            'waiting, for the email alone. [[slnc 500]] When the mail '
            'server is back, the next relay sends just that email. [[slnc '
            '300]] The email goes out once, and the stock is not reserved '
            'twice.'
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
            'Fifth demo: events are facts. [[slnc 400]] Place an order, '
            'and then cancel it. [[slnc 300]] Two events are recorded, in '
            'that order: order placed, then order cancelled. [[slnc 500]] '
            'Each event is a simple record. [[slnc 300]] It carries data, '
            'not the order itself. [[slnc 300]] So a handler that '
            'receives one cannot reach back and change the order.'
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
            'Finally, the cost: the gap between saving and telling. '
            '[[slnc 400]] Saving the order, and telling everyone about '
            'it, are two separate steps. [[slnc 300]] And the program can '
            'stop between them. [[slnc 500]] Here it does. [[slnc 300]] '
            'Nothing has reacted yet. [[slnc 300]] But the event was '
            'saved together with the order. [[slnc 500]] After a restart, '
            'the relay delivers it, and nothing is lost. [[slnc 500]] If '
            'the event had been sent straight after the save, and not '
            'kept, all three reactions would have been lost. [[slnc 300]] '
            'Keeping events with the data like this is called the '
            'transactional outbox, and it has its own video.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A method that records an event,', 'not one that calls a service.', '', 'Names in the past tense:', 'OrderPlaced.', '', 'A list of events on an entity,', 'collected when it is saved.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a method that records an event, '
            'instead of calling a service. [[slnc 300]] Look for event '
            'names in the past tense, like order placed, or payment '
            'received. [[slnc 300]] Look for a list of events on an '
            'entity, collected when it is saved. [[slnc 300]] And in '
            'Spring, look for the application event publisher, and the at '
            'Domain Events annotation.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Name it in the past tense.', '', 'Save events with the aggregate.', '', 'Deliver separately, and', 'expect repeats.', '', 'Make each handler safe to', 'run twice.', '', 'Not when the caller needs', 'the answer.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Raise a domain event '
            'when something happens that other parts of the business care '
            'about. [[slnc 300]] Name it in the past tense, and keep it '
            'small. [[slnc 500]] Save the events together with the data. '
            '[[slnc 300]] Deliver them separately. [[slnc 300]] Expect a '
            'delivery to be repeated, so make every handler safe to run '
            'twice. [[slnc 500]] And do not use an event where the caller '
            'needs an answer straight away.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'The mail server is a switch that', 'makes the email fail.', '', 'The relay is called by hand, so', 'the order of events is the same', 'every run.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] The mail server is a '
            'simple switch, which makes the email fail. [[slnc 300]] And '
            'the relay is run by hand, so events happen in the same order '
            'on every run.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['When there is one reaction and the', 'caller needs its answer, a plain', 'call is clearer.', '', 'An event is for reactions that may', 'come and go, later.'],
        narration=(
            'So, when is this too much? [[slnc 400]] When there is only '
            'one reaction, and the caller needs its answer, a plain '
            'method call is clearer. [[slnc 400]] An event is for '
            'reactions that may come and go, and may happen later.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add an OrderShipped event and a', 'handler that reacts to it.'],
        narration=(
            "That's the Domain Event pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] An '
            'event lets something say what happened, and leaves who cares '
            'to someone else, as long as saving and telling are kept '
            'together. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add an order shipped event. [[slnc 300]] And a handler '
            'that reacts to it. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
