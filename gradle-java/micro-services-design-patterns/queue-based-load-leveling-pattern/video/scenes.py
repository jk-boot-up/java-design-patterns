"""Scene definitions for the Queue-Based Load Leveling teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Queue-Based Load Leveling',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Queue-Based Load Leveling pattern, in Java. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] You put a queue '
            'between a source of sudden bursts of work, and the service '
            'that does the work. [[slnc 300]] The service works at its '
            'own steady pace. [[slnc 300]] And the burst waits its turn, '
            'instead of overwhelming it. [[slnc 600]] Think of a busy '
            'bakery with a ticket machine. [[slnc 300]] When a crowd '
            'rushes in, everyone takes a number. [[slnc 300]] The bakers '
            'serve at their normal speed, and nobody is turned away. '
            '[[slnc 700]] In our online store, the busiest moment is the '
            'start of a sale, when a hundred orders arrive at once. '
            '[[slnc 500]] By the end, you will hear a burst refused when '
            'it goes straight to the worker. [[slnc 300]] A queue spread '
            'the same burst, with nothing lost. [[slnc 300]] What waiting '
            'costs. [[slnc 300]] A queue with no limit hide a worker that '
            'is too slow. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A sale starts.', '100 orders arrive in one moment.', '', 'The order service handles 10 a', 'tick.', '', 'The rest of the day it is nearly', 'idle.', '', 'What happens to the other 90?'],
        narration=(
            'Here is the scenario. [[slnc 400]] A sale starts in the '
            'online store. [[slnc 300]] A hundred orders arrive in the '
            'same moment. [[slnc 500]] The order service can process ten '
            'orders in each tick of time. [[slnc 300]] The rest of the '
            'day, it is nearly idle. [[slnc 500]] So here is the '
            'question. [[slnc 300]] What happens to the other ninety?'
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
            'First demo: the burst goes straight to the worker. [[slnc '
            '400]] A hundred orders arrive at once. [[slnc 300]] The '
            'order service handles ten per tick. [[slnc 500]] Ten are '
            'processed. [[slnc 300]] Ninety are refused. [[slnc 500]] '
            'Ninety customers are told to try again. [[slnc 300]] On the '
            'busiest moment the shop has all day.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Put a queue between the work', 'and the worker.', '', 'The burst goes into the queue', 'at once.', '', 'The worker takes from the queue', 'at its own steady pace.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Put a queue between the work '
            'and the worker. [[slnc 500]] The burst goes into the queue, '
            'all at once. [[slnc 300]] The worker takes from the queue at '
            'its own steady pace. [[slnc 300]] The queue absorbs the '
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
            'Second demo: a queue in between. [[slnc 400]] The same '
            'hundred orders. [[slnc 500]] All hundred are processed. '
            '[[slnc 300]] None are refused. [[slnc 500]] The queue grew '
            'to a hundred orders. [[slnc 300]] And the worker never did '
            'more than ten in a tick. [[slnc 300]] The burst was spread '
            'over ten ticks.'
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
            'Third demo: what the queue costs. [[slnc 400]] The first '
            'order did not wait at all. [[slnc 300]] The last order '
            'waited nine ticks. [[slnc 300]] On average, an order waited '
            'four and a half ticks. [[slnc 600]] No order was lost. '
            '[[slnc 300]] But only the first ten were quick. [[slnc 500]] '
            'The queue swaps refusing for waiting.'
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
            'Fourth demo: a queue with no limit, and one with a limit. '
            '[[slnc 400]] Now fifteen orders arrive every tick, but the '
            'worker only handles ten. [[slnc 600]] With no limit, the '
            'queue reaches five hundred orders waiting. [[slnc 300]] And '
            'it is still growing. [[slnc 500]] With a limit of fifty, '
            'four hundred and sixty orders are refused. [[slnc 300]] But '
            'no order waits longer than four ticks. [[slnc 600]] A queue '
            'does not fix a worker that is too slow. [[slnc 300]] It '
            'hides it, until the limit reveals it.'
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
            'Fifth demo: size the worker for the average, not the peak. '
            '[[slnc 400]] A worker that handles ten per tick clears the '
            'burst, with a longest wait of nine ticks. [[slnc 300]] A '
            'worker that handles twenty cuts that to four. [[slnc 600]] '
            'To serve the whole peak at once, with no queue, you would '
            'need a worker of a hundred. [[slnc 300]] And it would sit '
            'idle almost all day. [[slnc 500]] The queue lets you pay for '
            'the average.'
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
            'Finally, the bill. [[slnc 400]] The program holding the '
            'queue stops, at tick three. [[slnc 300]] And the queue was '
            'only kept in memory. [[slnc 500]] Thirty orders had been '
            'processed. [[slnc 300]] Seventy were waiting, and they are '
            'gone. [[slnc 500]] Seventy customers were told their order '
            'was accepted. [[slnc 300]] And it never happened. [[slnc '
            '600]] A queue that must not lose orders has to be kept '
            'somewhere that survives a restart.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A message broker or a queue', 'between a web tier and a worker', '', 'A BlockingQueue between threads,', 'sized on purpose.', '', 'A chart of queue depth on a', 'dashboard, with an alert.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a message broker or queue between the '
            'web servers and the workers. [[slnc 300]] Look for a queue '
            'between threads, with a size chosen on purpose. [[slnc 300]] '
            'Look for a chart of queue length on a dashboard, with an '
            'alert. [[slnc 300]] Or names like Amazon S Q S, RabbitMQ, or '
            'Kafka on an architecture diagram.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a queue to level load when', 'work arrives in bursts, the caller', 'does not need the answer straight', 'away, and a short wait is', 'acceptable. Bound the queue, watch', 'its depth, and size the worker for', 'the average. Keep the queue', 'somewhere durable if orders must', 'not be lost. Do not use it where'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a queue to level '
            'the load when work arrives in bursts. [[slnc 300]] When the '
            'caller does not need the answer straight away. [[slnc 300]] '
            'And when a short wait is acceptable. [[slnc 600]] Give the '
            'queue a limit. [[slnc 300]] Watch how long it gets. [[slnc '
            '300]] Size the worker for the average. [[slnc 300]] And keep '
            'the queue somewhere that survives, if orders must not be '
            'lost. [[slnc 500]] Do not use it where the caller needs an '
            'immediate result.'
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
        body=['If load is steady and the service', 'copes, a queue is one more thing', 'to run. If the caller needs the', 'answer now, a queue is the wrong', 'shape.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If the load is '
            'steady, and the service copes, a queue is just one more '
            'thing to run. [[slnc 400]] And if the caller needs the '
            'answer now, a queue is the wrong shape.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Queue-Based Load Leveling pattern. [[slnc 400]] "
            'If you remember one sentence, make it this one. [[slnc 300]] '
            'A queue lets a service keep its own pace, and the price is '
            'waiting, a limit you must choose, and orders that must be '
            'stored somewhere safe. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 300]] It runs offline, with '
            'nothing installed except a Java development kit. [[slnc '
            '500]] Here is one exercise to try. [[slnc 300]] Change the '
            'queue limit to two hundred. [[slnc 300]] Then see what '
            'happens to the refusals, and to the longest wait. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
