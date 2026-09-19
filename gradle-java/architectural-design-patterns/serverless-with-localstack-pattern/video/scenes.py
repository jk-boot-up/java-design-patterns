"""Scene definitions for the Serverless with LocalStack teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Serverless with LocalStack',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Serverless '
            'pattern with LocalStack and AWS Lambda, in Java, and it is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] It '
            'is the framework version of the Serverless video. That one '
            "counted a platform's instances on a clock. It showed a "
            'server paid for while idle, a function per event, scale out '
            'and back to zero, a cold start, lost memory, and the price '
            'when busy. This one shows the same idea inside LocalStack '
            'and AWS Lambda. [[slnc 350]] The plain definition, in short: '
            'with Lambda, a function is uploaded once. The platform '
            'starts a container for each concurrent call, keeps it warm '
            'for a while, and removes it when it is idle. [[slnc 300]] By '
            'the end you will see a function uploaded to a real Lambda '
            'API, see five orders at once start five real containers, see '
            'them removed when idle, see a real cold start, see a '
            'function forget its variables, and see a job stopped at its '
            'time limit.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Serverless, the hand-built video,', 'counts instances on a clock.', '', 'It shows scale to zero, a cold', 'start and lost memory.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video assumes the Serverless video. If you have not '
            "seen it, start there. It counts a platform's instances on a "
            'clock, and shows scale to zero, a cold start, lost memory, '
            'and the price when busy. [[slnc 300]] This one uses the same '
            'example. It does not teach the pattern again. It shows what '
            'LocalStack and AWS Lambda does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: LocalStack,', 'and the AWS SDK.', '', 'You need Docker running. Without', 'it the demo says so and stops.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before the first line of code, what LocalStack and AWS '
            "Lambda is. Lambda is Amazon's function platform. LocalStack "
            'is a program that answers the same programming interface on '
            'your own machine, and runs each copy of a function in a '
            'container of its own. [[slnc 300]] And a promise: skipping '
            'this video loses none of the pattern. The hand-built one '
            'teaches all of it.'
        ),
    ),
    dict(
        key='04-server', kind='console', title='A Machine That Is Always On',
        body="""ONE. Always on.
  a server costs 2 a tick.
  100 ticks, 3 orders: 200.

  paid for 100 ticks,
  used for 3 orders.""",
        narration=(
            "First, a machine that is always on. In the earlier project's "
            'price units, a server costs two a tick. A hundred ticks with '
            'three orders costs two hundred. It was paid for a hundred '
            'ticks, and used for three orders.'
        ),
    ),
    dict(
        key='05-fn', kind='console', title='A Function Per Event',
        body="""TWO. A function per event.
  uploaded to a real Lambda API.
  run for 3 orders:
  3 receipts sent, bill 3.

  between orders nothing runs.""",
        narration=(
            'Second, a function per event. The function is uploaded to a '
            'real Lambda API, and run for each of three orders. Three '
            'receipts are sent, and the bill at one per call is three. '
            'Between orders nothing has to be running, and nothing is '
            'paid for.'
        ),
    ),
    dict(
        key='06-scale', kind='console', title='Scale Out, And Back To Zero',
        body="""THREE. Scale, and back to zero.
  before any order: 0 copies.
  5 orders at once: 5 distinct
  copies answered; 5 containers.
  5 quiet seconds later: 0.""",
        narration=(
            'Third, scale out, and back to zero. Before any order, no '
            'copies are running. Five orders at the same moment: five '
            'distinct copies answered, and five containers are running. '
            'Five quiet seconds later, with no orders: none are running.'
        ),
    ),
    dict(
        key='07-cold', kind='console', title='The Cold Start',
        body="""FOUR. The cold start.
  the first call after a quiet
  time: hundreds of milliseconds.
  the call right after: a few.

  the first had to start a container;
  the second found it running.""",
        narration=(
            'Fourth, the cold start. The first call after a quiet time '
            'took several hundred milliseconds, and the call right after '
            'it, a few. The cold call was slower. The first call had to '
            'start a container for the function, and the second found it '
            'running.'
        ),
    ),
    dict(
        key='08-state', kind='console', title='No Memory Between Calls',
        body="""FIVE. No memory.
  the running copy has handled 3
  calls.
  after the quiet time, a different
  copy answers: 1 call.

  what the first kept in its
  variables went with it.""",
        narration=(
            'Fifth, no memory between calls. A call to the copy that is '
            'running: it has handled three calls. After the quiet time, a '
            'different copy answers, and it has handled one. What the '
            'first copy kept in its variables went with it. Anything that '
            'must last goes in a store outside.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  100 ticks:
  quiet, 3 calls: 3 vs 200.
  busy, 300 calls: 300 vs 200.

  cheap when quiet, dear when busy.

  a 6-second job, limit 3:
  Task timed out after 3 seconds.""",
        narration=(
            "Last, the bill. In the earlier project's price units, in a "
            'hundred ticks, with three calls, functions cost three and '
            'the server two hundred. With three hundred calls, functions '
            'cost three hundred, and the server two hundred. Paying per '
            'call is cheap when quiet, and dear when busy all the time. '
            'And a job that needs six seconds, with a limit of three, '
            'fails: the platform says the task timed out.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Short, bursty work.', '', 'State outside the function.', '', 'Expect the cold start.', '', 'Price it at your busiest.'],
        narration=(
            'My verdict, plainly. Use functions for work that is short, '
            'bursty and keeps nothing between calls. Keep state outside. '
            'Expect a cold start after a quiet time, and set the time '
            'limit on purpose. Work out the price at your busiest, and '
            'keep long jobs off it.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A handler that takes an event and', 'a context.', '', "A function's `timeout` and", '`memorySize` settings.', '', '`InvokeRequest` calls in the AWS', 'SDK.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            "handler that takes an event and a context. A function's "
            'timeout and memorySize settings. InvokeRequest calls in the '
            'AWS SDK.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['AWS Lambda, Google Cloud Functions', 'and Azure Functions, and image', 'resizing, receipts and webhooks.'],
        narration=(
            'You have met this in aws lambda, google cloud functions and '
            'azure functions, and image resizing, receipts and webhooks.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['LocalStack 4.14.0.', '', 'AWS SDK for Java 2.55.1.', '', 'Lambda runtime Python 3.12.'],
        narration=(
            'For the record. LocalStack, 4.14.0. AWS SDK for Java, '
            '2.55.1. Lambda runtime, Python 3.12.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real Lambda', 'API, real containers for each', 'copy, and a real cold start.', '', 'The prices in act six are the', "earlier project's units, not real", 'charges.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: a real Lambda API, real containers for '
            'each copy, and a real cold start. The prices in act six are '
            "the earlier project's units, and not real charges."
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For steady heavy load, long jobs,', 'or work that needs memory between', 'calls, an ordinary server is', 'cheaper and simpler.'],
        narration=(
            'So when is it too much? For steady heavy load, long jobs, or '
            'work that needs memory between calls, an ordinary server is '
            'cheaper and simpler.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', "are in the repository. Raise the function's time limit to ten seconds, and rerun the last act.."],
        narration=(
            "That's Serverless with LocalStack. [[slnc 250]] If you take "
            'one sentence away, take this one: a real function platform '
            'starts a container for each concurrent call and drops it '
            'when idle, and the price is the cold start, lost memory and '
            'a time limit. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository. [[slnc 300]] If you try one exercise, raise '
            "the function's time limit to ten seconds, and rerun the last "
            'act. [[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
