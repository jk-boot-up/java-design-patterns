"""Scene definitions for the Content-Based Router with Camel teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, explains each of the broker's and
Camel's words in plain language before using it, and never points at a
picture the listener cannot see.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Content-Based Router with Camel',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Content-Based '
            'Router pattern in Java, using a real routing framework, '
            'Apache Camel, over a real message broker, RabbitMQ. '
            '[[slnc 250]] It is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] Here is the plain definition, in '
            'general words. A content-based router is a sorter that sits '
            'between the people who send messages and the people who '
            'handle them. It reads what is inside each message, and '
            'sends it on to the one place that suits it. The sender does '
            'not choose, and the receivers never see the messages that '
            'are not theirs. [[slnc 350]] Now the same thing in our '
            'online store. Every order lands in one place. A parcel that '
            'must go out today goes to express shipping. A gift card, '
            'with nothing to put in a box, goes to digital delivery. An '
            'order worth a thousand pounds or more goes to a fraud '
            'check first. [[slnc 300]] By the end you will have seen '
            'six orders sorted by what they contain, seen the order of '
            'the questions change the answer, and seen what Camel does '
            'with an order that no question claims. It keeps no count. '
            'It simply lets the order go.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Six orders arrive in one place.', '', 'Parcels to post today.',
              'Parcels that can wait.', 'Gift cards, with nothing to box.',
              'Big orders a person should check.', 'And a subscription.', '',
              'Who decides where each one goes?'],
        narration=(
            'Here is the scenario. Six orders arrive in one place. Some '
            'are parcels that must be posted today. Some are parcels '
            'that can wait. Some are gift cards, with nothing to put in '
            'a box. One is so valuable that a person should check it '
            'before anything ships. And one is a subscription, which is '
            'none of those. [[slnc 300]] The question is who decides '
            'where each order goes, and where that decision lives.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='One Queue For Everything',
        body="""ONE. One queue for everything.
  all 6 orders arrived on the
  warehouse's own queue.

  it shipped 3.
  it could do nothing with 3.

  an if for every kind of order,
  inside the warehouse.""",
        narration=(
            'First, with no router at all. All six orders are put in the '
            'warehouse\'s own line of waiting work. The warehouse can '
            'pack and post the three physical ones. It can do nothing '
            'with the other three: two gift cards and a subscription. '
            '[[slnc 250]] So the warehouse grows an if for every kind of '
            'order, and every new kind of order means changing the '
            'warehouse. The deciding is in the wrong place.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title='The Words, In Plain Language',
        body=['The broker:', '  a queue is a line of waiting messages.',
              '  an exchange is the post box.',
              '  a routing key is the label on it.', '',
              'Camel:', '  a route is the path, written down.',
              '  a predicate is a yes-or-no question.',
              '  otherwise is the branch for no.'],
        narration=(
            'Two tools bring their own words, so here they are in plain '
            'language first. [[slnc 250]] The broker is a separate '
            'program that holds messages. A named line of messages, '
            'waiting until somebody takes them, is called a queue. The '
            'post box a sender drops a message into is called an '
            'exchange. It keeps nothing. It reads the short label on '
            'the message, which is called the routing key, and puts the '
            'message in the matching line. [[slnc 300]] Camel has its '
            'own words. A written description of where messages come '
            'from, what is asked about them, and where they go, is '
            'called a route. A yes-or-no question asked about one '
            'message is called a predicate. And the branch taken when '
            'every question says no is called otherwise. Hold on to '
            'that last one.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='The Route Reads And Chooses',
        body="""TWO. The route chooses.
  ORD-1 physical, express -> express-shipping
  ORD-2 digital           -> digital-delivery
  ORD-3 physical, 1200.00 -> fraud-review
  ORD-4 digital           -> digital-delivery
  ORD-5 subscription      -> manual-review
  ORD-6 physical          -> standard-shipping

  4 questions, in a fixed order.""",
        narration=(
            'Second, a Camel route reads the orders line and asks four '
            'questions, in order. Is the order worth a thousand pounds '
            'or more? Is it digital? Was express delivery paid for? Is '
            'it a physical thing? The first question answered yes '
            'decides. [[slnc 250]] Order one, a parcel paid for express, '
            'goes to express shipping. Orders two and four, both '
            'digital, go to digital delivery. Order three is a parcel '
            'worth twelve hundred pounds, so the value question claims '
            'it first, and it goes to fraud review. Order six, an '
            'ordinary parcel, goes to standard shipping. [[slnc 250]] '
            'And order five, the subscription, is claimed by no '
            'question at all. It takes the otherwise branch, to manual '
            'review, where a person will see it.'
        ),
    ),
    dict(
        key='06-route', kind='diagram', title='The Route, As Written',
        body=None,
        narration=(
            'Here is the route, said in words. It starts at the orders '
            'line. Then comes one choice with four questions under it, '
            'in this order: high value, then digital, then express, '
            'then physical. Each question names one line to post to '
            'when the answer is yes. Last comes the otherwise branch, '
            'naming manual review. [[slnc 300]] That is the whole '
            'router. No sender knows it exists, and no receiver does '
            'either. Each receiver just reads its own line. The '
            'deciding lives in one place, written down, in order.'
        ),
    ),
    dict(
        key='07-three', kind='console', title='The First Yes Wins',
        body="""THREE. The first yes wins.
  a digital gift card worth 1500.00.

  high value asked first:
    fraud-review.
  high value asked last:
    digital-delivery.

  Camel does not warn you.""",
        narration=(
            'Third, the order of the questions. One digital gift card, '
            'worth fifteen hundred pounds, goes through two routes that '
            'ask the same four questions in two different orders. '
            '[[slnc 250]] With the value question asked first, it goes '
            'to fraud review. With the value question asked last, the '
            'digital question is reached first and says yes, so it goes '
            'to digital delivery, and nobody checks it. [[slnc 250]] '
            'Same card, same broker, same questions, a different answer. '
            'The order of the questions is part of the design, and Camel '
            'does not warn you when somebody changes it.'
        ),
    ),
    dict(
        key='08-four', kind='console', title='A Message No Question Claims',
        body="""FOUR. Nothing claims it.
  a subscription order.

  with otherwise:  manual-review.
  no otherwise:
    messages left anywhere: 0.
    the broker was told it was
    handled, so it is gone.
  otherwise named for it: unclaimed.""",
        narration=(
            'Fourth, and this is the heart of the video. A subscription '
            'order. Every one of the four questions says no. [[slnc 250]] '
            'Through the route with an otherwise branch, it arrives in '
            'manual review. [[slnc 250]] Now take the otherwise branch '
            'away. The route simply ends. It tells the broker the order '
            'was handled, and the broker deletes it. The demo then '
            'counts every message on all ten lines in the shop, and the '
            'count is zero. Nothing was logged. Nothing was counted. '
            'Nobody was told. [[slnc 300]] Give the otherwise branch a '
            'line named for the problem, called unclaimed, and the order '
            'lands there. That one line is the whole difference between '
            'an order that is lost and an order somebody knows about.'
        ),
    ),
    dict(
        key='09-otherwise', kind='code', title='The One Line That Keeps It',
        body="""from(inbox())
  .choice()
    .when(HIGH_VALUE).to(to("fraud-review"))
    .when(DIGITAL).to(to("digital-delivery"))
    .when(EXPRESS).to(to("express-shipping"))
    .when(PHYSICAL).to(to("standard-shipping"))
  // without the next line, a no is silence
  .otherwise().to(to("unclaimed"))
  .end();""",
        narration=(
            'In the route itself, the difference is one line. The four '
            'questions each say, when this is true, post it to that '
            'line. The last line says, otherwise, post it to the '
            'unclaimed line. [[slnc 250]] Leave that line out, and Camel '
            'will not complain. The route installs, it starts, it runs, '
            'and every order that no question claims disappears without '
            'a sound. So always write the otherwise branch, and send it '
            'somewhere named for the problem.'
        ),
    ),
    dict(
        key='10-five', kind='console', title='A New Question',
        body="""FIVE. A new question.
  questions before: 4, after: 5.
  senders and queues untouched.

  an EU subscription:
    was manual-review,
    now eu-vat-check.
  ORD-6, physical, from the EU:
    still standard-shipping.""",
        narration=(
            'Fifth, a new question. Orders from inside the European '
            'Union need their tax worked out before they ship, so a '
            'fifth question is added, asked after the other four. The '
            'route goes from four questions to five. No sender was '
            'changed, and no receiving line was changed. Only the route '
            'was. [[slnc 250]] A subscription from the European Union '
            'used to fall through to manual review. It now goes to the '
            'tax check. But order six, a parcel from the European '
            'Union, still goes to standard shipping, because the '
            'physical question is asked earlier and says yes first.'
        ),
    ),
    dict(
        key='11-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  kind=goods instead of physical:
    ORD-9 lands on manual-review,
    quietly.
  the fraud branch is broken:
    tried 3 times,
    router-errors now holds 1.
  1 container, 1 exchange,
  10 queues.""",
        narration=(
            'Last, the bill. Three costs. [[slnc 250]] First, the route '
            'is tied to the wording inside the message. The sender '
            'starts calling parcels goods instead of physical. The '
            'physical question no longer matches, so order nine lands '
            'in manual review, and nobody is told why. [[slnc 300]] '
            'Second, a branch can fail, which is not the same as not '
            'matching. The fraud check is broken, because the service '
            'behind it is not answering. Camel tried it three times, the '
            'first attempt and two retries, and then put the order on '
            'an errors line, which ended up holding one order. Somebody '
            'had to say where failures go. [[slnc 300]] Third, there is '
            'something to run: one container, one exchange and ten '
            'queues.'
        ),
    ),
    dict(
        key='12-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the idea right: questions', 'in order, first yes wins,',
              'a fallback, new rules for free.', '',
              'It left out three things.', '',
              'It counted what it dropped.', 'Camel counts nothing.',
              'Its rules could not fail.', 'And nothing left the process.'],
        narration=(
            'The hand-built partner project got the idea right. '
            'Questions asked in order. The first yes wins. A fallback '
            'for anything unclaimed. A new question added without '
            'touching anybody else. Every one of those lessons is true '
            'of Camel. [[slnc 300]] It left out three things. When it '
            'had no fallback, it dropped the order and counted it, so '
            'the loss was a number you could see. Camel counts nothing, '
            'and the order is simply gone. Its questions could only say '
            'yes or no, and could never fail. And the order never left '
            'the program. Here it really travels, through a broker, '
            'from one program to another.'
        ),
    ),
    dict(
        key='13-recognise', kind='bullets', title='How To Recognise It',
        body=['A choice with when and otherwise.', '',
              'A choice with no otherwise.', '',
              'A queue called manual-review,', 'parking-lot or unroutable.', '',
              'An if chain inside a listener,', 'picking the next service.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'choice step with a list of when questions and an '
            'otherwise at the end. Worse, a choice with no otherwise at '
            'all, which is a place orders can vanish. A line of waiting '
            'messages with a name like manual review, parking lot or '
            'unroutable, which is somebody\'s otherwise branch. And an '
            'if chain inside a message handler, deciding which service '
            'to call next, which is the same router with no name.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Route on content when one stream', 'carries several kinds of work.', '',
              'Put the questions in order on', 'purpose, and test that order.', '',
              'Always write otherwise, and send', 'it somewhere named for it.', '',
              'Always say where failures go.'],
        narration=(
            'Here is my verdict, plainly. Use a content-based router '
            'when one stream of messages carries several kinds of work, '
            'and the difference is inside the message. [[slnc 250]] Put '
            'the questions in order on purpose, and write a test for '
            'that order, because nothing warns you when it changes. '
            'Always write the otherwise branch, and send it somewhere '
            'named for the problem. And always say where a failing '
            'message goes, because a branch that fails is not a branch '
            'that did not match.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['RabbitMQ 4.3.6 in a container', 'the demo starts and removes.',
              'Apache Camel 4.20.0.', '',
              'Every number is the program\'s', 'own output, the same twice.', '',
              'Two stable rules in one program?', 'The hand-built version is',
              'smaller, and needs no broker.'],
        narration=(
            'What is real here? A RabbitMQ broker, version four point '
            'three point six, running in a container that the demo '
            'starts and removes by itself. Apache Camel, version four '
            'point twenty. You need a container runtime such as Docker '
            'running, and if it is not, the demo tells you so in two '
            'plain sentences. [[slnc 250]] Every number in this video '
            'comes from the program\'s own output, and two runs one '
            'after the other print the same thing. [[slnc 300]] And '
            'when is this too much? If the routing is two or three '
            'stable rules inside one program, the hand-built version is '
            'smaller and clearer, and needs no broker at all.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Content-Based Router with Camel. [[slnc 250]] If you "
            'take one sentence away, take this one: a message that no '
            'question claims is kept only if the route says where to '
            'keep it. [[slnc 350]] The full source, the written notes, '
            'the diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, take the '
            'error handler out of the broken fraud check, run it again, '
            'and find out where the order went. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, '
            'and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
