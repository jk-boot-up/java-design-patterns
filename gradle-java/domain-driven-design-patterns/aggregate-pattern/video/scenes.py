"""Scene definitions for the Aggregate teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Aggregate',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Aggregate pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An aggregate is a small '
            'group of objects that is treated as one unit. [[slnc 300]] '
            'It has one main object, called the root, which is the only '
            'way in. [[slnc 300]] So the rules that cover the whole group '
            'cannot be broken from outside. [[slnc 600]] Think of a bank '
            "teller's window. [[slnc 300]] You cannot reach into the "
            'vault yourself. [[slnc 300]] Every deposit and withdrawal '
            'goes through the teller, who checks the rules. [[slnc 700]] '
            'In our online store, the group is an order, and its lines. '
            '[[slnc 500]] In this video, an order breaks all its own '
            'rules, when anyone can reach inside it. [[slnc 300]] Then '
            'one root guards them all. [[slnc 300]] We will hear why it '
            'refers to other groups only by I D, how it is saved as a '
            'whole, and how drawing it too big goes wrong.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order has lines.', '', 'Rules span the lines:', 'one to ten of an item,', 'one line per item,', 'a total under a thousand pounds,', 'and a placed order cannot change.', '', 'Who enforces them?'],
        narration=(
            'Here is the scenario. [[slnc 400]] In our online store, an '
            'order has lines. [[slnc 300]] And some rules cover all the '
            'lines together. [[slnc 500]] A line holds between one and '
            'ten of an item. [[slnc 300]] Each item appears on only one '
            'line. [[slnc 300]] The total may not go over one thousand '
            'pounds. [[slnc 300]] And once an order is placed, it cannot '
            'change. [[slnc 500]] So here is the question. [[slnc 300]] '
            'Who enforces these rules?'
        ),
    ),
    dict(
        key='03-loose', kind='console', title='A Loose Order',
        body="""ONE. A loose order.
  -3 mugs: in.
  the same machine, two
  lines: in.
  total £5988.50: in.
  after placed: in.

  every rule lives in the
  caller's head.""",
        narration=(
            'First, a loose order. [[slnc 400]] It is just a list, with '
            'public fields. [[slnc 500]] A line of minus three mugs goes '
            'in. [[slnc 300]] The same machine goes on two separate '
            'lines. [[slnc 300]] The total reaches nearly six thousand '
            'pounds, far over the limit. [[slnc 300]] And a line is added '
            'after the order was placed. [[slnc 500]] All of it is '
            'accepted. [[slnc 300]] Every rule exists only in the head of '
            'whoever wrote the calling code.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One root: the Order.', '', 'Its lines cannot be reached, or', 'built, except through it.', '', 'Every rule that spans the lines', 'lives in the root.', '', 'Other aggregates: by id only.'],
        narration=(
            'Now, the pattern. [[slnc 400]] There is one root: the Order. '
            '[[slnc 300]] Its lines cannot be reached, or even created, '
            'except through it. [[slnc 500]] Every rule that covers the '
            'lines lives in the root. [[slnc 300]] So there is exactly '
            'one place to look. [[slnc 500]] And other aggregates, such '
            'as the customer, are referred to by I D only.'
        ),
    ),
    dict(
        key='05-guard', kind='console', title='The Root Guards The Rules',
        body="""TWO. The root.
  0 mugs: refused.
  11 mugs: refused.
  5 more, making 11: refused.
  over 1000: refused.
  after place(): refused.
  empty: refused.""",
        narration=(
            'Second demo: the same actions, through the root. [[slnc '
            '400]] Zero mugs is refused. [[slnc 300]] Eleven mugs is '
            'refused. [[slnc 300]] Six mugs is fine. [[slnc 300]] But '
            'five more of the same mug would make eleven, so that is '
            'refused too. [[slnc 400]] A total over one thousand pounds '
            'is refused. [[slnc 300]] A change after placing the order is '
            'refused. [[slnc 300]] And an empty order cannot be placed. '
            '[[slnc 500]] Six rules, each enforced, all in one class.'
        ),
    ),
    dict(
        key='06-door', kind='console', title='There Is Only One Door',
        body="""THREE. One door.
  order.lines().clear():
  UnsupportedOperation.

  an OrderLine has no public
  constructor.

  the root is the only way.""",
        narration=(
            'Third demo: there is only one door. [[slnc 400]] From '
            'outside, the list of lines is read-only. [[slnc 300]] Trying '
            'to clear it throws an error. [[slnc 500]] And an order line '
            'has no public constructor. [[slnc 300]] So no line can exist '
            'that the order has not checked.'
        ),
    ),
    dict(
        key='07-id', kind='console', title='Other Aggregates By Id',
        body="""FOUR. By id.
  orders holding the whole
  customer: 3 customer loads.

  orders holding a CustomerId:
  0 loads.

  the customer is another
  aggregate.""",
        narration=(
            'Fourth demo: other aggregates, by I D. [[slnc 400]] Three '
            'orders that each hold the whole customer object load the '
            'customer three times. [[slnc 300]] Three orders that only '
            'hold a customer I D load it no times at all. [[slnc 500]] '
            'The customer is a separate aggregate, with its own rules, '
            'and its own saves. [[slnc 300]] An order should know who the '
            'customer is, not carry the customer around.'
        ),
    ),
    dict(
        key='08-whole', kind='console', title='Saved Whole, Or Not At All',
        body="""FIVE. Saved whole.
  clerk A saves: accepted.
  clerk B saves: refused,
  changed since it was read.

  a half-updated order
  cannot exist.""",
        narration=(
            'Fifth demo: saved whole, or not at all. [[slnc 400]] Two '
            'clerks read the same order, and each adds a line. [[slnc '
            '400]] Clerk A saves, and it is accepted. [[slnc 300]] Clerk '
            'B saves, and it is refused, because the order changed since '
            'B read it. [[slnc 500]] The order is read whole, changed '
            'whole, and saved whole. [[slnc 300]] So an order with only '
            "half of one clerk's change can never exist."
        ),
    ),
    dict(
        key='09-big', kind='console', title='An Aggregate Drawn Too Big',
        body="""SIX. Too big.
  the customer and all their
  orders as one aggregate:
  two clerks, two orders:
  second save refused.

  one aggregate per order:
  both accepted.""",
        narration=(
            'Finally, the cost of drawing it too big. [[slnc 400]] '
            'Suppose the aggregate is the customer, together with all '
            'their orders. [[slnc 400]] Two clerks change two different '
            'orders. [[slnc 300]] The second save is refused, because '
            'both changed the same customer aggregate. [[slnc 300]] That '
            'is a false conflict. [[slnc 500]] With one aggregate per '
            'order, both saves go through. [[slnc 300]] The boundary is a '
            'choice. [[slnc 300]] And drawing it too wide costs you real '
            'conflicts.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Private collections, and methods', 'that add to them.', '', 'A read-only view, not the list.', '', 'A repository that saves the', 'root only.', '', 'Other aggregates held by id.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a class with private collections, and '
            'methods that add to them. [[slnc 300]] Look for a read-only '
            'view being returned, instead of the list itself. [[slnc '
            '300]] Look for a repository that saves the whole order, and '
            'never a single line. [[slnc 300]] And look for other '
            'aggregates held by I D.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Draw it around what must be', 'consistent together.', '', 'One root, one way in.', '', 'The rules live in the root.', '', 'Other aggregates by id.', '', 'Save and load the whole.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Draw the aggregate '
            'around what must stay consistent together, and no wider. '
            '[[slnc 300]] Make one class the root, and the only way in. '
            '[[slnc 300]] Keep the rules inside it. [[slnc 300]] Refer to '
            'other aggregates by I D. [[slnc 300]] And save and load the '
            'whole thing, together.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'The stores are in memory, and the', 'version check is a real check.', '', 'Two clerks are two loads in a row,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] The storage is in '
            'memory, and the version check is a real check. [[slnc 300]] '
            'The two clerks load one after the other, so every run gives '
            'the same result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a record with no rules across', 'its parts, one class is enough.', '', 'It earns its place when rules', 'span several objects.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a simple record '
            'with no rules across its parts, a single class is enough. '
            '[[slnc 300]] An aggregate earns its place when rules cover '
            'several objects together.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a rule that an order can', 'hold at most five different items.'],
        narration=(
            "That's the Aggregate pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] An aggregate is '
            'where a rule lives, and where a save begins and ends. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Add a rule that an '
            'order can hold at most five different items. [[slnc 300]] '
            'Then notice which class had to change. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
