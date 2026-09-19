"""Scene definitions for the Read-Write Lock teaching video.

Each scene has: key, title, kind, body, narration.

Same discipline as the three videos before it in this category: narration
names the threads -- "the reader", "the writer" -- speaks timings and
outcomes out loud, and never points at a picture the listener cannot see.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="Read-Write Lock",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Read-Write Lock "
            "pattern in Java, and it is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] The plain definition: many "
            "readers may hold the lock together, but a writer holds it "
            "alone, because two reads can never conflict with each "
            "other, and only a write can conflict with anything. "
            "[[slnc 350]] This is the fourth project in the concurrency "
            "category, and it moves from getting an answer back to "
            "protecting the shared data that answers are read from. "
            "[[slnc 300]] By the end you will know what a torn read is, "
            "why a writer waiting in line can still be overtaken, why "
            "upgrading a read lock deadlocks, and, the surprising part, "
            "when a read-write lock is slower than a plain lock."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online store shows a product's price:",
            "an amount and a currency, kept together.",
            "",
            "A thousand shoppers read it. Now and then,",
            "a merchandiser changes it.",
            "",
            "How do the readers stay safe, and stay fast?",
        ],
        narration=(
            "Here is the scenario. An online store shows a product's "
            "price. The price is two facts kept together: an amount, and "
            "a currency. [[slnc 300]] A thousand shoppers read that "
            "price all day. Now and then, a merchandiser changes it. "
            "[[slnc 300]] So the question this whole video answers is: "
            "how do the readers stay safe from a half-finished change, "
            "and how do they stay fast while they do?"
        ),
    ),
    dict(
        key="03-torn-read",
        kind="console",
        title="No Lock — The Torn Read",
        body="""ONE. No lock at all.
  read mid-update: 54.99 GBP

  never a true price: the new
  amount with the old currency.""",
        narration=(
            "First, with no lock at all. The writer changes the price in "
            "two steps: first the amount, then the currency. [[slnc 300]] "
            "In this demo, a reader is made to arrive exactly between "
            "those two steps. It reads fifty-four ninety-nine, in "
            "pounds. [[slnc 300]] That price never existed. The new "
            "amount is paired with the old currency. This is a torn "
            "read, and it needs two fields to happen. One field written "
            "in one step cannot be torn."
        ),
    ),
    dict(
        key="04-single-lock",
        kind="console",
        title="One Lock — Correct, But Queued",
        body="""TWO. One mutual-exclusion lock.
  8 readers x 50,000 reads: 15ms

  every reader queued behind
  every other reader.""",
        narration=(
            "The obvious fix is one lock around every read and every "
            "write. It is correct. A torn read is now impossible. "
            "[[slnc 300]] But look at what it does to the readers. Two "
            "readers can never conflict with each other, and this lock "
            "cannot tell a reader from a writer. So every reader queues "
            "behind every other reader, for no reason the data demands. "
            "[[slnc 300]] Eight readers, fifty thousand reads each: "
            "fifteen milliseconds. Hold on to that number."
        ),
    ),
    dict(
        key="05-pattern",
        kind="bullets",
        title="The Pattern — Two Locks In One",
        body=[
            "The read lock: shared. Any number of",
            "readers may hold it together.",
            "",
            "The write lock: exclusive. One writer,",
            "and nobody else, readers included.",
        ],
        narration=(
            "The pattern is one lock with two faces. [[slnc 300]] The "
            "read lock is shared. Any number of readers may hold it at "
            "the same time. [[slnc 300]] The write lock is exclusive. "
            "One writer holds it, and while it does, nobody else does, "
            "neither readers nor other writers. [[slnc 300]] In Java, "
            "that is ReentrantReadWriteLock."
        ),
    ),
    dict(
        key="06-surprise",
        kind="console",
        title="The Surprise",
        body="""THREE. Read-write lock.
  8 readers x 50,000 reads: 138ms

  no reader ever waited on another
  reader -- and this is slower.""",
        narration=(
            "Now the same eight readers, on the read-write lock. No "
            "reader ever waited on another reader. Surely this is "
            "faster. [[slnc 300]] It is not. One hundred and thirty-"
            "eight milliseconds, against fifteen for the plain lock. "
            "[[slnc 300]] The reason: the lock keeps a count of how many "
            "readers are inside, in shared memory. Every reader updates "
            "that count, every time, and eight threads fight over it. "
            "For a read as cheap as returning one price, that fight "
            "costs more than it saves."
        ),
    ),
    dict(
        key="07-starvation",
        kind="console",
        title="Cost One — Writer Starvation",
        body="""FOUR. Writer starvation.
  writer genuinely queued: true

  a second reader barged past
  it anyway: true""",
        narration=(
            "Now the honest costs. First, a writer waiting in line is "
            "not guaranteed to go next. [[slnc 300]] In this demo the "
            "writer is genuinely queued, waiting for the current reader "
            "to finish. A second reader then arrives, and its try-lock "
            "goes straight past the writer. The Java documentation says "
            "this is allowed. [[slnc 300]] Do that continuously, and "
            "nothing bounds how long the writer waits. That is writer "
            "starvation."
        ),
    ),
    dict(
        key="08-upgrade",
        kind="console",
        title="Cost Two — The Upgrade Deadlock",
        body="""FIVE. Read lock to write lock.
  deadlocked: true, rescued after
  203ms by a demonstration timeout

  left alone, this thread waits
  on itself forever.""",
        narration=(
            "Second cost. A thread holds the read lock, reads the price, "
            "and decides it needs to change it. So it asks for the write "
            "lock. [[slnc 300]] The write lock waits for every reader to "
            "leave. That includes this very thread, which cannot leave, "
            "because it is stuck waiting. It waits on itself, forever. "
            "[[slnc 300]] This demo rescues it after two hundred and "
            "three milliseconds, purely so it can report what happened. "
            "Going the other way, from write to read, is allowed. "
            "Upgrading is not."
        ),
    ),
    dict(
        key="09-loses",
        kind="console",
        title="Cost Three — When The Lock Loses",
        body="""SIX. Three ways to guard a price.
  single mutex:       16ms
  read-write lock:   137ms
  immutable snapshot:  2ms""",
        narration=(
            "Third cost, and the biggest. Here are three ways to guard "
            "the same price, measured on the same reads. [[slnc 300]] A "
            "single mutex: sixteen milliseconds. The read-write lock: "
            "one hundred and thirty-seven. An immutable snapshot: two "
            "milliseconds. [[slnc 300]] The price is an immutable "
            "record, so publishing a new one is one atomic swap of a "
            "reference. A reader sees the whole old price or the whole "
            "new one, never a mixture, and there is no lock and no "
            "reader count at all."
        ),
    ),
    dict(
        key="10-harness",
        kind="code",
        title="How The Demo Forces The Torn Read",
        body="""Gate midWrite = new Gate();
