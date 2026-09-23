"""Scene definitions for the Dead Letter Channel with RabbitMQ teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Dead Letter Channel with RabbitMQ',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Dead Letter '
            'Channel pattern with RabbitMQ, in Java, and it is written '
            'and presented by Jayasekhar Konduru. [[slnc 300]] The plain '
            'definition, in short: a dead letter channel is somewhere for '
            'a message to go when it can never be handled, so that it '
            'stops blocking the messages behind it and a person can look '
            'at it later. Think of a sorting office. A parcel with an '
            'address nobody can read does not sit at the front of the '
            'belt for ever. It is taken off, put on a shelf with a note '
            'saying why, and the belt keeps moving. [[slnc 350]] In our '
            'online store, the belt is a queue of orders, the parcel is '
            'an order whose address nothing can read, and the shelf is a '
            'second queue that a person looks at in the morning. [[slnc '
            '300]] What is new in this video is who makes the decision. '
            'This is the real version of the hand-built one, and here a '
            'real broker takes the order out of the queue, and writes '
            'down its own reason for the death.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Video',
        body=['Dead Letter Channel, the', 'hand-built video, builds all of', 'this in plain Java.', '', 'It has the whole idea: try a few', 'times, then move the message', 'aside with its reason.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video assumes the Dead Letter Channel video. If you '
            'have not seen it, start there. It builds the whole thing in '
            'plain Java, with nothing installed: a worker tries a few '
            'times, then moves the message aside with its reason. [[slnc '
            '300]] This one uses the same online store, and the same '
            'orders. It does not teach the pattern again. It shows what a '
            'real broker does with it.'
        ),
    ),
    dict(
        key='03-words', kind='bullets', title='Three Words First',
        body=['A queue is the line orders wait', 'in.', '', 'An exchange is the sorting desk.', 'You hand it a message, and it', 'decides which queues get a copy.', '', 'Refusing an order is the worker', 'saying it will not finish this', 'one.'],
        narration=(
            'Three words before the first line of code, because RabbitMQ '
            'brings its own vocabulary and it is easier in plain '
            'language. [[slnc 250]] A queue is the line that orders wait '
            'in. [[slnc 200]] An exchange is the sorting desk. You hand a '
            'message to the desk and the desk decides which queues get a '
            'copy. The desk that dead orders are handed to is what '
            'RabbitMQ calls a dead letter exchange. [[slnc 250]] And '
            'refusing an order is the worker telling the broker it will '
            'not finish this one. The worker can refuse it and ask for it '
            'back, which puts it at the head of the line again, or refuse '
            'it for good, which hands it to the desk.'
        ),
    ),
    dict(
        key='04-block', kind='console', title='An Order That Can Never Succeed',
        body="""ONE. No rule on the queue.
  four orders, one with an
  address nothing can read.
  handled: [ORD-1001]
  still waiting: 3
  deliveries of ORD-1002: 11

  the two good orders behind it
  never get their turn.""",
        narration=(
            'First, an order that can never succeed. Four orders go on a '
            'queue with no rule written on it. The second has an address '
            'nothing can read. The worker takes it, fails, refuses it, '
            'and asks for it back, and the broker puts it back at the '
            'head of the line. Over twelve turns, eleven of them go to '
            'that same order. One order was handled, three are still '
            'waiting, and the two good orders behind the bad one never '
            'get their turn.'
        ),
    ),
    dict(
        key='05-rule', kind='console', title='A Rule Written On The Queue',
        body="""TWO. A dead letter channel.
  three deliveries, then refuse
  it for good.
  handled: ORD-1001, ORD-1003,
  ORD-1004
  still waiting: 0   parked: 1
  deliveries in all: 7

  the broker did the moving.""",
        narration=(
            'Second, a rule written on the queue. When the shop declares '
            'the queue it names a desk to send a dead order to, and a '
            'second queue is tied to that desk. The worker gives each '
            'order three deliveries, and on the third failure it refuses '
            'the unreadable one for good. From that moment the worker '
            'does nothing more. The broker takes the order out of the '
            'queue and puts it on the second queue. Three orders were '
            'handled, nothing is waiting, one is parked, and it took '
            'seven deliveries in all. One of those orders had failed once '
            'on a payment gateway timeout, and went through on its second '
            'delivery. A slow day is not a dead order.'
        ),
    ),
    dict(
        key='06-why', kind='console', title='The Broker Writes Down Why',
        body="""THREE. The broker says why.
  ORD-1002: reason rejected
  from queue orders.work
  died 1 time

  the order is kept exactly as
  the shop sent it.""",
        narration=(
            'Third, the broker writes down why. The parked order comes '
            'back with a note attached to it, and the broker wrote that '
            'note, not the application. The note says the queue the order '
            'died in, how many times it has died, which is once, and one '
            'word for the reason, which is rejected. The order itself is '
            'exactly what the shop sent, so a person can read it, and put '
            'it back.'
        ),
    ),
    dict(
        key='07-reasons', kind='console', title='Deaths Nobody Chose',
        body="""FOUR. Two more reasons.
  ORD-1005: reason expired
  a 500 millisecond limit, and
  nobody read it in time.

  ORD-1006: reason maxlen
  the queue held two, a third
  arrived. still waiting: 2.""",
        narration=(
            'Fourth, deaths nobody chose. Two more orders die, and no '
            'worker touches either of them. The first sat in a queue that '
            'was given a time limit of five hundred milliseconds, and '
            'nobody read it in time, so the broker parked it, and its '
            'word for that is expired. The second was in a queue that was '
            'told to hold only two orders, and a third arrived, so the '
            'broker pushed the oldest one out to make room, and its word '
            'for that is maxlen. Two orders are left waiting there. This '
            'is the part the hand-built version cannot show, because in '
            'plain Java nothing but the worker can act.'
        ),
    ),
    dict(
        key='08-replay', kind='console', title='Fix It, And Put It Back',
        body="""FIVE. A replay.
  before: handled 3, parked 1.
  the parser is fixed, and 1 order
  goes back on the queue.
  handled: ORD-1001, ORD-1003,
  ORD-1004, ORD-1002

  a replay does not restore order.""",
        narration=(
            'Fifth, fix it, and put it back. Before the fix, three orders '
            'were handled and one was parked. An operator finds the '
            'cause, fixes the address parser, and publishes the parked '
            'order back onto the working queue, where it goes through. '
            'But notice where it ended up: it was handled last, behind '
            'the two orders that were behind it, because a replay puts a '
            'message at the back of the line. And it goes back as a new '
            'message, so the note the broker wrote is gone unless the '
            'operator copies it across first.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill: Nobody Is Looking',
        body="""SIX. The bill.
  40 orders, half unreadable:
  20 parked, 20 shipped.
  the working queue reports
  0 waiting: it looks healthy.

  11 queues, 1 exchange, and a
  broker to run.""",
        narration=(
            'Last, the bill. Forty orders, half of them unreadable. '
            'Twenty are shipped and twenty are parked, and every one of '
            'those forty was paid for by a customer who was told the '
            'order went through. The working queue reports nothing '
            'waiting, so every dashboard shows the shop perfectly '
            'healthy. The loss is all in the parked queue, and nothing '
            'tells anyone to look at it. That queue needs an owner, an '
            'alert on how deep it is getting, and a limit on how long an '
            'order may stay in it, because every parked order is a copy '
            'of a customer address. And a broker is another thing to run: '
            'this demo declared eleven queues and one exchange in one '
            'container.'
        ),
    ),
    dict(
        key='10-three', kind='bullets', title='The Three Reasons',
        body=['rejected: a worker refused it and', 'did not ask for it back.', '', 'expired: it sat past the time', 'limit on the queue.', '', 'maxlen: the queue was full, and', 'this was the oldest one in it.'],
        narration=(
            'The three reasons in one place, because they are the whole '
            'difference between this video and the hand-built one. '
            '[[slnc 250]] Rejected means a worker refused the message and '
            'did not ask for it back. [[slnc 200]] Expired means it sat '
            'in the queue past the time limit. [[slnc 200]] And maxlen '
            'means the queue was full and this was the oldest message in '
            'it. The worker started the first one. The broker did the '
            'other two on its own.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Write the rule on every queue', 'where a message can fail for ever.', '', 'Try a few times, then refuse it', 'for good. Let the broker move it.', '', 'Read the note it leaves.', '', 'Alert on the depth. Give the queue', 'an owner.'],
        narration=(
            'My verdict, plainly. Write the rule on every queue where a '
            'message can fail for ever. Let the worker try a few times, '
            'for the failures that pass on their own, and then refuse for '
            'good, for the ones that do not. Let the broker do the '
            'moving, because it will still do it when your process has '
            'crashed. Read the note it leaves, because at three in the '
            'morning it is the only account of the death you will have. '
            'Then put an alert on the depth of the parked queue, give the '
            'queue an owner, and decide how long an order may stay in it.'
        ),
    ),
    dict(
        key='12-recognise', kind='bullets', title='How To Recognise It',
        body=['A queue declared with', '`x-dead-letter-exchange`.', '', 'A queue name ending in `.dlq` or', '`.parked`.', '', 'A reject or nack with requeue set', 'to false.', '', 'An `x-death` header being read.'],
        narration=(
            'How do you recognise this in code you did not write? A queue '
            'declared with an argument called x dash dead dash letter '
            'dash exchange. A queue whose name ends in dot d l q, or dot '
            'parked. A consumer calling reject or nack with requeue set '
            'to false. And somewhere, code reading a header called x dash '
            'death out of a message. In Amazon’s queue service the '
            'same thing is called a redrive policy.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['RabbitMQ 4.3.6, in a container.', '', 'The RabbitMQ Java client 5.36.0.', '', 'Testcontainers 2.0.5.', '', 'Docker 24 or later, running.'],
        narration=(
            'For the record. RabbitMQ, four point three point six, in a '
            'container. The RabbitMQ Java client, five point three six '
            'point zero. Testcontainers, two point zero point five. '
            'And Docker, twenty four or later, running before you start.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real broker', 'in a container, real queues, and', 'the broker\'s own reasons.', '', 'The demo starts the container and', 'takes it away again.', '', 'Every wait is a poll on a real', 'condition, never a fixed pause.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything here is real: a real broker in a container, real '
            'queues, and reasons the broker wrote itself. The demo starts '
            'the container and takes it away again, so nothing is '
            'installed and nothing is left running. And every wait in the '
            'code is a poll on a real condition with a time limit, never '
            'a fixed pause, so the same numbers come out on every '
            'machine.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a queue where a message can', 'never be permanently bad, or where', 'losing one costs nothing, this is', 'more to run than it is worth.', '', 'Where a message can be poison, its', 'absence is the outage.'],
        narration=(
            'So when is this too much? For a queue where a message can '
            'never be permanently bad, or where losing one costs nothing, '
            'this is more to run than it is worth. But where a message '
            'can be poison, not having it is the outage.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository.', 'Give the parked queue a time limit of its own, and decide', 'where an order goes when it dies a second time.'],
        narration=(
            "That's the Dead Letter Channel with RabbitMQ. [[slnc 250]] "
            'If you take one sentence away, take this one: the '
            'application writes a rule on the queue, and from then on the '
            'broker decides when a message is dead and writes down why. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, give the '
            'parked queue a time limit of its own, and decide where an '
            'order should go when it dies a second time. [[slnc 300]] If '
            'this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
