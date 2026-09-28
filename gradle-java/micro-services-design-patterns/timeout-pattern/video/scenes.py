"""Scene definitions for the Timeout teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Timeout',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Timeout pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A timeout is a limit on how '
            'long you will wait for an answer. [[slnc 300]] So a slow or '
            'silent service cannot keep you waiting forever. [[slnc 600]] '
            'Think of waiting for a friend at a café. [[slnc 300]] You '
            'decide: if they are not here in twenty minutes, I will '
            'leave. [[slnc 300]] And you have a plan for what to do '
            'instead. [[slnc 700]] In our online store, the thing that '
            "may never answer is the supplier's stock service. [[slnc "
            '500]] By the end, you will hear a call that never returns '
            'hold up a worker forever. [[slnc 300]] A limit turn that '
            'into an answer. [[slnc 300]] Why giving up does not stop the '
            'work. [[slnc 300]] Why the number matters. [[slnc 300]] One '
            'time budget shared by a whole page. [[slnc 300]] And the '
            'bill: not knowing what happened.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A product page asks the supplier', 'how many mugs are left.', '', 'Usually: 50 milliseconds.', 'Sometimes: never.', '', 'How long should the page wait?'],
        narration=(
            'Here is the scenario. [[slnc 400]] A product page asks the '
            "supplier's stock service how many mugs are left. [[slnc "
            '500]] Usually, the answer comes in fifty milliseconds. '
            '[[slnc 300]] Sometimes, it never comes at all. [[slnc 500]] '
            'So here is the question. [[slnc 300]] How long should the '
            'page wait?'
        ),
    ),
    dict(
        key='03-none', kind='console', title='No Timeout',
        body="""ONE. No timeout.
  the supplier never answers.
  the page's thread: WAITING,
  with no limit.

  the customer sees a spinner.""",
        narration=(
            'First demo: no timeout. [[slnc 400]] The supplier never '
            "answers. [[slnc 500]] The product page's thread is waiting. "
            '[[slnc 300]] A thread is a worker that handles one request '
            'at a time. [[slnc 300]] And nothing in the code says how '
            'long to wait. [[slnc 300]] There is no limit. [[slnc 600]] '
            'The customer is looking at a spinning wheel. [[slnc 300]] '
            'And every thread stuck like this is one nobody else can use.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Decide how long you will wait.', '', 'When the time is up, stop', 'waiting, and do something else:', 'an answer you can live with.', '', 'The limit belongs to the caller,', 'not the service.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Decide how long you will '
            'wait. [[slnc 300]] When the time is up, stop waiting. [[slnc '
            '300]] And do something else: show an answer you can live '
            'with. [[slnc 500]] The limit belongs to the caller, not to '
            'the service.'
        ),
    ),
    dict(
        key='05-limit', kind='console', title='A Limit On The Wait',
        body="""TWO. A limit.
  limit: 100 milliseconds.
  the page shows: stock
  unknown, try again shortly.

  it loaded, without the
  number it could not get.""",
        narration=(
            'Second demo: a limit on the wait. [[slnc 400]] The same '
            'call, with a limit of a hundred milliseconds. [[slnc 500]] '
            'The page shows: stock unknown, try again shortly. [[slnc '
            '300]] The page loaded, without the one number it could not '
            'get. [[slnc 500]] An endless wait became a plain answer.'
        ),
    ),
    dict(
        key='06-work', kind='console', title='Giving Up Does Not Stop The Work',
        body="""THREE. Still working.
  the caller gave up.
  started: 1, finished: 0.

  later the supplier finishes
  anyway: finished 1.

  nobody was waiting.""",
        narration=(
            'Third demo: giving up does not stop the work. [[slnc 400]] '
            'The caller gave up. [[slnc 300]] At the supplier, one call '
            'had started, and none had finished. [[slnc 500]] Later, the '
            'supplier finishes it anyway. [[slnc 300]] Nobody was waiting '
            'for the answer. [[slnc 300]] But the work was done all the '
            'same.'
        ),
    ),
    dict(
        key='07-number', kind='console', title='Choosing The Number',
        body="""FOUR. The number.
  50 ms: 54 of 100 succeed.
  100 ms: 90.
  250 ms: 98.
  1000 ms: 98.
  3000 ms: 100.

  too tight fails healthy calls,
  too loose holds a thread.""",
        narration=(
            'Fourth demo: choosing the number. [[slnc 400]] Take a '
            'typical hundred calls. [[slnc 500]] A limit of fifty '
            'milliseconds lets fifty-four succeed. [[slnc 300]] A hundred '
            'milliseconds lets ninety succeed. [[slnc 300]] Two hundred '
            'and fifty lets ninety-eight. [[slnc 300]] And so does one '
            'second. [[slnc 300]] Only three seconds lets all hundred '
            'through. [[slnc 600]] Too tight, and healthy calls fail. '
            '[[slnc 300]] Too loose, and a slow supplier holds a thread '
            'for seconds. [[slnc 300]] So choose the limit from how long '
            'the calls really take.'
        ),
    ),
    dict(
        key='08-budget', kind='console', title='One Budget For The Page',
        body="""FIVE. A budget.
  3 calls, each allowed 1000 ms:
  worst case 3000 ms.

  one budget of 1000 ms, shared:
  call 1: answered, 400.
  call 2: cut off, 600.
  call 3: skipped.""",
        narration=(
            'Fifth demo: one budget for the whole page. [[slnc 400]] A '
            'page makes three supplier calls, one after another. [[slnc '
            '300]] Each is allowed one second. [[slnc 300]] So in the '
            'worst case, the page takes three seconds. [[slnc 600]] Now '
            'give the page one budget of one second, shared by all three '
            'calls. [[slnc 500]] The first call is answered, using four '
            'hundred milliseconds. [[slnc 300]] The second call is cut '
            'off, after the remaining six hundred. [[slnc 300]] The third '
            'is skipped. [[slnc 300]] One second in total.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill: You Do Not Know What Happened',
        body="""SIX. The bill.
  the payment call timed out.
  the customer: not taken.

  the provider then completed
  the charge: taken 1.

  a timeout says only that you
  stopped waiting.""",
        narration=(
            'Finally, the bill. [[slnc 400]] A payment call times out. '
            '[[slnc 300]] So the customer is told: we could not take your '
            'payment. [[slnc 500]] Then the payment provider completes '
            'the charge anyway. [[slnc 300]] The money was taken, and the '
            'customer thinks it was not. [[slnc 600]] A timeout only '
            'tells you that you stopped waiting. [[slnc 300]] It says '
            'nothing about what actually happened. [[slnc 300]] And '
            'retrying that payment, without an idempotency key to spot '
            'the repeat, would charge the customer again.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Future.get(timeout, unit) and', 'CompletableFuture.orTimeout.', '', 'A connectTimeout and a readTimeout', 'on an HTTP client.', '', 'A TimeoutException or an HTTP 504', 'in a log.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for Java waits that are given a time '
            'limit. [[slnc 300]] Look for a connect timeout and a read '
            'timeout on a web client. [[slnc 300]] Look for timeout '
            'errors in a log, or a web gateway timeout, error five oh '
            'four. [[slnc 300]] Or a time limiter from a library such as '
            'Resilience four J.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Put a timeout on every call to', 'another system, chosen from how', 'long the calls really take, and', "set it on the caller's side. Share", 'one budget across a chain of', 'calls. Decide what to show when', 'time runs out. And never treat a', 'timeout as a failure of the', 'operation: it may have happened,'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Put a timeout on every '
            'call to another system. [[slnc 300]] Choose it from how long '
            'the calls really take. [[slnc 300]] And set it on the '
            "caller's side. [[slnc 500]] Share one time budget across a "
            'chain of calls. [[slnc 300]] Decide what to show when time '
            'runs out. [[slnc 500]] And never treat a timeout as proof '
            'that the operation failed. [[slnc 300]] It may have '
            'happened. [[slnc 300]] So make the operation safe to check '
            'on, or to repeat.'
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
        body=['A timeout is never too much. The', 'cost is choosing it well, and', 'handling the case where it fires.'],
        narration=(
            'So, when is this too much? [[slnc 400]] A timeout is never '
            'too much. [[slnc 300]] The cost is choosing it well, and '
            'handling what happens when it runs out.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Timeout pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] A timeout stops you '
            'waiting, but it does not stop the work, or tell you whether '
            'it happened. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            "is one exercise to try. [[slnc 300]] Change the page's "
            'budget to two seconds. [[slnc 300]] Then see which of the '
            'three calls are cut off. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
