"""Scene definitions for the Serverless teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Serverless',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Serverless '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'serverless runs each piece of work as a short function. A '
            'platform starts it when an event arrives, and throws it away '
            'when it is idle, and you pay for each call. [[slnc 350]] '
            'This is another project in the architecture category, whose '
            'subject is how a whole application is arranged, and who may '
            'depend on whom. In our online store, a receipt must be sent '
            'when an order is placed, and orders come in bursts with long '
            'quiet gaps. [[slnc 300]] By the end you will see a machine '
            'paid for while idle, see a function per event, see the '
            'platform scale out and back to zero, see the cold start, see '
            'that a function has no memory, and see the bill, which is '
            'the price when busy and the time limit.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order is placed,', 'a receipt must be sent.', '', 'In 100 ticks only 3 orders', 'arrive,', '', 'and now and then 5 arrive', 'at once.', '', 'What should run, and when?'],
        narration=(
            'Here is the scenario. When an order is placed, a receipt '
            'must be sent. In a hundred ticks, only three orders arrive, '
            'and now and then, five arrive at once. [[slnc 300]] The '
            'question: what should run, and when?'
        ),
    ),
    dict(
        key='03-server', kind='console', title='A Machine That Is Always On',
        body="""ONE. Always on.
  100 ticks, 3 orders.
  the bill: 200.

  paid for 100 ticks,
  used for 3 orders.""",
        narration=(
            'First, a machine that is always on. One hundred ticks, three '
            'orders. The bill is two hundred. It was paid for a hundred '
            'ticks, and used for three orders.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Each piece of work is a short', 'function.', '', 'An event starts it. The platform', 'runs as many as needed, and', 'drops them when idle.', '', 'You pay per call.'],
        narration=(
            'The pattern. Each piece of work is a short function. An '
            'event starts it. The platform runs as many as are needed, '
            'and drops them when they are idle. You pay per call.'
        ),
    ),
    dict(
        key='05-fn', kind='console', title='A Function Per Event',
        body="""TWO. A function per event.
  the same 3 orders.
  3 calls: the bill is 3.

  between orders nothing runs,
  and nothing is paid for.""",
        narration=(
            'Second, a function per event. The same three orders, each '
            'running a send receipt function. Three calls, and a bill of '
            'three. Between orders nothing runs, and nothing is paid for.'
        ),
    ),
    dict(
        key='06-scale', kind='console', title='Scale Out, And Back To Zero',
        body="""THREE. Scale, and back to zero.
  before any order: 0.
  5 orders at once: 5 instances.
  10 quiet ticks later: 0.""",
        narration=(
            'Third, scale out, and back to zero. Before any order, no '
            'instances. Five orders at the same moment: five instances, '
            'five cold starts. Ten ticks later, with no orders: no '
            'instances again.'
        ),
    ),
    dict(
        key='07-cold', kind='console', title='The Cold Start',
        body="""FOUR. The cold start.
  extra wait:
  first call: 5 ticks.
  soon after: 0.
  after a long quiet: 5.

  an instance must be started.""",
        narration=(
            'Fourth, the cold start. The extra wait: first call, five '
            'ticks. A call soon after, none. A call after a long quiet, '
            'five ticks. The first call after a quiet time is slow, '
            'because an instance must be started for it.'
        ),
    ),
    dict(
        key='08-state', kind='console', title='No Memory Between Calls',
        body="""FIVE. No memory.
  two calls: instance 2, store 2.
  after the quiet time:
  instance 1, store 3.

  what is kept in the function
  is gone. keep it outside.""",
        narration=(
            'Fifth, no memory between calls. Two calls in a row: the '
            'instance remembers two, and the outside store two. After the '
            'quiet time: the instance remembers one, and the outside '
            'store three. What is kept in the function is gone. Anything '
            'that must last goes in a store outside.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  100 ticks:
  quiet, 3 calls: 3 vs 200.
  busy, 300 calls: 300 vs 200.

  cheap when quiet, dear when
  busy all the time.

  a 20-tick job, limit 15:
  stopped.""",
        narration=(
            'Last, the bill. In a hundred ticks, with three calls, '
            'functions cost three and the server two hundred. With three '
            'hundred calls, functions cost three hundred, and the server '
            'two hundred. Paying per call is cheap when quiet, and dear '
            'when busy all the time. And a job of twenty ticks against a '
            'limit of fifteen does not finish. Long work does not fit.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['AWS Lambda, Google Cloud', 'Functions, Azure Functions,', '', 'A handler that takes an event and', 'returns, with no fields.', '', 'A trigger: an upload, a queue', 'message, a schedule, an HTTP'],
        narration=(
            'How do you recognise this in code you did not write? AWS '
            'Lambda, Google Cloud Functions, Azure Functions, Cloudflare '
            'Workers. A handler that takes an event and returns, with no '
            'fields. A trigger: an upload, a queue message, a schedule, '
            'an HTTP request. A setting for timeout and memory, and a '
            'bill per request.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use serverless for work that is', 'short, comes in bursts, and keeps', 'nothing between calls. Keep state', 'outside. Expect a slow first call', 'after a quiet time. Work out the', 'price at your busiest, not your', 'quietest. Keep long jobs off it.'],
        narration=(
            'Here is my verdict, plainly. Use serverless for work that is '
            'short, comes in bursts, and keeps nothing between calls. '
            'Keep state outside. Expect a slow first call after a quiet '
            'time. Work out the price at your busiest, not your quietest. '
            'Keep long jobs off it.'
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
        body=['For steady heavy load, long jobs,', 'or work that needs memory between', 'calls, an ordinary server is', 'cheaper and simpler. Serverless', 'suits the quiet and the bursty.'],
        narration=(
            'So when is it too much? For steady heavy load, long jobs, or '
            'work that needs memory between calls, an ordinary server is '
            'cheaper and simpler. Serverless suits the quiet and the '
            'bursty.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Serverless. [[slnc 250]] If you take one sentence "
            'away, take this one: serverless pays per call and scales to '
            'zero, and the price is the cold start, no memory between '
            'calls, and a bill that grows with steady load. [[slnc 350]] '
            'The full source, the written notes, the diagrams and an '
            'animated walkthrough are all in the repository, running '
            'offline with nothing installed but a Java development kit. '
            '[[slnc 300]] If you try one exercise, find how many calls in '
            'a hundred ticks make the functions cost the same as the '
            'server. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
