"""Scene definitions for the Observer with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Observer with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Observer pattern '
            'with Spring Boot, in Java, and it is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] It is the framework '
            'version of the Observer video. That one let an order '
            'announce every status change to inventory, email, analytics '
            'and the warehouse feed, without knowing any of them, and '
            'reported a failing listener by name. This one shows the same '
            'idea inside Spring Boot. [[slnc 350]] The plain definition, '
            'in short: in Spring, an observer is a method marked as an '
            'event listener. The publisher only knows the event. [[slnc '
            '300]] By the end you will see the order announce events '
            "through Spring's publisher, then see how delivery really "
            "behaves: on the caller's thread, stopped by a failure, "
            'filtered by a condition, moved to another thread, and '
            'dropped when nobody listens.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Observer, the hand-built video,', 'lets an order announce each status', 'change to inventory, email,', 'analytics and the warehouse.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Observer video. If you have not seen '
            'it, start there. It lets an order announce each status '
            'change to inventory, email, analytics and the warehouse '
            'feed, without knowing any of them, and it reports a failing '
            'listener by name. [[slnc 300]] This one uses the same '
            'example. It does not teach the pattern again. It shows what '
            'Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'It has an event publisher, and', 'a listener annotation.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'is a framework whose core is a container that creates your '
            'objects. It includes an event publisher, and any method '
            'marked as an event listener is an observer. [[slnc 300]] And '
            'a promise: skipping this video loses none of the pattern. '
            'The hand-built one teaches all of it.'
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
            'First, the pattern working. The order is shipped, and '
            'publishes one event. Four listeners react: inventory, email, '
            'analytics and the warehouse feed. The order holds only a '
            'publisher. It has no list, and no field named after any '
            'listener.'
        ),
    ),
    dict(
        key='05-thread', kind='console', title="On The Caller's Thread",
        body="""TWO. Caller's thread.
  the caller is main, and every
  listener above ran on it.""",
        narration=(
            "Second, where they run. Every listener ran on the caller's "
            "own thread, before the publish call returned. Spring's "
            'events are synchronous by default. It is a method call in '
            'disguise.'
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
            'Third, a failing listener. The mail server times out, and '
            'the email listener throws. The exception reaches the caller. '
            'Inventory had heard already. Analytics and the warehouse '
            'feed never do. [[slnc 300]] The order is shipped, and the '
            'warehouse does not know. This is the exact trap of the naive '
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
            'Fourth, another thread. The audit listener is marked '
            'asynchronous, and held at a gate. Cancel has returned, and '
            'there is no audit line yet. [[slnc 300]] Open the gate, and '
            'the audit line appears, from a thread named task one. Now a '
            'failure in that listener could not reach the caller. That is '
            'the trade.'
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
            'Fifth, a filter. The warehouse listener carries a condition '
            'on its annotation. It hears shipments. It does not hear '
            'cancellations. In the hand-built version we refused filters, '
            'because they let a listener speak for the others. Here it is '
            'one line.'
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
            'Last, an event nobody hears. A refund is published. Zero '
            'listeners run, and there is no error. [[slnc 300]] If '
            'someone deletes the refund listener, or mistypes the event '
            'class, nothing complains. The only defence is a test that '
            'says the reaction happened.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Publish events.', '', 'Keep listeners independent.', '', 'Isolate failures inside', 'listeners.', '', 'Test that the wiring exists.'],
        narration=(
            'My verdict, plainly. Publish events. Keep listeners '
            'independent. Isolate failures inside the listeners that must '
            'not stop the others. And test that the wiring exists.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['ApplicationEventPublisher in a', 'constructor.', '', '@EventListener on a method.'],
        narration=(
            'How do you recognise this in code you did not write? An '
            'event publisher in a constructor. And an event listener '
            'annotation on a method, whose only argument is the event.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every Spring application that', 'reacts to something.', '', 'Startup, refresh, or your own', 'domain events.'],
        narration=(
            'You have met this in every Spring application that reacts to '
            'something. Startup, context refresh, or your own domain '
            'events.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. No web '
            'server, no database, and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's events", 'and its executor.', '', 'The other thread is held at a gate,', 'so the order is the same every time.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            "Everything is real: Spring's events and its executor. The "
            'other thread is held at a gate, so the order is the same '
            'every time.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['When there is one reaction and it', 'must succeed, call it directly.'],
        narration=(
            'So when is it too much? When there is one reaction and it '
            'must succeed, call it directly. An event is for reactions '
            'that may come and go.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Wrap the email listener in a try', 'block and rerun act three.'],
        narration=(
            "That's Observer with Spring. [[slnc 250]] If you take one "
            "sentence away, take this one: Spring's events decouple the "
            'publisher, but delivery is synchronous and silent about who '
            'is listening. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository. [[slnc 300]] If you try one exercise, wrap '
            'the email listener in a try block, and rerun act three. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
