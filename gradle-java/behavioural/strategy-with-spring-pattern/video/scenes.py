"""Scene definitions for the Strategy with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Strategy with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Strategy pattern, in Java, using Spring Boot. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] The Strategy '
            'pattern puts each option of a decision in its own class, '
            'behind one shared interface. [[slnc 500]] In Spring, the '
            'strategies are beans of one interface. [[slnc 300]] And the '
            'container collects them into a map for you, keyed by name. '
            "[[slnc 600]] Think of a phone's contact list. [[slnc 300]] "
            'You pick a name, and the phone knows the number. [[slnc '
            '700]] This is the framework version of the Strategy video, '
            'with the same delivery pricing. [[slnc 400]] We will let '
            'Spring find the four pricing rules, choose one by '
            'configuration, and add a fifth. [[slnc 300]] Then we will '
            'see the failures that come with it: an ambiguous injection, '
            'and a wrong name.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Strategy, the hand-built video,', 'prices delivery under four rules,', 'and chooses one by name.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Strategy video. [[slnc 400]] That '
            'one prices delivery under four interchangeable rules. [[slnc '
            '300]] It chooses one by a configured name, and refuses an '
            'unknown name. [[slnc 500]] If you are new to the pattern, '
            'watch that one first. [[slnc 400]] Here, we keep the same '
            'example, and ask what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'It gathers every bean of one', 'interface into a map.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            'At its heart, Spring is a container that creates your '
            'objects. [[slnc 300]] It can gather every bean of one '
            "interface into a map, keyed by each bean's name. [[slnc "
            '500]] And one promise. [[slnc 300]] If you skip this video, '
            'you lose none of the pattern. [[slnc 300]] This one is about '
            'the tool.'
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
            'First demo: Spring finds the strategies. [[slnc 400]] The '
            'checkout asks for a map of shipping rules. [[slnc 300]] It '
            'receives four: distance, flat, free over threshold, and '
            'weight banded. [[slnc 500]] The keys are the bean names. '
            '[[slnc 300]] And we chose those names ourselves, in each '
            "class's component annotation."
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
            'Second demo: three shipments, priced under every rule. '
            '[[slnc 400]] The flat rule charges four pounds ninety-nine '
            'for all of them. [[slnc 300]] Weight banded ranges from two '
            'ninety-nine to eight ninety-nine. [[slnc 300]] Free over '
            'threshold makes the heavy, expensive one free. [[slnc 500]] '
            'And an unknown rule name, like teleport, is refused. [[slnc '
            '300]] The error message lists the names that do exist.'
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
            'Third demo: configuration chooses the rule. [[slnc 400]] Set '
            'the shipping rule setting to distance, and the heavy '
            'shipment costs four ninety-nine. [[slnc 400]] Set it to '
            'teleport, and the application refuses to start. [[slnc 500]] '
            'That is the right moment to find a typo. [[slnc 300]] At '
            "startup, not at a customer's checkout."
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
            'Fourth demo: a failure. [[slnc 400]] One class asks for a '
            'single shipping rule, instead of the map. [[slnc 300]] '
            'Spring finds four candidates, and refuses to guess. [[slnc '
            '300]] The application does not start. [[slnc 300]] The '
            'message says it expected a single bean, but found four. '
            '[[slnc 500]] The message is clear. [[slnc 300]] But notice '
            'the risk. [[slnc 300]] Adding a second bean of an interface '
            'can break a class that worked perfectly yesterday.'
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
            'Fifth demo: adding a fifth rule, called express. [[slnc '
            '400]] It joins the map, and costs nine pounds ninety-nine. '
            '[[slnc 300]] The checkout class was not touched at all. '
            '[[slnc 500]] In this demo, it is registered by hand, so the '
            'default stays at four. [[slnc 300]] A normal scanned class '
            'would be found in exactly the same way.'
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
            'Last demo: a default, for when nobody chooses. [[slnc 400]] '
            'Mark the flat rule as primary. [[slnc 300]] Now the class '
            'that asked for a single rule starts up, and receives the '
            'flat rule. [[slnc 300]] And the map still holds all four. '
            '[[slnc 500]] Primary answers the question: which one, when '
            'nobody says? [[slnc 300]] The map answers: which ones exist?'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Inject the map.', '', 'Name the beans explicitly.', '', 'Check the configured name at', 'startup.', '', 'Use primary for one default.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Inject the map of '
            'strategies. [[slnc 300]] Name each bean explicitly. [[slnc '
            '300]] Check the configured name when the application starts. '
            '[[slnc 300]] And mark one bean as primary, where a single '
            'default is needed.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A Map of String to an interface', 'in a constructor.', '', '@Primary or @Qualifier next to', 'an interface.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a constructor that receives a map, from names '
            'to an interface. [[slnc 300]] Or the at Primary, or at '
            'Qualifier annotations, next to an interface.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Payment providers, message handlers', 'and export formats chosen by name.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In payment '
            'providers, message handlers, and export formats, chosen by '
            'name.'
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
        body=["Everything is real: Spring's", 'container and its injection.', '', 'Nothing depends on timing.'],
        narration=(
            "A quick, honest note about this demo. [[slnc 300]] Spring's "
            'container and its injection are real. [[slnc 300]] And '
            'nothing depends on timing.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['Two rules that never change need', 'no container.', '', 'A plain conditional is easier', 'to read.'],
        narration=(
            'So, when is this too much? [[slnc 400]] Two rules that never '
            'change do not need a container. [[slnc 300]] A plain if '
            'statement is easier to read.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Rename a bean and see which', 'configuration breaks.'],
        narration=(
            "That's Strategy with Spring. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Spring keeps '
            'the table of strategies for you, and the names in it are '
            'yours to choose, and to check. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Rename one of the beans. [[slnc 300]] '
            'Then find out which configuration breaks. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
