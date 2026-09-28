"""Scene definitions for the Bulkhead teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the ship's-hull analogy is spoken in full before
any class name appears, and the console slides are read out as a story about
which thread each job landed on rather than as columns. The slides illustrate
the narration; they never carry it.

Every number quoted in these scenes comes from the real output of
`./gradlew run`: one shared pool of four threads, four import batches that take
all four, a shopper who waits three hundred milliseconds and goes; then two
bulkheads of two threads each, a sale that completes on checkout-worker while
the feed sits at two busy and two queued; then four accepted and one refused in
zero milliseconds; and finally two busy threads beside two idle ones.

Scene order is the argument, and the shape of it is unusual for this series: the
mechanism in scene eight is deliberately an anticlimax, and it is placed late so
that it lands as a decision rather than as a technique. Everything before it is
about a failure you cannot see, and everything after it is about what the fix
costs. Do not move scene fourteen -- the bill -- earlier or drop it. A viewer who
leaves thinking bulkheads are free has learned something worse than nothing.

Scene eleven is the one that makes the demo evidence rather than anecdote: it
asks how we know the partition did it and not the partner API recovering. It
must stay immediately after act two, while the good result is still fresh
enough to be doubted.

Layout limit: on "bullets" and "quote" slides the body starts at y=260 and
steps 60 pixels a line, and the footer sits at y~1022, so twelve body lines
is the maximum.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Bulkhead",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Bulkhead pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Stop letting every kind of '
            'work draw from the same pot of resources. [[slnc 300]] Give '
            'the work that must never fail a pot of its own. [[slnc 300]] '
            'Then one slow job can fill up its own pot, but it cannot '
            'take what the important work needs. [[slnc 600]] The name '
            'comes from shipbuilding. [[slnc 300]] A bulkhead is a wall '
            "that divides a ship's hull into separate watertight "
            'compartments. [[slnc 300]] A hole floods one compartment, '
            'not the whole ship. [[slnc 700]] In our online store, there '
            "are two jobs. [[slnc 300]] Taking a shopper's money. [[slnc "
            "300]] And importing a supplier's catalogue overnight. [[slnc "
            '500]] By the end, you will know how a background job that '
            'nobody is waiting for can stop the shop selling. [[slnc '
            '300]] Why a bigger pool does not help. [[slnc 300]] And what '
            'the wall costs you, on every day that nothing goes wrong.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "One application. One pool of threads. Every job",
            "asks it for a thread, works, and gives it back.",
            "",
            "Two of those jobs matter here.",
            "",
            "CHECKOUT takes a shopper's money. It is fast, it",
            "is correct, and nobody has filed a bug against it.",
            "It needs exactly one thing: a thread.",
            "",
            "THE SUPPLIER FEED imports a catalogue overnight.",
            "Nobody is waiting for it. It calls a partner API",
            "that is, occasionally, very slow.",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] The shop runs as one '
            'application, with one pool of threads. [[slnc 300]] A thread '
            'is a worker that runs one job at a time. [[slnc 500]] Every '
            'job asks the pool for a thread, does its work, and gives the '
            'thread back. [[slnc 300]] Showing a product page, taking a '
            'payment, sending an email. [[slnc 300]] All from the same '
            'pool. [[slnc 500]] That is a completely normal design, and '
            'for a long time it is the right one. [[slnc 600]] Two of '
            'those jobs matter here. [[slnc 400]] The first is checkout. '
            "[[slnc 300]] It takes a shopper's money. [[slnc 300]] It is "
            'fast, it is correct, and it needs exactly one thing: a '
            'thread. [[slnc 500]] The second is the supplier feed. [[slnc '
            "300]] It imports the supplier's catalogue overnight. [[slnc "
            '300]] Nobody is waiting for it. [[slnc 300]] And it calls a '
            'partner service which is, sometimes, very slow. [[slnc 500]] '
            'In the code, these two jobs have nothing to do with each '
            'other. [[slnc 300]] Keep that in mind.'
        ),
    ),
    dict(
        key="03-the-shared-pool",
        kind="code",
        title="One Pool, Shared By Everything",
        body="""Bulkhead shared = new Bulkhead("shared", 4, 4, log);

