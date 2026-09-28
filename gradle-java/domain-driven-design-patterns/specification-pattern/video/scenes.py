"""Scene definitions for the Specification teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Specification',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Specification pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A specification is a '
            'business rule, written as an object. [[slnc 300]] It can say '
            'whether something meets the rule. [[slnc 300]] It can '
            'explain itself. [[slnc 300]] And it can combine with other '
            "rules to make new ones. [[slnc 600]] Think of a job advert's "
            'requirements. [[slnc 300]] Speaks English, and has a driving '
            'licence, and lives nearby. [[slnc 300]] Each part is simple, '
            'and together they describe exactly who fits. [[slnc 700]] In '
            'our online store, the rule is: which products are cheap, and '
            'available? [[slnc 500]] In this video, one rule is copied '
            'into three places, and drifts apart. [[slnc 300]] Then it is '
            'named once, and combined. [[slnc 300]] We will hear it '
            'explain why a product fails, and then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Three features need the same idea:', 'cheap and available.', '', 'The search page shows such products.', 'A promotion is offered on them.', 'They ship free.', '', 'Where does the rule live?'],
        narration=(
            'Here is the scenario. [[slnc 400]] In our online store, '
            'three features need the same idea: cheap, and available. '
            '[[slnc 500]] The search page shows those products. [[slnc '
            '300]] A promotion is offered on them. [[slnc 300]] And they '
            'get free shipping. [[slnc 500]] So here is the question. '
            '[[slnc 300]] Where should the rule live?'
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
            'First, the naive way: the same rule, written three times. '
            '[[slnc 400]] The search page and free shipping agree. [[slnc '
            '300]] The blue mug, and the tea. [[slnc 500]] But the '
            'promotion, written later, offers four products. [[slnc 300]] '
            'It includes a mug at exactly ten pounds, because its copy '
            'says ten pounds or less. [[slnc 300]] And it includes a '
            'discontinued mug, because it forgot to check. [[slnc 500]] '
            'Nobody meant that. [[slnc 300]] Three copies simply drift '
            'apart.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A rule is an object.', '', 'It says whether a candidate', 'satisfies it.', '', 'It says what it means, in words.', '', 'It combines with others:', 'and, or, not.'],
        narration=(
            'Now, the pattern. [[slnc 400]] A rule becomes an object. '
            '[[slnc 300]] It says whether something meets it. [[slnc '
            '300]] It can describe itself, in words. [[slnc 300]] And it '
            'combines with other rules, using and, or, and not. [[slnc '
            '500]] Written once, and used everywhere.'
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
            'Second demo: the rule, named once. [[slnc 400]] It reads: in '
            'stock, and under ten pounds, and not discontinued. [[slnc '
            '500]] The search page, the promotion, and free shipping all '
            'use it. [[slnc 300]] And now they all agree: the blue mug, '
            'and the tea. [[slnc 500]] Change the rule in one place, and '
            'all three features change together.'
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
            'Third demo: rules combine. [[slnc 400]] Here is a gift idea '
            'rule. [[slnc 300]] A mug under ten pounds, or a tea that is '
            'on sale. [[slnc 500]] It is built from small rules, joined '
            'with and, and or. [[slnc 300]] It describes itself in those '
            'words. [[slnc 300]] And it finds three products that are in '
            'stock. [[slnc 500]] No new class was written.'
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
            'Fourth demo: a rule can explain why not. [[slnc 400]] The '
            'red mug fails on price. [[slnc 300]] The old mug fails '
            'because it is discontinued. [[slnc 300]] The green mug fails '
            'because it is out of stock. [[slnc 300]] And the blue mug '
            'qualifies. [[slnc 500]] Each explanation comes from the rule '
            'itself. [[slnc 300]] Nobody wrote an error message by hand. '
            '[[slnc 300]] So the message can never drift away from the '
            'rule.'
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
            'Fifth demo: one rule, two jobs. [[slnc 400]] First, it '
            'selects from a list, and finds two products. [[slnc 500]] '
            'Second, it checks a single product a customer picked. [[slnc '
            '300]] The old mug is refused, with the reason: it is '
            'discontinued. [[slnc 500]] One definition of cheap and '
            'available, used both to filter, and to check.'
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
            'Finally, the cost. [[slnc 400]] Ten thousand products, and '
            'sixty-six matches. [[slnc 300]] But to find them, all ten '
            'thousand were checked. [[slnc 500]] A specification runs in '
            'memory. [[slnc 300]] To let a database do the searching '
            'instead, the rule must be turned into a database query. '
            '[[slnc 500]] And one more thing. [[slnc 300]] For a rule '
            'used in only one place, a simple lambda is easier than a '
            'specification.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['isSatisfiedBy, with and, or, not.', '', 'Classes named for a business', 'condition, like InStock.', '', 'Predicate.and and Predicate.or.', '', "Spring Data's Specification."],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for an interface with a method like, is '
            'satisfied by, together with and, or, and not. [[slnc 300]] '
            'Look for classes named after a business condition, like In '
            "Stock. [[slnc 300]] Look for Java's Predicate interface, "
            'with its and, and or methods. [[slnc 300]] And look for '
            "Spring Data's Specification."
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['When a rule is shared, combined,', 'or must explain itself.', '', "Small leaves, in the business's", 'words.', '', 'Turn it into a query for large', 'data.', '', 'A rule used once: a lambda.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a specification '
            'when a rule is needed in several places. [[slnc 300]] Or '
            'when rules must be combined, or explained. [[slnc 300]] Or '
            'when a rule is chosen while the program runs. [[slnc 500]] '
            "Keep the small rules small, and name them in the business's "
            'own words. [[slnc 300]] Turn it into a database query when '
            'the data is large. [[slnc 300]] And for a rule used only '
            'once, a lambda is enough.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'The drift between the three copies', 'is real output.', '', 'The catalogue of ten thousand', 'products is built in memory, and', 'the count of products looked at', 'is exact.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] The drift between the '
            'three copies is real output. [[slnc 300]] The catalogue of '
            'ten thousand products is built in memory. [[slnc 300]] And '
            'the count of products checked is exact.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a condition used once, a', 'lambda is clearer.', '', 'It earns its place when a rule is', 'shared, combined or must explain', 'itself.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a condition used '
            'only once, a lambda is clearer. [[slnc 300]] A specification '
            'earns its place when a rule is shared, combined, or must '
            'explain itself.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a rule for products in a', 'given category that are also on sale.'],
        narration=(
            "That's the Specification pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'specification gives a business rule one home, so every '
            'feature that needs it agrees. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Add a rule for products in a given '
            'category, that are also on sale. [[slnc 300]] And build it '
            'only from the existing small rules. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
