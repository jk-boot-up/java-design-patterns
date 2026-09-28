"""Scene definitions for the Message Channel teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Message Channel',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Message Channel pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A message channel is a named '
            'queue that carries messages from a sender to a receiver. '
            '[[slnc 300]] So the two systems can talk, without needing to '
            'be running at the same moment. [[slnc 600]] Think of a '
            'letterbox. [[slnc 300]] The postman drops a letter in, even '
            'when you are out. [[slnc 300]] And you read it when you come '
            'home. [[slnc 700]] In our online store, the two systems that '
            'must talk are checkout, and the warehouse. [[slnc 500]] In '
            'this video, checkout fails while the warehouse is down. '
            '[[slnc 300]] Then a channel lets it carry on. [[slnc 300]] '
            'We will hear messages wait and arrive in order, an envelope, '
            'a channel that carries one kind of message, and then the '
            'cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order is placed, checkout', 'tells the warehouse to pick it.', '', 'The warehouse system is taken down', 'for maintenance now and then.', '', 'Should checkout fail then?'],
        narration=(
            'Here is the scenario. [[slnc 400]] When an order is placed, '
            'checkout must tell the warehouse to pick it. [[slnc 400]] '
            'But the warehouse system is taken down for maintenance every '
            'so often. [[slnc 500]] So here is the question. [[slnc 300]] '
            'Should checkout fail while the warehouse is down?'
        ),
    ),
    dict(
        key='03-direct', kind='console', title='Checkout Calls The Warehouse',
        body="""ONE. A direct call.
  the warehouse is down.
  3 orders placed.
  checkouts that failed: 3.

  the shop cannot sell while
  another system is away.""",
        narration=(
            'First, the naive way: checkout calls the warehouse directly. '
            '[[slnc 400]] The warehouse is down for maintenance. [[slnc '
            '300]] Three orders are placed. [[slnc 300]] And all three '
            'checkouts fail. [[slnc 500]] The shop cannot sell while '
            'another system is away. [[slnc 300]] Even though selling '
            'does not need the warehouse to answer yet.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A named queue between the', 'sender and the receiver.', '', 'The sender puts a message in, and', 'carries on.', '', 'The receiver takes it out when it', 'is ready.', '', 'Neither waits for the other.'],
        narration=(
            'Now, the pattern. [[slnc 400]] A named queue sits between '
            'the sender and the receiver. [[slnc 300]] The sender puts a '
            'message in, and carries on. [[slnc 300]] The receiver takes '
            'it out when it is ready. [[slnc 500]] Neither waits for the '
            'other.'
        ),
    ),
    dict(
        key='05-chan', kind='console', title='A Channel Between Them',
        body="""TWO. A channel.
  checkout sends 3 and carries
  on. 3 waiting.

  the warehouse takes each
  once, in order.""",
        narration=(
            'Second demo: a channel between them. [[slnc 400]] Checkout '
            'sends three messages, and carries on. [[slnc 300]] Three '
            'messages are waiting in the channel. [[slnc 500]] Then the '
            'warehouse takes them. [[slnc 300]] Each one exactly once, in '
            'the order they were sent.'
        ),
    ),
    dict(
        key='06-away', kind='console', title='The Receiver Is Away',
        body="""THREE. Receiver away.
  the warehouse is down.
  checkout sends 3: none fail.
  waiting: 3.

  the warehouse returns and
  works through them, in order.""",
        narration=(
            'Third demo: the receiver is away. [[slnc 400]] The warehouse '
            'is down. [[slnc 300]] Checkout sends three messages. [[slnc '
            '300]] And none of them fail. [[slnc 500]] Three are waiting '
            'in the channel. [[slnc 300]] When the warehouse comes back, '
            'it works through them, in order. [[slnc 500]] The shop kept '
            'selling, while the warehouse was away.'
        ),
    ),
    dict(
        key='07-env', kind='console', title='An Envelope',
        body="""FOUR. An envelope.
  headers: correlation ORD-1,
  priority express.
  type: PickOrder.
  body: 2 x MUG-BLUE.

  decide from the envelope.""",
        narration=(
            'Fourth demo: an envelope. [[slnc 400]] A message is like a '
            'letter in an envelope. [[slnc 300]] On the outside are '
            'headers, like its priority, express, and which order it '
            'concerns. [[slnc 300]] These can be read without opening it. '
            '[[slnc 500]] It also has a type: pick order. [[slnc 300]] '
            'And inside is the body: two blue mugs. [[slnc 500]] A '
            'router, or a receiver, can decide what to do from the '
            'envelope alone.'
        ),
    ),
    dict(
        key='08-type', kind='console', title='One Channel, One Kind Of Message',
        body="""FIVE. One kind.
  pick-orders carries PickOrder.
  a RefundRequest is refused.

  a receiver never has to ask
  what it was given.""",
        narration=(
            'Fifth demo: one channel, one kind of message. [[slnc 400]] '
            'The pick orders channel only carries pick orders. [[slnc '
            '300]] A refund request sent to it is refused. [[slnc 500]] '
            'So a receiver of pick orders never has to wonder what it was '
            'given.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  the warehouse stays down.
  a channel of 5: 5 accepted,
  3 refused.

  the sender does not learn
  whether it was picked.
  sent 5, received 0.""",
        narration=(
            'Finally, the costs. [[slnc 400]] The warehouse stays down, '
            'and a channel that holds five fills up. [[slnc 300]] Five '
            'messages are accepted, and three are refused. [[slnc 500]] '
            'So a channel needs a limit. [[slnc 300]] And someone must '
            'decide what happens when it is full. [[slnc 500]] And the '
            'sender no longer learns whether the order was picked. [[slnc '
            '300]] It only learns that the message was accepted. [[slnc '
            '500]] Five sent, and none received yet. [[slnc 300]] That '
            'difference is work that nobody has done yet.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A queue name in a configuration', 'file, such as pick-orders.', '', 'A send call that returns at once,', 'and a separate receive loop.', '', 'JMS destinations, SQS queues,', 'RabbitMQ queues, Kafka topics.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a queue name in a settings file, such '
            'as pick orders. [[slnc 300]] Look for a send call that '
            'returns at once, and a separate loop that receives. [[slnc '
            '300]] Look for message queue products, like Amazon S Q S, '
            'RabbitMQ queues, or Kafka topics. [[slnc 300]] And a message '
            'class with headers and a body.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a channel between systems that', 'are not always up together, or', 'that work at different speeds.', 'Give it a type, a limit and a', 'name. Put the routing information', 'in the envelope. Decide what', 'happens when it is full, and how', 'the sender finds out the result,', 'since it will not hear it from the'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a channel between '
            'systems that are not always running at the same time. [[slnc '
            '300]] Or that work at different speeds. [[slnc 500]] Give it '
            'a type, a limit, and a name. [[slnc 300]] Put the routing '
            'information on the envelope. [[slnc 300]] Decide what '
            'happens when it is full. [[slnc 500]] And decide how the '
            'sender finds out the result. [[slnc 300]] Because it will '
            'not hear it from the call.'
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
        body=['If both systems are always up and', 'the caller needs the answer now, a', 'direct call is simpler. A channel', 'is for decoupling in time.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If both systems are '
            'always running, and the caller needs the answer right now, a '
            'direct call is simpler. [[slnc 400]] A channel is for '
            'letting systems work at different times.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Message Channel pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'message channel lets two systems talk without waiting for '
            'each other, and the price is that the sender never hears the '
            'answer. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Make the channel drop its oldest message when it is '
            'full. [[slnc 300]] And decide what that costs. [[slnc 500]] '
            'If this helped, a like really does help other people find '
            "it. [[slnc 300]] And subscribe, if you'd like the rest of "
            'the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
