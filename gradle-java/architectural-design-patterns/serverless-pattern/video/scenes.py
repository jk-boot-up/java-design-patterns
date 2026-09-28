"""Scene definitions for the Serverless teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Serverless',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Serverless pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Serverless runs each piece '
            'of work as a short function. [[slnc 300]] A platform starts '
            'the function when an event arrives. [[slnc 300]] It throws '
            'the function away when it is idle. [[slnc 300]] And you pay '
            'for each call. [[slnc 600]] Think of a taxi, compared with '
            'owning a car. [[slnc 300]] You pay for a taxi only when you '
            'ride. [[slnc 300]] But you may wait for one to arrive, and a '
            'taxi every day can cost more than a car. [[slnc 700]] In our '
            'online store, a receipt must be sent whenever an order is '
            'placed. [[slnc 300]] Orders come in bursts, with long quiet '
            'gaps in between. [[slnc 500]] In this video, we compare an '
            'always-on server with functions. [[slnc 300]] We will hear '
            'about scaling to zero, the slow first call, and why a '
            'function forgets. [[slnc 300]] Then we will look at the '
            'bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['When an order is placed,', 'a receipt must be sent.', '', 'In 100 ticks only 3 orders', 'arrive,', '', 'and now and then 5 arrive', 'at once.', '', 'What should run, and when?'],
        narration=(
            'Here is the scenario. [[slnc 400]] When an order is placed, '
            'a receipt must be sent. [[slnc 400]] We measure time in '
            'ticks. [[slnc 300]] In one hundred ticks, only three orders '
            'arrive. [[slnc 300]] But now and then, five orders arrive at '
            'the same moment. [[slnc 500]] So here is the question. '
            '[[slnc 300]] What should run, and when?'
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
            'First, the traditional way: a machine that is always on. '
            '[[slnc 400]] It runs for one hundred ticks, and handles '
            'three orders. [[slnc 400]] The bill is two hundred. [[slnc '
            '400]] We paid for one hundred ticks of running, and used it '
            'for just three orders.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Each piece of work is a short', 'function.', '', 'An event starts it. The platform', 'runs as many as needed, and', 'drops them when idle.', '', 'You pay per call.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Each piece of work is a short '
            'function. [[slnc 300]] An event, such as a new order, starts '
            'it. [[slnc 400]] The platform runs as many copies as are '
            'needed. [[slnc 300]] It removes them when they are idle. '
            '[[slnc 300]] And you pay for each call.'
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
            'Second demo: one function per event. [[slnc 400]] The same '
            'three orders arrive. [[slnc 300]] Each one runs a function '
            'that sends the receipt. [[slnc 400]] Three calls, and a bill '
            'of three. [[slnc 500]] Between orders, nothing runs, and '
            'nothing is paid for.'
        ),
    ),
    dict(
        key='06-scale', kind='console', title='Scale Out, And Back To Zero',
        body="""THREE. Scale, and back to zero.
  before any order: 0.
  5 orders at once: 5 instances.
  10 quiet ticks later: 0.""",
        narration=(
            'Third demo: scaling out, and back to zero. [[slnc 400]] '
            'Before any order arrives, there are no running copies at '
            'all. [[slnc 400]] Then five orders arrive at the same '
            'moment. [[slnc 300]] The platform starts five copies. [[slnc '
            '400]] Ten quiet ticks later, there are none again.'
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
            "Fourth demo: the cold start. [[slnc 400]] Let's measure the "
            'extra wait before each call begins. [[slnc 400]] The very '
            'first call waits five ticks. [[slnc 300]] A call soon after '
            'that waits no extra time. [[slnc 300]] A call after a long '
            'quiet period waits five ticks again. [[slnc 500]] Why? '
            '[[slnc 300]] After a quiet time, no copy is running, so a '
            'new one must be started first. [[slnc 300]] That delay is '
            'called a cold start.'
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
            'Fifth demo: a function has no memory between calls. [[slnc '
            '400]] Each call adds one to two counters. [[slnc 300]] One '
            'counter lives inside the function. [[slnc 300]] The other '
            'lives in a store outside it. [[slnc 500]] After two calls in '
            'a row, both counters say two. [[slnc 400]] Then there is a '
            'quiet time, and one more call. [[slnc 300]] The counter '
            'inside the function says one, because it started again from '
            'nothing. [[slnc 300]] The counter outside says three. [[slnc '
            '500]] Anything kept inside a function is lost. [[slnc 300]] '
            'Anything that must last goes in a store outside.'
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
            'Finally, the bill. [[slnc 400]] In a quiet hundred ticks, '
            'with three calls, functions cost three, and the server costs '
            'two hundred. [[slnc 400]] In a busy hundred ticks, with '
            'three hundred calls, functions cost three hundred, and the '
            'server still costs two hundred. [[slnc 500]] So paying per '
            'call is cheap when you are quiet. [[slnc 300]] And expensive '
            'when you are busy all the time. [[slnc 500]] There is one '
            'more limit. [[slnc 300]] A job that needs twenty ticks, on a '
            'platform with a limit of fifteen, is stopped before it '
            'finishes. [[slnc 300]] Long work does not fit.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['AWS Lambda, Google Cloud', 'Functions, Azure Functions,', '', 'A handler that takes an event and', 'returns, with no fields.', '', 'A trigger: an upload, a queue', 'message, a schedule, an HTTP'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for platforms like A W S Lambda, Google '
            'Cloud Functions, Azure Functions, or Cloudflare Workers. '
            '[[slnc 400]] Look for a handler method that takes an event, '
            'returns a result, and keeps no fields. [[slnc 300]] Look for '
            'a trigger, such as a file upload, a queue message, a '
            'schedule, or a web request. [[slnc 300]] And look for '
            'settings for a timeout and memory, with a bill per request.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use serverless for work that is', 'short, comes in bursts, and keeps', 'nothing between calls. Keep state', 'outside. Expect a slow first call', 'after a quiet time. Work out the', 'price at your busiest, not your', 'quietest. Keep long jobs off it.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use serverless for '
            'work that is short, comes in bursts, and keeps nothing '
            'between calls. [[slnc 500]] Then follow four rules. [[slnc '
            '300]] One. [[slnc 200]] Keep any lasting state outside the '
            'function. [[slnc 300]] Two. [[slnc 200]] Expect a slow first '
            'call after a quiet time. [[slnc 300]] Three. [[slnc 200]] '
            'Work out the price at your busiest, not your quietest. '
            '[[slnc 300]] And four. [[slnc 200]] Keep long jobs somewhere '
            'else.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'time is counted in ticks, not by the clock, so every run '
            'gives the same result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For steady heavy load, long jobs,', 'or work that needs memory between', 'calls, an ordinary server is', 'cheaper and simpler. Serverless', 'suits the quiet and the bursty.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For heavy, steady '
            'traffic, for long jobs, or for work that needs memory '
            'between calls, an ordinary server is cheaper and simpler. '
            '[[slnc 400]] Serverless suits work that is quiet, or comes '
            'in bursts.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Serverless pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Serverless pays '
            'per call and scales to zero, and the price is the cold '
            'start, no memory between calls, and a bill that grows with '
            'steady traffic. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Work out how many calls, in one hundred ticks, make '
            'the functions cost the same as the server. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
