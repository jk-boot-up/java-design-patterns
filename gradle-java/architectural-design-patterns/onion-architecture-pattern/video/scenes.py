"""Scene definitions for the Onion Architecture teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Onion Architecture',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Onion Architecture pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Onion Architecture arranges '
            'code in rings, like the layers of an onion. [[slnc 300]] The '
            'business rules sit at the centre. [[slnc 300]] And every '
            'ring may depend only on rings further in, never on rings '
            'further out. [[slnc 600]] Think of a tree. [[slnc 300]] The '
            'trunk does not depend on the leaves. [[slnc 300]] The leaves '
            'depend on the trunk. [[slnc 300]] You can lose every leaf in '
            'autumn, and the tree is still the same tree. [[slnc 700]] In '
            'our online store, the order class saves itself to a '
            'database. [[slnc 300]] So you cannot change the storage '
            'without editing the order. [[slnc 500]] In this video, we '
            'arrange the code in rings, and write the rule as a check. '
            '[[slnc 300]] We will swap the storage without touching the '
            'centre, test the rules with no storage at all, and then look '
            'at the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order is placed,', 'priced and saved.', '', 'Ten percent off orders of', '100 pounds or more.', '', 'Storage may change:', 'memory, a file, a database.', '', 'What sits at the centre?'],
        narration=(
            'Here is the scenario. [[slnc 400]] An order is placed, '
            'priced, and saved. [[slnc 400]] The pricing rule gives ten '
            'percent off any order of one hundred pounds or more. [[slnc '
            '400]] And the storage may change over time. [[slnc 300]] '
            'First memory, then a file, then a database. [[slnc 500]] So '
            'here is the question. [[slnc 300]] What should sit at the '
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
            'First, the old way: the core reaches outward. [[slnc 400]] '
            'The order class saves itself, by writing a database command. '
            '[[slnc 500]] So to change the storage, you must edit the '
            'order class. [[slnc 300]] And the order class sits right at '
            'the centre of the program.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Rings, with the rules at the', 'centre.', '', 'Storage and screens outside.', '', 'One rule: a class may refer to', 'its own ring, or a ring further', 'in. Never outward.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Arrange the code in rings, '
            'with the business rules at the centre. [[slnc 300]] Storage '
            'and screens go on the outside. [[slnc 500]] And one rule. '
            '[[slnc 300]] A class may refer to its own ring, or to a ring '
            'further in. [[slnc 300]] Never to a ring further out.'
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
            'Second demo: the rings, and the one rule. [[slnc 500]] Ring '
            'zero, at the centre, holds the order, its lines, and the '
            'idea of a repository, a place to keep orders. [[slnc 400]] '
            'Ring one holds the pricing rules. [[slnc 300]] Ring two '
            'holds the use cases, like placing an order. [[slnc 300]] '
            'Ring three, on the outside, holds storage and screens. '
            '[[slnc 500]] The onion has eight classes. [[slnc 300]] How '
            'many break the rule? [[slnc 300]] None.'
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
            'Third demo: checking the rule. [[slnc 400]] A checker is '
            'pointed at the old, naive order class. [[slnc 400]] It '
            'reports a problem. [[slnc 300]] The naive order, in ring '
            'zero, refers to the database, in ring three. [[slnc 500]] '
            'The checker reads every field, constructor and method of '
            'each class. [[slnc 300]] So the rule is tested, not just '
            'hoped for.'
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
            'Fourth demo: swap the outside. [[slnc 400]] First, orders '
            'are stored in memory. [[slnc 300]] The total is one hundred '
            'and eight pounds. [[slnc 400]] Then, orders are stored as a '
            'line of text instead. [[slnc 300]] The total is the same, '
            'one hundred and eight pounds. [[slnc 400]] The text line '
            'holds the order I D, two mugs at sixty pounds, and a '
            'discount of twelve pounds. [[slnc 500]] And the use case, '
            'the rules, and the order were not touched at all.'
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
            'Fifth demo: the inside, all on its own. [[slnc 400]] A small '
            'order costs nine pounds fifty, with no discount. [[slnc '
            '300]] A big order of one hundred and twenty pounds gets ten '
            'percent off, and costs one hundred and eight pounds. [[slnc '
            '500]] No storage, no screen, and no framework was needed to '
            'check these rules. [[slnc 400]] And when the same order goes '
            'through the outer rings, it gives exactly the same total.'
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
            'Finally, the cost. [[slnc 400]] Saving one order, and '
            'reading it back, needed two conversions. [[slnc 300]] Each '
            'time data crosses a ring, it may be copied into a different '
            'shape. [[slnc 500]] To place one order, we used four classes '
            'in three rings, plus the repository idea. [[slnc 300]] For a '
            'small program, that is a lot of ceremony. [[slnc 500]] And '
            'one more thing. [[slnc 300]] The repository idea lives at '
            'the centre. [[slnc 300]] So the centre knows that storage '
            'exists, even though it does not know how it works.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Packages named domain, application', 'and infrastructure.', '', 'An interface in the domain', 'package, implemented in the', '', 'Entities with no framework', 'annotations, and a use-case class'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for packages named domain, application, '
            'and infrastructure. [[slnc 300]] Look for an interface in '
            'the domain package, implemented in the infrastructure '
            'package. [[slnc 300]] Look for business classes with no '
            'framework annotations, and a use case that is handed its '
            'repository. [[slnc 300]] And look for an ArchUnit test that '
            'fails when domain code imports infrastructure.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Put the business rules at the', 'centre, and let everything else', 'depend on them. Let the centre own', 'the ideas it needs, such as a', 'repository, and let the outside', 'supply them. Check the rule with a', 'test, not a diagram. Do not use it', 'for a program too small to have an', 'outside worth swapping.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Put the business rules '
            'at the centre, and let everything else depend on them. '
            '[[slnc 400]] Let the centre own the ideas it needs, such as '
            'a repository. [[slnc 300]] And let the outside provide them. '
            '[[slnc 400]] Check the rule with a test, not a diagram. '
            '[[slnc 400]] And do not use it for a program too small to '
            'have an outside worth swapping.'
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
        body=['For a small tool with one fixed', 'storage and few rules, rings are', 'heavier than the problem. They pay', 'off when rules are rich and the', 'outside changes.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a small tool '
            'with one fixed kind of storage, and only a few rules, rings '
            'are heavier than the problem. [[slnc 400]] They pay off when '
            'the rules are rich, and the outside keeps changing.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Onion Architecture. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Onion Architecture '
            'puts the rules at the centre, and points every dependency '
            'inward, and the price is the copying and the extra classes '
            'the rings need. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add a third kind of storage, which keeps orders in a '
            'sorted list. [[slnc 300]] Then check that the checker still '
            'finds no violations. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
