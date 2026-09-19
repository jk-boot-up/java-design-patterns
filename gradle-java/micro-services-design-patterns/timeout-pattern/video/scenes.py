"""Scene definitions for the Timeout teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Timeout',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Timeout pattern '
            'in Java, and it is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] The plain definition: a timeout is a '
            'limit on how long you will wait for an answer, so that a '
            'slow or silent service cannot hold you forever. [[slnc 350]] '
            'This is another project in the microservices category, whose '
            'subject is how many small services stay reliable when they '
            'talk to each other. In our online store, the thing that may '
            "never answer is the supplier's stock API. [[slnc 300]] By "
            'the end you will see a call that never returns hold a '
            'thread, see a limit turn that into an answer, see that '
            'giving up does not stop the work, see the choice of number '
            'matter, see one budget shared by a whole page, and see the '
            'bill, which is not knowing what happened.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A product page asks the supplier', 'how many mugs are left.', '', 'Usually: 50 milliseconds.', 'Sometimes: never.', '', 'How long should the page wait?'],
        narration=(
            "Here is the scenario. A product page asks the supplier's "
            'stock API how many mugs are left. Usually the answer comes '
            'in fifty milliseconds. Sometimes it never comes at all. '
            '[[slnc 300]] The question: how long should the page wait?'
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
            'First, no timeout. The supplier never answers. The product '
            "page's thread is waiting, and nothing in the code says for "
            'how long. There is no limit. The customer is looking at a '
            'spinner, and every thread like this one is a thread nobody '
            'else can use.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Decide how long you will wait.', '', 'When the time is up, stop', 'waiting, and do something else:', 'an answer you can live with.', '', 'The limit belongs to the caller,', 'not the service.'],
        narration=(
            'The pattern. Decide how long you will wait. When the time is '
            'up, stop waiting, and do something else: show an answer you '
            'can live with. The limit belongs to the caller, not to the '
            'service.'
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
            'Second, a limit on the wait. The same call, with a limit of '
            'a hundred milliseconds. The page shows: stock unknown, try '
            'again shortly. The page loaded, without the one number it '
            'could not get. A slow answer became a plain one.'
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
            'Third, giving up does not stop the work. The caller gave up. '
            'At the supplier, one call had started, and none had '
            'finished. Later the supplier finishes it anyway. Nobody was '
            'waiting for the answer, and the work was done all the same.'
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
            'Fourth, choosing the number. On a typical hundred calls, a '
            'limit of fifty milliseconds lets fifty four succeed. A '
            'hundred lets ninety. Two hundred and fifty lets ninety '
            'eight, and so does a thousand. Only three seconds lets all '
            'hundred. [[slnc 300]] Too tight, and healthy calls fail. Too '
            'loose, and a slow supplier holds a thread for seconds. '
            'Choose from what the calls really take.'
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
            'Fifth, one budget for the page. A page makes three supplier '
            'calls in a row, each allowed a second, so the worst case is '
            'three seconds. Give the page one budget of a second, shared '
            'by all three. The first call is answered in four hundred. '
            'The second is cut off at six hundred. The third is skipped. '
            'One second, in total.'
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
            'Last, the bill. A payment call times out, and the customer '
            'is told: we could not take your payment. Then the provider '
            'completes the charge anyway. One charge taken, and the '
            'customer thinks nothing was. [[slnc 300]] A timeout says '
            'only that you stopped waiting. It says nothing about what '
            'happened. Retrying a payment without an idempotency key '
            'would charge again.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Future.get(timeout, unit) and', 'CompletableFuture.orTimeout.', '', 'A connectTimeout and a readTimeout', 'on an HTTP client.', '', 'A TimeoutException or an HTTP 504', 'in a log.'],
        narration=(
            'How do you recognise this in code you did not write? '
            'Future.get(timeout, unit) and CompletableFuture.orTimeout. A '
            'connectTimeout and a readTimeout on an HTTP client. A '
            "TimeoutException or an HTTP 504 in a log. Resilience4j's "
            "TimeLimiter, and Spring's @Timeout-style settings."
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Put a timeout on every call to', 'another system, chosen from how', 'long the calls really take, and', "set it on the caller's side. Share", 'one budget across a chain of', 'calls. Decide what to show when', 'time runs out. And never treat a', 'timeout as a failure of the', 'operation: it may have happened,'],
        narration=(
            'Here is my verdict, plainly. Put a timeout on every call to '
            'another system, chosen from how long the calls really take, '
            "and set it on the caller's side. Share one budget across a "
            'chain of calls. Decide what to show when time runs out. And '
            'never treat a timeout as a failure of the operation: it may '
            'have happened, so make the operation safe to ask about or '
            'repeat.'
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
        body=['A timeout is never too much. The', 'cost is choosing it well, and', 'handling the case where it fires.'],
        narration=(
            'So when is it too much? A timeout is never too much. The '
            'cost is choosing it well, and handling the case where it '
            'fires.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Timeout. [[slnc 250]] If you take one sentence away, "
            'take this one: a timeout stops you waiting, and it does not '
            'stop the work or tell you whether it happened. [[slnc 350]] '
            'The full source, the written notes, the diagrams and an '
            'animated walkthrough are all in the repository, running '
            'offline with nothing installed but a Java development kit. '
            '[[slnc 300]] If you try one exercise, change the budget to '
            'two seconds, and see which of the three calls are cut off. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
