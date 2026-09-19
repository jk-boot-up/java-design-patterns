"""Scene definitions for the Event Bus teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Event Bus',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Event Bus '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: an '
            'event bus is a single place where components post events and '
            'subscribe to the kinds they care about, so that none of them '
            'holds a reference to any other. [[slnc 350]] This is the '
            'fifth project in the messaging and integration category, '
            'whose subject is how separate systems exchange messages '
            'safely. In our online store, five parts of the same program '
            'all want to know when an order is placed or cancelled. '
            '[[slnc 300]] By the end you will see five components that '
            'all know each other, see each know only the bus, see '
            'subscribers pick events by type, see one failing subscriber '
            'leave the others alone, see an event nobody hears, and see '
            'the bill, which is that the flow becomes hard to see.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=["Inside the shop's program, five", 'components react to orders:', '', 'inventory, email, analytics,', 'loyalty, and the audit log.', '', 'Who talks to whom?'],
        narration=(
            "Here is the scenario. Inside the online store's program, "
            'five components react when an order is placed or cancelled: '
            'inventory, email, analytics, loyalty points and the audit '
            'log. [[slnc 300]] The question: who talks to whom?'
        ),
    ),
    dict(
        key='03-web', kind='console', title='Everyone Knows Everyone',
        body="""ONE. A web.
  5 components tell each other:
  20 references.

  a sixth needs 10 more.""",
        narration=(
            'First, everyone knows everyone. Five components that each '
            'tell each other about orders need twenty references between '
            'them. Add a sixth, and it needs ten more. The web grows '
            'faster than the components.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One bus, inside the program.', '', 'Components post events to it.', '', 'Components subscribe to the kinds', 'of event they care about.', '', 'Nobody holds a reference to', 'anybody else.'],
        narration=(
            'The pattern. One bus, inside the program. Components post '
            'events to it. Components subscribe to the kinds of event '
            'they care about. And nobody holds a reference to anybody '
            'else.'
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
            'Second, everyone knows the bus. One post reaches inventory, '
            'email and analytics. Five components each hold one '
            'reference, to the bus: five references, not twenty. And the '
            'poster holds no reference to any subscriber.'
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
            'Third, by type. A subscriber for order placed hears only '
            'that. A subscriber for every order event, the parent type, '
            'hears both the placed and the cancelled. Each subscriber '
            'asks for the kind of thing it cares about.'
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
            'Fourth, one failing subscriber. Email fails, on a timeout. '
            'Analytics still hears the event. The failure is recorded. '
            'The poster does not see it. It posted, and carried on.'
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
            'Fifth, an event nobody hears. With no subscriber, the bus '
            'counts it as a dead event, and nothing complains. With a '
            'subscriber for dead events, the unheard event arrives there. '
            'A typo in an event type, or a forgotten subscription, is a '
            'silent loss, unless something listens for dead events.'
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
            'Last, the bill. Who reacts to an order placed event? Nothing '
            'in the code that posts it says. The bus can be asked, but '
            'you have to know to ask. A thousand short lived components '
            'that subscribe and are thrown away without cancelling are '
            'all still held: a memory leak. Cancelling each leaves none. '
            'And delivery is a method call in one process, so a slow '
            'subscriber holds up the poster.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['eventBus.post(...) and @Subscribe', 'in Guava.', '', "Spring's ApplicationEventPublisher", 'and @EventListener.', '', "Android's LocalBroadcastManager,", "and Vert.x's EventBus."],
        narration=(
            'How do you recognise this in code you did not write? '
            "eventBus.post(...) and @Subscribe in Guava. Spring's "
            "ApplicationEventPublisher and @EventListener. Android's "
            "LocalBroadcastManager, and Vert.x's EventBus. Classes with "
            'names ending in Listener or Subscriber and no visible '
            'caller.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use an event bus inside a program', 'to decouple components that react', 'to what happened. Type the events,', 'subscribe by type, always cancel a', 'subscription when the subscriber', 'goes away, listen for dead events,', 'and keep a list of who reacts to', 'what somewhere a person can find.', 'Do not use one across processes,'],
        narration=(
            'Here is my verdict, plainly. Use an event bus inside a '
            'program to decouple components that react to what happened. '
            'Type the events, subscribe by type, always cancel a '
            'subscription when the subscriber goes away, listen for dead '
            'events, and keep a list of who reacts to what somewhere a '
            'person can find. Do not use one across processes, where you '
            'need a real broker, or where the poster needs an answer.'
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
        body=['For two components that always', 'talk, a direct call is clearer. A', 'bus is for many-to-many, and its', 'cost is a flow you cannot see by', 'reading one class.'],
        narration=(
            'So when is it too much? For two components that always talk, '
            'a direct call is clearer. A bus is for many-to-many, and its '
            'cost is a flow you cannot see by reading one class.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Event Bus. [[slnc 250]] If you take one sentence "
            'away, take this one: an event bus removes the references '
            'between components, and the price is a flow you cannot see, '
            'and subscriptions you must clean up. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, add a subscriber that unsubscribes '
            'itself after its first event. [[slnc 300]] If this helped, a '
            'like genuinely does help other people find it, and subscribe '
            'if you would like the rest of the series. [[slnc 250]] '
            'Thanks for watching.'
        ),
    ),
]
