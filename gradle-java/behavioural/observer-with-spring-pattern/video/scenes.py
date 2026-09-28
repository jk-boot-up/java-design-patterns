"""Scene definitions for the Observer with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Observer with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Observer pattern, in Java, using Spring Boot. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] The Observer '
            'pattern lets one object announce that something happened, '
            'and any number of others react, without the announcer '
            'knowing who they are. [[slnc 500]] In Spring, a listener is '
            'simply a method marked as an event listener. [[slnc 300]] '
            'And the publisher only knows about the event. [[slnc 600]] '
            'Think of a radio station. [[slnc 300]] It broadcasts, and '
            'never knows who is tuned in. [[slnc 700]] This is the '
            'framework version of the Observer video, with the same '
            'online orders. [[slnc 400]] We will send order events '
            "through Spring's publisher. [[slnc 300]] Then we will hear "
            "how delivery really behaves. [[slnc 300]] On the caller's "
            'thread, stopped by a failure, filtered by a condition, moved '
            'to another thread, and silently dropped when nobody listens.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Observer, the hand-built video,', 'lets an order announce each status', 'change to inventory, email,', 'analytics and the warehouse.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Observer video. [[slnc 400]] That '
            'one lets an order announce each status change to inventory, '
            'email, analytics, and the warehouse feed, without knowing '
            'any of them. [[slnc 300]] And it reports a failing listener '
            'by name. [[slnc 500]] If you are new to the pattern, watch '
            'that one first. [[slnc 400]] Here, we keep the same example, '
            'and ask what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'It has an event publisher, and', 'a listener annotation.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            'At its heart, Spring is a container that creates your '
            'objects. [[slnc 300]] It includes an event publisher. [[slnc '
            '300]] And any method marked with the at Event Listener '
            'annotation becomes an observer. [[slnc 500]] And one '
            'promise. [[slnc 300]] If you skip this video, you lose none '
            'of the pattern. [[slnc 300]] This one is about the tool.'
        ),
    ),
    dict(
        key='04-subject', kind='console', title='The Subject Knows Nobody',
        body="""ONE. Knows nobody.
  inventory: released stock
  email: told the customer
  analytics: counted
  warehouse feed: pick line""",
        narration=(
            'First demo: the subject knows nobody. [[slnc 400]] An order '
            'is shipped, and publishes one event. [[slnc 400]] Four '
            'listeners react. [[slnc 300]] Inventory releases the stock. '
            '[[slnc 200]] Email tells the customer. [[slnc 200]] '
            'Analytics counts it. [[slnc 200]] And the warehouse feed '
            'writes a pick line. [[slnc 500]] The order only holds a '
            'publisher. [[slnc 300]] It has no list of listeners, and no '
            'field named after any of them.'
        ),
    ),
    dict(
        key='05-thread', kind='console', title="On The Caller's Thread",
        body="""TWO. Caller's thread.
  the caller is main, and every
  listener above ran on it.""",
        narration=(
            'Second demo: which thread do the listeners run on? [[slnc '
            "400]] Every listener ran on the caller's own thread. [[slnc "
            '300]] And all of them finished before the publish call '
            "returned. [[slnc 500]] Spring's events are synchronous by "
            'default. [[slnc 300]] Publishing an event is really a method '
            'call in disguise.'
        ),
    ),
    dict(
        key='06-fail', kind='console', title='One Listener Fails',
        body="""THREE. A failure.
  the caller got: mail server
  timed out.
  order shipped: true.

  inventory heard. analytics and
  the warehouse feed did not.""",
        narration=(
            'Third demo: one listener fails. [[slnc 400]] The mail server '
            'times out, and the email listener throws an error. [[slnc '
            '400]] That error travels all the way back to the caller. '
            '[[slnc 300]] Inventory had already heard the event. [[slnc '
            '300]] But analytics and the warehouse feed never do. [[slnc '
            '500]] So the order is shipped, and the warehouse does not '
            'know. [[slnc 300]] This is exactly the trap from the naive '
            'version, arriving through the framework.'
        ),
    ),
    dict(
        key='07-async', kind='console', title='A Listener On Another Thread',
        body="""FOUR. Another thread.
  cancel() has returned.
  no audit line yet.

  gate opens: 1 audit line,
  on a thread named task-1.""",
        narration=(
            'Fourth demo: a listener on another thread. [[slnc 400]] The '
            'audit listener is marked to run asynchronously. [[slnc 300]] '
            'And for this demo, it is held back at a gate. [[slnc 500]] '
            'The cancel call has already returned. [[slnc 300]] But there '
            'is no audit line yet. [[slnc 400]] Then the gate opens. '
            '[[slnc 300]] The audit line appears, written from a separate '
            'thread, named task one. [[slnc 500]] Now a failure in that '
            'listener could never reach the caller. [[slnc 300]] But the '
            'caller also cannot know when, or whether, it finished. '
            '[[slnc 300]] That is the trade.'
        ),
    ),
    dict(
        key='08-filter', kind='console', title='A Listener That Filters',
        body="""FIVE. A filter.
  shipped: the warehouse heard:
  true.
  cancelled: the warehouse heard:
  false.""",
        narration=(
            'Fifth demo: a listener that filters. [[slnc 400]] The '
            'warehouse listener has a condition on its annotation. [[slnc '
            '400]] When an order ships, the warehouse hears about it. '
            '[[slnc 300]] When an order is cancelled, it does not. [[slnc '
            '500]] In the hand-built version, filters were refused, '
            'because they let a listener decide things for the others. '
            '[[slnc 300]] Here, a filter is one line, and easy to add.'
        ),
    ),
    dict(
        key='09-silent', kind='console', title='An Event Nobody Hears',
        body="""SIX. Nobody hears.
  refund published.
  listeners that ran: 0.
  errors: 0.

  a publisher cannot tell.""",
        narration=(
            'Last demo: an event that nobody hears. [[slnc 400]] A refund '
            'event is published. [[slnc 300]] Zero listeners run. [[slnc '
            '300]] And there is no error. [[slnc 500]] If someone deletes '
            'the refund listener, or types the wrong event class, nothing '
            'complains. [[slnc 400]] The only defence is a test that '
            'checks the reaction actually happened.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Publish events.', '', 'Keep listeners independent.', '', 'Isolate failures inside', 'listeners.', '', 'Test that the wiring exists.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Publish events. [[slnc '
            '300]] Keep listeners independent of each other. [[slnc 300]] '
            'Catch failures inside any listener that must not stop the '
            'others. [[slnc 300]] And write tests that prove the wiring '
            'exists.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['ApplicationEventPublisher in a', 'constructor.', '', '@EventListener on a method.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for an Application Event Publisher passed into a '
            'constructor. [[slnc 300]] And look for methods marked at '
            'Event Listener, whose only parameter is the event.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every Spring application that', 'reacts to something.', '', 'Startup, refresh, or your own', 'domain events.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In every Spring '
            'application that reacts to something. [[slnc 300]] Such as '
            'the application starting up, or your own business events.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] No web server, '
            'no database, and no web library.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's events", 'and its executor.', '', 'The other thread is held at a gate,', 'so the order is the same every time.'],
        narration=(
            "A quick, honest note about this demo. [[slnc 300]] Spring's "
            'events, and its thread pool, are real. [[slnc 300]] The '
            'extra thread is held at a gate, so things happen in the same '
            'order every time.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['When there is one reaction and it', 'must succeed, call it directly.'],
        narration=(
            'So, when is this too much? [[slnc 400]] When there is only '
            'one reaction, and it must succeed, just call it directly. '
            '[[slnc 300]] Events are for reactions that may come and go.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Wrap the email listener in a try', 'block and rerun act three.'],
        narration=(
            "That's Observer with Spring. [[slnc 400]] If you remember "
            "one sentence, make it this one. [[slnc 300]] Spring's events "
            'separate the publisher from its listeners, but delivery is '
            'synchronous, and silent about who is listening. [[slnc 500]] '
            'The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Wrap the email '
            "listener's work in a try block. [[slnc 300]] Then run the "
            'failure demo again, and listen for the difference. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
