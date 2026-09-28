"""Scene definitions for the Content-Based Router teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Content-Based Router',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Content-Based Router pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A content-based '
            'router looks inside each message. [[slnc 300]] Then it sends '
            'the message to a different channel, depending on what it '
            'contains. [[slnc 300]] So senders and receivers never need '
            'to know about each other. [[slnc 600]] Think of a post '
            'office sorting room. [[slnc 300]] A clerk reads each '
            'address, and drops the letter into the right bag. [[slnc '
            '700]] In our online store, orders of different kinds arrive '
            'together. [[slnc 300]] And each kind needs to go somewhere '
            'different. [[slnc 500]] In this video, every order lands on '
            'one channel, and the warehouse must sort them. [[slnc 300]] '
            'Then a router sends each one to its own channel. [[slnc '
            '300]] We will hear why the order of rules matters, what '
            'happens to a message nothing matches, and then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Orders arrive together.', '', 'Physical goods: to the warehouse.', 'Gift cards: to digital delivery.', 'Very high value: to fraud review.', '', 'Who decides?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Orders arrive together in '
            'the online store. [[slnc 300]] Physical goods, gift cards, '
            'subscriptions, and some very expensive orders. [[slnc 500]] '
            'Physical goods must go to the warehouse. [[slnc 300]] Gift '
            'cards must go to digital delivery. [[slnc 300]] And very '
            'expensive orders must go to fraud review. [[slnc 500]] So '
            'here is the question. [[slnc 300]] Who decides where each '
            'one goes?'
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
            'First, the naive way: one channel for everything. [[slnc '
            "400]] All six orders arrive on the warehouse's channel. "
            '[[slnc 300]] Two of them are gift cards, which the warehouse '
            'cannot pack. [[slnc 300]] And one is neither kind. [[slnc '
            '500]] So the warehouse needs an if statement for each kind '
            'of order. [[slnc 300]] And every new kind means changing the '
            'warehouse.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A router reads each message.', '', 'Rules say: if it looks like this,', 'send it to that channel.', '', 'The first rule that matches wins.', '', 'Senders and receivers do not', 'know about the rules.'],
        narration=(
            'Now, the pattern. [[slnc 400]] A router reads each message. '
            '[[slnc 300]] Rules say: if it looks like this, send it to '
            'that channel. [[slnc 300]] The first rule that matches wins. '
            '[[slnc 500]] And the senders and receivers know nothing '
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
            'Second demo: a router that looks inside. [[slnc 400]] Order '
            'one is physical, so it goes to the warehouse. [[slnc 300]] '
            'Order two is a gift card, so it goes to digital delivery. '
            '[[slnc 300]] Order three is physical, but worth twelve '
            'hundred pounds, so it goes to fraud review. [[slnc 300]] And '
            'the subscription, which no rule covers, goes to manual '
            'review. [[slnc 500]] Every order ends up in exactly one '
            'place.'
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
            'Third demo: the first rule that matches wins. [[slnc 400]] '
            'Take a gift card worth fifteen hundred pounds. [[slnc 500]] '
            'With the high value rule checked first, it goes to fraud '
            'review. [[slnc 300]] With the high value rule checked last, '
            'it goes to digital delivery instead. [[slnc 500]] The order '
            'of the rules is part of the design. [[slnc 300]] And nothing '
            'warns you when that order changes.'
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
            'Fourth demo: when nothing matches. [[slnc 400]] A '
            'subscription order arrives, and no rule covers it. [[slnc '
            '500]] With a fallback channel, it goes to manual review. '
            '[[slnc 300]] With no fallback, it goes nowhere. [[slnc 300]] '
            'It is dropped, and counted as dropped. [[slnc 500]] A router '
            'with no fallback silently loses anything it does not '
            'recognise.'
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
            'Fifth demo: a new route, and nobody else changes. [[slnc '
            '400]] One rule is added. [[slnc 300]] Three rules become '
            'four. [[slnc 300]] Now a European subscription goes to a tax '
            'check. [[slnc 500]] The senders and the receivers were not '
            'touched at all. [[slnc 300]] And a physical European order '
            'still goes to the warehouse, because an earlier rule matches '
            'it first.'
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
            'Finally, the cost. [[slnc 400]] The sender starts calling '
            'physical orders, goods, instead of physical. [[slnc 300]] '
            "The router's rule is looking for the word physical. [[slnc "
            '300]] So it misses them, and they all fall through to manual '
            'review. [[slnc 500]] The router reads the content, so it '
            "depends on the content's exact format. [[slnc 300]] Routing "
            "on a label in the message's envelope avoids that. [[slnc "
            '300]] But then the sender must fill that label in. [[slnc '
            '500]] And every route is one more rule to test.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A method that returns a channel or', 'queue name from a message.', '', "Apache Camel's choice().when(...),", "Spring Integration's router.", '', 'RabbitMQ topic exchanges and', 'routing keys.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a method that takes a message, and '
            'returns a channel or queue name. [[slnc 300]] Look for '
            "Apache Camel's choice and when, or Spring Integration's "
            'router. [[slnc 300]] Look for RabbitMQ topic exchanges, with '
            'routing keys. [[slnc 300]] And a chain of if statements in '
            'the sender, choosing a queue.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a content-based router when', 'one stream carries messages that', 'need different handling, and the', 'difference is in the content.', 'Order the rules on purpose, always', 'have a fallback that keeps and', 'reports what it cannot route, and', 'prefer routing on a header that', 'the sender sets deliberately over'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a content-based '
            'router when one stream carries messages that need different '
            'handling. [[slnc 300]] And the difference is in the content. '
            '[[slnc 500]] Order the rules on purpose. [[slnc 300]] Always '
            'have a fallback, which keeps and reports what it cannot '
            'route. [[slnc 300]] Prefer routing on a label the sender '
            'sets deliberately, over reaching into the body. [[slnc 300]] '
            'And test every rule, and the order between them.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every result you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If there is only one destination,', 'or the sender already knows where', 'each message goes, a router is a', 'step for nothing.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If there is only one '
            'destination, or the sender already knows where each message '
            'goes, a router is an extra step for nothing.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Content-Based Router. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'content-based router puts all the sorting in one place, and '
            'its price is depending on the content, and rules whose order '
            'matters. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add a rule sending orders over one thousand pounds to '
            'a manual approval channel. [[slnc 300]] And decide where it '
            'belongs in the order of rules. [[slnc 500]] If this helped, '
            'a like really does help other people find it. [[slnc 300]] '
            "And subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
