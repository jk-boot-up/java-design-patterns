"""Scene definitions for the Onion Architecture teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Onion Architecture',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Onion '
            'Architecture pattern in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] The plain '
            'definition: onion architecture arranges code in rings, with '
            'the business rules at the centre. Every ring may depend only '
            'on rings further in, never outward. [[slnc 350]] This is '
            'another project in the architecture category, whose subject '
            'is how a whole application is arranged, and who may depend '
            'on whom. In our online store, the order class saves itself '
            'with a database statement, and so it cannot change without '
            'touching the database. [[slnc 300]] By the end you will see '
            'an order that reaches out to a database, see the rings and '
            'the one rule, see a checker catch a class that breaks the '
            'rule, see the storage swapped without touching the inside, '
            'see the rules checked with no storage at all, and see the '
            'bill, which is conversions and ceremony.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order is placed,', 'priced and saved.', '', 'Ten percent off orders of', '100 pounds or more.', '', 'Storage may change:', 'memory, a file, a database.', '', 'What sits at the centre?'],
        narration=(
            'Here is the scenario. An order is placed, priced and saved. '
            'The pricing rule gives ten percent off orders of one hundred '
            'pounds or more. Storage may change, from memory, to a file, '
            'to a database. [[slnc 300]] The question: what sits at the '
            'centre?'
        ),
    ),
    dict(
        key='03-core', kind='console', title='The Core Reaches Outward',
        body="""ONE. The core reaches out.
  the order saved itself with a
  SQL statement.

  to change the storage, the
  order class, at the centre,
  must be edited.""",
        narration=(
            'First, the core reaches outward. The order saved itself with '
            'a SQL statement. To change the storage, the order class, at '
            'the centre, must be edited.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Rings, with the rules at the', 'centre.', '', 'Storage and screens outside.', '', 'One rule: a class may refer to', 'its own ring, or a ring further', 'in. Never outward.'],
        narration=(
            'The pattern. Rings, with the business rules at the centre. '
            'Storage and screens outside. One rule: a class may refer to '
            'its own ring, or to a ring further in. Never outward.'
        ),
    ),
    dict(
        key='05-rings', kind='console', title='Rings, And One Rule',
        body="""TWO. Rings, and one rule.
  ring 0: order, repository idea.
  ring 1: pricing rules.
  ring 2: use cases.
  ring 3: storage and screens.

  never refer outward.
  violations among 8 classes: 0.""",
        narration=(
            'Second, rings, and one rule. Ring zero is the order, the '
            'order line, and the idea of a repository. Ring one is the '
            'pricing rules. Ring two is the use cases. Ring three is '
            'storage and screens. The rule: a class may refer to its own '
            'ring, or to a ring further in, never outward. Among the '
            'eight classes of the onion, violations: none.'
        ),
    ),
    dict(
        key='06-check', kind='console', title='Checking The Rule',
        body="""THREE. Checking the rule.
  the naive order, ring 0,
  refers to the database, ring 3.

  the checker reads fields,
  constructors and methods.
  the rule is tested, not hoped.""",
        narration=(
            'Third, checking the rule. The checker is pointed at the '
            'naive order. It reports: the naive order, in ring zero, '
            'refers to the SQL database, in ring three. The checker reads '
            'the fields, constructors and methods of each class, so the '
            'rule is tested, not just hoped for.'
        ),
    ),
    dict(
        key='07-swap', kind='console', title='Swap The Outside',
        body="""FOUR. Swap the outside.
  in memory: 10800.
  as a text record: 10800.
  the record: ORD-1|MUG:2:6000|
  discount:1200.

  the inside was not touched.""",
        narration=(
            'Fourth, swap the outside. Stored in memory, the total is ten '
            'thousand eight hundred. Stored as a text record, the same. '
            'The record is the order id, the mug, two at sixty pounds, '
            'and a discount of twelve hundred. The use case, the rules '
            'and the order were not touched.'
        ),
    ),
    dict(
        key='08-inside', kind='console', title='The Inside, On Its Own',
        body="""FIVE. The inside, alone.
  small order: 950.
  big order: 10800,
  10% off 12000.

  no storage, no screen, no
  framework was used.""",
        narration=(
            'Fifth, the inside, on its own. A small order is nine fifty. '
            'A big order is ten thousand eight hundred, ten percent off '
            'twelve thousand. No storage, no screen, and no framework was '
            'used to check the rules. Through the outside, the same order '
            'gives the same total.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  saved and read back:
  conversions 2.

  4 classes in 3 rings to place
  one order: a lot of ceremony
  for a small program.

  the centre knows storage
  exists, though not how.""",
        narration=(
            'Last, the bill. One order saved and read back through the '
            'outer ring costs two conversions. Every trip across a ring '
            'may copy the order into another shape. To place one order '
            'there are four classes in three rings, plus the repository '
            'idea. For a small program, that is a lot of ceremony. And '
            'the repository idea lives in the centre, so the centre knows '
            'that storage exists, though not how.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Packages named domain, application', 'and infrastructure.', '', 'An interface in the domain', 'package, implemented in the', '', 'Entities with no framework', 'annotations, and a use-case class'],
        narration=(
            'How do you recognise this in code you did not write? '
            'Packages named domain, application and infrastructure. An '
            'interface in the domain package, implemented in the '
            'infrastructure package. Entities with no framework '
            'annotations, and a use-case class that receives its '
            'repository. An ArchUnit test that fails when domain code '
            'imports infrastructure.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Put the business rules at the', 'centre, and let everything else', 'depend on them. Let the centre own', 'the ideas it needs, such as a', 'repository, and let the outside', 'supply them. Check the rule with a', 'test, not a diagram. Do not use it', 'for a program too small to have an', 'outside worth swapping.'],
        narration=(
            'Here is my verdict, plainly. Put the business rules at the '
            'centre, and let everything else depend on them. Let the '
            'centre own the ideas it needs, such as a repository, and let '
            'the outside supply them. Check the rule with a test, not a '
            'diagram. Do not use it for a program too small to have an '
            'outside worth swapping.'
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
        body=['For a small tool with one fixed', 'storage and few rules, rings are', 'heavier than the problem. They pay', 'off when rules are rich and the', 'outside changes.'],
        narration=(
            'So when is it too much? For a small tool with one fixed '
            'storage and few rules, rings are heavier than the problem. '
            'They pay off when rules are rich and the outside changes.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Onion Architecture. [[slnc 250]] If you take one "
            'sentence away, take this one: onion architecture puts the '
            'rules at the centre and points every dependency inward, and '
            'the price is the copying and the classes that the rings '
            'need. [[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add a third storage that keeps orders in a sorted list, and '
            'confirm the checker still finds no violations. [[slnc 300]] '
            'If this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