for (int i = 1; i <= 4; i++) {
    shared.submit("feed-" + i, feed.importBatch(i));
}

shared.submit("checkout",
        new Checkout().takePayment("ORD-5001"));

// four threads. no bug. every test passes.""",
        narration=(
            'Here is the setup. [[slnc 400]] One pool, with four threads. '
            '[[slnc 300]] Four import batches are handed to it, one after '
            'another. [[slnc 300]] Then a shopper arrives, and the '
            'payment is handed to the same pool. [[slnc 500]] To be fair '
            'to this code, there is no bug in it. [[slnc 300]] Every test '
            'passes. [[slnc 300]] Almost every service starts this way. '
            '[[slnc 300]] And in a code review, nobody would say a word. '
            '[[slnc 500]] Tonight, the partner service that the feed '
            'calls has gone slow. [[slnc 300]] Not failing. [[slnc 300]] '
            "Answering, but slowly. [[slnc 300]] Let's run it."
        ),
    ),
    dict(
        key="04-act-one",
        kind="console",
        title="Act One — One Shared Pool Of Four",
        body="""$ ./gradlew run

1. One shared pool of four threads
  ~  10ms  shared     feed-1     started on shared-worker
  ~  10ms  shared     feed-2     started on shared-worker
  ~  10ms  shared     feed-3     started on shared-worker
  ~  10ms  shared     feed-4     started on shared-worker
  checkout: still waiting for a thread after 300ms

  all 4 threads are held by the feed,
  and the sale is lost""",
        narration=(
            'Everything follows from one small fact. [[slnc 400]] A job '
            'that is waiting still holds its thread. [[slnc 300]] It uses '
            'no processor time, and does nothing. [[slnc 300]] But the '
            'thread stays with it, until its call comes back. [[slnc '
            '500]] So, the first import batch starts, and takes a thread. '
            '[[slnc 300]] The second takes a thread. [[slnc 200]] The '
            'third. [[slnc 200]] The fourth. [[slnc 400]] Four batches, '
            'four threads, and the pool only has four. [[slnc 500]] Now '
            'the shopper tries to pay. [[slnc 300]] There is no thread '
            'free. [[slnc 300]] After three hundred milliseconds, they '
            'are still waiting, and the sale is lost. [[slnc 600]] And '
            'here is the strange part. [[slnc 300]] There is no line for '
            'checkout in the output at all. [[slnc 300]] Not a slow line, '
            'and not an error. [[slnc 300]] Checkout never started.'
        ),
    ),
    dict(
        key="05-absence",
        kind="bullets",
        title="Starved, Not Broken",
        body=[
            "Checkout has no line in the timeline. Absence is",
            "the symptom, and absence is very hard to notice.",
            "",
            "A test in this project takes that same checkout job",
            "and runs it the moment a thread is free. It works",
            "perfectly. There is nothing to fix in it.",
            "",
            "So: the shop stopped selling because of a",
            "background job that nobody was waiting for.",
            "",
            "And neither job mentions the other. No import, no",
            "call, no shared field. Only a shared pool.",
        ],
        narration=(
            'It would be easier if checkout were broken, because then '
            'there would be something to fix. [[slnc 400]] But it is not '
            'broken. [[slnc 300]] A test in this project runs the same '
            'checkout job the moment a thread is free, and it works '
            'perfectly. [[slnc 500]] It was starved, not broken. [[slnc '
            '300]] And from the outside, those two look exactly the same. '
            '[[slnc 300]] That is why this is so hard to find at three in '
            'the morning. [[slnc 300]] You are looking for a bug in a '
            'class that does not have one. [[slnc 600]] So here is the '
            'key sentence. [[slnc 300]] The shop stopped selling because '
            'of a background job that nobody was waiting for. [[slnc '
            '500]] And the link between them is invisible. [[slnc 300]] '
            'Checkout never mentions the feed. [[slnc 300]] The feed '
            'never mentions checkout. [[slnc 300]] They are tied together '
            'only by the pool they share. [[slnc 300]] So reading either '
            'file will never show you the problem.'
        ),
    ),
    dict(
        key="06-the-hull",
        kind="quote",
        title="The Ship's Hull",
        body=[
            "A bulkhead is not a metaphor. It is the actual",
            "word for the walls dividing a ship's hull into",
            "watertight compartments.",
            "",
            "Hole in an undivided hull: the water spreads the",
            "length of the ship, and the ship goes down.",
            "Hole in a divided one: one compartment floods,",
            "the ship sits lower, and it keeps going.",
            "",
            "Nothing about the hole changed.",
            "",
            "And look at where the walls take up space.",
        ],
        narration=(
            "Let's leave the code for a moment, and think about a ship. "
            "[[slnc 400]] A bulkhead is a wall that divides a ship's hull "
            'into watertight compartments. [[slnc 500]] Make a hole in a '
            'hull with no walls, and the water spreads along the whole '
            'ship, and it sinks. [[slnc 300]] Make the same hole in a '
            'divided hull, and only one compartment floods. [[slnc 300]] '
            'The ship sits a little lower, and keeps going. [[slnc 600]] '
            'There are two lessons here. [[slnc 400]] First, the hole did '
            'not change. [[slnc 300]] Just as much water came in. [[slnc '
            '300]] The wall only limits how far it spreads. [[slnc 500]] '
            'Second, the walls take up space. [[slnc 300]] One '
            'compartment can be empty while the next one is full. [[slnc '
            '300]] And you cannot move space from one to the other. '
            '[[slnc 300]] That is not a flaw. [[slnc 300]] That is the '
            'design. [[slnc 300]] Isolation is paid for in capacity you '
            'are not allowed to use. [[slnc 300]] Hold on to that, '
            'because we will come back to it.'
        ),
    ),
    dict(
        key="07-tempting-fixes",
        kind="bullets",
        title="Two Tempting Fixes, Both Wrong",
        body=[
            "✗ \"Make the pool bigger.\" Forty threads instead",
            "  of four. The feed takes forty whenever the",
            "  partner is slow enough for long enough, and",
            "  checkout is starved at forty as it was at four.",
            "  The number moved. The failure did not.",
            "",
            "✗ \"Never refuse a job — queue them all.\" That",
            "  turns a fast, visible failure into an out-of-",
            "  memory crash at an hour of its choosing.",
            "",
            "A queue that never says no is not generous.",
            "It is a slow leak with good manners.",
        ],
        narration=(
            'Before the real fix, here are two tempting fixes. [[slnc '
            '300]] Both are wrong. [[slnc 500]] The first is: make the '
            'pool bigger. [[slnc 300]] Forty threads, instead of four. '
            '[[slnc 400]] That only buys time. [[slnc 300]] If the '
            'partner is slow for long enough, the feed takes all forty '
            'threads. [[slnc 300]] And checkout is starved at forty, just '
            'as it was at four. [[slnc 300]] The number changed. [[slnc '
            '300]] The failure did not. [[slnc 300]] Worse, a bigger pool '
            'takes longer to notice, and uses more memory when it finally '
            'fills up. [[slnc 600]] The second is: never refuse a job. '
            '[[slnc 300]] Let every job wait in a queue with no limit. '
            '[[slnc 400]] That sounds generous, but it is more dangerous. '
            '[[slnc 300]] It turns a fast, visible failure into a slow, '
            'invisible one. [[slnc 300]] Jobs pile up until the program '
            'runs out of memory. [[slnc 300]] And every caller waits for '
            'work that will not start for minutes. [[slnc 600]] So '
            'neither fix works. [[slnc 300]] The two jobs are only '
            'connected by the pool they share. [[slnc 300]] So what if '
            'they stop sharing it?'
        ),
    ),
    dict(
        key="08-the-mechanism",
        kind="code",
        title="The Whole Mechanism",
        body="""new ThreadPoolExecutor(threads, threads,
        0L, TimeUnit.MILLISECONDS,
        new ArrayBlockingQueue<>(queueCapacity),
        r -> new Thread(r, name + "-worker"));

// a fixed pool. a bounded queue. a name.
// no algorithm. nothing adaptive.
// nothing to tune at runtime.""",
        narration=(
            'Here is the whole mechanism, and it is very plain. [[slnc '
            '400]] A pool with a fixed number of threads. [[slnc 300]] A '
            'queue that holds a fixed number of waiting jobs. [[slnc '
            '300]] And a name, which every thread in the pool carries. '
            '[[slnc 500]] That is all. [[slnc 300]] No clever algorithm. '
            '[[slnc 300]] Nothing that adapts to load. [[slnc 300]] '
            'Nothing to tune while it runs. [[slnc 600]] So a bulkhead is '
            'not clever machinery. [[slnc 300]] It is a decision to stop '
            'sharing. [[slnc 300]] The pattern is not in this class. '
            '[[slnc 300]] It is in having two of them. [[slnc 500]] The '
            'hard part is deciding where the walls go. [[slnc 300]] And '
            'that is a business decision, not a coding one. [[slnc 500]] '
            'For now, the feed gets two threads of its own. [[slnc 300]] '
            'Checkout gets two threads of its own. [[slnc 300]] And we '
            'give them exactly the same bad night.'
        ),
    ),
    dict(
        key="09-act-two",
        kind="console",
        title="Act Two — Two Bulkheads",
        body="""2. Two bulkheads: the feed has its own threads
  ~   0ms  feed       feed-1     started on feed-worker
  ~   0ms  feed       feed-2     started on feed-worker
  ~   0ms  checkout   checkout   started on checkout-worker
  ~   0ms  checkout   checkout   finished
  checkout: paid ORD-5001

  the feed is jammed -- 2 threads busy, 2 jobs queued --
  and the shop is still selling, because it never shared.""",
        narration=(
            'Same slow partner. [[slnc 200]] Same four batches. [[slnc '
            '200]] Same moment. [[slnc 500]] Two batches start. [[slnc '
            "300]] The other two wait in the feed's queue for a feed "
            'thread. [[slnc 300]] On the feed side, nothing has improved. '
            '[[slnc 500]] Then the shopper arrives, gets a thread '
            'straight away, and pays. [[slnc 300]] The sale goes through '
            'in milliseconds. [[slnc 600]] The names of the threads tell '
            'the whole story. [[slnc 400]] The import batches run on '
            'threads called feed worker. [[slnc 300]] The payment runs on '
            'a thread called checkout worker. [[slnc 500]] They come from '
            'different pools. [[slnc 300]] The feed cannot borrow from '
            'checkout. [[slnc 300]] And checkout is not allowed to help '
            'the feed. [[slnc 500]] That is the whole pattern, and it '
            'just saved a sale.'
        ),
    ),
    dict(
        key="10-roles",
        kind="diagram",
        title="Who Owns What",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 300]] There are only a few, "
            'and each has one job. [[slnc 500]] A bulkhead is a named '
            'pool of threads, with a limit, that one kind of work may '
            'use. [[slnc 300]] Underneath, it is a fixed thread pool with '
            'a limited queue. [[slnc 500]] When all its threads are busy '
            'and its queue is full, it refuses at once. [[slnc 300]] And '
            'the error says which bulkhead was full. [[slnc 300]] Not '
            'that the system is busy, but which pool ran out. [[slnc '
            '600]] Then there is the work. [[slnc 300]] Checkout, which '
            'must never be starved. [[slnc 300]] And the supplier feed, '
            'which nobody is waiting for, and which holds its thread the '
            'whole time it waits. [[slnc 600]] Those two facts are the '
            'most important in the system. [[slnc 300]] And they appear '
            'nowhere in the code. [[slnc 300]] They come from the people '
            'who run the shop. [[slnc 300]] If nobody writes them down, '
            'as a pool and a thread count, then in an outage they are '
            'decided by whichever job asked for a thread first. [[slnc '
            '600]] One more piece. [[slnc 300]] The slow partner is not a '
            'real network call, and nothing in this project sleeps. '
            '[[slnc 300]] It is a gate that a job waits at, until the '
            'test opens it. [[slnc 300]] A job waiting at a closed gate '
            'holds its thread, just like a job waiting on a slow network.'
        ),
    ),
    dict(
        key="11-still-stuck",
        kind="quote",
        title="How Do We Know It Was The Wall?",
        body=[
            "Checkout worked. Fine. But how do we know the",
            "partition did that — and not the partner API",
            "quietly recovering at a convenient moment?",
            "",
            "A lucky run would look exactly the same.",
            "",
            "So one test asserts that the feed is STILL jammed",
            "— two threads busy, two jobs queued — at the",
            "instant the sale goes through.",
            "",
            "A test that only checks the good thing happened",
            "has not ruled out it happening by accident.",
        ],
        narration=(
            'Before we celebrate, here is a fair question. [[slnc 400]] '
            'Checkout worked. [[slnc 300]] But how do we know the wall '
            'did that? [[slnc 500]] Suppose the partner service had '
            'started answering again, just before the shopper arrived. '
            '[[slnc 300]] The output would look exactly the same. [[slnc '
            '300]] We would have proved nothing. [[slnc 500]] So one test '
            'checks that the feed is still jammed at the very moment the '
            'sale goes through. [[slnc 300]] Two threads busy, and two '
            'jobs waiting. [[slnc 500]] Nothing about the partner was '
            'fixed. [[slnc 300]] The slow thing is still slow, and the '
            'shop is selling anyway. [[slnc 600]] This lesson works far '
            'beyond thread pools. [[slnc 300]] A test that only checks '
            'the good thing happened has not ruled out that it happened '
            'by luck.'
        ),
    ),
    dict(
        key="12-act-three",
        kind="console",
        title="Act Three — A Fifth Batch, With Nowhere To Go",
        body="""3. A fifth batch arrives with nowhere to go
  feed is full: no thread and no room in the queue (in 0ms)
  4 accepted, 1 refused

  an unbounded queue would have taken it, and every
  batch after it, until the shop ran out of memory
  instead of out of threads.""",
        narration=(
            "The feed's bulkhead has two threads, and a queue that holds "
            'two. [[slnc 300]] So four batches fit. [[slnc 300]] Now a '
            'fifth batch arrives. [[slnc 500]] It is refused, and the '
            'refusal takes zero milliseconds. [[slnc 500]] That can feel '
            'unfriendly, but it is the opposite. [[slnc 300]] The speed '
            'is the whole point. [[slnc 300]] The caller finds out at '
            'once, while it still has time to do something useful. [[slnc '
            '300]] Drop the batch, do less, or try again later. [[slnc '
            '500]] It is the same idea as a circuit breaker failing fast, '
            'but applied to a queue. [[slnc 600]] Now compare it with a '
            'queue that has no limit. [[slnc 300]] That queue would have '
            'accepted this batch, and the next one, and every one after '
            'that. [[slnc 300]] Nobody would be told anything, until the '
            'program ran out of memory instead of threads. [[slnc 500]] '
            'Refusing is a feature.'
        ),
    ),
    dict(
        key="13-refusing",
        kind="bullets",
        title="Refusing Immediately Is A Feature",
        body=[
            "The exception names the pot that is full — not",
            "\"the system is busy\". An on-call engineer can",
            "act on \"the feed's pool is full\".",
            "",
            "✓ The caller is told in a millisecond, and can",
            "  still shed, degrade, or defer the work.",
            "",
            "✓ The blast radius was decided in advance, in",
            "  daylight — not by scheduling, during an incident.",
            "",
            "The failure does not go away. It becomes something",
            "you chose, at a moment you chose.",
        ],
        narration=(
            'That refusal gives you three things, not just speed. [[slnc '
            '500]] First, the error names the pool that is full. [[slnc '
            "300]] Not, the system is busy. [[slnc 300]] But, the feed's "
            'pool is full. [[slnc 300]] One of those tells an engineer '
            'where to look. [[slnc 500]] Second, the caller is told in a '
            'millisecond, so it still has choices. [[slnc 300]] It can '
            'drop the work, do a smaller version, or save it for later. '
            '[[slnc 300]] A caller that is simply kept waiting has no '
            'choices at all. [[slnc 500]] Third, the size of the damage '
            'was decided in advance, calmly, in daylight. [[slnc 300]] '
            'Not by chance, in the middle of an incident. [[slnc 600]] '
            'The failure has not gone away. [[slnc 300]] The partner is '
            'no faster. [[slnc 300]] What changed is that you chose the '
            'shape of the failure, ahead of time.'
        ),
    ),
    dict(
        key="14-act-four",
        kind="console",
        title="Act Four — What The Partition Costs",
        body="""4. What the partition costs on a quiet afternoon
  feed:     2 threads, 2 busy, 2 queued and waiting
  checkout: 2 threads, 0 busy, 2 idle

  two threads are doing nothing while two jobs wait
  for a thread. One shared pool would have finished
  the feed sooner. Bulkheads buy isolation and pay
  for it in throughput.""",
        narration=(
            'Now the bill. [[slnc 300]] Any honest explanation of this '
            'pattern has to include it. [[slnc 500]] On a quiet '
            'afternoon, the divided shop looks like this. [[slnc 300]] '
            'The feed has two threads busy, and two more jobs waiting. '
            '[[slnc 300]] And checkout has two threads doing nothing at '
            'all. [[slnc 500]] Two threads are idle, while two jobs wait '
            'for a thread. [[slnc 300]] And they are not allowed to help. '
            '[[slnc 600]] One shared pool of four would have run all four '
            'batches at once, and finished sooner. [[slnc 300]] A test in '
            'this project checks exactly that. [[slnc 300]] On a good '
            'day, the shared pool really is faster. [[slnc 500]] So '
            'divided pools leave capacity idle, on purpose. [[slnc 300]] '
            'That is not a bug, or a tuning problem. [[slnc 300]] It is '
            'the price of the isolation. [[slnc 500]] It is the ship '
            'again. [[slnc 300]] The empty compartment cannot lend its '
            'space to the full one.'
        ),
    ),
    dict(
        key="15-costs",
        kind="bullets",
        title="So Where Do The Walls Go?",
        body=[
            "Worth it for work whose failure ends the business.",
            "In a shop, that is taking money.",
            "",
            "Not worth it for everything. Fifteen bulkheads is",
            "fifteen numbers to size, fifteen that drift out of",
            "date, and a lot of threads idle at 3pm.",
            "",
            "Two or three partitions, drawn along what must",
            "survive — not along the package structure.",
            "",
            "And pair it with a circuit breaker: a bulkhead stops",
            "damage spreading, not you calling the dead thing.",
        ],
        narration=(
            'So where should the walls go? [[slnc 400]] The trade is '
            'worth it for work whose failure ends the business. [[slnc '
            '300]] In a shop, that is taking money. [[slnc 500]] It is '
            'not worth it for everything. [[slnc 300]] Fifteen bulkheads '
            'means fifteen pools to size. [[slnc 300]] Fifteen numbers '
            'that go out of date as traffic changes. [[slnc 300]] And a '
            'lot of threads doing nothing in the afternoon. [[slnc 500]] '
            'A good rule is two or three pools, divided by what must '
            'survive. [[slnc 300]] Not by how the code is organised into '
            'packages, even though that looks tidy. [[slnc 500]] And '
            'remember, this is a business decision. [[slnc 300]] Nobody '
            'can tell from the code that the supplier feed matters less '
            'than checkout. [[slnc 600]] One last point. [[slnc 300]] A '
            'bulkhead stops the damage spreading. [[slnc 300]] It does '
            'not stop you calling a service that has stopped answering. '
            '[[slnc 300]] That is the job of a circuit breaker. [[slnc '
            '500]] The two belong together. [[slnc 300]] A breaker, so '
            'you stop calling a service that is down. [[slnc 300]] And a '
            'bulkhead, so the calls already waiting cannot drown anything '
            'that matters.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the test that proves",
            "the starved checkout was never broken, and the one that",
            "proves the slow feed is still stuck while the shop sells.",
        ],
        narration=(
            "That's the Bulkhead pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A bulkhead '
            'gives the work that must survive a pool of its own, and pays '
            'for that safety with capacity left idle on purpose. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 300]] '
            'It runs offline, with nothing installed except a Java '
            'development kit. [[slnc 300]] It uses real threads, but '
            'nothing sleeps, so all the tests run in about a second. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] Give '
            "checkout's bulkhead one thread instead of two. [[slnc 300]] "
            'Then put two sales through it while the feed is jammed. '
            '[[slnc 300]] The second sale waits. [[slnc 300]] The wall '
            'protects checkout from the feed, but not from checkout '
            'itself. [[slnc 500]] And one question to think about. [[slnc '
            '300]] In your own system, which work must never be starved? '
            '[[slnc 300]] And what are you willing to leave idle, to '
            'guarantee it? [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
