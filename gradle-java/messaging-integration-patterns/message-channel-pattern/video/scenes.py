"""Scene definitions for the Message Channel teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Message Channel',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Message Channel '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'message channel is a named queue that carries messages from '
            'a sender to a receiver, so the two systems can talk without '
            'needing to be up at the same moment. [[slnc 350]] This is '
            'another project in the messaging and integration category, '
            'whose subject is how separate systems exchange messages '
            'safely. In our online store, the two systems that must talk '
            'are checkout and the warehouse. [[slnc 300]] By the end you '
            'will see checkout fail while the warehouse is down, see a '
            'channel let it carry on, see the messages wait and arrive in '
            'order, see an envelope, see a channel carry one kind of '
            'message, and see the bill, which is that the sender no '
            'longer hears the answer.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order is placed, checkout', 'tells the warehouse to pick it.', '', 'The warehouse system is taken down', 'for maintenance now and then.', '', 'Should checkout fail then?'],
        narration=(
            'Here is the scenario. When an order is placed, checkout must '
            'tell the warehouse to pick it. The warehouse system is taken '
            'down for maintenance every so often. [[slnc 300]] The '
            'question: should checkout fail while it is down?'
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
            'First, checkout calls the warehouse. The warehouse system is '
            'down for maintenance. Three orders are placed, and all three '
            'checkouts fail. The shop cannot sell while another system is '
            'away, though selling does not need the warehouse to answer '
            'yet.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A named queue between the', 'sender and the receiver.', '', 'The sender puts a message in, and', 'carries on.', '', 'The receiver takes it out when it', 'is ready.', '', 'Neither waits for the other.'],
        narration=(
            'The pattern. A named queue between the sender and the '
            'receiver. The sender puts a message in, and carries on. The '
            'receiver takes it out when it is ready. Neither waits for '
            'the other.'
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
            'Second, a channel between them. Checkout sends three '
            'messages, and carries on. Three are waiting in the channel. '
            'The warehouse takes them, each once, in the order they were '
            'sent.'
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
            'Third, the receiver is away. The warehouse is down. Checkout '
            'sends three messages, and none fail. Three are waiting. When '
            'the warehouse comes back, it works through them, in order. '
            'The shop kept selling while the warehouse was away.'
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
            'Fourth, an envelope. A message has headers, such as its '
            'priority, and which order it concerns, that can be read '
            'without opening the body. It has a type, and then a body. A '
            'router or a receiver can decide what to do from the envelope '
            'alone.'
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
            'Fifth, one channel, one kind of message. The pick orders '
            'channel carries pick orders. A refund request sent to it is '
            'refused. A receiver of pick orders never has to ask what it '
            'was given.'
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
            'Last, the bill. The warehouse stays down, and a channel of '
            'five fills: five accepted, three refused. A channel must '
            'have a limit, and somebody must decide what to do when it is '
            'reached. And the sender no longer learns whether the order '
            'was picked. It learns only that the message was accepted. '
            'Sent five, received none: that difference is work nobody has '
            'done yet.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A queue name in a configuration', 'file, such as pick-orders.', '', 'A send call that returns at once,', 'and a separate receive loop.', '', 'JMS destinations, SQS queues,', 'RabbitMQ queues, Kafka topics.'],
        narration=(
            'How do you recognise this in code you did not write? A queue '
            'name in a configuration file, such as pick-orders. A send '
            'call that returns at once, and a separate receive loop. JMS '
            'destinations, SQS queues, RabbitMQ queues, Kafka topics. A '
            'message class with headers and a payload.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a channel between systems that', 'are not always up together, or', 'that work at different speeds.', 'Give it a type, a limit and a', 'name. Put the routing information', 'in the envelope. Decide what', 'happens when it is full, and how', 'the sender finds out the result,', 'since it will not hear it from the'],
        narration=(
            'Here is my verdict, plainly. Use a channel between systems '
            'that are not always up together, or that work at different '
            'speeds. Give it a type, a limit and a name. Put the routing '
            'information in the envelope. Decide what happens when it is '
            'full, and how the sender finds out the result, since it will '
            'not hear it from the call.'
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
        body=['If both systems are always up and', 'the caller needs the answer now, a', 'direct call is simpler. A channel', 'is for decoupling in time.'],
        narration=(
            'So when is it too much? If both systems are always up and '
            'the caller needs the answer now, a direct call is simpler. A '
            'channel is for decoupling in time.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Message Channel. [[slnc 250]] If you take one "
            'sentence away, take this one: a message channel lets two '
            'systems talk without waiting for each other, and the price '
            'is that the sender never hears the answer. [[slnc 350]] The '
            'full source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, make the channel drop the oldest '
            'message when it is full, and decide what that costs. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
