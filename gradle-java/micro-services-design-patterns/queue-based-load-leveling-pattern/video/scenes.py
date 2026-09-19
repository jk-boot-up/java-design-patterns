"""Scene definitions for the Queue-Based Load Leveling teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Queue-Based Load Leveling',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Queue-Based Load '
            'Leveling pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: queue '
            'based load leveling puts a queue between a source of bursty '
            'work and the service that does it. The service works at its '
            'own steady pace, and the burst waits its turn instead of '
            'overwhelming it. [[slnc 350]] This is another project in the '
            'microservices category, whose subject is how many small '
            'services stay reliable when they talk to each other. In our '
            'online store, the busiest moment is the start of a sale, '
            'when a hundred orders arrive at once. [[slnc 300]] By the '
            'end you will see a burst refused when it goes straight to '
            'the worker, see a queue spread the same burst with nothing '
            'lost, see what waiting costs, see an unbounded queue hide a '
            'worker that is too slow, and see the bill, which is that an '
            'in-memory queue forgets.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A sale starts.', '100 orders arrive in one moment.', '', 'The order service handles 10 a', 'tick.', '', 'The rest of the day it is nearly', 'idle.', '', 'What happens to the other 90?'],
        narration=(
            'Here is the scenario. A sale starts in the online store, and '
            'a hundred orders arrive in the same moment. The order '
            'service can process ten in a tick. The rest of the day it is '
            'nearly idle. [[slnc 300]] The question: what happens to the '
            'other ninety?'
        ),
    ),
    dict(
        key='03-direct', kind='console', title='A Burst, Straight To The Worker',
        body="""ONE. Straight through.
  100 orders at once.
  the service takes 10 a tick.
  processed: 10.
  refused: 90.

  on the busiest moment.""",
        narration=(
            'First, a burst straight to the worker. A hundred orders '
            'arrive at once. The order service handles ten a tick. Ten '
            'are processed. Ninety are refused. Ninety customers are told '
            'to try again, on the busiest moment the shop has all day.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Put a queue between the work', 'and the worker.', '', 'The burst goes into the queue', 'at once.', '', 'The worker takes from the queue', 'at its own steady pace.'],
        narration=(
            'The pattern. Put a queue between the work and the worker. '
            'The burst goes into the queue all at once. The worker takes '
            'from the queue at its own steady pace. The queue absorbs the '
            'difference.'
        ),
    ),
    dict(
        key='05-queue', kind='console', title='A Queue In Between',
        body="""TWO. A queue.
  the same 100 orders:
  processed: 100.
  refused: 0.
  deepest the queue got: 100.

  the worker never did more
  than 10 a tick.""",
        narration=(
            'Second, a queue in between. The same hundred orders. All '
            'hundred are processed. None are refused. The queue got a '
            'hundred deep, and the worker never did more than ten in a '
            'tick. The burst was spread over ten ticks.'
        ),
    ),
    dict(
        key='06-wait', kind='console', title='What The Queue Costs: Waiting',
        body="""THREE. Waiting.
  first order: 0 ticks.
  last order: 9.
  average: 4.5.

  nothing was lost, and only the
  first ten were quick.""",
        narration=(
            'Third, what the queue costs. The first order waited nothing. '
            'The last waited nine ticks. On average, an order waited four '
            'and a half. No order was lost, but only the first ten were '
            'quick. The queue trades refusal for waiting.'
        ),
    ),
    dict(
        key='07-bound', kind='console', title='A Queue With No End, And One With A Limit',
        body="""FOUR. No end, or a limit.
  15 arrive, 10 processed.
  unbounded: 500 waiting,
  growing.

  limit 50: 460 refused,
  no wait over 4 ticks.

  it hides a slow worker.""",
        narration=(
            'Fourth, a queue with no end, and one with a limit. Fifteen '
            'orders arrive every tick, and the worker does ten. An '
            'unbounded queue reaches five hundred waiting, and is still '
            'growing. A queue limited to fifty refuses four hundred and '
            'sixty, and no order waits more than four ticks. [[slnc 300]] '
            'A queue does not fix a worker that is too slow. It hides it, '
            'until the limit says so.'
        ),
    ),
    dict(
        key='08-size', kind='console', title='Size The Worker For The Average',
        body="""FIVE. Sizing.
  worker of 10: longest wait 9.
  worker of 20: longest wait 4.

  to serve the peak with no
  queue: a worker of 100, idle
  almost all day.""",
        narration=(
            'Fifth, size the worker for the average, not the peak. A '
            'worker of ten clears the burst with a longest wait of nine. '
            'A worker of twenty halves that, to four. To serve the whole '
            'peak at once with no queue, you would need a worker of a '
            'hundred, idle almost all day. The queue lets you pay for the '
            'average.'
        ),
    ),
    dict(
        key='09-lost', kind='console', title='The Bill: An In-Memory Queue Forgets',
        body="""SIX. The bill.
  the process stops at tick 3.
  processed: 30. lost: 70.

  70 customers were told their
  order was accepted.

  it must be kept somewhere
  that survives.""",
        narration=(
            'Last, the bill. The process that holds the queue stops at '
            'tick three, and the queue was in memory. Thirty orders had '
            'been processed. Seventy were waiting, and are gone. Seventy '
            'customers were told their order was accepted, and it never '
            'happened. A queue that must not lose orders has to live '
            'somewhere that survives.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A message broker or a queue', 'between a web tier and a worker', '', 'A BlockingQueue between threads,', 'sized on purpose.', '', 'A chart of queue depth on a', 'dashboard, with an alert.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'message broker or a queue between a web tier and a worker '
            'tier. A BlockingQueue between threads, sized on purpose. A '
            'chart of queue depth on a dashboard, with an alert. Amazon '
            'SQS, RabbitMQ, Kafka, or Azure Service Bus in an '
            'architecture diagram.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a queue to level load when', 'work arrives in bursts, the caller', 'does not need the answer straight', 'away, and a short wait is', 'acceptable. Bound the queue, watch', 'its depth, and size the worker for', 'the average. Keep the queue', 'somewhere durable if orders must', 'not be lost. Do not use it where'],
        narration=(
            'Here is my verdict, plainly. Use a queue to level load when '
            'work arrives in bursts, the caller does not need the answer '
            'straight away, and a short wait is acceptable. Bound the '
            'queue, watch its depth, and size the worker for the average. '
            'Keep the queue somewhere durable if orders must not be lost. '
            'Do not use it where the caller needs an immediate result.'
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
        body=['If load is steady and the service', 'copes, a queue is one more thing', 'to run. If the caller needs the', 'answer now, a queue is the wrong', 'shape.'],
        narration=(
            'So when is it too much? If load is steady and the service '
            'copes, a queue is one more thing to run. If the caller needs '
            'the answer now, a queue is the wrong shape.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Queue-Based Load Leveling. [[slnc 250]] If you take "
            'one sentence away, take this one: a queue lets a service '
            'keep its pace, and the price is waiting, a limit you must '
            'choose, and a copy of the orders that must survive. [[slnc '
            '350]] The full source, the written notes, the diagrams and '
            'an animated walkthrough are all in the repository, running '
            'offline with nothing installed but a Java development kit. '
            '[[slnc 300]] If you try one exercise, change the queue limit '
            'to two hundred and see what happens to the refusals and the '
            'longest wait. [[slnc 300]] If this helped, a like genuinely '
            'does help other people find it, and subscribe if you would '
            'like the rest of the series. [[slnc 250]] Thanks for '
            'watching.'
        ),
    ),
]
