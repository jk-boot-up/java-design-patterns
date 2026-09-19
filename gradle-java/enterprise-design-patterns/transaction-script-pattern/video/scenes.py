"""Scene definitions for the Transaction Script teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Transaction Script',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Transaction '
            'Script pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'transaction script organises business logic as one procedure '
            'for each request. The procedure runs as one transaction, and '
            'there are no domain objects behind it. The steps are the '
            'design. [[slnc 350]] This is another project in the '
            'enterprise category, whose subject is how a business '
            'application organises its logic, its data and its requests. '
            'In our online store, the action is placing an order. [[slnc '
            '300]] By the end you will see an order placed by one '
            'procedure, see it undone as one transaction, see two scripts '
            'drift when they copy a rule, and see the bill, which is that '
            'a script grows in the middle. I will also say plainly where '
            'a script is exactly right.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Placing an order:', '', 'check the quantity and the stock,', 'take the stock,', 'price it, with a bulk discount,', 'charge the card,', 'save the order.', '', 'One method, or many objects?'],
        narration=(
            'Here is the scenario. When a customer places an order, the '
            'store checks the quantity and the stock. It takes the stock. '
            'It prices the order, with a bulk discount. It charges the '
            'card, and saves the order. [[slnc 300]] The question: one '
            'method, or a set of objects?'
        ),
    ),
    dict(
        key='03-proc', kind='console', title='One Request, One Procedure',
        body="""ONE. One procedure.
  ORD-1 for £16.00.
  stock of MUG-BLUE: 8.

  one method, read from the
  top to the bottom.""",
        narration=(
            'First, one request, one procedure. Two mugs are ordered. The '
            'order is sixteen pounds, and the stock falls to eight. The '
            'whole business action is one method, and you read it from '
            'the top to the bottom. No order object, no rules class.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One procedure for each request.', '', 'It runs as one transaction.', '', 'No domain objects behind it:', 'the steps are the design.', '', 'Shared code goes in helper', 'functions.'],
        narration=(
            'The pattern. One procedure for each request. It runs as one '
            'transaction. There are no domain objects behind it: the '
            'steps are the design. Anything shared goes in helper '
            'functions.'
        ),
    ),
    dict(
        key='05-tx', kind='console', title='One Transaction',
        body="""TWO. One transaction.
  card declined after the
  stock was taken.

  stock: 10. orders: 0.

  undone together.""",
        narration=(
            'Second, one transaction. The card is declined after the '
            'stock was taken. The transaction undoes everything the '
            'script did. The stock is back to ten, and no order was '
            'saved. That is the reason a script is one transaction: it '
            'either all happened, or none of it did.'
        ),
    ),
    dict(
        key='06-drift', kind='console', title='A Second Script Copies The Rule',
        body="""THREE. A copy.
  7 mugs placed: £50.40.
  the same order amended:
  £56.00.

  the discount changed in one
  script only.""",
        narration=(
            'Third, a second script copies the rule. The amend script '
            'needed to price a quantity, so it copied the pricing. Later '
            'the bulk discount moved from ten items to five, and one '
            'script was told. Seven mugs cost fifty pounds forty when '
            'placed, and fifty six pounds when the same order is amended.'
        ),
    ),
    dict(
        key='07-share', kind='console', title='Share A Procedure',
        body="""FOUR. Share.
  a helper: Pricing.total.
  both scripts: £50.40.

  still procedural: no Order
  object, only a function.""",
        narration=(
            'Fourth, share a procedure. The pricing moves into one helper '
            'function that both scripts call. Now they agree. It is still '
            'procedural. There is no order object. There is a function '
            'that both scripts call.'
        ),
    ),
    dict(
        key='08-grow', kind='console', title='The Bill: Growth',
        body="""FIVE. Growth.
  first script: 3 decisions,
  8 paths.

  a year later: 7 decisions,
  128 paths.

  every rule in the middle of
  one method.""",
        narration=(
            'Fifth, the bill. The first script has three decisions, so '
            'eight paths to test. A year later, after loyalty, region and '
            'coupon rules, it has seven decisions, and a hundred and '
            'twenty eight paths. Every new rule went in the middle of one '
            'method. [[slnc 300]] That is what a script costs as the '
            'rules pile up.'
        ),
    ),
    dict(
        key='09-right', kind='console', title='Where A Script Is Right',
        body="""SIX. Right for this.
  month end:
  2 orders, £316.00 taken.

  one purpose, a few rules:
  clearer as a script.""",
        narration=(
            'Last, where a script is exactly right. A month end job that '
            'adds up the orders: two orders, three hundred and sixteen '
            'pounds. A dozen lines, read once, changed rarely. A job with '
            'one purpose and a few rules is clearer as a script than as a '
            'set of objects.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A method named for a use case,', 'such as placeOrder, that does', '', 'Service classes with long methods', 'and no domain objects, only data', '', 'Two methods that each contain the', 'same price calculation.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'method named for a use case, such as placeOrder, that does '
            'everything from validation to saving. Service classes with '
            'long methods and no domain objects, only data holders. Two '
            'methods that each contain the same price calculation. '
            '@Transactional on a method that contains most of the '
            'business logic.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a transaction script when the', 'logic is simple, mostly sequential', 'and unlikely to grow, and when a', 'team wants the shortest path from', 'request to result. Keep shared', 'rules in helper functions. Move to', 'a domain model when the same rules', 'start to appear in several', "scripts, or when a script's"],
        narration=(
            'Here is my verdict, plainly. Use a transaction script when '
            'the logic is simple, mostly sequential and unlikely to grow, '
            'and when a team wants the shortest path from request to '
            'result. Keep shared rules in helper functions. Move to a '
            'domain model when the same rules start to appear in several '
            "scripts, or when a script's decisions outgrow what anyone "
            'can test.'
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
        body=['A script is the opposite of too', 'much. Its risk is too little', 'structure as the rules grow, so', 'watch the decisions in the middle', 'of the method.'],
        narration=(
            'So when is it too much? A script is the opposite of too '
            'much. Its risk is too little structure as the rules grow, so '
            'watch the decisions in the middle of the method.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Transaction Script. [[slnc 250]] If you take one "
            'sentence away, take this one: a transaction script is the '
            'simplest design that works, and its cost is measured in how '
            'it grows. [[slnc 350]] The full source, the written notes, '
            'the diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add a fourth rule to the grown script, and count how many '
            'new paths it needs a test for. [[slnc 300]] If this helped, '
            'a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
