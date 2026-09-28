"""Scene definitions for the Event Bus teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Event Bus',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Event Bus pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An event bus is one central '
            'place inside a program. [[slnc 300]] Parts of the program '
            'post events to it. [[slnc 300]] And other parts subscribe to '
            'the kinds of event they care about. [[slnc 300]] So none of '
            'them needs a reference to any other. [[slnc 600]] Think of '
            'the announcement speakers in a railway station. [[slnc 300]] '
            'The announcer does not know who is listening. [[slnc 300]] '
            'Each traveller only listens for their own train. [[slnc '
            '700]] In our online store, five parts of one program all '
            'want to know when an order is placed, or cancelled. [[slnc '
            '500]] In this video, five parts that all know each other are '
            'replaced by a bus. [[slnc 300]] We will hear subscribers '
            'choosing events by type, a failing subscriber that harms '
            'nobody else, an event nobody hears, and then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=["Inside the shop's program, five", 'components react to orders:', '', 'inventory, email, analytics,', 'loyalty, and the audit log.', '', 'Who talks to whom?'],
        narration=(
            "Here is the scenario. [[slnc 400]] Inside the online store's "
            'program, five parts react when an order is placed or '
            'cancelled. [[slnc 300]] Inventory, email, analytics, loyalty '
            'points, and the audit log. [[slnc 500]] So here is the '
            'question. [[slnc 300]] Who talks to whom?'
        ),
    ),
    dict(
        key='03-web', kind='console', title='Everyone Knows Everyone',
        body="""ONE. A web.
  5 components tell each other:
  20 references.

  a sixth needs 10 more.""",
        narration=(
            'First, the naive way: everyone knows everyone. [[slnc 400]] '
            'Five parts that each tell each other about orders need '
            'twenty references between them. [[slnc 500]] Add a sixth '
            'part, and it needs ten more. [[slnc 300]] The web of '
            'connections grows much faster than the number of parts.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One bus, inside the program.', '', 'Components post events to it.', '', 'Components subscribe to the kinds', 'of event they care about.', '', 'Nobody holds a reference to', 'anybody else.'],
        narration=(
            'Now, the pattern. [[slnc 400]] There is one bus, inside the '
            'program. [[slnc 300]] Parts post events to it. [[slnc 300]] '
            'Parts subscribe to the kinds of event they care about. '
            '[[slnc 500]] And nobody holds a reference to anybody else.'
        ),
    ),
    dict(
        key='05-bus', kind='console', title='Everyone Knows The Bus',
        body="""TWO. The bus.
  one post reaches inventory,
  email, analytics.

  5 components, 1 reference
  each: 5, not 20.

  the poster knows no one.""",
        narration=(
            'Second demo: everyone knows the bus. [[slnc 400]] One post '
            'reaches inventory, email, and analytics. [[slnc 500]] Five '
            'parts, each holding one reference, to the bus. [[slnc 300]] '
            'That is five references, not twenty. [[slnc 500]] And the '
            'part that posts the event does not know who hears it.'
        ),
    ),
    dict(
        key='06-type', kind='console', title='By Type',
        body="""THREE. By type.
  for OrderPlaced: ORD-1.
  for every OrderEvent:
  OrderPlaced ORD-1,
  OrderCancelled ORD-1.""",
        narration=(
            'Third demo: subscribing by type. [[slnc 400]] One subscriber '
            'listens for order placed, and hears only that. [[slnc 500]] '
            'Another listens for every kind of order event. [[slnc 300]] '
            'So it hears both: order placed, and order cancelled. [[slnc '
            '500]] Each subscriber asks for exactly the kind of thing it '
            'cares about.'
        ),
    ),
    dict(
        key='07-fail', kind='console', title='One Failing Subscriber',
        body="""FOUR. A failure.
  email fails.
  analytics still hears it.
  the failure is recorded.

  the poster carried on.""",
        narration=(
            'Fourth demo: one failing subscriber. [[slnc 400]] The email '
            'subscriber fails, with a timeout. [[slnc 300]] But analytics '
            'still hears the event. [[slnc 500]] The failure is recorded. '
            '[[slnc 300]] And the part that posted the event never sees '
            'it. [[slnc 300]] It posted, and carried on.'
        ),
    ),
    dict(
        key='08-dead', kind='console', title='An Event Nobody Hears',
        body="""FIVE. Nobody hears.
  no subscriber: 1 dead event,
  nothing complained.

  a subscriber for DeadEvent
  receives it.

  a forgotten subscription is a
  silent loss.""",
        narration=(
            'Fifth demo: an event that nobody hears. [[slnc 400]] With no '
            'subscriber at all, the bus counts it as a dead event. [[slnc '
            '300]] And nothing complains. [[slnc 500]] With a subscriber '
            'that listens for dead events, the unheard event arrives '
            'there instead. [[slnc 500]] A typo in an event type, or a '
            'forgotten subscription, is a silent loss. [[slnc 300]] '
            'Unless something listens for dead events.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  who reacts to OrderPlaced?
  not visible where it is posted.

  1000 uncancelled subscribers:
  1002 held.
  cancelled: 0 held.

  a slow subscriber holds up the
  poster.""",
        narration=(
            'Finally, the costs. [[slnc 400]] First: who reacts to an '
            'order placed event? [[slnc 300]] Nothing in the code that '
            'posts it says. [[slnc 300]] You can ask the bus, but only if '
            'you know to ask. [[slnc 500]] Second: a thousand short-lived '
            'parts subscribe, and are thrown away without unsubscribing. '
            '[[slnc 300]] The bus still holds all of them. [[slnc 300]] '
            'That is a memory leak. [[slnc 300]] Unsubscribing each one '
            'leaves none. [[slnc 500]] Third: delivery is just a method '
            'call, inside one program. [[slnc 300]] So a slow subscriber '
            'holds up the part that posted.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['eventBus.post(...) and @Subscribe', 'in Guava.', '', "Spring's ApplicationEventPublisher", 'and @EventListener.', '', "Android's LocalBroadcastManager,", "and Vert.x's EventBus."],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for event bus post, and the at Subscribe '
            "annotation, in Google's Guava library. [[slnc 300]] Look for "
            "Spring's application event publisher, and at Event Listener. "
            '[[slnc 300]] Look for the event bus in Vert x. [[slnc 300]] '
            'And look for classes named listener or subscriber, that '
            'nobody seems to call.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use an event bus inside a program', 'to decouple components that react', 'to what happened. Type the events,', 'subscribe by type, always cancel a', 'subscription when the subscriber', 'goes away, listen for dead events,', 'and keep a list of who reacts to', 'what somewhere a person can find.', 'Do not use one across processes,'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use an event bus '
            'inside one program, to separate parts that react to what '
            'happened. [[slnc 500]] Give events clear types, and '
            'subscribe by type. [[slnc 300]] Always unsubscribe when a '
            'subscriber goes away. [[slnc 300]] Listen for dead events. '
            '[[slnc 300]] And keep a list of who reacts to what, '
            'somewhere a person can find it. [[slnc 500]] Do not use one '
            'between separate programs, where you need a real message '
            'broker. [[slnc 300]] Or where the poster needs an answer.'
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
        body=['For two components that always', 'talk, a direct call is clearer. A', 'bus is for many-to-many, and its', 'cost is a flow you cannot see by', 'reading one class.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For two parts that '
            'always talk to each other, a direct call is clearer. [[slnc '
            '400]] A bus is for many parts talking to many parts. [[slnc '
            '300]] And its cost is a flow you cannot see by reading one '
            'class.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Event Bus pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] An event bus '
            'removes the references between parts of a program, and the '
            'price is a flow you cannot see, and subscriptions you must '
            'clean up. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add a subscriber that unsubscribes itself, after its '
            'first event. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
