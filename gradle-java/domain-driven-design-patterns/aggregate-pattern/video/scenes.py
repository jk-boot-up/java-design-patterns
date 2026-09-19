"""Scene definitions for the Aggregate teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Aggregate',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Aggregate '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: an '
            'aggregate is a small cluster of objects that is treated as '
            'one unit. It has one root, which is the only way in, so the '
            'rules that span the cluster cannot be broken from outside. '
            '[[slnc 350]] This is the second project in the domain-driven '
            'design category, whose subject is writing code that says '
            'what the business says. In our online store, the cluster is '
            'an order and its lines. [[slnc 300]] By the end you will see '
            'an order break every one of its own rules when anyone can '
            'reach inside it, then see one root guard them all, why it '
            'refers to other aggregates only by id, how it is saved '
            'whole, and how drawing it too big goes wrong.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order has lines.', '', 'Rules span the lines:', 'one to ten of an item,', 'one line per item,', 'a total under a thousand pounds,', 'and a placed order cannot change.', '', 'Who enforces them?'],
        narration=(
            'Here is the scenario. In the online store, an order has '
            'lines. And there are rules that span the lines. A line holds '
            'between one and ten of an item. An item appears on one line '
            'only. The total may not pass a thousand pounds. And a placed '
            'order cannot change. [[slnc 300]] The question: who enforces '
            'them?'
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
            'First, a loose order. It is a list with public fields. A '
            'line of minus three mugs goes in. The same machine goes on '
            'two lines. The total comes to nearly six thousand pounds, '
            'far over the limit. And a line is added after the order was '
            'placed. [[slnc 300]] Every rule is true only in the head of '
            'whoever wrote the caller.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One root: the Order.', '', 'Its lines cannot be reached, or', 'built, except through it.', '', 'Every rule that spans the lines', 'lives in the root.', '', 'Other aggregates: by id only.'],
        narration=(
            'The pattern. One root, the order. Its lines cannot be '
            'reached, or even built, except through it. Every rule that '
            'spans the lines lives in the root, so there is exactly one '
            'place to look. And it refers to other aggregates, like the '
            'customer, by id only.'
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
            'Second, the same operations through the root. Nought mugs is '
            'refused. Eleven mugs is refused. Six mugs are fine, but five '
            'more of the same would make eleven, and that is refused too. '
            'A total over a thousand pounds is refused. A change after '
            'placing is refused, and an empty order cannot be placed. '
            '[[slnc 300]] Six rules, each enforced, all in one class.'
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
            'Third, one door. The list of lines, seen from outside, is '
            'read only. Trying to clear it throws. And an order line has '
            'no public constructor, so no line can exist that the order '
            'has not checked.'
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
            'Fourth, other aggregates by id. Three orders that hold the '
            'whole customer object load the customer three times. Three '
            'that hold only a customer id load none. The customer is a '
            'different aggregate, with its own rules and its own saves. '
            'An order should know who, not carry them.'
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
            'Fifth, saved whole. Two clerks read the same order, and each '
            'add a line. Clerk A saves, and it is accepted. Clerk B '
            'saves, and is refused, because the order changed since it '
            'was read. [[slnc 300]] The order is read whole, changed '
            "whole and saved whole. So an order with half of one clerk's "
            'change cannot exist.'
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
            'Last, the bill. Suppose the aggregate is the customer and '
            'all their orders. Two clerks change two different orders. '
            'The second save is refused, because both changed the '
            'customer. That is a false conflict. [[slnc 300]] With one '
            'aggregate per order, both saves go through. The boundary is '
            'a choice, and drawing it too wide costs you real contention.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Private collections, and methods', 'that add to them.', '', 'A read-only view, not the list.', '', 'A repository that saves the', 'root only.', '', 'Other aggregates held by id.'],
        narration=(
            'How do you recognise this in code you did not write? A class '
            'with private collections and methods that add to them. A '
            'read only view returned instead of the list itself. A '
            'repository that saves the order, and never a line. And other '
            'aggregates held by id.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Draw it around what must be', 'consistent together.', '', 'One root, one way in.', '', 'The rules live in the root.', '', 'Other aggregates by id.', '', 'Save and load the whole.'],
        narration=(
            'Here is my verdict, plainly. Draw the aggregate around what '
            'must be consistent together, and no wider. Make one class '
            'the root, and the only way in. Keep the rules in it. Refer '
            'to other aggregates by id. And save and load the whole '
            'thing.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'The stores are in memory, and the', 'version check is a real check.', '', 'Two clerks are two loads in a row,', 'so every run is the same.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. The stores are in memory, and the '
            'version check is a real check. The two clerks are two loads, '
            'one after the other, so every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a record with no rules across', 'its parts, one class is enough.', '', 'It earns its place when rules', 'span several objects.'],
        narration=(
            'So when is it too much? For a plain record with no rules '
            'across its parts, a single class is enough. An aggregate '
            'earns its place when rules span several objects.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a rule that an order can', 'hold at most five different items.'],
        narration=(
            "That's Aggregate. [[slnc 250]] If you take one sentence "
            'away, take this one: an aggregate is where a rule lives, and '
            'where a save begins and ends. [[slnc 350]] The full source, '
            'the written notes, the diagrams and an animated walkthrough '
            'are all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, add a rule that an order can hold at most '
            'five different items, and see which class changes. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
