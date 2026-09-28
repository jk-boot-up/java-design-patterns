"""Scene definitions for the Serverless with LocalStack teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Serverless with LocalStack',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Serverless pattern, in Java, using LocalStack and A W S '
            'Lambda. [[slnc 300]] This video is presented by Jayasekhar '
            'Konduru. [[slnc 600]] First, a simple definition. [[slnc '
            '300]] Serverless runs each piece of work as a short '
            'function, started by an event, and you pay for each call. '
            '[[slnc 500]] With A W S Lambda, you upload a function once. '
            '[[slnc 300]] The platform starts a container for each call '
            'that runs at the same time. [[slnc 300]] It keeps that '
            'container warm for a while, and removes it when it is idle. '
            '[[slnc 600]] Think of a taxi rank. [[slnc 300]] When a crowd '
            'arrives, more taxis pull in. [[slnc 300]] When the street is '
            'quiet, they drive away. [[slnc 700]] This is the framework '
            'version of the Serverless video, with the same online store. '
            '[[slnc 400]] We will upload a real function, watch five real '
            'containers start for five orders, and watch them disappear. '
            '[[slnc 300]] We will hear a real cold start, a function that '
            'forgets, and a job stopped at its time limit.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Serverless, the hand-built video,', 'counts instances on a clock.', '', 'It shows scale to zero, a cold', 'start and lost memory.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Serverless video. [[slnc 400]] That '
            'one simulates a function platform, counting in ticks. [[slnc '
            '300]] It shows scaling to zero, a cold start, lost memory, '
            'and the price when busy. [[slnc 500]] If you are new to the '
            'pattern, watch that one first. [[slnc 400]] Here, we keep '
            'the same example, and ask what a real Lambda platform does '
            'with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: LocalStack,', 'and the AWS SDK.', '', 'You need Docker running. Without', 'it the demo says so and stops.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Two things are new in this project. [[slnc 400]] First, A W '
            "S Lambda, which is Amazon's function platform. [[slnc 300]] "
            'And LocalStack, a program that offers the same Lambda '
            'interface on your own machine. [[slnc 300]] It runs each '
            'copy of a function in its own container. [[slnc 400]] '
            'Second, the A W S software kit for Java, which our program '
            'uses to talk to it. [[slnc 500]] You need Docker running. '
            '[[slnc 300]] Without it, the demo tells you so, and stops. '
            '[[slnc 500]] And one promise. [[slnc 300]] If you skip this '
            'video, you lose none of the pattern. [[slnc 300]] This one '
            'is about the tool.'
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
            'First, the traditional way: a machine that is always on. '
            '[[slnc 400]] Using the same price units as the earlier '
            'video, a server costs two per tick. [[slnc 400]] One hundred '
            'ticks, with three orders, costs two hundred. [[slnc 400]] We '
            'paid for one hundred ticks, and used it for three orders.'
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
            'Second demo: one function per event. [[slnc 400]] The '
            'receipt function is uploaded to a real Lambda interface. '
            '[[slnc 300]] Then it is called once for each of three '
            'orders. [[slnc 400]] Three receipts are sent. [[slnc 300]] '
            'At one unit per call, the bill is three. [[slnc 400]] '
            'Between orders, nothing needs to run, and nothing is paid '
            'for.'
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
            'Third demo: scaling out, and back to zero. [[slnc 400]] '
            'Before any order arrives, no copies are running. [[slnc '
            '400]] Then five orders arrive at the same moment. [[slnc '
            '300]] Five different copies answer, and five containers are '
            'running. [[slnc 400]] Five quiet seconds later, none are '
            'running.'
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
            'Fourth demo: the cold start. [[slnc 400]] After a quiet '
            'time, the first call takes several hundred milliseconds. '
            '[[slnc 300]] The call right after it takes just a few '
            'milliseconds. [[slnc 500]] Why? [[slnc 300]] The first call '
            'had to start a container for the function. [[slnc 300]] The '
            'second call found one already running.'
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
            'Fifth demo: a function has no memory between calls. [[slnc '
            '400]] We call the copy that is running. [[slnc 300]] It says '
            'it has handled three calls so far. [[slnc 500]] Then there '
            'is a quiet time, and we call again. [[slnc 300]] A different '
            'copy answers. [[slnc 300]] It says it has handled one call. '
            '[[slnc 500]] Whatever the first copy kept in its variables '
            'is gone. [[slnc 300]] Anything that must last belongs in a '
            'store outside the function.'
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
            'Finally, the bill, in the same price units as before. [[slnc '
            '400]] In a quiet hundred ticks, with three calls, functions '
            'cost three, and the server costs two hundred. [[slnc 400]] '
            'In a busy hundred ticks, with three hundred calls, functions '
            'cost three hundred, and the server still costs two hundred. '
            '[[slnc 500]] So paying per call is cheap when quiet, and '
            'expensive when busy all the time. [[slnc 500]] And there is '
            'a time limit. [[slnc 300]] A job that needs six seconds, on '
            'a function limited to three, fails. [[slnc 300]] The '
            'platform reports that the task timed out after three '
            'seconds.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Short, bursty work.', '', 'State outside the function.', '', 'Expect the cold start.', '', 'Price it at your busiest.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use functions for work '
            'that is short, comes in bursts, and keeps nothing between '
            'calls. [[slnc 500]] Keep any lasting state outside. [[slnc '
            '300]] Expect a cold start after a quiet time. [[slnc 300]] '
            'Set the time limit on purpose. [[slnc 300]] Work out the '
            'price at your busiest. [[slnc 300]] And keep long jobs '
            'somewhere else.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A handler that takes an event and', 'a context.', '', "A function's `timeout` and", '`memorySize` settings.', '', '`InvokeRequest` calls in the AWS', 'SDK.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a handler method that takes an event and a '
            "context. [[slnc 300]] Look for a function's timeout and "
            'memory size settings. [[slnc 300]] And look for Invoke '
            'Request calls in the A W S software kit.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['AWS Lambda, Google Cloud Functions', 'and Azure Functions, and image', 'resizing, receipts and webhooks.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In A W S '
            'Lambda, Google Cloud Functions, and Azure Functions. [[slnc '
            '300]] And in jobs like resizing images, sending receipts, '
            'and handling webhooks.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['LocalStack 4.14.0.', '', 'AWS SDK for Java 2.55.1.', '', 'Lambda runtime Python 3.12.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] '
            'LocalStack four point fourteen. [[slnc 300]] The A W S '
            'software kit for Java, two point fifty-five point one. '
            '[[slnc 300]] And the Lambda runtime, Python three point '
            'twelve.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real Lambda', 'API, real containers for each', 'copy, and a real cold start.', '', 'The prices in act six are the', "earlier project's units, not real", 'charges.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything in it is real. [[slnc 300]] A real Lambda '
            'interface, real containers for each copy, and a real cold '
            'start. [[slnc 400]] The prices, though, use the earlier '
            "video's units. [[slnc 300]] They are not real charges."
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For steady heavy load, long jobs,', 'or work that needs memory between', 'calls, an ordinary server is', 'cheaper and simpler.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For heavy, steady '
            'traffic, for long jobs, or for work that needs memory '
            'between calls, an ordinary server is cheaper and simpler.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', "are in the repository. Raise the function's time limit to ten seconds, and rerun the last act.."],
        narration=(
            "That's Serverless with LocalStack. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A real '
            'function platform starts a container for each call that runs '
            'at once, and removes it when idle, and the price is the cold '
            'start, lost memory, and a time limit. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            "one exercise to try. [[slnc 300]] Raise the function's time "
            'limit to ten seconds. [[slnc 300]] Then run the last demo '
            'again. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
