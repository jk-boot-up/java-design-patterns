"""Scene definitions for the Strategy with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Strategy with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Strategy pattern '
            'with Spring Boot, in Java, and it is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] It is the framework '
            'version of the Strategy video. That one priced the same '
            'delivery under four interchangeable rules, chose one by '
            'configuration name, and refused an unknown name. This one '
            'shows the same idea inside Spring Boot. [[slnc 350]] The '
            'plain definition, in short: in Spring, the strategies are '
            'beans of one interface, and the container collects them into '
            'a map for you. [[slnc 300]] By the end you will see the four '
            'rules found by the container, chosen by configuration, and '
            'extended by a fifth, then see the failures that come with '
            'it: an ambiguous injection, and a wrong name.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Strategy, the hand-built video,', 'prices delivery under four rules,', 'and chooses one by name.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Strategy video. If you have not seen '
            'it, start there. It prices delivery under four '
            'interchangeable rules, chooses one by a configured name, and '
            'refuses an unknown name. [[slnc 300]] This one uses the same '
            'example. It does not teach the pattern again. It shows what '
            'Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'It gathers every bean of one', 'interface into a map.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'is a framework whose core is a container that creates your '
            'objects. It can gather every bean of one interface into a '
            'map, keyed by name. [[slnc 300]] And a promise: skipping '
            'this video loses none of the pattern. The hand-built one '
            'teaches all of it.'
        ),
    ),
    dict(
        key='04-find', kind='console', title='Spring Finds The Strategies',
        body="""ONE. Finds them.
  rules found:
  distance, flat,
  freeOverThreshold, weightBanded.

  the keys are bean names.""",
        narration=(
            'First, the container finds the strategies. The checkout asks '
            'for a map of shipping rules, and receives four. The keys are '
            'the bean names, and we chose them, in the component '
            'annotations.'
        ),
    ),
    dict(
        key='05-prices', kind='console', title='The Same Shipments, Every Rule',
        body="""TWO. Every rule.
  flat: 4.99 for all
  weightBanded: 2.99 to 8.99
  freeOverThreshold: heavy 0.00

  teleport: refused.""",
        narration=(
            'Second, the same three shipments under every rule. Flat '
            'charges four ninety nine for all. Weight banded ranges from '
            'two ninety nine to eight ninety nine. Free over threshold '
            'makes the heavy one free. [[slnc 300]] An unknown name at '
            'run time is refused, and the message lists the names that '
            'exist.'
        ),
    ),
    dict(
        key='06-config', kind='console', title='Configuration Chooses',
        body="""THREE. Configuration.
  shipping.rule=distance: works.

  shipping.rule=teleport:
  the application does not
  start.""",
        narration=(
            'Third, configuration chooses. Set the property to distance, '
            'and the heavy shipment costs four ninety nine. Set it to '
            'teleport, and the application does not start. [[slnc 300]] '
            'That is the right place to find a typo: at startup, not at a '
            "customer's checkout."
        ),
    ),
    dict(
        key='07-ambiguous', kind='console', title='Four Beans, One Interface',
        body="""FOUR. Ambiguous.
  a class asks for a single
  ShippingCostRule:
  expected a single bean but
  found 4.""",
        narration=(
            'Fourth, the failure. A class asks for one shipping rule, not '
            'the map. The container finds four, and will not choose. The '
            'application does not start. [[slnc 300]] The message is '
            'clear. But adding a second bean of an interface can break a '
            'class that worked yesterday.'
        ),
    ),
    dict(
        key='08-fifth', kind='console', title='A Fifth Rule',
        body="""FIVE. A fifth rule.
  rules found: 5.
  express: 9.99.

  CheckoutService did not
  change.""",
        narration=(
            'Fifth, adding a rule. A fifth rule joins the map, and the '
            'checkout class is not touched. The demo registers it by '
            'hand, to keep the default at four. A scanned class would be '
            'found the same way.'
        ),
    ),
    dict(
        key='09-primary', kind='console', title='A Default When Nobody Chooses',
        body="""SIX. A default.
  flat marked primary:
  the same class starts, and
  gets the flat rule.

  the map still holds all four.""",
        narration=(
            'Last, a default. Mark the flat rule primary, and the class '
            'that asked for a single rule now starts. It gets the flat '
            'rule. The map still holds all four. [[slnc 300]] Primary '
            'answers, which one when nobody says. The map answers, which '
            'ones exist.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Inject the map.', '', 'Name the beans explicitly.', '', 'Check the configured name at', 'startup.', '', 'Use primary for one default.'],
        narration=(
            'My verdict, plainly. Inject the map. Name the beans '
            'explicitly. Check the configured name at startup. And mark '
            'one primary where a single default is needed.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A Map of String to an interface', 'in a constructor.', '', '@Primary or @Qualifier next to', 'an interface.'],
        narration=(
            'How do you recognise this in code you did not write? A map '
            'of string to an interface, in a constructor. Or a primary or '
            'qualifier annotation next to an interface.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Payment providers, message handlers', 'and export formats chosen by name.'],
        narration=(
            'You have met this in payment providers, message handlers and '
            'export formats, chosen by name.'
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
        body=["Everything is real: Spring's", 'container and its injection.', '', 'Nothing depends on timing.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            "Everything is real: Spring's container and its injection. "
            'Nothing depends on timing.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['Two rules that never change need', 'no container.', '', 'A plain conditional is easier', 'to read.'],
        narration=(
            'So when is it too much? Two rules that never change need no '
            'container. A plain conditional is easier to read.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Rename a bean and see which', 'configuration breaks.'],
        narration=(
            "That's Strategy with Spring. [[slnc 250]] If you take one "
            'sentence away, take this one: Spring keeps the table of '
            'strategies, and the names in it are yours to choose and to '
            'check. [[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, rename a '
            'bean, and see which configuration breaks. [[slnc 300]] If '
            'this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
