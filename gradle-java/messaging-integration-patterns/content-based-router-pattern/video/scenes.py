"""Scene definitions for the Content-Based Router teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Content-Based Router',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Content-Based '
            'Router pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'content based router looks inside each message, and sends it '
            'to a different channel depending on what it contains, so '
            'senders and receivers never have to know about each other. '
            '[[slnc 350]] This is the second project in the messaging and '
            'integration category, whose subject is how separate systems '
            'exchange messages safely. In our online store, orders of '
            'different kinds arrive together, and each kind needs a '
            'different place to go. [[slnc 300]] By the end you will see '
            'every order arrive on one channel and the warehouse forced '
            'to sort them, see a router send each to its own channel, see '
            'that the order of the rules decides, see what happens to a '
            'message nothing matches, add a route without touching anyone '
            'else, and see the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Orders arrive together.', '', 'Physical goods: to the warehouse.', 'Gift cards: to digital delivery.', 'Very high value: to fraud review.', '', 'Who decides?'],
        narration=(
            'Here is the scenario. Orders arrive together in the online '
            'store: physical goods, gift cards, subscriptions, and some '
            'of very high value. Physical goods go to the warehouse. Gift '
            'cards go to digital delivery. Very high value orders go to '
            'fraud review. [[slnc 300]] The question: who decides where '
            'each one goes?'
        ),
    ),
    dict(
        key='03-one', kind='console', title='One Channel For Everything',
        body="""ONE. One channel.
  6 orders on the warehouse's
  channel.
  2 gift cards, 1 neither.

  an if for each kind.""",
        narration=(
            'First, one channel for everything. All six orders arrive on '
            "the warehouse's channel. Two are gift cards, which nothing "
            'physical can be done for, and one is neither. The warehouse '
            'now has an if for each kind, and every new kind means '
            'changing the warehouse.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A router reads each message.', '', 'Rules say: if it looks like this,', 'send it to that channel.', '', 'The first rule that matches wins.', '', 'Senders and receivers do not', 'know about the rules.'],
        narration=(
            'The pattern. A router reads each message. Rules say: if it '
            'looks like this, send it to that channel. The first rule '
            'that matches wins. And senders and receivers do not know '
            'about the rules.'
        ),
    ),
    dict(
        key='05-route', kind='console', title='A Router Looks Inside',
        body="""TWO. Routed.
  physical -> warehouse.
  gift cards -> digital.
  high value -> fraud review.
  subscription -> manual review.

  each order in one place.""",
        narration=(
            'Second, a router looks inside. Order one, physical, goes to '
            'the warehouse. Order two, a gift card, goes to digital '
            'delivery. Order three, physical but worth twelve hundred '
            'pounds, goes to fraud review. The subscription, which no '
            'rule covers, goes to manual review. Every order is in '
            'exactly one place.'
        ),
    ),
    dict(
        key='06-first', kind='console', title='The First Rule That Matches Wins',
        body="""THREE. Order matters.
  a gift card for 1500.00:
  high value first: fraud review.
  high value last: digital.

  nothing warns you when the
  order changes.""",
        narration=(
            'Third, the first rule that matches wins. A gift card worth '
            'fifteen hundred pounds. With the high value rule first, it '
            'goes to fraud review. With the high value rule last, it goes '
            'to digital delivery. The order of the rules is part of the '
            'design, and nothing warns you when it changes.'
        ),
    ),
    dict(
        key='07-none', kind='console', title='Nothing Matches',
        body="""FOUR. No match.
  a subscription, no rule.
  with a fallback: manual
  review.
  with none: nowhere, dropped: 1.

  it loses what it does not
  recognise.""",
        narration=(
            'Fourth, nothing matches. A subscription order that no rule '
            'covers. With a fallback channel, it goes to manual review. '
            'With no fallback, it goes nowhere, and is dropped, and '
            'counted. A router with no fallback loses what it does not '
            'recognise, and says nothing.'
        ),
    ),
    dict(
        key='08-add', kind='console', title='A New Route, And Nobody Else Changes',
        body="""FIVE. A new route.
  rules: 3, then 4.
  an EU subscription now goes
  to eu-vat-check.

  senders and receivers not
  touched.""",
        narration=(
            'Fifth, a new route, and nobody else changes. One rule is '
            'added: three rules become four. An EU subscription now goes '
            'to a VAT check. The senders and the receivers were not '
            'touched. A physical EU order still goes to the warehouse, '
            'because an earlier rule matched first.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  the sender says 'goods', not
  'physical'.
  the rule misses it:
  manual review.

  the router is coupled to the
  content's format.
  every route: a rule to test.""",
        narration=(
            'Last, the bill. The sender starts calling physical orders '
            "goods. The router's rule looks for physical, misses them, "
            'and they fall to manual review. The router reads the '
            "content, so it is coupled to the content's format. Routing "
            'on a header keeps that in the envelope, at the cost of the '
            'sender filling it in. And every route is one more rule to '
            'test.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A method that returns a channel or', 'queue name from a message.', '', "Apache Camel's choice().when(...),", "Spring Integration's router.", '', 'RabbitMQ topic exchanges and', 'routing keys.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'method that returns a channel or queue name from a message. '
            "Apache Camel's choice().when(...), Spring Integration's "
            'router. RabbitMQ topic exchanges and routing keys. An if '
            'chain that chooses a queue, in the sender.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a content-based router when', 'one stream carries messages that', 'need different handling, and the', 'difference is in the content.', 'Order the rules on purpose, always', 'have a fallback that keeps and', 'reports what it cannot route, and', 'prefer routing on a header that', 'the sender sets deliberately over'],
        narration=(
            'Here is my verdict, plainly. Use a content-based router when '
            'one stream carries messages that need different handling, '
            'and the difference is in the content. Order the rules on '
            'purpose, always have a fallback that keeps and reports what '
            'it cannot route, and prefer routing on a header that the '
            'sender sets deliberately over reaching into the body. Test '
            'every rule and the order between them.'
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
        body=['If there is only one destination,', 'or the sender already knows where', 'each message goes, a router is a', 'step for nothing.'],
        narration=(
            'So when is it too much? If there is only one destination, or '
            'the sender already knows where each message goes, a router '
            'is a step for nothing.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Content-Based Router. [[slnc 250]] If you take one "
            'sentence away, take this one: a content-based router puts '
            'the sorting in one place, and its price is coupling to the '
            'content and rules whose order matters. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, add a rule for orders over a '
            'thousand pounds to a manual approval channel, and decide '
            'where it goes in the order. [[slnc 300]] If this helped, a '
            'like genuinely does help other people find it, and subscribe '
            'if you would like the rest of the series. [[slnc 250]] '
            'Thanks for watching.'
        ),
    ),
]
