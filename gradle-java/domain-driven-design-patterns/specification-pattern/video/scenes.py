"""Scene definitions for the Specification teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Specification',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Specification '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'specification is a business rule written as an object. It '
            'can say whether something satisfies it, it can explain '
            'itself, and it combines with other rules into new ones. '
            '[[slnc 350]] This is the fourth project in the domain-driven '
            'design category, whose subject is writing code that says '
            'what the business says. In our online store, the rule is '
            'what counts as a cheap product that is available. [[slnc '
            '300]] By the end you will see one rule copied into three '
            'places and drift, see it named once and combined, see it '
            'explain why a product fails, and see the bill, which is that '
            'it looks at everything.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Three features need the same idea:', 'cheap and available.', '', 'The search page shows such products.', 'A promotion is offered on them.', 'They ship free.', '', 'Where does the rule live?'],
        narration=(
            'Here is the scenario. In the online store, three features '
            'need the same idea: cheap and available. The search page '
            'shows such products. A promotion is offered on them. And '
            'they ship free. [[slnc 300]] The question: where does the '
            'rule live?'
        ),
    ),
    dict(
        key='03-three', kind='console', title='The Same Rule, Written Three Times',
        body="""ONE. Three copies.
  search:    MUG-BLUE, TEA-050.
  promotion: MUG-BLUE,
  MUG-RED, MUG-OLD, TEA-050.
  shipping:  MUG-BLUE, TEA-050.

  the promotion drifted.""",
        narration=(
            'First, the same rule written three times. The search page '
            'and the shipping offer agree: the blue mug and the tea. The '
            'promotion, written later, offers four. It includes a mug at '
            'exactly ten pounds, because its copy says ten pounds or '
            'less. And it includes a discontinued mug, because it forgot '
            'to check. [[slnc 300]] Nobody meant that. Three copies '
            'drift.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A rule is an object.', '', 'It says whether a candidate', 'satisfies it.', '', 'It says what it means, in words.', '', 'It combines with others:', 'and, or, not.'],
        narration=(
            'The pattern. A rule is an object. It says whether a '
            'candidate satisfies it. It can say what it means, in words. '
            'And it combines with other rules, using and, or, and not, to '
            'make new ones. Written once, and used everywhere.'
        ),
    ),
    dict(
        key='05-named', kind='console', title='The Rule, Named Once',
        body="""TWO. Named once.
  in stock and under £10 and
  not discontinued.

  search, promotion, shipping:
  MUG-BLUE, TEA-050.

  change it once.""",
        narration=(
            'Second, the rule, named once. It reads: in stock, and under '
            'ten pounds, and not discontinued. The search page, the '
            'promotion and shipping all use it, and they all agree: the '
            'blue mug and the tea. Change the rule in one place, and all '
            'three change.'
        ),
    ),
    dict(
        key='06-combine', kind='console', title='Rules Combine',
        body="""THREE. Combine.
  a mug under £10, or a tea
  on sale.

  MUG-BLUE, MUG-OLD, TEA-050
  in stock.

  no new class.""",
        narration=(
            'Third, rules combine. A gift idea: a mug under ten pounds, '
            'or a tea that is on sale. Built from small rules with and, '
            'and or. It describes itself, and it picks out three products '
            'that are in stock. No new class was written.'
        ),
    ),
    dict(
        key='07-why', kind='console', title='A Rule Can Say Why Not',
        body="""FOUR. Why not.
  MUG-RED: under £10.
  MUG-OLD: not discontinued.
  MUG-GREEN: in stock.
  MUG-BLUE: qualifies.

  the rule explains itself.""",
        narration=(
            'Fourth, a rule can say why not. The red mug fails on price. '
            'The old mug fails on being discontinued. The green mug fails '
            'on stock. Each explanation comes from the rule itself. '
            'Nobody wrote an error message by hand, so it cannot drift '
            'from the rule.'
        ),
    ),
    dict(
        key='08-jobs', kind='console', title='The Same Rule, Two Jobs',
        body="""FIVE. Two jobs.
  select from a list: 2.
  check one choice, MUG-OLD:
  refused, not discontinued.

  one definition.""",
        narration=(
            'Fifth, the same rule does two jobs. It selects from a list. '
            'And it checks a single product that a customer picked, and '
            'if it fails, says why. One definition of cheap and '
            'available, used to filter, and to validate.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  10000 products.
  66 matches.
  10000 looked at.

  a rule used once needs no
  specification.""",
        narration=(
            'Last, the bill. Ten thousand products, and sixty six '
            'matches. To find them, every one of the ten thousand was '
            'looked at. A specification runs in memory. To let a database '
            'do the work, the rule has to be turned into a query. [[slnc '
            '300]] And one more thing. For a rule used in a single place, '
            'a plain lambda is simpler than a specification.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['isSatisfiedBy, with and, or, not.', '', 'Classes named for a business', 'condition, like InStock.', '', 'Predicate.and and Predicate.or.', '', "Spring Data's Specification."],
        narration=(
            'How do you recognise this in code you did not write? An '
            'interface with a method like is satisfied by, and with and, '
            'or, and not. Classes named for a business condition, like in '
            'stock. The predicate class in the JDK, with its and, and or. '
            "And Spring Data's Specification."
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['When a rule is shared, combined,', 'or must explain itself.', '', "Small leaves, in the business's", 'words.', '', 'Turn it into a query for large', 'data.', '', 'A rule used once: a lambda.'],
        narration=(
            'Here is my verdict, plainly. Use a specification when a rule '
            'is needed in several places, when rules must be combined or '
            'explained, or when a rule is chosen at run time. Keep the '
            "small rules small, and name them in the business's words. "
            'Turn it into a query when the data is large. And for a rule '
            'used once, a lambda is enough.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'The drift between the three copies', 'is real output.', '', 'The catalogue of ten thousand', 'products is built in memory, and', 'the count of products looked at', 'is exact.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. The drift between the three copies '
            'is real output. The catalogue of ten thousand products is '
            'built in memory, and the count of products looked at is '
            'exact.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a condition used once, a', 'lambda is clearer.', '', 'It earns its place when a rule is', 'shared, combined or must explain', 'itself.'],
        narration=(
            'So when is it too much? For a condition used once, a lambda '
            'is clearer. A specification earns its place when a rule is '
            'shared, combined, or must explain itself.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a rule for products in a', 'given category that are also on sale.'],
        narration=(
            "That's Specification. [[slnc 250]] If you take one sentence "
            'away, take this one: a specification gives a business rule '
            'one home, so every feature that needs it agrees. [[slnc '
            '350]] The full source, the written notes, the diagrams and '
            'an animated walkthrough are all in the repository, running '
            'offline with nothing installed but a Java development kit. '
            '[[slnc 300]] If you try one exercise, add a rule for '
            'products in a given category that are also on sale, built '
            'only from the existing small rules. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
