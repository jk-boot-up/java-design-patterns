"""Scene definitions for the Competing Consumers teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Competing Consumers',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Competing Consumers pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Competing consumers '
            'means several workers take messages from the same queue. '
            '[[slnc 300]] Each message goes to exactly one of them. '
            '[[slnc 300]] So the work is shared, without the workers ever '
            'talking to each other. [[slnc 600]] Think of a supermarket '
            'with one long queue and several tills. [[slnc 300]] '
            'Whichever till is free calls the next customer. [[slnc 300]] '
            'Each customer is served once, and the tills never need to '
            'agree on anything. [[slnc 700]] In our online store, the '
            'work waiting to be done is a queue of orders. [[slnc 500]] '
            'By the end, you will hear one worker, then three, share the '
            'same queue. [[slnc 300]] Every message handled exactly once. '
            '[[slnc 300]] The order of messages given up. [[slnc 300]] A '
            'failed message taken over. [[slnc 300]] And the costs: '
            'duplicates, and workers stuck waiting for something they '
            'share.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Orders wait in a queue.', '', 'One worker cannot keep up.', '', 'Add a second, without rewriting', 'anything, and without handling', 'an order twice.', '', 'How?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Orders wait in a queue to '
            'be processed. [[slnc 300]] One worker cannot keep up. [[slnc '
            '500]] We want to add a second worker, and a third. [[slnc '
            '300]] Without rewriting anything. [[slnc 300]] And without '
            'handling any order twice. [[slnc 500]] So here is the '
            'question. [[slnc 300]] How?'
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
            'First demo: one consumer, then three. [[slnc 400]] A '
            'consumer is simply a worker that takes messages from the '
            'queue. [[slnc 500]] There are six slow jobs. [[slnc 300]] '
            'With one consumer, one job is in progress, and five are '
            'waiting. [[slnc 500]] With three consumers, three are in '
            'progress, and three are waiting. [[slnc 500]] The consumers '
            'do not talk to each other. [[slnc 300]] They just take from '
            'the same queue.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Several consumers read from', 'one queue.', '', 'Each message goes to exactly one', 'of them.', '', 'A message that is not finished', 'goes back.', '', 'Add capacity by adding a consumer.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Several consumers read from '
            'one queue. [[slnc 300]] Each message goes to exactly one of '
            'them. [[slnc 300]] If a message is not finished, it goes '
            'back on the queue. [[slnc 500]] And to add capacity, you '
            'simply add another consumer. [[slnc 300]] Nothing else '
            'changes.'
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
            'Second demo: each message is handled once. [[slnc 400]] A '
            'thousand orders, and four consumers. [[slnc 500]] The orders '
            'were handled a thousand times in total. [[slnc 300]] And '
            'they were a thousand different orders. [[slnc 300]] None '
            'twice, and none missed. [[slnc 500]] Which consumer got '
            'which order is not decided in advance. [[slnc 300]] And it '
            'does not matter.'
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
            'Third demo: the order is not kept. [[slnc 400]] Orders one, '
            'two, and three are put on the queue, in that order. [[slnc '
            '300]] But the consumer handling order one is slow. [[slnc '
            '500]] So they finish as two, then three, then one. [[slnc '
            '500]] If order two depends on order one, that is a bug. '
            '[[slnc 300]] Competing consumers give up ordering, to gain '
            'capacity.'
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
            'Fourth demo: a consumer fails, and another takes over. '
            '[[slnc 400]] The first attempt fails. [[slnc 300]] The '
            'message goes back to the queue. [[slnc 300]] And a second '
            'attempt succeeds. [[slnc 500]] The message was not lost. '
            '[[slnc 300]] Because it was never truly removed from the '
            'queue until it was finished.'
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
            'Fifth demo: a duplicate. [[slnc 400]] A consumer charges a '
            "customer's card. [[slnc 300]] Then it crashes, before it can "
            'say it has finished. [[slnc 500]] So the message comes back, '
            'and the card is charged again. [[slnc 300]] Two charges. '
            '[[slnc 500]] Now try a consumer that remembers what it has '
            'already done. [[slnc 300]] It charges only once. [[slnc '
            '500]] The queue promises to deliver each message at least '
            'once, not exactly once. [[slnc 300]] So the consumer itself '
            'has to make a repeat harmless.'
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
            'Finally, the bill. [[slnc 400]] Six consumers share a '
            'database that only lets two in at a time. [[slnc 500]] Two '
            'consumers are inside. [[slnc 300]] Four are waiting for a '
            'place. [[slnc 300]] So four of the six are doing nothing '
            'useful. [[slnc 500]] Adding consumers only helps while the '
            'thing they share still has room.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Several instances of a service', 'reading the same queue or topic', '', 'Kafka consumer groups, SQS with', 'several pollers, RabbitMQ work', '', 'An acknowledge or delete call', 'after the work is done.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for several copies of a service, reading '
            'from the same queue. [[slnc 300]] Look for Kafka consumer '
            'groups, several programs polling one Amazon queue, or '
            'RabbitMQ work queues. [[slnc 300]] Look for a call that '
            'acknowledges or deletes a message after the work is done. '
            '[[slnc 300]] Or a pool of threads, all taking tasks from one '
            'shared queue.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use competing consumers to scale', 'work that can be done in any', 'order, where each item is', 'independent. Acknowledge only when', 'finished, make every consumer safe', 'to run twice on the same message,', 'and size the pool for the slowest', 'thing they share. Do not use it', 'where order matters, unless the'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use competing '
            'consumers to scale work that can be done in any order. '
            '[[slnc 300]] Where each item is independent of the others. '
            '[[slnc 500]] Only confirm a message once the work is '
            'finished. [[slnc 300]] Make every consumer safe to run twice '
            'on the same message. [[slnc 300]] And size the number of '
            'consumers for the slowest thing they share. [[slnc 500]] Do '
            'not use it where order matters. [[slnc 300]] Unless the '
            'queue is split so that related messages always go to the '
            'same consumer.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] "
            'Nothing depends on a real clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['When one consumer keeps up, extra', 'consumers are cost and risk. When', 'order matters, competing consumers', 'are wrong until the queue is', 'partitioned.'],
        narration=(
            'So, when is this too much? [[slnc 400]] When one consumer '
            'can keep up, extra consumers only add cost and risk. [[slnc '
            '400]] And when order matters, competing consumers are the '
            'wrong choice, until the queue is split by the thing that '
            'needs ordering.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Competing Consumers pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] '
            'Competing consumers share the work by giving up ordering, '
            'and the consumer itself must handle the duplicates the queue '
            'cannot avoid. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] Make the consumer safe '
            'to run twice. [[slnc 300]] Then prove it, by delivering '
            'every message twice. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