CountDownLatch amountSet = new CountDownLatch(1);

// writer: set amount, signal, then WAIT
// at the gate before setting currency.

amountSet.await();        // amount is written
Price torn = catalogue.read();  // lands in the gap
midWrite.open();          // let the writer finish""",
        narration=(
            "None of these demos is left to luck. To force the torn "
            "read, the writer sets the new amount, tells a latch it has "
            "done so, and then waits at a gate before setting the "
            "currency. [[slnc 300]] The main thread waits for that "
            "latch, reads the price, and only then opens the gate. "
            "[[slnc 300]] So the read is proven to land in the gap "
            "between the two writes, every run. No sleeping, no hoping."
        ),
    ),
    dict(
        key="11-scheduler",
        kind="bullets",
        title="What The Scheduler Really Does",
        body=[
            "Each outcome is bought by pinning one fact:",
            "a writer is queued, a gap is open.",
            "",
            "Timings are real and vary run to run.",
            "The ordering between them does not.",
        ],
        narration=(
            "The same honest admission every project here makes. Every "
            "outcome you have heard is bought by pinning one specific "
            "fact on purpose: that a writer is queued, that a gap is "
            "open. [[slnc 300]] The timings are real measurements, and "
            "they change from run to run on different machines. What "
            "holds is their order: the mutex and the snapshot both "
            "beating the read-write lock, for a read this cheap. [[slnc "
            "300]] A passing test proves the forced scenario, not that "
            "the lock is safe under every schedule."
        ),
    ),
    dict(
        key="12-bill",
        kind="bullets",
        title="The Bill",
        body=[
            "A queued writer can be overtaken.",
            "",
            "Upgrading read to write deadlocks.",
            "",
            "For a cheap read, the lock can be",
            "slower than a plain mutex.",
        ],
        narration=(
            "Here is the bill, gathered in one place. [[slnc 300]] A "
            "queued writer can be overtaken, so nothing bounds its wait. "
            "[[slnc 300]] Upgrading from a read lock to a write lock "
            "deadlocks the thread that tries it. [[slnc 300]] And for a "
            "critical section as cheap as returning one reference, the "
            "lock's own bookkeeping can cost more than a plain mutex."
        ),
    ),
    dict(
        key="13-too-much",
        kind="bullets",
        title="When To Use It, And When Not",
        body=[
            "Worth it: many readers, few writers, and",
            "each read takes real time, like a big lookup.",
            "",
            "Not worth it: a tiny read. Prefer a plain",
            "mutex, or an immutable snapshot.",
        ],
        narration=(
            "So when does the pattern earn its place? [[slnc 300]] When "
            "there are many readers, few writers, and each read takes "
            "real time, such as scanning a large in-memory catalogue. "
            "Then letting readers overlap is worth the bookkeeping. "
            "[[slnc 300]] Not for a tiny read like this price. There, "
            "use a plain mutex, or better, an immutable snapshot "
            "swapped in one step."
        ),
    ),
    dict(
        key="14-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Try making the price read slower,",
            "and watch which of the three wins.",
        ],
        narration=(
            "That's the Read-Write Lock. [[slnc 250]] If you take one "
            "sentence away, take this one: letting readers share a lock "
            "is only worth it when a read is expensive enough to pay for "
            "the lock's own bookkeeping. [[slnc 350]] The full source, "
            "the written notes, the diagrams and an animated "
            "walkthrough are all in the repository, running offline with "
            "nothing installed but a Java development kit. [[slnc 300]] "
            "If you try one exercise, make the price read slower, by "
            "doing real work inside it, and watch which of the three "
            "approaches wins. [[slnc 300]] If this helped, a like "
            "genuinely does help other people find it, and subscribe if "
            "you would like the rest of the series. [[slnc 250]] Thanks "
            "for watching."
        ),
    ),
]
