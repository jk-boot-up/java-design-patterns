"""Scene definitions for the Future/Promise teaching video.

Each scene has: key, title, kind, body, narration.

Same discipline as the two videos before it in this category: narration
names the threads -- "the reader thread", "the writer thread" -- speaks
timings and outcomes out loud, and never points at a picture the listener
cannot see.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="Future/Promise",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Future and Promise pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] When you start a piece of '
            'work, you immediately get back a handle to a result that '
            'does not exist yet. [[slnc 300]] That handle is called a '
            'future. [[slnc 400]] So independent pieces of work can run '
            'at the same time, instead of each one waiting for the last. '
            '[[slnc 600]] Think of a coffee shop buzzer. [[slnc 300]] You '
            'order, and get a buzzer straight away. [[slnc 300]] You sit '
            'down, and the buzzer tells you when your coffee is ready. '
            '[[slnc 700]] In our online store, a product page needs three '
            'separate lookups. [[slnc 500]] By the end, you will know '
            'which half of this pattern belongs to the reader, and which '
            'to the writer. [[slnc 300]] You will hear an error whose '
            'report does not mention the line that caused it. [[slnc '
            '300]] And you will learn why cancelling a task is only a '
            'request.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "A product page needs three things: price,",
            "stock, and a review score. Each is a real",
            "lookup, and this video measures each at 200ms.",
            "",
            "None of the three depends on either of the",
            "other two.",
            "",
            "So why does the naive version make them wait",
            "for each other anyway?",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] A product page needs '
            'three things before it can appear. [[slnc 300]] The price, '
            'the stock count, and a review score. [[slnc 400]] Each is a '
            'real lookup, and each takes about two hundred milliseconds. '
            '[[slnc 500]] Here is the key detail. [[slnc 300]] None of '
            'the three depends on the others. [[slnc 300]] The price does '
            'not need the stock count. [[slnc 300]] The review score does '
            'not care about the price. [[slnc 500]] So why would the code '
            'make them wait for each other?'
        ),
    ),
    dict(
        key="03-sequential",
        kind="console",
        title="Naive — Sequential Lookups",
        body="""ONE. Sequential.
  price £129.99, stock 7, rating 4.6

  rendered in 619ms -- three lookups,
  none depending on the others, paid
  for one after another anyway.""",
        narration=(
            'First, the naive version. [[slnc 400]] It calls all three '
            'lookups, one after another. [[slnc 300]] It waits for each '
            'to finish before starting the next. [[slnc 500]] The page '
            'takes six hundred and nineteen milliseconds. [[slnc 300]] '
            'Three lookups of two hundred milliseconds each, simply added '
            'together. [[slnc 300]] For work that has no reason to wait '
            'at all.'
        ),
    ),
    dict(
        key="04-concurrent",
        kind="console",
        title="The Pattern — Concurrent Lookups",
        body="""TWO. Concurrent.
  price £129.99, stock 7, rating 4.6

  rendered in 208ms -- roughly one
  lookup's cost, not three.""",
        narration=(
            'Now the fix, in one sentence. [[slnc 400]] Each lookup is '
            'started, and immediately returns a future. [[slnc 300]] All '
            'three are started before the page asks any of them for its '
            'value. [[slnc 500]] The page now takes two hundred and eight '
            'milliseconds. [[slnc 300]] Not the sum of three lookups. '
            '[[slnc 300]] Roughly the time of the slowest one, because '
            'all three really ran at the same time.'
        ),
    ),
    dict(
        key="05-future-promise",
        kind="bullets",
        title="The Two Halves Beginners Conflate",
        body=[
            "A CompletableFuture is both halves at once,",
            "which is exactly why it is easy to conflate.",
            "",
            "The Future: the reader's half. Calls get(),",
            "and blocks until a value shows up.",
            "",
            "The Promise: the writer's half. Calls",
            "complete(value), once its own work is done.",
        ],
        narration=(
            'Before the next demo, one important distinction. [[slnc '
            "400]] Java's Completable Future holds both halves of this "
            'pattern at once. [[slnc 300]] That is why they are easy to '
            "mix up. [[slnc 500]] The future is the reader's half. [[slnc "
            '300]] Whoever holds it calls get, and waits until a value '
            'appears. [[slnc 300]] It does not need to know who produces '
            "the value. [[slnc 500]] The promise is the writer's half. "
            '[[slnc 300]] Whoever holds it calls complete, once its work '
            'is done. [[slnc 300]] It does not need to know who is '
            'reading, or whether anyone is.'
        ),
    ),
    dict(
        key="06-handoff-demo",
        kind="console",
        title="Future And Promise, Made Explicit",
        body="""THREE. Future and Promise.
  the writer thread completed the
  promise: £129.99

  the reader thread was blocked on
  the future until it did.""",
        narration=(
            'Third demo: the two halves, on two separate threads. [[slnc '
            '400]] A reader thread creates a future, and immediately '
            'calls get. [[slnc 300]] So it waits. [[slnc 400]] At the '
            'same moment, a writer thread does its own work. [[slnc 300]] '
            'Then it calls complete on that very same object, with the '
            'price: one hundred and twenty-nine pounds ninety-nine. '
            '[[slnc 500]] The reader wakes up the instant the writer '
            'completes it. [[slnc 300]] One piece of code fills in '
            'exactly what another piece is waiting for.'
        ),
    ),
    dict(
        key="07-exceptions-move",
        kind="console",
        title="Exceptions Move",
        body="""FOUR. Exceptions move.
  cause: catalogue unavailable

  stack top: ProductPageDemo dot
  lambda, on the worker thread

  the call site that submitted this
  task appears nowhere above.""",
        narration=(
            'Now the first honest cost. [[slnc 400]] A task that fails '
            'does not fail where it was started. [[slnc 300]] It fails '
            'quietly, on whichever worker thread ran it. [[slnc 300]] The '
            'error only appears later, wrapped up, when someone calls '
            "get. [[slnc 500]] And the error's stack trace belongs "
            'entirely to the worker thread. [[slnc 300]] The line of code '
            'that started the task is not in it. [[slnc 300]] It cannot '
            'be, because a stack trace records one thread, at one moment. '
            '[[slnc 300]] And the thread that started the task was '
            'somewhere else entirely when it failed.'
        ),
    ),
    dict(
        key="08-hang",
        kind="console",
        title="get() With No Timeout Is A Hang",
        body="""FIVE. The hang.
  a task parked forever, waited on
  with a 200ms rescue timeout:

  timed out: true, after 205ms

  a bare get() with no timeout does
  not time out -- it just never
  returns.""",
        narration=(
            'The second honest cost. [[slnc 400]] A task that never '
            'finishes leaves a plain get call waiting for as long as the '
            'thread is willing. [[slnc 300]] And by default, that is '
            'forever. [[slnc 500]] This demo protects itself with a two '
            'hundred millisecond timeout, so it can finish, and report '
            'what happened. [[slnc 300]] It timed out after about two '
            'hundred and five milliseconds. [[slnc 500]] That timeout is '
            'not a nice extra. [[slnc 300]] For a task that never '
            'finishes, it is the only difference between waiting, and '
            'hanging forever.'
        ),
    ),
    dict(
        key="09-cancellation",
        kind="console",
        title="Cancellation Is Cooperative",
        body="""SIX. Cancellation.
  cancel(true) reported: true

  the task ran to completion anyway:
  true

  it caught every interrupt and
  carried on -- cancel asked; the
  task said no.""",
        narration=(
            'The third honest cost surprises people most. [[slnc 400]] '
            'Calling cancel with true interrupts the thread running the '
            'task. [[slnc 300]] But it does not stop the task. [[slnc '
            '500]] In this demo, the task catches every interruption, and '
            'simply carries on. [[slnc 300]] Real code sometimes does '
            'this by accident. [[slnc 500]] Cancel reports success. '
            '[[slnc 300]] And the task runs to the end anyway. [[slnc '
            '300]] Cancel asked, the task said no, and nothing forced it '
            'to listen.'
        ),
    ),
    dict(
        key="10-callback-depth",
        kind="bullets",
        title="One More Cost: Chained Callbacks",
        body=[
            "thenApply, thenCompose, thenCombine -- each",
            "one adds a closure, an indentation, a place",
            "an exception can be silently swallowed.",
            "",
            "Powerful in a small example. Unreadable by",
            "the fourth or fifth chained step.",
        ],
        narration=(
            'One more cost, briefly. [[slnc 400]] Completable Future has '
            'methods like then apply, then compose, and then combine. '
            '[[slnc 300]] They let results flow from one step to the '
            'next, without ever calling get. [[slnc 500]] In a small '
            'example, they are powerful. [[slnc 300]] But by the fourth '
            'or fifth step, they become hard to read. [[slnc 300]] Each '
            'step adds another nested function. [[slnc 300]] And another '
            'place where an error can quietly disappear, if a handler is '
            'forgotten.'
        ),
    ),
    dict(
        key="11-lost-update",
        kind="code",
        title="The Same Harness, Proven Again",
        body="""int[] stock = {10};
Rendezvous bothRead = new Rendezvous(2);

Runnable decrement = () -> {
    int seen = stock[0];
    bothRead.meet();      // forces the race
    stock[0] = seen - 1;
};
// two threads, same code: result is always 9.
// (two decrements. one is lost. every run.)""",
        narration=(
            'How does the demo make its results repeatable? [[slnc 400]] '
            'With the same small tools used across these concurrency '
            'videos. [[slnc 500]] For example: two threads each read a '
            'shared stock count of ten. [[slnc 300]] Then they meet at a '
            'meeting point, which releases neither until both have '
            'arrived. [[slnc 300]] Only then does each write back what it '
            'read, minus one. [[slnc 500]] Run it twenty times, and the '
            'answer is nine, twenty times, never eight. [[slnc 300]] '
            'Because both threads are proven to hold the same old value '
            'before either writes.'
        ),
    ),
    dict(
        key="12-scheduler",
        kind="bullets",
        title="What The Scheduler Really Does",
        body=[
            "Every demonstrated number is bought by pinning",
            "one specific fact on purpose -- a lookup has",
            "started, a gate will never open, a task has",
            "begun its loop.",
            "",
            "The real scheduler chooses freely everywhere",
            "this project does not pin something directly.",
        ],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] Every '
            'repeatable result was made repeatable on purpose. [[slnc '
            '300]] A lookup is proven to have started. [[slnc 300]] A '
            'gate is set never to open. [[slnc 300]] A task is proven to '
            'be inside its loop. [[slnc 500]] Everywhere else, the '
            'operating system decides freely which thread runs when. '
            '[[slnc 300]] So a passing test proves the forced scene, not '
            'every possible timing.'
        ),
    ),
    dict(
        key="13-bill",
        kind="bullets",
        title="The Bill",
        body=[
            "Exceptions move -- surfacing wrapped, later,",
            "with a stack trace that omits the caller.",
            "",
            "get() with no timeout is a hang, not a wait.",
            "",
            "cancel() is a request a task is free to ignore.",
        ],
        narration=(
            'Here are the costs, gathered in one place. [[slnc 500]] One. '
            '[[slnc 200]] Errors move. [[slnc 300]] They appear later, '
            'wrapped up, and their stack trace never includes the line '
            'that started the task. [[slnc 500]] Two. [[slnc 200]] A '
            'plain get with no timeout is not a long wait. [[slnc 300]] '
            'It can be a hang. [[slnc 500]] Three. [[slnc 200]] Cancel is '
            'a request, not a command. [[slnc 300]] A task must check for '
            'it, and choose to stop. [[slnc 300]] Plenty of real code '
            'forgets.'
        ),
    ),
    dict(
        key="14-too-much",
        kind="bullets",
        title="When This Is Too Much",
        body=[
            "Worth it: two or more genuinely independent",
            "calls, each taking real, measurable time.",
            "",
            "Not worth it: calls that are already fast, or",
            "where the second genuinely needs the first's",
            "result. There is nothing to overlap.",
        ],
        narration=(
            'So, when is this pattern worth it? [[slnc 400]] When two or '
            'more pieces of work are truly independent, and each takes '
            'real, measurable time. [[slnc 300]] Exactly like this '
            "video's three lookups. [[slnc 500]] It is not worth it for "
            'calls that are already fast. [[slnc 300]] Or when the second '
            "call needs the first call's result. [[slnc 300]] Then there "
            'is nothing to overlap.'
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Try removing the timeout from",
            "act five's get() call, and think hard before you",
            "actually run it.",
        ],
        narration=(
            "That's the Future and Promise pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'future promises when a value will be ready, but never that '
            'the work behind it can be stopped. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Remove the timeout from '
            "the hanging demo's get call. [[slnc 300]] Read the code "
            'carefully, and work out what would happen, before you run '
            'it. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
