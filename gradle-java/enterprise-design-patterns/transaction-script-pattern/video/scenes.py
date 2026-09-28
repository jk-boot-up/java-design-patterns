"""Scene definitions for the Transaction Script teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Transaction Script',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Transaction Script pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A transaction script '
            'organises business logic as one procedure for each request. '
            '[[slnc 300]] The procedure runs as one transaction. [[slnc '
            '300]] And there are no business objects behind it. [[slnc '
            '300]] The steps themselves are the design. [[slnc 600]] '
            'Think of a recipe card. [[slnc 300]] Step one, step two, '
            'step three, from top to bottom. [[slnc 300]] No theory, just '
            'the steps. [[slnc 700]] In our online store, the action is '
            'placing an order. [[slnc 500]] In this video, one procedure '
            'places an order, and undoes it as one transaction. [[slnc '
            '300]] Two scripts drift apart when they copy a rule. [[slnc '
            '300]] And we hear how a script grows in the middle. [[slnc '
            '300]] We will also hear where a script is exactly right.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Placing an order:', '', 'check the quantity and the stock,', 'take the stock,', 'price it, with a bulk discount,', 'charge the card,', 'save the order.', '', 'One method, or many objects?'],
        narration=(
            'Here is the scenario. [[slnc 400]] When a customer places an '
            'order, the store checks the quantity, and the stock. [[slnc '
            '300]] It takes the items from stock. [[slnc 300]] It prices '
            'the order, with a bulk discount. [[slnc 300]] It charges the '
            'card. [[slnc 300]] And it saves the order. [[slnc 500]] So '
            'here is the question. [[slnc 300]] One method, or a set of '
            'objects?'
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
            'First demo: one request, one procedure. [[slnc 400]] Two '
            'mugs are ordered. [[slnc 300]] The order costs sixteen '
            'pounds, and the stock falls to eight. [[slnc 500]] The whole '
            'business action is one method. [[slnc 300]] You read it from '
            'top to bottom. [[slnc 300]] No order object, and no rules '
            'class.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One procedure for each request.', '', 'It runs as one transaction.', '', 'No domain objects behind it:', 'the steps are the design.', '', 'Shared code goes in helper', 'functions.'],
        narration=(
            'Now, the pattern. [[slnc 400]] One procedure for each '
            'request. [[slnc 300]] It runs as one transaction. [[slnc '
            '500]] There are no business objects behind it. [[slnc 300]] '
            'The steps are the design. [[slnc 300]] And anything shared '
            'goes into helper functions.'
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
            'Second demo: one transaction. [[slnc 400]] The card is '
            'declined, after the stock was already taken. [[slnc 500]] '
            'The transaction undoes everything the script did. [[slnc '
            '300]] The stock is back to ten. [[slnc 300]] And no order '
            'was saved. [[slnc 500]] That is why a script is one '
            'transaction. [[slnc 300]] Either all of it happened, or none '
            'of it did.'
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
            'Third demo: a second script copies the rule. [[slnc 400]] '
            'The script that changes an existing order needed to price a '
            'quantity. [[slnc 300]] So it copied the pricing code. [[slnc '
            '500]] Later, the bulk discount changed, from ten items to '
            'five. [[slnc 300]] And only one script was updated. [[slnc '
            '500]] Now seven mugs cost fifty pounds forty when first '
            'ordered. [[slnc 300]] But fifty-six pounds when the same '
            'order is changed.'
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
            'Fourth demo: share a procedure. [[slnc 400]] The pricing '
            'moves into one helper function, which both scripts call. '
            '[[slnc 300]] Now both agree: fifty pounds forty. [[slnc '
            '500]] It is still procedural. [[slnc 300]] There is no order '
            'object. [[slnc 300]] Just one function that both scripts '
            'share.'
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
            'Fifth demo, and the cost: growth. [[slnc 400]] The first '
            'script makes three decisions. [[slnc 300]] So there are '
            'eight different paths through it, to test. [[slnc 500]] A '
            'year later, after loyalty, region, and coupon rules are '
            'added, it makes seven decisions. [[slnc 300]] That means one '
            'hundred and twenty-eight paths. [[slnc 500]] Every new rule '
            'went into the middle of one method. [[slnc 300]] That is '
            'what a script costs as the rules pile up.'
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
            'Last demo: where a script is exactly right. [[slnc 400]] A '
            'month-end job adds up the orders. [[slnc 300]] Two orders, '
            'three hundred and sixteen pounds. [[slnc 500]] A dozen '
            'lines, read once, and rarely changed. [[slnc 300]] A job '
            'with one purpose, and a few rules, is clearer as a script '
            'than as a set of objects.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A method named for a use case,', 'such as placeOrder, that does', '', 'Service classes with long methods', 'and no domain objects, only data', '', 'Two methods that each contain the', 'same price calculation.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a method named after a use case, such '
            'as place order, that does everything from checking to '
            'saving. [[slnc 300]] Look for service classes with long '
            'methods, and no business objects, only data holders. [[slnc '
            '300]] Look for two methods containing the same price '
            'calculation. [[slnc 300]] And the at Transactional '
            'annotation, on a method holding most of the business logic.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a transaction script when the', 'logic is simple, mostly sequential', 'and unlikely to grow, and when a', 'team wants the shortest path from', 'request to result. Keep shared', 'rules in helper functions. Move to', 'a domain model when the same rules', 'start to appear in several', "scripts, or when a script's"],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a transaction '
            'script when the logic is simple, runs step by step, and is '
            'unlikely to grow. [[slnc 300]] And when a team wants the '
            'shortest path from request to result. [[slnc 500]] Keep '
            'shared rules in helper functions. [[slnc 500]] Move to '
            'business objects when the same rules start appearing in '
            'several scripts. [[slnc 300]] Or when one script has more '
            'decisions than anyone can test.'
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
        body=['A script is the opposite of too', 'much. Its risk is too little', 'structure as the rules grow, so', 'watch the decisions in the middle', 'of the method.'],
        narration=(
            'So, when is this too much? [[slnc 400]] A script is the '
            'opposite of too much. [[slnc 300]] Its risk is too little '
            'structure, as the rules grow. [[slnc 300]] So watch the '
            'decisions piling up in the middle of the method.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Transaction Script pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'transaction script is the simplest design that works, and '
            'its cost is measured in how it grows. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Add one more rule to the '
            'grown script. [[slnc 300]] And count how many new paths now '
            'need a test. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
