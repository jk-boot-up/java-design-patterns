"""Scene definitions for the Delegation teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Delegation',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Delegation pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Delegation is when an object '
            'does not do a job itself. [[slnc 300]] Instead, it hands the '
            'job to a helper object that it holds. [[slnc 300]] And that '
            'helper can be swapped. [[slnc 600]] Think of a busy manager '
            'with an assistant. [[slnc 300]] The manager passes the diary '
            'to the assistant. [[slnc 300]] And if the assistant changes, '
            "the manager's job does not. [[slnc 700]] In our online "
            'store, an order can be priced in several ways. [[slnc 300]] '
            'And each new way seems to need a new kind of order. [[slnc '
            '500]] In this video, classes multiply for every way of '
            'pricing. [[slnc 300]] Then an order hands its pricing to a '
            'helper. [[slnc 300]] We will swap the helper, combine two '
            'helpers, and then hear the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order can be priced with a', 'premium discount,', 'with gift wrap,', 'with both, or neither.', '', 'A customer may become premium', 'in the middle of shopping.', '', 'Do we need a class for each?'],
        narration=(
            'Here is the scenario. [[slnc 400]] An order can be priced '
            'with a premium discount. [[slnc 300]] Or with gift wrap. '
            '[[slnc 300]] Or with both, or neither. [[slnc 500]] And a '
            'customer might become premium in the middle of shopping. '
            '[[slnc 500]] So here is the question. [[slnc 300]] Do we '
            'need a separate class for each combination?'
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
            'First, the naive way: a subclass for each combination. '
            '[[slnc 400]] Premium, gift wrap, and both. [[slnc 300]] That '
            'is four classes, for just two features. [[slnc 300]] A third '
            'feature would need eight. [[slnc 500]] A premium gift order '
            'costs ninety-six pounds. [[slnc 300]] But once an order '
            'exists, it can never change its class.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['The object holds a helper.', '', 'When asked to do the job, it', 'hands the job to the helper.', '', 'The helper can be swapped,', 'and used with others.'],
        narration=(
            'Now, the pattern. [[slnc 400]] The object holds a helper. '
            '[[slnc 300]] When asked to do the job, it hands the job to '
            'the helper. [[slnc 500]] The helper can be swapped. [[slnc '
            '300]] And it can be combined with other helpers.'
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
            'Second demo: the order hands its pricing on. [[slnc 400]] '
            'There is just one order class. [[slnc 500]] With no pricing '
            'rule, the order costs one hundred pounds. [[slnc 300]] With '
            'the premium rule, ninety pounds. [[slnc 300]] With the gift '
            'wrap rule, one hundred and six pounds.'
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
            'Third demo: change the helper while the order exists. [[slnc '
            '400]] The customer joins the premium plan, while shopping. '
            '[[slnc 500]] The very same order object costs one hundred '
            'pounds, and then ninety.'
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
            'Fourth demo: two helpers at once. [[slnc 400]] Premium, and '
            'then gift wrap. [[slnc 300]] The total is ninety-six pounds. '
            '[[slnc 300]] Exactly the same as the special class made for '
            'both. [[slnc 500]] And the number of classes added: none.'
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
            'Fifth demo: the helper needs to see the order. [[slnc 400]] '
            'Gift wrap costs three pounds for each item. [[slnc 300]] So '
            'the helper must look at the order it is pricing. [[slnc '
            '500]] Two items: one hundred and six pounds. [[slnc 300]] '
            'Three items: one hundred and nine pounds. [[slnc 500]] That '
            'is why the order passes itself in, when it calls the helper. '
            '[[slnc 300]] The helper is a separate object. [[slnc 300]] '
            'It does not know which order it is helping, unless it is '
            'told.'
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
            'Finally, the cost. [[slnc 400]] Working out one total made '
            'three calls to helpers. [[slnc 300]] Inheritance would have '
            'made none. [[slnc 300]] So there is one extra hop, for every '
            "helper. [[slnc 500]] To offer a helper's four methods, the "
            'order had to write four forwarding methods. [[slnc 300]] '
            'They do nothing but pass the call along. [[slnc 500]] And a '
            'helper knows nothing about its owner, unless it is told.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A field of an interface type, and', 'a method that just calls it.', '', 'Strategy, State, Decorator and', 'Proxy, which are all delegation', '', "Kotlin's by keyword, and Lombok's", '@Delegate.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a field whose type is an interface, '
            'and a method that simply calls it. [[slnc 500]] Many famous '
            'patterns are delegation with a purpose. [[slnc 300]] '
            'Strategy, State, Decorator, and Proxy. [[slnc 500]] Kotlin '
            "has a keyword for it, called by. [[slnc 300]] And Java's "
            'unmodifiable list simply hands each call to a list it holds.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Prefer holding a helper to', 'inheriting from a parent, when', 'what varies is one job. Pass the', 'owner in if the helper needs it.', 'Let the helper be swapped, and', 'combined. Accept the extra hop,', 'and the forwarding code, or use a', 'language feature that writes it', 'for you.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] When what varies is '
            'one job, prefer holding a helper, over inheriting from a '
            'parent. [[slnc 500]] Pass the owner in, if the helper needs '
            'to see it. [[slnc 300]] Let the helper be swapped, and '
            'combined. [[slnc 500]] And accept the extra hop, and the '
            'forwarding code. [[slnc 300]] Or use a language feature that '
            'writes the forwarding for you.'
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
        body=['If there is one fixed way of doing', 'a job, do it directly. Delegation', 'pays off when a job varies, or', 'must change at run time.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If there is only one '
            'fixed way to do a job, just do it directly. [[slnc 400]] '
            'Delegation pays off when a job varies, or must change while '
            'the program runs.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Delegation pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Delegation '
            'hands a job to a helper you can swap and combine, and the '
            'price is an extra call, and forwarding code you must write. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] Add a '
            'fourth rule that adds a shipping fee. [[slnc 300]] And '
            'combine it with premium, without adding a class. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
