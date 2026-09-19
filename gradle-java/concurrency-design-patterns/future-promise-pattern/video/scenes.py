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
            "Hello, and welcome. This video explains the Future and "
            "Promise pattern in Java, and it is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] The plain definition: each "
            "unit of work is submitted and immediately returns a handle "
            "to a result that does not exist yet, so independent work "
            "can run at once instead of one call waiting out the last "
            "before it even starts. [[slnc 350]] This is the third "
            "project in the concurrency category, and it answers a "
            "question the first two left open: once work is handed to a "
            "queue or a pool, how does the caller ever find out what "
            "happened? [[slnc 300]] By the end you will know exactly "
            "which half of a Future and Promise is the reader's and "
            "which is the writer's, you will have watched an exception "
            "surface with a stack trace that does not contain the line "
            "that caused it, and you will know why asking a task to "
            "cancel is a request, never a guarantee."
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
            "Here is the scenario. A product page needs three things "
            "before it can render: the price, the stock count, and a "
            "review score. Each one is a genuine catalogue lookup, and "
            "this video measures each of them at two hundred "
            "milliseconds. [[slnc 300]] Here is the detail worth sitting "
            "with. None of the three depends on either of the other two. "
            "Price does not need the stock count. The review score does "
            "not care what the price is. [[slnc 300]] So the question "
            "this whole video answers is simple: if they do not depend "
            "on each other, why would the code that fetches them make "
            "them wait for each other anyway?"
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
            "The naive version calls all three, one after another, "
            "waiting each one out fully before starting the next. "
            "[[slnc 300]] Six hundred and nineteen milliseconds. Three "
            "lookups, at two hundred milliseconds apiece, simply added "
            "together -- for work that a moment's thought shows has no "
            "reason to be serial at all."
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
            "Here is the fix, and it is one sentence. Each lookup is "
            "submitted and immediately returns a handle to a result that "
            "does not exist yet -- a Future. All three are submitted "
            "before the page asks any of them for a value. [[slnc 300]] "
            "Two hundred and eight milliseconds. Not the sum of three "
            "lookups -- roughly the cost of the single slowest one, "
            "because all three were genuinely running at the same time."
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
            "Before the next demo, one distinction worth making "
            "explicit, because it is genuinely easy to conflate. Java's "
            "CompletableFuture is both halves of this pattern at once. "
            "[[slnc 300]] The Future is the reader's half. Whoever holds "
            "it calls get, and blocks until a value shows up -- and does "
            "not need to know who produces that value, or how. [[slnc "
            "300]] The Promise is the writer's half. Whoever holds it "
            "calls complete, once its own work is genuinely done -- and "
            "does not need to know who is reading, or whether anyone is "
            "reading at all."
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
            "Here is that split, made deliberately explicit, on two "
            "separate threads. A reader thread creates a fresh future "
            "and immediately calls get, blocking. A writer thread, "
            "started at the same moment, does its own work and then "
            "calls complete on that exact same object. [[slnc 300]] The "
            "reader thread unblocks the instant the writer calls "
            "complete -- one piece of code completing exactly what "
            "another piece is waiting on."
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
            "Now the first honest cost. A task that throws does not "
            "throw where it was called. It throws, silently, on "
            "whatever worker thread happened to run it -- and the "
            "failure only surfaces later, wrapped, when something calls "
            "get. [[slnc 300]] Look closely at the stack trace this "
            "produces. It belongs entirely to the worker thread. The "
            "line of code that actually submitted the doomed task is "
            "not on it, and cannot be -- because a stack trace is "
            "captured on one thread, at one moment, and the thread that "
            "submitted this task was somewhere else entirely when it "
            "failed."
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
            "Second honest cost. A task that never completes leaves a "
            "bare get call blocked for as long as the calling thread is "
            "willing to wait -- which, by default, is forever. [[slnc "
            "300]] This demo rescues itself with a two hundred "
            "millisecond timeout, purely so it can finish and tell you "
            "what happened. That timeout is not a nicety sitting on top "
            "of get -- for a task that genuinely never finishes, it is "
            "the only thing standing between waiting and hanging."
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
            "Third honest cost, and the one that surprises people most. "
            "Future dot cancel with true interrupts the thread running "
            "the task. It does not stop the task. [[slnc 300]] This "
            "demo's task catches every interrupt sent its way and simply "
            "carries on -- the exact anti-pattern real code sometimes "
            "writes by accident. Cancel reports true. The task runs to "
            "completion anyway. Cancellation asked; the task said no, "
            "and nothing forced it to listen."
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
            "One more cost, briefly, because it matters without needing "
            "its own demo. CompletableFuture's callback methods -- then "
            "apply, then compose, then combine -- let results chain "
            "together without ever calling get. [[slnc 300]] They are "
            "genuinely powerful in a small example, and genuinely "
            "unreadable by the fourth or fifth chained step -- each "
            "level adds another closure, another indentation, another "
            "place an exception quietly disappears if the matching "
            "handler is forgotten at that one level."
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
            "This project's determinism is not a new mechanism -- it is "
            "the same three harness pieces from the first video, copied "
            "unchanged, proven again here. [[slnc 300]] Two threads each "
            "read a shared stock count of ten, meet at a rendezvous that "
            "will not release either one until both have arrived, and "
            "only then write back what they read, minus one. [[slnc "
            "350]] Run it twenty times, and the answer is nine, twenty "
            "times -- never eight -- because both threads are provably "
            "standing on the same stale read before either one writes."
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
            "The same honest admission every project in this category "
            "makes. Every deterministic outcome you have watched is "
            "bought by pinning one specific fact on purpose -- that a "
            "lookup has genuinely started, that a gate will never open, "
            "that a task has begun the very loop being demonstrated. "
            "[[slnc 300]] The real JVM scheduler chooses freely "
            "everywhere this project does not pin something directly -- "
            "which worker picks up which submitted lookup first, and in "
            "what order. A passing test here proves the forced scenario "
            "behaves as shown -- not that Future and Promise are safe "
            "under every possible schedule a busier machine might "
            "produce."
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
            "Every project in this category pays a bill honestly, and "
            "here is this one's, gathered in one place. [[slnc 300]] "
            "Exceptions move -- surfacing wrapped, later, with a stack "
            "trace that never contains the line that submitted the "
            "doomed task. [[slnc 300]] A bare get with no timeout is not "
            "a long wait -- it is a hang, indistinguishable from one "
            "until something outside the call itself intervenes. [[slnc "
            "300]] And cancel is a request, not a command -- a task has "
            "to actually check for it and choose to stop, and plenty of "
            "real code forgets to."
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
            "So when does this pattern actually earn its place? [[slnc "
            "300]] The moment two or more units of work are genuinely "
            "independent and each takes real, measurable time -- exactly "
            "this video's three catalogue lookups. [[slnc 300]] Not "
            "worth it for two calls that are already fast, or for two "
            "calls where the second genuinely needs the first's result. "
            "There is nothing to overlap, and a Future around work that "
            "was never going to run concurrently with anything is "
            "ceremony with no payoff behind it."
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
            "That's Future and Promise. [[slnc 250]] If you take one "
            "sentence away, take this one: a Future is a promise about "
            "when a value will be ready, never a promise about whether "
            "the work producing it can be stopped once it has started. "
            "[[slnc 350]] The full source, the written notes, the "
            "diagrams and an animated walkthrough are all in the "
            "repository, running offline with nothing installed but a "
            "Java development kit. [[slnc 300]] If you try one exercise, "
            "try this. Remove the timeout from act five's get call, "
            "read the code carefully, and think hard about what would "
            "happen before you actually run it. [[slnc 300]] If this "
            "helped, a like genuinely does help other people find it, "
            "and subscribe if you would like the rest of the series. "
            "[[slnc 250]] Thanks for watching, and I'll see you in the "
            "next one."
        ),
    ),
]
