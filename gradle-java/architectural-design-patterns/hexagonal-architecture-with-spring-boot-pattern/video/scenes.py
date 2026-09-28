"""Scene definitions for the Hexagonal Architecture with Spring Boot teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Hexagonal Architecture with Spring Boot',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Hexagonal Architecture pattern, in Java, using Spring Boot. '
            '[[slnc 300]] This video is presented by Jayasekhar Konduru. '
            '[[slnc 600]] First, a simple definition. [[slnc 300]] In '
            'Hexagonal Architecture, the core of the program declares '
            'what it needs as interfaces, called ports. [[slnc 300]] '
            'Adapters outside the core plug into those ports. [[slnc '
            '500]] With Spring Boot, the adapters become beans, chosen by '
            'configuration. [[slnc 300]] And the core stays a plain Java '
            'class, which the framework simply hands out. [[slnc 600]] '
            'Think of a games console. [[slnc 300]] The console stays the '
            'same, and you choose which controller to plug in. [[slnc '
            '700]] This is the framework version of the Hexagonal '
            'Architecture video, with the same online store. [[slnc 400]] '
            'We will run the same core on two storage options, through '
            'two different entry points, and with no framework at all. '
            '[[slnc 300]] Then we will see what happens when the core '
            'reaches for Spring.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Hexagonal Architecture, the', 'hand-built video, puts the order', 'use case in a core that knows only', 'ports.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Hexagonal Architecture video. [[slnc '
            '400]] That one puts the order logic in a core that knows '
            'only ports. [[slnc 300]] So storage and notification can '
            'change, without the core changing. [[slnc 500]] If you are '
            'new to the pattern, watch that one first. [[slnc 400]] Here, '
            'we keep the same example, and ask what Spring Boot does with '
            'it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new: Spring Boot,', 'an in-memory database, and ArchUnit,', 'which checks the inside rule.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Three things are new in this project. [[slnc 400]] One. '
            '[[slnc 200]] Spring Boot, which picks the adapters and wires '
            'them together, from configuration. [[slnc 300]] Two. [[slnc '
            '200]] An in-memory database, called H2. [[slnc 300]] Three. '
            '[[slnc 200]] ArchUnit, a library that checks, in a test, '
            'that the core does not depend on the framework. [[slnc 500]] '
            'And one promise. [[slnc 300]] If you skip this video, you '
            'lose none of the pattern. [[slnc 300]] This one is about the '
            'tool.'
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
            'First demo: the core is plain Java. [[slnc 400]] We ask '
            'Spring for the use case. [[slnc 300]] It hands back an '
            'ordinary class from the core package. [[slnc 300]] Not a '
            'special wrapped object, called a proxy. [[slnc 400]] And how '
            'many core classes mention Spring, or any adapter? [[slnc '
            '300]] Zero.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='Two Storage Adapters',
        body="""TWO. Two storages.
  memory: ORD-000001, 30000.
  jdbc: ORD-000001, 30000.

  the core did not change.""",
        narration=(
            'Second demo: two ways to store orders. [[slnc 400]] One '
            'setting in the configuration chooses the storage. [[slnc '
            '400]] Set it to memory, and orders are kept in a list. '
            '[[slnc 300]] Set it to J D B C, and orders go into a '
            'database. [[slnc 500]] Either way, the receipt is the same. '
            '[[slnc 300]] The first order is number one, for three '
            'hundred pounds, and the stock falls to four. [[slnc 400]] '
            'And the core did not change at all.'
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
            'Third demo: two doors into the same room. [[slnc 400]] Door '
            'one is a console adapter. [[slnc 300]] It orders one coffee '
            'machine, which works. [[slnc 300]] Then it asks for ten, and '
            'is refused, because there is not enough stock. [[slnc 500]] '
            'Door two is a batch adapter. [[slnc 300]] It sends three '
            'order lines at once. [[slnc 300]] Two are accepted, and one '
            'is refused. [[slnc 500]] Neither door knows how the other '
            'works. [[slnc 300]] Both call the same port.'
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
            'Fourth demo: the core with no framework at all. [[slnc 400]] '
            'Ten thousand orders go through the real use case. [[slnc '
            '300]] The adapters are created by hand. [[slnc 300]] There '
            'is no Spring anywhere in this test. [[slnc 500]] The payment '
            'port is filled with a tiny one-line function. [[slnc 300]] '
            'That is exactly what a port is for.'
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
            'Fifth demo: the shortcut. [[slnc 400]] Someone writes a use '
            'case that uses Spring directly. [[slnc 300]] It has a '
            'transaction annotation, and a database client. [[slnc 500]] '
            'The architecture rule reports ten violations. [[slnc 300]] '
            'All ten are in that one shortcut class. [[slnc 300]] The '
            'real core has none. [[slnc 500]] Spring will not stop you '
            'writing the shortcut. [[slnc 300]] A rule will.'
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
            'Last demo: a port with no adapter. [[slnc 400]] We set the '
            'storage setting to a value that no adapter handles. [[slnc '
            '400]] The application refuses to start. [[slnc 300]] It says '
            'there is no bean of type Order Store, naming the missing '
            'port. [[slnc 500]] Wiring by hand would have caught this '
            'when the code compiled. [[slnc 300]] The container only '
            'finds out at startup. [[slnc 300]] That is later, but still '
            'before any customer is affected.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['A core with no annotations.', '', 'One config class wires it.', '', 'Adapters chosen by property.', '', 'A rule guards the inside.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Keep the core free of '
            'framework annotations. [[slnc 300]] Wire it together in one '
            'configuration class. [[slnc 300]] Choose the adapters with '
            'configuration settings. [[slnc 300]] And keep a test rule '
            'that guards the core.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A Configuration class calling new on', 'a use case.', '', 'ConditionalOnProperty on adapters.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a configuration class that creates the use '
            'case with the new keyword. [[slnc 300]] And look for '
            'adapters marked with the at Conditional On Property '
            'annotation, so a setting decides which one is used.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Spring applications whose business', 'code has no annotations.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In Spring '
            'applications whose business code has no framework '
            'annotations at all.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1, H2 and', 'ArchUnit 1.5.0.', '', 'No web server.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] The H2 database. '
            '[[slnc 300]] And ArchUnit one point five. [[slnc 300]] There '
            'is no web server.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the real container,', 'a real database and a real rule.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything in it is real. [[slnc 300]] The real Spring '
            'container, a real database, and a real architecture rule.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a small service with one storage,', 'a port with one adapter is ceremony.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a small service '
            'with only one kind of storage, a port with a single adapter '
            'is just ceremony.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add an annotation to the core', 'and run the rule.'],
        narration=(
            "That's Hexagonal Architecture with Spring Boot. [[slnc 400]] "
            'If you remember one sentence, make it this one. [[slnc 300]] '
            'Spring wires the hexagon together, but only a rule keeps the '
            'core free of Spring. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Add a Spring annotation to a core class. [[slnc '
            '300]] Then run the rule, and listen to what it reports. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
