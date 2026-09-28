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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Content-Based Router pattern, in Java, using Apache Camel, '
            'with a real message broker called RabbitMQ. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A content-based '
            'router is a sorter, sitting between the people who send '
            'messages and the people who handle them. [[slnc 300]] It '
            'reads what is inside each message, and sends it to the one '
            'place that suits it. [[slnc 300]] The sender does not '
            'choose. [[slnc 300]] And the receivers never see messages '
            'that are not theirs. [[slnc 600]] Now, our online store. '
            '[[slnc 300]] Every order lands in one place. [[slnc 300]] A '
            'parcel that must go out today goes to express shipping. '
            '[[slnc 300]] A gift card, with nothing to box, goes to '
            'digital delivery. [[slnc 300]] And an order worth a thousand '
            'pounds or more goes to a fraud check first. [[slnc 500]] By '
            'the end, you will hear six orders sorted by what they '
            'contain. [[slnc 300]] You will hear the order of the '
            'questions change the answer. [[slnc 300]] And you will hear '
            'what Camel does with an order that no question claims. '
            '[[slnc 300]] It keeps no count. [[slnc 300]] It simply lets '
            'the order go.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Six orders arrive in one place.', '', 'Parcels to post today.',
              'Parcels that can wait.', 'Gift cards, with nothing to box.',
              'Big orders a person should check.', 'And a subscription.', '',
              'Who decides where each one goes?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Six orders arrive in one '
            'place. [[slnc 300]] Some are parcels that must be posted '
            'today. [[slnc 300]] Some are parcels that can wait. [[slnc '
            '300]] Some are gift cards, with nothing to put in a box. '
            '[[slnc 300]] One is so valuable that a person should check '
            'it before anything ships. [[slnc 300]] And one is a '
            'subscription, which is none of those. [[slnc 500]] So here '
            'is the question. [[slnc 300]] Who decides where each order '
            'goes, and where does that decision live?'
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
            'First, with no router at all. [[slnc 400]] All six orders go '
            "into the warehouse's own queue of work. [[slnc 500]] The "
            'warehouse can pack and post the three physical orders. '
            '[[slnc 300]] But it can do nothing with the other three: two '
            'gift cards, and a subscription. [[slnc 500]] So the '
            'warehouse grows an if statement for every kind of order. '
            '[[slnc 300]] And every new kind of order means changing the '
            'warehouse. [[slnc 300]] The deciding is in the wrong place.'
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
            'The two tools bring their own words, so here they are in '
            'plain language. [[slnc 500]] The broker is a separate '
            'program that holds messages. [[slnc 300]] A named line of '
            'messages, waiting to be taken, is called a queue. [[slnc '
            '300]] The post box a sender drops a message into is called '
            'an exchange. [[slnc 300]] It keeps nothing. [[slnc 300]] It '
            'reads a short label on the message, called the routing key, '
            'and puts the message in the matching queue. [[slnc 600]] '
            'Camel has its own words too. [[slnc 300]] A written '
            'description of where messages come from, what is asked about '
            'them, and where they go, is called a route. [[slnc 300]] A '
            'yes-or-no question about one message is called a predicate. '
            '[[slnc 300]] And the branch taken when every question says '
            'no is called otherwise. [[slnc 300]] Remember that last one.'
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
            'Second demo: the route reads, and chooses. [[slnc 400]] A '
            'Camel route reads the orders queue, and asks four questions, '
            'in order. [[slnc 300]] Is the order worth a thousand pounds '
            'or more? [[slnc 200]] Is it digital? [[slnc 200]] Was '
            'express delivery paid for? [[slnc 200]] Is it a physical '
            'thing? [[slnc 300]] The first question answered yes decides. '
            '[[slnc 600]] Order one, a parcel with express delivery, goes '
            'to express shipping. [[slnc 300]] Orders two and four, both '
            'digital, go to digital delivery. [[slnc 300]] Order three is '
            'a parcel worth twelve hundred pounds. [[slnc 300]] So the '
            'value question claims it first, and it goes to fraud review. '
            '[[slnc 300]] Order six, an ordinary parcel, goes to standard '
            'shipping. [[slnc 500]] And order five, the subscription, is '
            'claimed by no question. [[slnc 300]] It takes the otherwise '
            'branch, to manual review, where a person will see it.'
        ),
    ),
    dict(
        key='06-route', kind='diagram', title='The Route, As Written',
        body=None,
        narration=(
            'Here is the route, described in words. [[slnc 400]] It '
            'starts at the orders queue. [[slnc 300]] Then comes one '
            'choice, with four questions, in this order. [[slnc 300]] '
            'High value, then digital, then express, then physical. '
            '[[slnc 300]] Each question names one queue to send to, when '
            'the answer is yes. [[slnc 300]] Last comes the otherwise '
            'branch, naming manual review. [[slnc 600]] That is the whole '
            'router. [[slnc 300]] No sender knows it exists. [[slnc 300]] '
            'And no receiver does either. [[slnc 300]] Each receiver just '
            'reads its own queue. [[slnc 300]] The deciding lives in one '
            'place, written down, in order.'
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
            'Third demo: the first yes wins. [[slnc 400]] One digital '
            'gift card, worth fifteen hundred pounds, goes through two '
            'routes. [[slnc 300]] Both ask the same four questions, but '
            'in different orders. [[slnc 500]] With the value question '
            'asked first, it goes to fraud review. [[slnc 500]] With the '
            'value question asked last, the digital question is reached '
            'first, and says yes. [[slnc 300]] So it goes to digital '
            'delivery, and nobody checks it. [[slnc 500]] The same card, '
            'the same broker, the same questions, and a different answer. '
            '[[slnc 300]] The order of the questions is part of the '
            'design. [[slnc 300]] And Camel does not warn you when '
            'someone changes it.'
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
            'Fourth demo, and the heart of this video: a message no '
            'question claims. [[slnc 400]] A subscription order arrives. '
            '[[slnc 300]] Every one of the four questions says no. [[slnc '
            '500]] Through the route with an otherwise branch, it arrives '
            'in manual review. [[slnc 600]] Now take the otherwise branch '
            'away. [[slnc 300]] The route simply ends. [[slnc 300]] It '
            'tells the broker the order was handled, and the broker '
            'deletes it. [[slnc 500]] The demo counts every message, on '
            'all ten queues in the shop. [[slnc 300]] The count is zero. '
            '[[slnc 300]] Nothing was logged. [[slnc 200]] Nothing was '
            'counted. [[slnc 200]] Nobody was told. [[slnc 600]] Now give '
            'the otherwise branch a queue named after the problem: '
            'unclaimed. [[slnc 300]] And the order lands there. [[slnc '
            '500]] That one line is the whole difference between an order '
            'that is lost, and an order somebody knows about.'
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
            'In the route itself, the difference is one line. [[slnc '
            '400]] The four questions each say: when this is true, send '
            'it to that queue. [[slnc 300]] The last line says: '
            'otherwise, send it to the unclaimed queue. [[slnc 500]] '
            'Leave that line out, and Camel will not complain. [[slnc '
            '300]] The route installs, starts, and runs. [[slnc 300]] And '
            'every order that no question claims disappears, without a '
            'sound. [[slnc 500]] So always write the otherwise branch. '
            '[[slnc 300]] And send it somewhere named for the problem.'
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
            'Fifth demo: a new question. [[slnc 400]] Orders from the '
            'European Union need their tax worked out before they ship. '
            '[[slnc 300]] So a fifth question is added, after the other '
            'four. [[slnc 500]] The route goes from four questions to '
            'five. [[slnc 300]] No sender was changed. [[slnc 300]] No '
            'receiving queue was changed. [[slnc 300]] Only the route. '
            '[[slnc 500]] A European subscription used to fall through to '
            'manual review. [[slnc 300]] Now it goes to the tax check. '
            '[[slnc 500]] But order six, a European parcel, still goes to '
            'standard shipping. [[slnc 300]] Because the physical '
            'question is asked earlier, and says yes first.'
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
            'Finally, the costs, and there are three. [[slnc 500]] First, '
            'the route depends on the wording inside the message. [[slnc '
            '300]] The sender starts calling parcels goods, instead of '
            'physical. [[slnc 300]] The physical question no longer '
            'matches. [[slnc 300]] So order nine lands in manual review, '
            'and nobody is told why. [[slnc 600]] Second, a branch can '
            'fail, which is not the same as not matching. [[slnc 300]] '
            'The fraud check is broken, because the service behind it is '
            'not answering. [[slnc 300]] Camel tries three times, and '
            'then puts the order on an errors queue. [[slnc 300]] Someone '
            'had to decide where failures go. [[slnc 600]] Third, there '
            'is more to run. [[slnc 300]] One container, one exchange, '
            'and ten queues.'
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
            'The hand-built partner project got the main ideas right. '
            '[[slnc 400]] Questions asked in order. [[slnc 200]] The '
            'first yes wins. [[slnc 200]] A fallback for anything '
            'unclaimed. [[slnc 200]] And new questions, added without '
            'touching anyone else. [[slnc 300]] All of that is true of '
            'Camel too. [[slnc 600]] But it left out three things. [[slnc '
            '400]] With no fallback, it dropped the order, but counted '
            'it. [[slnc 300]] So the loss was a number you could see. '
            '[[slnc 300]] Camel counts nothing, and the order is simply '
            'gone. [[slnc 500]] Its questions could only say yes or no, '
            'and could never fail. [[slnc 500]] And its orders never left '
            'the program. [[slnc 300]] Here, they really travel through a '
            'broker, from one program to another.'
        ),
    ),
    dict(
        key='13-recognise', kind='bullets', title='How To Recognise It',
        body=['A choice with when and otherwise.', '',
              'A choice with no otherwise.', '',
              'A queue called manual-review,', 'parking-lot or unroutable.', '',
              'An if chain inside a listener,', 'picking the next service.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a choice step, with a list of when '
            'questions, and an otherwise at the end. [[slnc 300]] Worse, '
            'a choice with no otherwise at all, which is a place orders '
            'can vanish. [[slnc 300]] Look for a queue named manual '
            'review, parking lot, or unroutable. [[slnc 300]] That is '
            "somebody's otherwise branch. [[slnc 300]] And look for a "
            'chain of if statements inside a message handler, deciding '
            'which service to call next. [[slnc 300]] That is the same '
            'router, without a name.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Route on content when one stream', 'carries several kinds of work.', '',
              'Put the questions in order on', 'purpose, and test that order.', '',
              'Always write otherwise, and send', 'it somewhere named for it.', '',
              'Always say where failures go.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a content-based '
            'router when one stream of messages carries several kinds of '
            'work, and the difference is inside the message. [[slnc 500]] '
            'Put the questions in order on purpose. [[slnc 300]] And '
            'write a test for that order, because nothing warns you when '
            'it changes. [[slnc 500]] Always write the otherwise branch, '
            'and send it somewhere named for the problem. [[slnc 500]] '
            'And always say where a failing message goes. [[slnc 300]] '
            'Because a branch that fails is not the same as a branch that '
            'did not match.'
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
            'A quick, honest note about this demo. [[slnc 400]] The '
            'RabbitMQ broker is real, version four point three point six. '
            '[[slnc 300]] It runs in a container that the demo starts and '
            'removes by itself. [[slnc 300]] Apache Camel is real too, '
            'version four point twenty. [[slnc 300]] You need Docker '
            'running. [[slnc 300]] If it is not, the demo says so, in two '
            'plain sentences. [[slnc 500]] Every number you heard comes '
            "from the program's own output. [[slnc 300]] And two runs, "
            'one after the other, print the same results. [[slnc 600]] '
            'So, when is this too much? [[slnc 300]] If the routing is '
            'two or three stable rules inside one program, the hand-built '
            'version is smaller, and clearer. [[slnc 300]] And it needs '
            'no broker at all.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's the Content-Based Router, with Camel. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] A '
            'message that no question claims is only kept if the route '
            'says where to keep it. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Remove the error handler from the broken fraud '
            'check, and run it again. [[slnc 300]] Then find out where '
            'the order went. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
