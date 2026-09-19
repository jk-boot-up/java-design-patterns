"""Scene definitions for the Delegation teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Delegation',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Delegation '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'delegation is when an object does not do a job itself. It '
            'hands the job to a helper object that it holds, and that it '
            'can swap. [[slnc 350]] This is another project in the '
            'foundational category, whose subject is how an object gets '
            'hold of another, and how small idioms shape everyday Java. '
            'In our online store, an order can be priced in several ways, '
            'and each new way seems to need a new kind of order. [[slnc '
            '300]] By the end you will see classes multiply for each way '
            'of pricing, see an order hand its pricing on, see the helper '
            'swapped while the order lives, see two helpers used at once, '
            'see why the helper is given the order, and see the bill, '
            'which is an extra call and forwarding methods.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order can be priced with a', 'premium discount,', 'with gift wrap,', 'with both, or neither.', '', 'A customer may become premium', 'in the middle of shopping.', '', 'Do we need a class for each?'],
        narration=(
            'Here is the scenario. An order can be priced with a premium '
            'discount, with gift wrap, with both, or with neither. A '
            'customer may become premium in the middle of shopping. '
            '[[slnc 300]] The question: do we need a class for each?'
        ),
    ),
    dict(
        key='03-inherit', kind='console', title='A Subclass For Each Way',
        body="""ONE. A subclass for each.
  premium, gift wrap, both:
  4 classes for 2 features.
  a third feature: 8.

  an order cannot change its
  class once it exists.""",
        narration=(
            'First, a subclass for each way. Premium, gift wrap, and '
            'both: four classes for two features. A third feature would '
            'need eight. A premium gift order is ninety six hundred. And '
            'an order cannot change its class once it exists.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['The object holds a helper.', '', 'When asked to do the job, it', 'hands the job to the helper.', '', 'The helper can be swapped,', 'and used with others.'],
        narration=(
            'The pattern. The object holds a helper. When asked to do the '
            'job, it hands the job to the helper. The helper can be '
            'swapped, and used with others.'
        ),
    ),
    dict(
        key='05-hand', kind='console', title='The Order Hands The Pricing On',
        body="""TWO. The order hands it on.
  one Order class.
  no rule: 10000.
  premium: 9000.
  gift wrap: 10600.""",
        narration=(
            'Second, the order hands the pricing on. One order class. '
            'With no rule, ten thousand. With premium, nine thousand. '
            'With gift wrap, ten thousand six hundred.'
        ),
    ),
    dict(
        key='06-swap', kind='console', title='Change The Helper While It Lives',
        body="""THREE. Change the helper.
  the customer joins premium
  while shopping.
  the same order object:
  10000, then 9000.""",
        narration=(
            'Third, change the helper while it lives. The customer joins '
            'the premium plan while shopping. The same order object: ten '
            'thousand, then nine thousand.'
        ),
    ),
    dict(
        key='07-two', kind='console', title='Two Helpers At Once',
        body="""FOUR. Two helpers.
  premium then gift wrap: 9600.
  the same as the class made
  for both.
  classes added: 0.""",
        narration=(
            'Fourth, two helpers at once. Premium then gift wrap: ninety '
            'six hundred, the same as the class made for both. Classes '
            'added: none.'
        ),
    ),
    dict(
        key='08-self', kind='console', title='The Helper Needs To See The Order',
        body="""FIVE. The helper needs the order.
  gift wrap: 300 for each item.
  2 items: 10600.
  3 items: 10900.

  the order passes itself in: the
  helper does not know which
  order it is helping.""",
        narration=(
            'Fifth, the helper needs to see the order. Gift wrap is three '
            'hundred for each item, so it must look at the order it was '
            'called for. Two items: ten thousand six hundred. Three '
            'items: ten thousand nine hundred. That is why the order '
            'passes itself in: the helper is a different object, and does '
            'not know which order it is helping.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  one total() made 3 calls to
  helpers: a hop for each.

  a helper with 4 methods: 4
  forwarding methods that only
  pass the call on.

  the helper knows nothing of
  its owner unless told.""",
        narration=(
            'Last, the bill. One total made three calls to helpers, where '
            'inheritance made none: one more hop for every helper. To '
            'look like a helper with four methods, the order had to write '
            'four forwarding methods that only pass the call on. And a '
            'helper knows nothing of its owner unless it is told.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A field of an interface type, and', 'a method that just calls it.', '', 'Strategy, State, Decorator and', 'Proxy, which are all delegation', '', "Kotlin's by keyword, and Lombok's", '@Delegate.'],
        narration=(
            'How do you recognise this in code you did not write? A field '
            'of an interface type, and a method that just calls it. '
            'Strategy, State, Decorator and Proxy, which are all '
            "delegation with a purpose. Kotlin's by keyword, and Lombok's "
            '@Delegate. Collections.unmodifiableList, which hands each '
            'call to a list it holds.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Prefer holding a helper to', 'inheriting from a parent, when', 'what varies is one job. Pass the', 'owner in if the helper needs it.', 'Let the helper be swapped, and', 'combined. Accept the extra hop,', 'and the forwarding code, or use a', 'language feature that writes it', 'for you.'],
        narration=(
            'Here is my verdict, plainly. Prefer holding a helper to '
            'inheriting from a parent, when what varies is one job. Pass '
            'the owner in if the helper needs it. Let the helper be '
            'swapped, and combined. Accept the extra hop, and the '
            'forwarding code, or use a language feature that writes it '
            'for you.'
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
        body=['If there is one fixed way of doing', 'a job, do it directly. Delegation', 'pays off when a job varies, or', 'must change at run time.'],
        narration=(
            'So when is it too much? If there is one fixed way of doing a '
            'job, do it directly. Delegation pays off when a job varies, '
            'or must change at run time.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Delegation. [[slnc 250]] If you take one sentence "
            'away, take this one: delegation hands a job to a helper you '
            'can swap and combine, and the price is an extra call, and '
            'the forwarding code you must write. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, add a fourth rule that adds a '
            'shipping fee, and combine it with premium without adding a '
            'class. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
