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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Read-Write Lock pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A read-write lock lets many '
            'readers in together, but lets a writer in only alone. [[slnc '
            '300]] Because two reads can never conflict with each other. '
            '[[slnc 300]] Only a write can conflict with anything. [[slnc '
            '600]] Think of a museum painting. [[slnc 300]] Any number of '
            'visitors can look at it at once. [[slnc 300]] But when the '
            'restorer works on it, the room is closed to everyone. [[slnc '
            "700]] In our online store, many shoppers read a product's "
            'price, and a merchandiser sometimes changes it. [[slnc 500]] '
            'By the end, you will know what a torn read is. [[slnc 300]] '
            'Why a waiting writer can still be overtaken. [[slnc 300]] '
            'Why upgrading a read lock deadlocks. [[slnc 300]] And, '
            'surprisingly, when a read-write lock is slower than a plain '
            'lock.'
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
            'Here is the scenario. [[slnc 400]] An online store shows a '
            "product's price. [[slnc 300]] The price is two facts, kept "
            'together: an amount, and a currency. [[slnc 500]] A thousand '
            'shoppers read that price all day. [[slnc 300]] Now and then, '
            'a merchandiser changes it. [[slnc 500]] So how do readers '
            'stay safe from a half-finished change? [[slnc 300]] And how '
            'do they stay fast?'
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
            'First demo: no lock at all. [[slnc 400]] The writer changes '
            'the price in two steps. [[slnc 300]] First the amount, then '
            'the currency. [[slnc 500]] A reader is made to arrive '
            'exactly between those two steps. [[slnc 300]] It reads '
            'fifty-four ninety-nine, in pounds. [[slnc 500]] That price '
            'never existed. [[slnc 300]] It is the new amount, with the '
            'old currency. [[slnc 300]] This is called a torn read. '
            '[[slnc 400]] It needs two separate fields to happen. [[slnc '
            '300]] A single value, written in one step, cannot be torn.'
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
            'The obvious fix is one lock, around every read and every '
            'write. [[slnc 300]] It is correct. [[slnc 300]] A torn read '
            'is now impossible. [[slnc 500]] But think about the readers. '
            '[[slnc 300]] Two readers can never conflict with each other. '
            '[[slnc 300]] Yet this lock cannot tell a reader from a '
            'writer. [[slnc 300]] So every reader queues behind every '
            'other reader, for no good reason. [[slnc 500]] Eight '
            'readers, each reading fifty thousand times, take fifteen '
            'milliseconds. [[slnc 300]] Remember that number.'
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
            'Now, the pattern: one lock, with two sides. [[slnc 500]] The '
            'read lock is shared. [[slnc 300]] Any number of readers can '
            'hold it at the same time. [[slnc 500]] The write lock is '
            'exclusive. [[slnc 300]] One writer holds it, and while it '
            'does, nobody else can get in. [[slnc 300]] Not readers, and '
            'not other writers. [[slnc 500]] In Java, this is the '
            'Reentrant Read Write Lock.'
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
            'Third demo: the same eight readers, using the read-write '
            'lock. [[slnc 400]] No reader ever waited for another reader. '
            '[[slnc 300]] So surely this is faster? [[slnc 500]] It is '
            'not. [[slnc 300]] One hundred and thirty-eight milliseconds, '
            'compared with fifteen for the plain lock. [[slnc 500]] Why? '
            '[[slnc 300]] The lock keeps a count of how many readers are '
            'inside, in shared memory. [[slnc 300]] Every reader updates '
            'that count, every time. [[slnc 300]] And eight threads fight '
            'over it. [[slnc 400]] For a read as cheap as returning one '
            'price, that fight costs more than it saves.'
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
            'Now the honest costs. [[slnc 300]] The first: a waiting '
            'writer is not guaranteed to go next. [[slnc 500]] In this '
            'demo, the writer is really waiting in line, for the current '
            'reader to finish. [[slnc 300]] Then a second reader arrives. '
            '[[slnc 300]] And it slips straight past the waiting writer. '
            "[[slnc 300]] Java's documentation says this is allowed. "
            '[[slnc 500]] If readers keep arriving, nothing limits how '
            'long the writer waits. [[slnc 300]] That is called writer '
            'starvation.'
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
            'The second cost: the upgrade deadlock. [[slnc 400]] A thread '
            'holds the read lock, reads the price, and decides to change '
            'it. [[slnc 300]] So it asks for the write lock. [[slnc 500]] '
            'But the write lock waits for every reader to leave. [[slnc '
            '300]] That includes this very thread. [[slnc 300]] And it '
            'cannot leave, because it is stuck waiting. [[slnc 300]] It '
            'waits for itself, forever. [[slnc 500]] This demo rescues it '
            'after about two hundred milliseconds, just to report what '
            'happened. [[slnc 400]] Moving from the write lock down to '
            'the read lock is allowed. [[slnc 300]] Moving up is not.'
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
            'The third cost, and the biggest. [[slnc 400]] Here are three '
            'ways to protect the same price, measured on the same reads. '
            '[[slnc 500]] A plain single lock: sixteen milliseconds. '
            '[[slnc 300]] The read-write lock: one hundred and '
            'thirty-seven. [[slnc 300]] An unchangeable snapshot: two '
            'milliseconds. [[slnc 600]] How does the snapshot work? '
            '[[slnc 300]] The price is an object that can never change. '
            '[[slnc 300]] To publish a new price, you swap one reference, '
            'in one atomic step. [[slnc 300]] A reader sees either the '
            'whole old price, or the whole new one. [[slnc 300]] Never a '
            'mixture. [[slnc 300]] And there is no lock, and no reader '
            'count, at all.'
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
            'How does the demo force the torn read, every time? [[slnc '
            '400]] Nothing is left to luck. [[slnc 500]] The writer sets '
            'the new amount. [[slnc 300]] It signals, through a latch, '
            'that it has done so. [[slnc 300]] Then it waits at a gate, '
            'before setting the currency. [[slnc 500]] The main thread '
            'waits for that signal, reads the price, and only then opens '
            'the gate. [[slnc 300]] So the read is proven to land in the '
            'gap, on every run. [[slnc 300]] No sleeping, and no hoping.'
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
            'A quick, honest note about this demo. [[slnc 400]] Every '
            'result was made repeatable by pinning one fact on purpose. '
            '[[slnc 300]] A writer is waiting. [[slnc 200]] A gap is '
            'open. [[slnc 500]] The timings are real measurements, and '
            'they change from machine to machine. [[slnc 300]] What stays '
            'the same is the ranking. [[slnc 300]] For a read this cheap, '
            'the plain lock and the snapshot both beat the read-write '
            'lock. [[slnc 500]] A passing test proves the forced scene, '
            'not safety under every possible timing.'
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
            'Here are the costs, all in one place. [[slnc 500]] A waiting '
            'writer can be overtaken, so nothing limits its wait. [[slnc '
            '300]] Upgrading from a read lock to a write lock deadlocks '
            'the thread that tries it. [[slnc 300]] And for a very cheap '
            "read, the lock's own bookkeeping can cost more than a plain "
            'lock.'
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
            'So, when is this pattern worth it? [[slnc 400]] When there '
            'are many readers, few writers, and each read takes real '
            'time. [[slnc 300]] Such as searching a large catalogue held '
            'in memory. [[slnc 300]] Then letting readers overlap is '
            'worth the bookkeeping. [[slnc 500]] Not for a tiny read, '
            'like this price. [[slnc 300]] There, use a plain lock. '
            '[[slnc 300]] Or better, an unchangeable snapshot, swapped in '
            'one step.'
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
            "That's the Read-Write Lock pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] '
            'Letting readers share a lock is only worth it when each read '
            "is expensive enough to pay for the lock's own bookkeeping. "
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] Make '
            'the price read slower, by doing real work inside it. [[slnc '
            '300]] Then measure which of the three approaches wins. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
