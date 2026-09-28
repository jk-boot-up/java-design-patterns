"""Scene definitions for the Dead Letter Channel with RabbitMQ teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Dead Letter Channel with RabbitMQ',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Dead Letter Channel pattern, in Java, using RabbitMQ. [[slnc '
            '300]] This video is presented by Jayasekhar Konduru. [[slnc '
            '600]] First, a simple definition. [[slnc 300]] A dead letter '
            'channel is somewhere for a message to go when it can never '
            'be handled. [[slnc 300]] So it stops blocking the messages '
            'behind it, and a person can look at it later. [[slnc 600]] '
            'Think of a sorting office. [[slnc 300]] A parcel with an '
            'address nobody can read does not sit at the front of the '
            'belt forever. [[slnc 300]] It is taken off, put on a shelf '
            'with a note saying why, and the belt keeps moving. [[slnc '
            '700]] In our online store, the belt is a queue of orders. '
            '[[slnc 300]] The parcel is an order whose address cannot be '
            'read. [[slnc 300]] And the shelf is a second queue that a '
            'person checks in the morning. [[slnc 500]] What is new here '
            'is who decides. [[slnc 300]] A real broker takes the order '
            'off the queue, and writes down its own reason.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Video',
        body=['Dead Letter Channel, the', 'hand-built video, builds all of', 'this in plain Java.', '', 'It has the whole idea: try a few', 'times, then move the message', 'aside with its reason.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Dead Letter Channel video. [[slnc '
            '400]] That one builds the whole idea in plain Java, with '
            'nothing installed. [[slnc 300]] A worker tries a few times, '
            'then moves the message aside, with its reason. [[slnc 500]] '
            'Here, we use the same online store, and the same orders. '
            '[[slnc 300]] We will not teach the pattern again. [[slnc '
            '300]] Instead, we hear what a real broker does with it.'
        ),
    ),
    dict(
        key='03-words', kind='bullets', title='Three Words First',
        body=['A queue is the line orders wait', 'in.', '', 'An exchange is the sorting desk.', 'You hand it a message, and it', 'decides which queues get a copy.', '', 'Refusing an order is the worker', 'saying it will not finish this', 'one.'],
        narration=(
            'First, three words, in plain language. [[slnc 500]] A queue '
            'is the line that orders wait in. [[slnc 400]] An exchange is '
            'the sorting desk. [[slnc 300]] You hand a message to the '
            'desk, and it decides which queues get a copy. [[slnc 300]] '
            'The desk that dead orders are handed to is called a dead '
            'letter exchange. [[slnc 500]] And refusing an order is the '
            'worker telling the broker it will not finish this one. '
            '[[slnc 300]] The worker can refuse it and ask for it back, '
            'which puts it at the front of the line again. [[slnc 300]] '
            'Or it can refuse it for good, which hands it to the dead '
            'letter desk.'
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
            'First demo: an order that can never succeed. [[slnc 400]] '
            'Four orders go onto a queue with no rule. [[slnc 300]] The '
            'second one has an address that cannot be read. [[slnc 500]] '
            'The worker takes it, fails, refuses it, and asks for it '
            'back. [[slnc 300]] And the broker puts it back at the front '
            'of the line. [[slnc 500]] Over twelve turns, eleven go to '
            'that same bad order. [[slnc 300]] One order is handled, and '
            'three are still waiting. [[slnc 300]] The two good orders '
            'behind the bad one never get a turn.'
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
            'Second demo: a rule written on the queue. [[slnc 400]] When '
            'the shop creates the queue, it names a desk for dead orders. '
            '[[slnc 300]] And a second queue is connected to that desk. '
            '[[slnc 500]] The worker gives each order three tries. [[slnc '
            '300]] On the third failure, it refuses the unreadable order '
            'for good. [[slnc 300]] From that moment, the worker does '
            'nothing more. [[slnc 300]] The broker moves the order to the '
            'second queue. [[slnc 500]] Three orders are handled. [[slnc '
            '300]] Nothing is waiting. [[slnc 300]] One order is parked. '
            '[[slnc 500]] One of the handled orders had failed once, on a '
            'payment timeout, and went through on its second try. [[slnc '
            '300]] A slow moment is not a dead order.'
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
            'Third demo: the broker writes down why. [[slnc 400]] The '
            'parked order comes back with a note attached. [[slnc 300]] '
            'And the broker wrote that note, not the application. [[slnc '
            '500]] It says which queue the order died in, and that it has '
            'died once. [[slnc 300]] And it gives one word for the '
            'reason: rejected. [[slnc 500]] The order itself is exactly '
            'what the shop sent. [[slnc 300]] So a person can read it, '
            'and put it back.'
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
            'Fourth demo: deaths nobody chose. [[slnc 400]] Two more '
            'orders die, and no worker touches either one. [[slnc 500]] '
            'The first sat in a queue with a time limit of half a second. '
            '[[slnc 300]] Nobody read it in time, so the broker parked '
            'it. [[slnc 300]] Its reason word is: expired. [[slnc 500]] '
            'The second was in a queue told to hold only two orders. '
            '[[slnc 300]] A third arrived, so the broker pushed the '
            'oldest one out, to make room. [[slnc 300]] Its reason word '
            'is: max length. [[slnc 500]] This is what the hand-built '
            'version cannot show. [[slnc 300]] In plain Java, only the '
            'worker can act.'
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
            'Fifth demo: fix it, and put it back. [[slnc 400]] Before the '
            'fix, three orders are handled, and one is parked. [[slnc '
            '500]] An operator finds the cause, and fixes the address '
            'reader. [[slnc 300]] Then sends the parked order back onto '
            'the working queue. [[slnc 300]] And it goes through. [[slnc '
            '500]] But notice where it ended up: handled last, behind the '
            'two orders that were behind it. [[slnc 300]] A replay goes '
            'to the back of the line. [[slnc 500]] And it goes back as a '
            "new message. [[slnc 300]] So the broker's note is lost, "
            'unless the operator copies it across first.'
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
            'Finally, the cost: nobody is looking. [[slnc 400]] Forty '
            'orders, and half of them cannot be read. [[slnc 300]] Twenty '
            'are shipped, and twenty are parked. [[slnc 300]] And all '
            'forty customers were told their order went through. [[slnc '
            '500]] The working queue shows nothing waiting. [[slnc 300]] '
            'So every dashboard shows a perfectly healthy shop. [[slnc '
            '500]] The loss is all in the parked queue. [[slnc 300]] And '
            'nothing tells anyone to look at it. [[slnc 500]] That queue '
            'needs an owner, an alert as it fills up, and a limit on how '
            'long an order may stay. [[slnc 300]] Because every parked '
            "order is a copy of a customer's address. [[slnc 500]] And a "
            'broker is one more thing to run.'
        ),
    ),
    dict(
        key='10-three', kind='bullets', title='The Three Reasons',
        body=['rejected: a worker refused it and', 'did not ask for it back.', '', 'expired: it sat past the time', 'limit on the queue.', '', 'maxlen: the queue was full, and', 'this was the oldest one in it.'],
        narration=(
            'Here are the three reasons, together, because they are the '
            'whole difference from the hand-built video. [[slnc 500]] '
            'Rejected means a worker refused the message, and did not ask '
            'for it back. [[slnc 300]] Expired means it waited in the '
            'queue past its time limit. [[slnc 300]] And max length means '
            'the queue was full, and this was the oldest message in it. '
            '[[slnc 500]] The worker caused the first one. [[slnc 300]] '
            'The broker did the other two on its own.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Write the rule on every queue', 'where a message can fail for ever.', '', 'Try a few times, then refuse it', 'for good. Let the broker move it.', '', 'Read the note it leaves.', '', 'Alert on the depth. Give the queue', 'an owner.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Write the rule on '
            'every queue where a message could fail forever. [[slnc 500]] '
            'Let the worker try a few times, for failures that pass on '
            'their own. [[slnc 300]] Then refuse for good, for the ones '
            'that do not. [[slnc 500]] Let the broker do the moving. '
            '[[slnc 300]] It will still do it even if your program has '
            'crashed. [[slnc 500]] Read the note the broker leaves. '
            '[[slnc 300]] In the middle of the night, it may be the only '
            'record of what happened. [[slnc 500]] Then add an alert as '
            'the parked queue fills, give it an owner, and decide how '
            'long an order may stay.'
        ),
    ),
    dict(
        key='12-recognise', kind='bullets', title='How To Recognise It',
        body=['A queue declared with', '`x-dead-letter-exchange`.', '', 'A queue name ending in `.dlq` or', '`.parked`.', '', 'A reject or nack with requeue set', 'to false.', '', 'An `x-death` header being read.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a queue created with a dead letter '
            'exchange setting. [[slnc 300]] Look for a queue whose name '
            'ends in D L Q, or parked. [[slnc 300]] Look for a worker '
            'that refuses a message, with requeue set to false. [[slnc '
            '300]] And look for code reading a message header called x '
            "death. [[slnc 500]] In Amazon's queue service, the same idea "
            'is called a redrive policy.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['RabbitMQ 4.3.6, in a container.', '', 'The RabbitMQ Java client 5.36.0.', '', 'Testcontainers 2.0.5.', '', 'Docker 24 or later, running.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] RabbitMQ '
            'four point three point six, in a container. [[slnc 300]] The '
            'RabbitMQ Java client, five point thirty-six. [[slnc 300]] '
            'Testcontainers two point zero point five. [[slnc 300]] And '
            'Docker, version twenty-four or later, running before you '
            'start.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real broker', 'in a container, real queues, and', 'the broker\'s own reasons.', '', 'The demo starts the container and', 'takes it away again.', '', 'Every wait is a poll on a real', 'condition, never a fixed pause.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] '
            'Everything here is real. [[slnc 300]] A real broker in a '
            'container, real queues, and reasons the broker wrote itself. '
            '[[slnc 500]] The demo starts the container, and removes it '
            'again. [[slnc 300]] So nothing is installed, and nothing is '
            'left running. [[slnc 500]] And every wait checks a real '
            'condition, with a time limit, instead of pausing for a fixed '
            'time. [[slnc 300]] So the same numbers come out on every '
            'machine.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a queue where a message can', 'never be permanently bad, or where', 'losing one costs nothing, this is', 'more to run than it is worth.', '', 'Where a message can be poison, its', 'absence is the outage.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a queue where a '
            'message can never be permanently bad, or where losing one '
            'costs nothing, it is more to run than it is worth. [[slnc '
            '400]] But where a message can be poison, not having a dead '
            'letter channel is the outage.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository.', 'Give the parked queue a time limit of its own, and decide', 'where an order goes when it dies a second time.'],
        narration=(
            "That's the Dead Letter Channel, with RabbitMQ. [[slnc 400]] "
            'If you remember one sentence, make it this one. [[slnc 300]] '
            'The application writes a rule on the queue, and from then '
            'on, the broker decides when a message is dead, and writes '
            'down why. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Give the parked queue a time limit of its own. [[slnc '
            '300]] And decide where an order should go if it dies a '
            'second time. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
