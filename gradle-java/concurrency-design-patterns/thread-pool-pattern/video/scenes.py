"""Scene definitions for the Thread Pool teaching video.

Each scene has: key, title, kind, body, narration.

Same discipline as the Producer-Consumer video before it: narration names
the threads -- "the worker", "the submitting thread" -- speaks counts and
outcomes out loud, and never points at a picture the listener cannot see.
This project reuses that one's harness and its packing scenario, so several
scenes lean on "the same failure, from a different side" rather than
re-teaching what a listener who watched that video already has.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="Thread Pool",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Thread Pool "
            "pattern in Java, and it is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] The plain definition: a "
            "fixed, small number of worker threads is created once and "
            "reused for every task handed to it, pulling from a queue "
            "whose own capacity is also chosen on purpose. [[slnc 350]] "
            "This is the second project in the concurrency category, and "
            "it picks up exactly where the first one left off. That "
            "project built a bounded queue and one packer thread; this "
            "one asks what happens the moment there is more than one "
            "packer, and shows that a fixed number of workers, on its "
            "own, is only half the fix. [[slnc 300]] By the end you will "
            "know why the JDK's own default thread pool factory hides an "
            "unbounded queue, you will have watched a genuine deadlock "
            "that a fixed pool can reach at any size, and you will know "
            "exactly what Java's virtual threads do and do not change "
            "about any of it."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario, Continued",
        body=[
            "Same shop. Orders arrive at checkout, and a",
            "packing step handles each one.",
            "",
            "The last video gave that job to one packer",
            "thread. This one gives it to a team.",
            "",
            "A team needs two bounds, not one: how many",
            "packers, and how many orders may wait for them.",
        ],
        narration=(
            "Same shop, same orders, same packing step. Last time, "
            "exactly one packer thread did all the work, pulling from a "
            "bounded queue. [[slnc 300]] This time, the packer becomes a "
            "team -- more than one worker thread, sharing the work. And a "
            "team, it turns out, needs two separate decisions, not one: "
            "how many packers are on shift, and how many orders are "
            "allowed to wait for them before somebody says no. [[slnc "
            "300]] Losing track of that second bound is this whole "
            "video's first lesson, and it is easier to lose than it "
            "sounds."
        ),
    ),
    dict(
        key="03-thread-per-order",
        kind="console",
        title="Naive One — A Thread Per Order, Again",
        body="""ONE. A thread per order.
  created 2,000 real threads in 98.1ms
  (49.1 microseconds each)

  every thread is live and holding a
  stack until its order is packed --
  nothing caps how many pile up.""",
        narration=(
            "The first naive version is not new -- it is the identical "
            "failure the last video measured, seen from the packing "
            "team's side this time. Every order gets its own brand new "
            "thread. [[slnc 300]] Two thousand real threads, created in "
            "under a hundred milliseconds. Fast, and completely "
            "unbounded -- exactly the number from last time, quoted "
            "again here on purpose, because act six is going to put a "
            "very different number right next to it."
        ),
    ),
    dict(
        key="04-unbounded-trap",
        kind="console",
        title="Naive Two — The Queue Nobody Chose",
        body="""TWO. A fixed pool, an unbounded queue.
  2 workers, both provably busy;
  500 more orders submitted

  Executors.newFixedThreadPool never
  blocked and never rejected once

  backlog waiting behind the 2 busy
  workers: 500""",
        narration=(
            "Here is the fix most people reach for, and it looks right. "
            "Executors dot new Fixed Thread Pool of two: exactly two "
            "worker threads, created once, reused for everything. "
            "[[slnc 300]] Watch what happens underneath it, though. Both "
            "workers are confirmed busy -- parked deliberately, so this "
            "is certain, not guessed -- and five hundred more orders are "
            "submitted on top. Every single one is accepted immediately. "
            "[[slnc 350]] That factory method hands its two workers an "
            "unbounded queue, with no argument anywhere to change it. "
            "Five hundred orders are now waiting, invisibly, and nothing "
            "printed that number until this demo went looking for it on "
            "purpose. A fixed worker count is not the same promise as a "
            "fixed pool."
        ),
    ),
    dict(
        key="05-the-pattern",
        kind="bullets",
        title="The Pattern: Two Bounds, Not One",
        body=[
            "A fixed number of workers, created once",
            "and reused -- exactly like the naive version.",
            "",
            "PLUS a queue with its own fixed capacity,",
            "built directly rather than left to a default.",
            "",
            "Both bounds are constructor arguments.",
            "Neither one is a number the JDK picked for you.",
        ],
        narration=(
            "So here is the actual pattern, and it is one sentence with "
            "two halves. A fixed number of worker threads, created once "
            "and reused -- that part the naive version already had "
            "right. And a queue with its own fixed capacity, standing "
            "in front of them, refusing work once it is full. [[slnc "
            "300]] Both numbers are arguments you choose, not defaults "
            "the JDK chose for you three versions ago. That is the "
            "entire difference between this pattern and the trap in the "
            "previous scene."
        ),
    ),
    dict(
        key="06-capacity",
        kind="console",
        title="The Queue At Capacity — And No Patience For It",
        body="""THREE. One worker, queue capacity three.
  1 worker busy, queue filled to
  capacity 3: 3

  one more order, submitted with the
  worker busy and the queue full:
  REJECTED on the spot -- no patience
  window, no room""",
        narration=(
            "One worker this time, and a queue capacity of three, both "
            "forced the same careful way the last video forced its own "
            "queue -- the worker parked deliberately, confirmed busy by "
            "a latch, before a single real order goes in. Three orders "
            "fill the queue exactly to its bound. [[slnc 300]] A fourth "
            "is submitted, and here is the detail worth pausing on. "
            "Last video's bounded queue offered a hundred and fifty "
            "milliseconds of patience before giving up. This pool has "
            "none. The moment every worker is busy and the queue is "
            "full, the rejection happens synchronously, on the calling "
            "thread, before the submit call even returns. There is no "
            "waiting, no retrying, nothing free -- if you want a "
            "patience window here, you write it yourself, on top."
        ),
    ),
    dict(
        key="07-sizing",
        kind="bullets",
        title="Sizing Is A Real Decision, Both Directions",
        body=[
            "Too few workers: the backlog from act two",
            "grows by five hundred before anyone asks why.",
            "",
            "Too many workers: each one is a stack held",
            "open, whether or not there is work for it --",
            "the same cost act one measured, merely capped.",
            "",
            "There is no size that is free.",
        ],
        narration=(
            "Choosing how many workers to run is a real decision, and it "
            "is wrong in both directions. [[slnc 300]] Too few, and the "
            "backlog from act two happens -- five hundred orders "
            "queued, silently, before anyone thinks to ask why the "
            "shop feels slow. [[slnc 300]] Too many, and each idle "
            "worker is still a thread holding a stack for nothing, the "
            "exact cost act one measured, just capped at a number "
            "somebody has to pick. There is no size here that is free -- "
            "only a size chosen on purpose, the same two words this "
            "whole pattern keeps coming back to."
        ),
    ),
    dict(
        key="08-starvation",
        kind="console",
        title="Pool Starvation — A Deadlock At Any Size",
        body="""FIVE. A fixed pool of one.
  the running task submits a second
  task to that same pool, and waits
  for its result

  no free worker will ever run it

  starved: true, rescued after 210ms
  by a demonstration timeout -- left
  alone, this never resolves""",
        narration=(
            "Now a failure that has nothing to do with either bound "
            "being too small. A task running inside a pool of exactly "
            "one worker submits a second task to that very same pool, "
            "and then waits for its result. [[slnc 300]] Think about "
            "what has to happen for that wait to end. Some worker has to "
            "pick up the second task. There is exactly one worker, and "
            "it is the one doing the waiting. The second task can never "
            "be scheduled -- not eventually, not with a bigger queue, "
            "not ever. [[slnc 350]] This demo rescues itself with a "
            "timeout so it can finish and tell you what happened, but "
            "that timeout is not the pool's patience -- it is only the "
            "demonstration's own escape hatch. Left alone, a real "
            "service in this state hangs until somebody notices every "
            "thread reads as busy while doing nothing at all, which is a "
            "far worse debugging session than a failed test."
        ),
    ),
    dict(
        key="09-lost-update",
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
            "This project's determinism does not come from a new "
            "mechanism -- it is the same three harness pieces from the "
            "first video, copied unchanged, proven again here before "
            "anything else relies on them. [[slnc 300]] The smallest "
            "proof: two threads each read a shared stock count of ten, "
            "meet at a rendezvous that will not release either one until "
            "both have arrived, and only then write back what they read, "
            "minus one. [[slnc 350]] Run it twenty times, and the answer "
            "is nine, twenty times -- never eight, because both threads "
            "are provably standing on the same stale read before either "
            "one writes. The pool-starvation deadlock a moment ago "
            "needed none of this forcing, and that is worth noticing: "
            "one worker waiting on itself has exactly one outcome, on "
            "every scheduler, with nothing to force at all."
        ),
    ),
    dict(
        key="10-scheduler",
        kind="bullets",
        title="What The Scheduler Really Does",
        body=[
            "Every demonstrated number is bought by pinning",
            "one interleaving on purpose -- except one.",
            "",
            "Pool starvation needs no forcing: one worker",
            "waiting on itself has exactly one outcome.",
            "",
            "Everywhere else, the real scheduler is free",
            "to choose which worker runs which task, and when.",
        ],
        narration=(
            "The same honest admission the first video made, required "
            "again here. Almost every number in this video is bought by "
            "pinning one specific interleaving with a gate or a latch -- "
            "the real scheduler is free to hand any queued task to "
            "either worker, in whatever order it likes. [[slnc 300]] "
            "Pool starvation is the one exception worth naming directly. "
            "It needed no forcing at all, because a pool of exactly one "
            "worker waiting on itself has exactly one possible outcome, "
            "regardless of what the scheduler does with anything else in "
            "the program. A passing test elsewhere in this project "
            "proves the forced interleaving behaves as shown -- not that "
            "every schedule does."
        ),
    ),
    dict(
        key="11-virtual-threads",
        kind="console",
        title="Java's Answer — And What It Does Not Answer",
        body="""SIX. Virtual threads, same count as act one.
  created 2,000 virtual threads in
  11.4ms (5.68 microseconds each)

  compare act one: 98.1ms, real
  platform threads, same measurement

  a pool still bounds a resource,
  not a thread count""",
        narration=(
            "One more comparison, and the numbers do the talking. The "
            "exact same flood of two thousand threads from act one, run "
            "again with Java 21's virtual threads instead of platform "
            "ones. [[slnc 300]] Eleven milliseconds, against ninety "
            "eight. A virtual thread does not hold a dedicated operating "
            "system thread the whole time it exists, only while it is "
            "actually running unblocked, which is why creating a huge "
            "number of them barely registers. [[slnc 350]] Here is the "
            "honest limit of that number, though. It says nothing about "
            "act three's pool. A downstream resource with ten "
            "connections available still has ten, whether a handful of "
            "platform threads or a million virtual ones are asking for "
            "one. Cheap thread creation retires the old argument for "
            "pooling threads purely to avoid that cost -- it does not "
            "retire the pool itself."
        ),
    ),
    dict(
        key="12-bill",
        kind="bullets",
        title="The Bill",
        body=[
            "Rejection here has no patience window --",
            "it is instant, or it does not happen at all.",
            "",
            "Nesting a submit-and-wait inside a pool it",
            "already belongs to is a deadlock, at any size.",
            "",
            "Sizing the pool has no free answer, either way.",
        ],
        narration=(
            "Every project in this category pays a bill honestly, and "
            "here is this one's. [[slnc 300]] Rejection has no patience "
            "window built in -- it happens the instant the pool is full, "
            "in the caller's own thread, or it does not happen at all. "
            "If a real service wants to wait a little before giving up, "
            "that waiting is code somebody has to write on top. [[slnc "
            "300]] Nesting a submit-and-wait inside the very pool "
            "already running the outer task is a deadlock waiting for "
            "the wrong day -- it happens on every schedule, at every "
            "pool size, the moment that nesting occurs. [[slnc 300]] And "
            "sizing the pool, in both directions, has no free answer "
            "either -- there is only a size chosen on purpose."
        ),
    ),
    dict(
        key="13-too-much",
        kind="bullets",
        title="When This Is Too Much",
        body=[
            "Worth it: more than one worker genuinely",
            "helps -- parallel CPU work, or blocking I/O",
            "under the traditional platform-thread model.",
            "",
            "Not worth it: a single background task that",
            "runs once. A pool sized for concurrency it",
            "will never use is ceremony with nothing to bound.",
        ],
        narration=(
            "So when does this pattern actually earn its place? [[slnc "
            "300]] Worth it the moment more than one worker genuinely "
            "helps -- CPU-bound work that can run in parallel, or "
            "blocking I-O work under Java's traditional platform-thread "
            "model, where thread creation cost is real money. [[slnc "
            "300]] Not worth it for a single background task that runs "
            "once and finishes. A pool sized for concurrency it will "
            "never use is ceremony with nothing left to bound."
        ),
    ),
    dict(
        key="14-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Try changing the pool starvation",
            "demo from one worker to two, and predict the outcome",
            "before you run it.",
        ],
        narration=(
            "That's Thread Pool. [[slnc 250]] If you take one sentence "
            "away, take this one: a fixed number of workers is only half "
            "the pattern -- the queue behind them needs a bound too, or "
            "you have simply moved where the unbounded growth happens. "
            "[[slnc 350]] The full source, the written notes, the "
            "diagrams and an animated walkthrough are all in the "
            "repository, running offline with nothing installed but a "
            "Java development kit. [[slnc 300]] If you try one exercise, "
            "try this. Change the pool-starvation demo's worker count "
            "from one to two, predict what happens before you run it, "
            "and then check whether you were right. [[slnc 300]] If this "
            "helped, a like genuinely does help other people find it, "
            "and subscribe if you would like the rest of the series. "
            "[[slnc 250]] Thanks for watching, and I'll see you in the "
            "next one."
        ),
    ),
]
