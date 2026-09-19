"""Scene definitions for the Hexagonal Architecture with Spring Boot teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Hexagonal Architecture with Spring Boot',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Hexagonal '
            'Architecture pattern with Spring Boot, in Java, and it is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] It '
            'is the framework version of the Hexagonal Architecture '
            'video. That one put the order use case in a core that knows '
            'only ports, with adapters outside it, so storage and '
            'notification could change without the core changing. This '
            'one shows the same idea inside Spring Boot. [[slnc 350]] The '
            'plain definition, in short: in Spring Boot, the adapters are '
            'beans chosen by configuration, and the core stays a plain '
            'class that the container is handed. [[slnc 300]] By the end '
            'you will see the same core run on two storage adapters '
            'chosen by a property, through two driving adapters, and with '
            'no container at all, then see what happens when the core '
            'reaches for Spring.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Hexagonal Architecture, the', 'hand-built video, puts the order', 'use case in a core that knows only', 'ports.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Hexagonal Architecture video. If you '
            'have not seen it, start there. It puts the order use case in '
            'a core that knows only ports, with adapters outside it, so '
            'storage and notification can change without the core '
            'changing. [[slnc 300]] This one uses the same example. It '
            'does not teach the pattern again. It shows what Spring Boot '
            'does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new: Spring Boot,', 'an in-memory database, and ArchUnit,', 'which checks the inside rule.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'Boot picks and wires the adapters from configuration. '
            'ArchUnit is a library that checks, in a test, that the core '
            'does not depend on the framework. [[slnc 300]] And a '
            'promise: skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-plain', kind='console', title='The Core Is Plain Java',
        body="""ONE. A plain core.
  the use case: a plain class,
  not a proxy.

  core classes that mention
  Spring: 0.""",
        narration=(
            'First, the core is plain Java. The container hands out the '
            'use case as an ordinary class from the core package. It is '
            'not a proxy. And no class in the core mentions Spring, or '
            'any adapter.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='Two Storage Adapters',
        body="""TWO. Two storages.
  memory: ORD-000001, 30000.
  jdbc: ORD-000001, 30000.

  the core did not change.""",
        narration=(
            'Second, one property chooses the storage. With memory, the '
            'order is kept in a list. With jdbc, it goes to a database. '
            'The receipt is the same, and the stock falls to four in '
            'both. The core did not change.'
        ),
    ),
    dict(
        key='06-doors', kind='console', title='Two Doors Into One Room',
        body="""THREE. Two doors.
  console: ORD-000001.
  console: refused.
  batch: ORD-000002,
  refused, ORD-000003.""",
        narration=(
            'Third, two doors into the same room. A console adapter '
            'places an order for a machine, and is refused for ten. A '
            'batch adapter places three lines, and one is refused. '
            'Neither knows how the other works. Both call the same port.'
        ),
    ),
    dict(
        key='07-nocontainer', kind='console', title='The Core Without A Container',
        body="""FOUR. No container.
  10000 orders through the real
  use case.

  no Spring context.
  payments: a one-line lambda.""",
        narration=(
            'Fourth, the core without a container. Ten thousand orders go '
            'through the real use case, with adapters made by hand. No '
            'Spring at all. The payment port is a one line lambda. That '
            'is what a port is for.'
        ),
    ),
    dict(
        key='08-leak', kind='console', title='A Use Case That Reaches For Spring',
        body="""FIVE. Reaching out.
  the inside rule: 10
  violations.

  all in SpringyPlaceOrder.
  the real core: none.""",
        narration=(
            'Fifth, the shortcut. A use case with a transaction '
            'annotation and a database client breaks the inside rule ten '
            'times. All ten are in that class. The real core breaks it '
            'never. [[slnc 300]] Spring will not stop you writing the '
            'shortcut. A rule will.'
        ),
    ),
    dict(
        key='09-missing', kind='console', title='A Port With No Adapter',
        body="""SIX. A missing adapter.
  orders.store=nothing:
  the application does not
  start.
  no bean of type OrderStore.""",
        narration=(
            'Last, a port with no adapter. Set the property to a value '
            'nobody handles, and the application does not start. It names '
            'the missing port. Hand wiring would have failed at compile '
            'time. The container finds out at startup, which is later, '
            'but still before any customer.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['A core with no annotations.', '', 'One config class wires it.', '', 'Adapters chosen by property.', '', 'A rule guards the inside.'],
        narration=(
            'My verdict, plainly. Keep the core free of annotations. Wire '
            'it in one configuration class. Choose adapters by '
            'configuration. And keep a rule that guards the inside.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A Configuration class calling new on', 'a use case.', '', 'ConditionalOnProperty on adapters.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'configuration class that calls new on a use case. And '
            'conditional on property annotations on adapters.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Spring applications whose business', 'code has no annotations.'],
        narration=(
            'You have met this in Spring applications whose business code '
            'has no annotations.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1, H2 and', 'ArchUnit 1.5.0.', '', 'No web server.'],
        narration=(
            'For the record. Spring Boot four point one point one, H2, '
            'and ArchUnit one point five. No web server.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the real container,', 'a real database and a real rule.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: the real container, a real database and '
            'a real rule.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a small service with one storage,', 'a port with one adapter is ceremony.'],
        narration=(
            'So when is it too much? For a small service with one '
            'storage, a port with one adapter is ceremony.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add an annotation to the core', 'and run the rule.'],
        narration=(
            "That's Hexagonal Architecture with Spring Boot. [[slnc 250]] "
            'If you take one sentence away, take this one: Spring wires '
            'the hexagon, and only a rule keeps the core free of Spring. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, add an '
            'annotation to the core, and run the rule. [[slnc 300]] If '
            'this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
