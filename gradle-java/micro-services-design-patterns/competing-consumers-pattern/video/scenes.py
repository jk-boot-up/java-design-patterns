"""Scene definitions for the Competing Consumers teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Competing Consumers',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Competing '
            'Consumers pattern in Java, and it is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'competing consumers means several workers take messages from '
            'the same queue. Each message goes to exactly one of them, '
            'and the work is shared without the workers ever having to '
            'coordinate. [[slnc 350]] This is another project in the '
            'microservices category, whose subject is how many small '
            'services stay reliable when they talk to each other. In our '
            'online store, the work waiting to be done is a queue of '
            'orders. [[slnc 300]] By the end you will see one worker and '
            'three workers take from the same queue, see every message '
            'handled exactly once, see ordering given up, see a failed '
            'message taken over, and see the bills: duplicates, and '
            'workers that can only wait for a shared limit.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Orders wait in a queue.', '', 'One worker cannot keep up.', '', 'Add a second, without rewriting', 'anything, and without handling', 'an order twice.', '', 'How?'],
        narration=(
            'Here is the scenario. Orders wait in a queue to be '
            'processed. One worker cannot keep up. We want to add a '
            'second, and a third, without rewriting anything, and without '
            'handling an order twice. [[slnc 300]] The question: how?'
        ),
    ),
    dict(
        key='03-more', kind='console', title='One Consumer, Then Three',
        body="""ONE. More consumers.
  6 slow jobs, 1 consumer:
  1 in progress, 5 waiting.

  3 consumers:
  3 in progress, 3 waiting.

  they do not talk to each other.""",
        narration=(
            'First, one consumer, then three. Six slow jobs. With one '
            'consumer, one is in progress and five are waiting. With '
            'three consumers, three are in progress and three are '
            'waiting. The consumers do not talk to each other. They just '
            'take from the same queue.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Several consumers read from', 'one queue.', '', 'Each message goes to exactly one', 'of them.', '', 'A message that is not finished', 'goes back.', '', 'Add capacity by adding a consumer.'],
        narration=(
            'The pattern. Several consumers read from one queue. Each '
            'message goes to exactly one of them. A message that is not '
            'finished goes back on the queue. And you add capacity by '
            'adding a consumer, without changing anything else.'
        ),
    ),
    dict(
        key='05-once', kind='console', title='Each Message Is Handled Once',
        body="""TWO. Once each.
  1000 orders, 4 consumers.
  handled 1000 times in all,
  1000 different orders.

  none twice, none missed.""",
        narration=(
            'Second, each message is handled once. A thousand orders, '
            'four consumers. The orders were handled a thousand times in '
            'all, and they were a thousand different orders. None twice, '
            'and none missed. Which consumer got which order is not '
            'defined, and does not matter.'
        ),
    ),
    dict(
        key='06-order', kind='console', title='The Order Is Not Kept',
        body="""THREE. No order.
  published: 1, 2, 3.
  order 1's consumer is slow.
  finished: 2, 3, 1.

  if 2 depends on 1, a bug.""",
        narration=(
            'Third, the order is not kept. Orders one, two and three are '
            "published in that order. Order one's consumer is slow. They "
            'finish as two, three, one. If order two depends on order '
            'one, that is a bug. Competing consumers give up ordering to '
            'gain capacity.'
        ),
    ),
    dict(
        key='07-fail', kind='console', title='A Consumer Fails, Another Takes Over',
        body="""FOUR. A failure.
  attempt 1 fails.
  the message goes back.
  attempt 2 succeeds.

  it was not lost.""",
        narration=(
            'Fourth, a consumer fails, and another takes over. The first '
            'attempt fails. The message is given back to the queue, and a '
            'second attempt succeeds. The message was not lost, because '
            'it was never really removed until it was finished.'
        ),
    ),
    dict(
        key='08-dup', kind='console', title='At Least Once, So A Duplicate',
        body="""FIVE. A duplicate.
  charged, then crashed before
  saying so.
  charges made: 2.

  a consumer that remembers
  what it has done: 1.""",
        narration=(
            'Fifth, at least once, so a duplicate. A consumer charges the '
            'card, and crashes before it can say it finished. The message '
            'comes back, and the card is charged again: two charges. A '
            'consumer that remembers what it has done charges once. The '
            'queue cannot give you exactly once. The consumer has to.'
        ),
    ),
    dict(
        key='09-shared', kind='console', title='The Bill: The Same Downstream',
        body="""SIX. The bill.
  6 consumers, a database that
  lets 2 in.
  inside: 2. waiting: 4.

  four of the six do nothing
  useful.""",
        narration=(
            'Last, the bill. Six consumers share a database that lets '
            'only two in at a time. Two are inside. Four are waiting for '
            'a place. Four of the six are doing nothing useful. Adding '
            'consumers only helps while the thing they share has room.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Several instances of a service', 'reading the same queue or topic', '', 'Kafka consumer groups, SQS with', 'several pollers, RabbitMQ work', '', 'An acknowledge or delete call', 'after the work is done.'],
        narration=(
            'How do you recognise this in code you did not write? Several '
            'instances of a service reading the same queue or topic '
            'partition group. Kafka consumer groups, SQS with several '
            'pollers, RabbitMQ work queues. An acknowledge or delete call '
            'after the work is done. A thread pool whose tasks come from '
            'one shared queue.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use competing consumers to scale', 'work that can be done in any', 'order, where each item is', 'independent. Acknowledge only when', 'finished, make every consumer safe', 'to run twice on the same message,', 'and size the pool for the slowest', 'thing they share. Do not use it', 'where order matters, unless the'],
        narration=(
            'Here is my verdict, plainly. Use competing consumers to '
            'scale work that can be done in any order, where each item is '
            'independent. Acknowledge only when finished, make every '
            'consumer safe to run twice on the same message, and size the '
            'pool for the slowest thing they share. Do not use it where '
            'order matters, unless the queue is partitioned by the key '
            'that carries the order.'
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
        body=['When one consumer keeps up, extra', 'consumers are cost and risk. When', 'order matters, competing consumers', 'are wrong until the queue is', 'partitioned.'],
        narration=(
            'So when is it too much? When one consumer keeps up, extra '
            'consumers are cost and risk. When order matters, competing '
            'consumers are wrong until the queue is partitioned.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Competing Consumers. [[slnc 250]] If you take one "
            'sentence away, take this one: competing consumers share the '
            'work by giving up ordering, and the duplicate they cannot '
            'avoid must be handled by the consumer. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, make the consumer safe to run '
            'twice, and prove it by delivering every message twice. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
