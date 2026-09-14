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
            "Hello, and welcome. This video explains the Bulkhead pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 300]] Let's start with the simple definition. Stop letting "
            "every kind of work draw from the same pot of resources. Give the "
            "work that must never fail a pot of its own, so that one slow job "
            "filling up its own pot cannot take the last of something the "
            "important work needed. [[slnc 350]] The name comes from "
            "shipbuilding. A bulkhead is a wall that divides a hull into "
            "separate watertight compartments, so that a hole in one of them "
            "floods that compartment and not the whole ship. [[slnc 300]] The "
            "rest of the video builds a real working Java project: an online "
            "shop with two jobs to do. Taking a shopper's money, and importing "
            "a supplier's catalogue overnight. [[slnc 300]] By the end you'll "
            "know how a background job that nobody was waiting for stops the "
            "shop selling, without either piece of code so much as mentioning "
            "the other; why making the pool bigger does not help; why the "
            "broken-looking thing is not broken at all; and exactly what the "
            "wall costs you on every day that nothing goes wrong."
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
            "Here is the situation, and it is worth picturing before any code. "
            "[[slnc 300]] The shop runs on one application with one pool of "
            "threads. Everything it does — serving a product page, taking a "
            "payment, sending an email, importing the supplier's catalogue — "
            "asks that pool for a thread, does its job, and hands the thread "
            "back. [[slnc 250]] That is a completely ordinary way to build a "
            "service, and for a long time it is the right one. Threads are "
            "expensive, a pool is the standard way to bound how many exist, and "
            "one pool means one number to tune. [[slnc 350]] Two of the jobs in "
            "that shop matter for this video. [[slnc 300]] The first is "
            "checkout. It takes a shopper's money. It is fast, it is correct, "
            "and nobody has ever filed a bug against it. It needs exactly one "
            "thing in order to work: a thread. [[slnc 350]] The second is the "
            "supplier feed. It imports the supplier's catalogue overnight. "
            "Nobody is waiting for it. If it finished an hour late, nothing bad "
            "would happen to anyone. [[slnc 250]] And it calls a partner API "
            "which is, occasionally, very slow. [[slnc 300]] Hold those two in "
            "your head, because the whole video is about what they have in "
            "common — which, as far as the code is concerned, is nothing at all."
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
            "Here is the arrangement, and there is nothing clever about it. "
            "[[slnc 300]] One pool with four threads in it. Four import batches "
            "are handed to it, one after another. Then a shopper turns up and "
            "the payment is handed to the same pool. [[slnc 350]] I want to be "
            "fair to this code, because it is the villain of the next few "
            "minutes and it does not deserve to be. [[slnc 300]] There is no "
            "bug in it. Every test written against it passes. It is the "
            "arrangement almost every service starts with, and in a code review "
            "nobody would say a word — because the cost of it is not in the "
            "code at all. [[slnc 350]] Now, tonight, the partner API that the "
            "feed calls has gone slow. Not failing. Answering, but slowly. "
            "[[slnc 300]] Let's run it."
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
            "Here is the fact that everything else in this video follows from, "
            "and it is a small one. [[slnc 300]] A job that is waiting still "
            "holds its thread. It is using no processor time. It is doing "
            "nothing whatsoever. But that thread belongs to it until the call it "
            "is waiting on comes back. [[slnc 350]] So: the first import batch "
            "starts, and takes a thread. The second starts, and takes a thread. "
            "The third. The fourth. [[slnc 250]] Four batches, four threads, and "
            "the pool has four threads. [[slnc 300]] Now the shopper tries to "
            "pay, and there is no thread for them. After three hundred "
            "milliseconds they are still waiting, and the sale is gone. "
            "[[slnc 350]] But I want you to notice what is not in that output "
            "rather than what is. [[slnc 300]] There is no line for checkout. "
            "Not a slow line. Not an error line. No line at all — because it "
            "never started."
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
            "It would honestly be easier if checkout were faulty, because then "
            "there would be something to fix. [[slnc 300]] It is not faulty. "
            "There is a test in this project that takes exactly that same "
            "checkout job, runs it the moment a thread is free, and watches it "
            "complete perfectly. [[slnc 350]] It was starved, not broken. And "
            "from the outside those two look completely identical. Which is "
            "exactly why this is so hard to diagnose at three in the morning: "
            "you are looking for a bug in a class that does not have one. "
            "[[slnc 300]] So here is the sentence that matters. The shop stopped "
            "selling because of a background job that nobody was waiting for. "
            "[[slnc 350]] And now notice how invisible the connection is. "
            "Nothing in the checkout code mentions the supplier feed. Nothing in "
            "the supplier feed mentions checkout. No import, no method call, no "
            "shared variable, no message. [[slnc 300]] They are coupled by a "
            "resource that neither of them names — which means no amount of "
            "reading either file will ever show you this."
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
            "Let me leave the code for half a minute, because the name of this "
            "pattern is not a metaphor. It is the actual word for something. "
            "[[slnc 300]] A bulkhead is a wall that divides a ship's hull into "
            "separate watertight compartments. [[slnc 350]] Punch a hole below "
            "the waterline in a hull that has no walls in it, and the water "
            "spreads the length of the ship, and the ship goes down. Punch "
            "exactly the same hole in a hull that is divided, and one "
            "compartment floods. The ship sits a little lower in the water, and "
            "it keeps going. [[slnc 350]] Two things are worth taking from that, "
            "and the second is the one people skip. [[slnc 300]] First: nothing "
            "about the hole changed. The bulkhead did not make the hull "
            "stronger, or the sea calmer, or the damage smaller. Exactly as much "
            "water came in. All that changed is how far it was allowed to "
            "spread. [[slnc 350]] Second: think about where those walls "
            "physically are. They take up space. One compartment can be "
            "completely empty while the one next to it is packed full, and you "
            "cannot move the space between them. [[slnc 300]] That is not a flaw "
            "in the design. That is the design. Isolation is paid for in "
            "capacity you are not allowed to use. [[slnc 250]] Hold on to that, "
            "because we will come back to it, and it is the part most "
            "explanations of this pattern leave out."
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
            "Before the fix, the two answers that come up first in every room I "
            "have ever asked this in. [[slnc 350]] The first is: make the pool "
            "bigger. Four threads was too few, so use forty. [[slnc 300]] That "
            "buys time and nothing else. Whenever the partner API is slow enough "
            "for long enough, the feed will take forty threads instead of four, "
            "and checkout will be starved at forty exactly as it was at four. "
            "The number changes; the failure does not. [[slnc 250]] And it is "
            "worse than a draw, because the bigger the pool, the longer it takes "
            "anybody to notice, and the more memory the eventual pile-up "
            "consumes. [[slnc 350]] The second answer is: never refuse a job. "
            "Just let them all wait their turn. An unbounded queue. [[slnc 300]] "
            "That one sounds generous, and it is the more dangerous of the two. "
            "What it actually does is convert a fast, visible failure into a "
            "slow, invisible one. Jobs accumulate until the process runs out of "
            "memory, and every caller sits waiting for work that will not start "
            "for minutes. [[slnc 350]] A queue that never says no is not "
            "generous. It is a slow leak with good manners. [[slnc 300]] So "
            "neither of those is the answer. The two jobs are connected only by "
            "the pool they share. What happens if they stop sharing it?"
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
            "And here is the entire mechanism. I would like you to be "
            "disappointed by it. [[slnc 350]] A fixed pool of threads. A queue "
            "that holds a fixed number of waiting jobs. And a name, so that "
            "every worker thread in this pool is called after it. [[slnc 300]] "
            "That is all. There is no algorithm here. Nothing adaptive. Nothing "
            "that reacts to load. Nothing to tune at runtime. [[slnc 350]] Say "
            "that out loud, because it is the point of the whole video. A "
            "bulkhead is not a clever piece of machinery. It is a decision to "
            "stop sharing. [[slnc 300]] The pattern does not live in this class. "
            "It lives in having two of them. [[slnc 350]] Which means the "
            "interesting work is not writing any of this. The interesting work "
            "is deciding where the walls go — and we will come back to that, "
            "because it is a decision about the business, not about the code. "
            "[[slnc 300]] For now: the feed gets two threads of its own, "
            "checkout gets two threads of its own, and we give them exactly the "
            "same bad night."
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
            "Same slow partner. Same four batches. Same instant. [[slnc 300]] "
            "Two of the batches start, and the other two sit in the feed's queue "
            "waiting for a feed thread. Nothing there has improved at all. "
            "[[slnc 350]] And then the shopper arrives, asks for a thread, gets "
            "one immediately, and pays. The sale goes through in milliseconds. "
            "[[slnc 300]] Now listen to the names of the threads, because they "
            "are the entire argument. [[slnc 250]] The import batches are "
            "running on something called feed-worker. The payment ran on "
            "something called checkout-worker. [[slnc 300]] Those are different "
            "threads, out of different pools, and no amount of demand on one "
            "side can produce a thread on the other. The feed cannot borrow from "
            "checkout, and checkout is not allowed to help the feed. "
            "[[slnc 350]] That is the whole pattern, and it just saved a sale."
        ),
    ),
    dict(
        key="10-roles",
        kind="diagram",
        title="Who Owns What",
        body=None,
        narration=(
            "Let me name the pieces, because there are only a few and each one "
            "has exactly one job. [[slnc 300]] A bulkhead is a named, bounded "
            "pot of threads that one kind of work is allowed to use. Underneath "
            "it there is a fixed thread pool with a bounded queue, and that is "
            "genuinely the whole of it. [[slnc 350]] When both its threads are "
            "busy and its queue is full, it throws — immediately — and the "
            "exception says which bulkhead was full. Not that the system is "
            "busy. Which pot ran out. [[slnc 300]] Then the work. Checkout, "
            "which must never be starved. The supplier feed, which nobody is "
            "waiting for and which holds a thread the entire time it waits. "
            "[[slnc 350]] And here is the uncomfortable part. Those two "
            "descriptions — must never be starved, and nobody is waiting for it "
            "— are the most important facts in this entire system, and they "
            "appear nowhere in the code. Nothing in the compiler knows them. "
            "Nothing can derive them. [[slnc 300]] They come from the people who "
            "run the shop. And if they are not written down somewhere — as a "
            "pool, as a thread count — then during the outage they get decided "
            "by whichever job happened to ask for a thread first. [[slnc 350]] "
            "One more piece. The slow partner API is not a real network call "
            "here, and nothing in this project sleeps. It is a gate that a job "
            "waits at until the test opens it. A job waiting at a closed gate "
            "holds its thread exactly the way a job waiting on a slow network "
            "does — and it holds it for precisely as long as the test wants, "
            "instead of a guessed number of milliseconds."
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
            "Now, before anybody celebrates, the question I would want asked in "
            "a review. [[slnc 350]] Checkout worked. Good. But how do we know "
            "the partition is what did that? [[slnc 300]] Suppose the partner "
            "API had quietly started answering again a moment before the shopper "
            "turned up. The output would look exactly the same. We would have "
            "proved nothing, and we would have believed it. [[slnc 350]] So "
            "there is a test in this project whose entire job is to assert that "
            "the feed is still jammed — two threads busy, two jobs queued — at "
            "the very instant the sale goes through. [[slnc 300]] That is the "
            "difference between a demonstration and an anecdote. Nothing about "
            "the partner API was fixed. The slow thing is still slow, still "
            "stuck, still holding both of its threads, and the shop is selling "
            "anyway. [[slnc 350]] And this generalises well beyond thread pools, "
            "so it is worth taking away on its own. A test that only checks that "
            "the good thing happened has not ruled out the good thing happening "
            "by accident."
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
            "The feed's bulkhead has two threads and a queue that holds two, so "
            "four batches fit. A fifth arrives. [[slnc 300]] It is refused, and "
            "the refusal comes back in zero milliseconds. [[slnc 350]] That can "
            "feel hostile, and it is the exact opposite. The speed is the whole "
            "value of it. The caller finds out instantly, while it still has "
            "time to do something useful — shed the batch, degrade, try again "
            "later, write it down somewhere for tonight. [[slnc 300]] This is "
            "the same idea as a circuit breaker's fast failure, applied to a "
            "queue rather than to a broken service. [[slnc 350]] Compare it with "
            "the alternative one more time, because the contrast is the lesson. "
            "An unbounded queue would have accepted that batch. And the one "
            "after it. And every one after that. Nobody would have been told "
            "anything at all, until the process ran out of memory instead of "
            "running out of threads. [[slnc 300]] Refusing is a feature."
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
            "It is worth being precise about what that refusal buys, because it "
            "is more than speed. [[slnc 300]] The exception names the pot that "
            "is full. Not the system is busy — the feed's pool is full. "
            "[[slnc 250]] Those are very different sentences to be woken up by. "
            "One of them tells you where to look. [[slnc 350]] Second, the "
            "caller is told in a millisecond, which means it still has options. "
            "It can shed the work, do a smaller version of it, or write it down "
            "for later. A caller that is merely kept waiting has no options at "
            "all. [[slnc 300]] And third, the size of the damage was decided in "
            "advance, in daylight, by somebody thinking clearly — rather than "
            "being an accident of which job happened to ask for a thread first "
            "in the middle of an incident. [[slnc 350]] The failure has not gone "
            "away. Nothing here made the partner API faster. What changed is "
            "that the failure became something you chose, at a moment you chose, "
            "in a shape you chose."
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
            "And now the bill, because any explanation of this pattern that "
            "stops before here is selling you something. [[slnc 350]] On a quiet "
            "afternoon, this is what the partitioned shop looks like. The feed "
            "has two threads busy, with two more jobs queued up behind them, "
            "waiting. And checkout has two threads doing absolutely nothing. "
            "[[slnc 300]] Let those two sentences sit next to each other for a "
            "moment. Two threads are idle, while two jobs are waiting for a "
            "thread. And they are not allowed to help. [[slnc 350]] One shared "
            "pool of four would have run all four batches at once and finished "
            "the import sooner. There is a test in this project that asserts "
            "exactly that — the shared pool, on a good day, is genuinely faster. "
            "[[slnc 300]] So: partitioned pools are idle capacity by design. Not "
            "a bug. Not a tuning problem you will get around to. That is what "
            "you are buying the isolation with. [[slnc 350]] It is the ship "
            "again. The walls take up space, and the empty compartment cannot "
            "lend any of it to the full one."
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
            "So where do the walls actually go? [[slnc 300]] The trade is worth "
            "making for anything whose failure ends the business. In a shop, "
            "that is taking money. [[slnc 350]] It is not worth making for "
            "everything. A shop with fifteen bulkheads has fifteen pools to "
            "size, fifteen numbers that drift out of date as traffic changes, "
            "and a great many threads doing nothing at three in the afternoon. "
            "[[slnc 300]] The useful instinct is two or three partitions, drawn "
            "along the lines of what must survive — not along the lines of the "
            "package structure, which is the tempting thing to do because it "
            "looks tidy. [[slnc 350]] And remember that the classification is a "
            "business decision, not a technical one. Nobody can tell from the "
            "code that the supplier feed matters less than checkout. "
            "[[slnc 300]] One last thing, and it matters. A bulkhead is not the "
            "whole answer to an outage. It stops the damage spreading; it does "
            "not stop you calling the thing that has stopped answering. "
            "[[slnc 350]] That is the circuit breaker's job, and the two belong "
            "together: a breaker so you stop calling a service that is down, and "
            "a bulkhead so that the calls still in flight cannot drown anything "
            "that matters."
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
            "That's the bulkhead. [[slnc 250]] The full source, the written "
            "notes, the diagrams and an animated walkthrough are all in the "
            "repository, and everything runs offline with nothing installed but "
            "a Java development kit. [[slnc 300]] This is the only project in "
            "the series that uses real threads, because the subject genuinely is "
            "threads waiting for one another, and you cannot fake a thread being "
            "unavailable. But nothing in it sleeps, so the whole suite still "
            "runs in about a second. [[slnc 350]] If you try one exercise, try "
            "this one. Give checkout's bulkhead one thread instead of two, and "
            "put two sales through it while the feed is jammed. [[slnc 300]] "
            "Watch the second sale wait. The wall protects checkout from the "
            "feed. It does not protect checkout from checkout, and that is worth "
            "feeling rather than being told. [[slnc 350]] And then the harder "
            "question, the one no exercise can answer for you. In the system you "
            "work on, which work must never be starved? [[slnc 300]] And — this "
            "is the half people skip — what are you willing to leave sitting "
            "idle in order to guarantee it? [[slnc 350]] Because that is the "
            "real lesson here. The mechanism is a second thread pool and you "
            "already know how to write one. Deciding what must survive, and "
            "paying for it in capacity you are not allowed to use, is the part "
            "that needs a person. [[slnc 300]] If this helped, a like genuinely "
            "does help other people find it, and subscribe if you would like the "
            "rest of the series. [[slnc 250]] Thanks for watching, and I'll see "
            "you in the next one."
        ),
    ),
]
