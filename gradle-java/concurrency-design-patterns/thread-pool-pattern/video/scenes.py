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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Thread Pool pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A thread pool creates a '
            'small, fixed number of worker threads once. [[slnc 300]] '
            'Then it reuses them for every task. [[slnc 300]] Tasks wait '
            "in a queue, and that queue's size limit is also chosen on "
            'purpose. [[slnc 600]] Think of a taxi rank with ten taxis. '
            '[[slnc 300]] The same ten cars carry passenger after '
            'passenger. [[slnc 300]] And the waiting line has a limit, '
            'too. [[slnc 700]] In our online store, a team of packers '
            'handles incoming orders. [[slnc 500]] By the end, you will '
            "know why Java's most popular pool factory hides a queue with "
            'no limit. [[slnc 300]] You will hear a real deadlock that a '
            'pool of any size can reach. [[slnc 300]] And you will know '
            "what Java's virtual threads do, and do not, change."
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
            'Here is the scenario. [[slnc 400]] Orders arrive at '
            'checkout, and a packing step handles each one. [[slnc 500]] '
            'Now the packing is done by a team of worker threads, sharing '
            'the work. [[slnc 400]] And a team needs two separate '
            'decisions, not one. [[slnc 300]] How many packers are on '
            'shift. [[slnc 300]] And how many orders may wait for them, '
            'before someone says no. [[slnc 500]] Forgetting that second '
            "limit is this video's first lesson."
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
            'First, the naive way: a new thread for every order. [[slnc '
            '400]] Two thousand real threads are created in under a '
            'hundred milliseconds. [[slnc 300]] About forty-nine '
            'microseconds each. [[slnc 500]] Fast, but completely '
            'unlimited. [[slnc 300]] Every thread stays alive, holding '
            'its own memory, until its order is packed. [[slnc 300]] '
            'Nothing limits how many pile up.'
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
            'Here is the fix most people reach for, and it looks right. '
            "[[slnc 400]] Java's new Fixed Thread Pool, with two workers. "
            '[[slnc 300]] Exactly two threads, created once, and reused. '
            '[[slnc 500]] But listen to what happens underneath. [[slnc '
            '300]] Both workers are proven to be busy. [[slnc 300]] Then '
            'five hundred more orders are submitted. [[slnc 300]] Every '
            'single one is accepted immediately. [[slnc 500]] That '
            'factory gives its workers a queue with no limit, and no way '
            'to change it. [[slnc 300]] Five hundred orders are now '
            'waiting, invisibly. [[slnc 300]] And nothing reported it, '
            'until this demo went looking. [[slnc 500]] A fixed number of '
            'workers is not the same as a fixed pool.'
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
            'So here is the real pattern, in two halves. [[slnc 500]] '
            'First, a fixed number of worker threads, created once, and '
            'reused. [[slnc 300]] The naive version already got that part '
            'right. [[slnc 500]] Second, a queue in front of them, with '
            'its own fixed limit. [[slnc 300]] Once it is full, it '
            'refuses new work. [[slnc 500]] Both numbers are choices you '
            'make. [[slnc 300]] Not defaults someone else chose for you.'
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
            'Third demo: a full queue, and no patience. [[slnc 400]] This '
            'time there is one worker, and a queue that holds three. '
            '[[slnc 300]] The worker is held busy on purpose, and a latch '
            'confirms it. [[slnc 300]] Then three orders fill the queue '
            'exactly. [[slnc 500]] A fourth order is submitted. [[slnc '
            '300]] And it is refused instantly, before the submit call '
            'even returns. [[slnc 500]] There is no waiting period, and '
            'no retry. [[slnc 300]] If you want the caller to wait a '
            'little before giving up, you must write that yourself.'
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
            'Choosing how many workers to run is a real decision, and it '
            'can be wrong both ways. [[slnc 500]] Too few, and orders '
            'pile up silently, like the five hundred we just heard, '
            'before anyone asks why the shop feels slow. [[slnc 500]] Too '
            'many, and every idle worker still holds its own memory, for '
            'nothing. [[slnc 300]] The same cost as a thread per order, '
            'just capped. [[slnc 500]] There is no free size. [[slnc '
            '300]] Only a size chosen on purpose.'
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
            'Fourth demo: a failure that has nothing to do with the '
            'limits. [[slnc 400]] A pool has exactly one worker. [[slnc '
            '300]] A task running on that worker submits a second task to '
            'the same pool. [[slnc 300]] Then it waits for the second '
            "task's result. [[slnc 600]] Think about what must happen for "
            'that wait to end. [[slnc 300]] Some worker must run the '
            'second task. [[slnc 300]] But there is only one worker, and '
            'it is the one waiting. [[slnc 300]] So the second task can '
            'never run. [[slnc 300]] Not eventually, not with a bigger '
            'queue, not ever. [[slnc 500]] This is called pool '
            'starvation. [[slnc 300]] The demo rescues itself with a '
            'timeout, just to report what happened. [[slnc 300]] A real '
            'service would simply hang.'
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
            'How does the demo make its results repeatable? [[slnc 400]] '
            'With the same small tools used across these concurrency '
            'videos. [[slnc 500]] For example, two threads each read a '
            'shared stock count of ten. [[slnc 300]] Then they meet at a '
            'meeting point, which releases neither until both have '
            'arrived. [[slnc 300]] Only then does each write back what it '
            'read, minus one. [[slnc 500]] Run it twenty times, and the '
            'answer is nine, twenty times. [[slnc 300]] Never eight. '
            '[[slnc 500]] Interestingly, the starvation deadlock needed '
            'no forcing at all. [[slnc 300]] One worker waiting on itself '
            'has only one possible outcome.'
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
            'A quick, honest note about this demo. [[slnc 400]] Almost '
            'every result was made repeatable by pinning one timing on '
            'purpose, with a gate or a latch. [[slnc 300]] Everywhere '
            'else, the operating system is free to run any task on any '
            'worker, in any order. [[slnc 500]] Pool starvation is the '
            'exception. [[slnc 300]] It needs no forcing, because it '
            'happens on every possible schedule. [[slnc 500]] Elsewhere, '
            'a passing test proves the forced timing, not every timing.'
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
            "Fifth demo: Java's virtual threads. [[slnc 400]] The same "
            'two thousand threads as the first demo, but using Java '
            "twenty-one's virtual threads. [[slnc 500]] Eleven "
            'milliseconds, compared with ninety-eight. [[slnc 300]] A '
            'virtual thread only uses a real operating system thread '
            'while it is actually running. [[slnc 300]] So creating huge '
            'numbers of them is cheap. [[slnc 600]] But here is the '
            'honest limit. [[slnc 300]] Suppose a database allows only '
            'ten connections. [[slnc 300]] It still allows ten, whether a '
            'handful of threads, or a million virtual threads, are '
            'asking. [[slnc 500]] Cheap threads remove one old reason for '
            'pooling. [[slnc 300]] They do not remove the need to limit a '
            'shared resource.'
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
            'Here are the costs, all in one place. [[slnc 500]] A refusal '
            'has no waiting period built in. [[slnc 300]] It happens the '
            'instant the pool is full, or not at all. [[slnc 500]] A task '
            'that waits on another task in its own pool can deadlock. '
            '[[slnc 300]] At any pool size, whenever that nesting '
            'happens. [[slnc 500]] And choosing the pool size has no free '
            'answer, in either direction.'
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
            'So, when is this pattern worth it? [[slnc 400]] When more '
            'than one worker truly helps. [[slnc 300]] Heavy calculations '
            'that can run in parallel. [[slnc 300]] Or waiting on files '
            'and networks, using traditional threads, where creating '
            'threads really costs something. [[slnc 500]] It is not worth '
            'it for a single background task that runs once. [[slnc 300]] '
            'A pool sized for work it will never do is just ceremony.'
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
            "That's the Thread Pool pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A fixed number '
            'of workers is only half the pattern, because the queue '
            'behind them needs a limit too. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Change the starvation demo from one '
            'worker to two. [[slnc 300]] Predict what will happen, before '
            'you run it. [[slnc 300]] Then check whether you were right. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
