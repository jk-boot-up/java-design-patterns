"""Scene definitions for the Monitor Object teaching video.

Each scene has: key, title, kind, body, narration.

Narration names the threads, speaks counts and outcomes out loud, and never
points at a picture the listener cannot see.
"""

SCENES = [
    dict(
        key="01-poster", kind="poster", title="Monitor Object", body=None,
        narration=(
            "Hello, and welcome. This video explains the Monitor Object "
            "pattern in Java, and it is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] The plain definition: an "
            "object owns its own lock and its own waiting, so every "
            "method runs safely and a caller cannot forget to be careful. "
            "[[slnc 350]] This is the fifth project in the concurrency "
            "category. The last one shared a lock between readers. This "
            "one asks who should own the lock at all. [[slnc 300]] By "
            "the end you will know why volatile does not stop a lost "
            "update, why a lock held by the caller is weaker than a lock "
            "the object owns, why waiting must sit in a loop, and how a "
            "correct monitor can still deadlock."
        ),
    ),
    dict(
        key="02-scenario", kind="bullets", title="The Scenario",
        body=[
            "An online store keeps one number per product:",
            "how many are in stock.",
            "",
            "Many checkout threads reduce it. A delivery",
            "thread adds to it.",
            "",
            "A checkout wanting three when two are left",
            "should wait, not fail.",
        ],
        narration=(
            "Here is the scenario. An online store keeps one number for "
            "each product: how many are in stock. [[slnc 300]] Many "
            "checkout threads reduce that number, one sale at a time. A "
            "delivery thread adds to it when new stock arrives. [[slnc "
            "300]] And a checkout that wants three items when only two "
            "are left should wait for the delivery, not simply fail."
        ),
    ),
    dict(
        key="03-lost-update", kind="console", title="A Plain Count — The Lost Update",
        body="""ONE. A plain count.
  stock started at 10; two
  checkout threads each sold one.

  stock now: 9 -- two items sold,
  one gone from the count.""",
        narration=(
            "First, a plain number. Selling one item is three steps: "
            "read the count, subtract one, write the answer back. "
            "[[slnc 300]] In this demo, two checkout threads both read "
            "ten. Both subtract one. Both write nine. [[slnc 300]] Two "
            "items left the shelf, and the count says only one did. That "
            "is a lost update, and the demo makes it happen on every "
            "run."
        ),
    ),
    dict(
        key="04-volatile", kind="console", title="volatile — Still Not Atomic",
        body="""TWO. volatile.
  stock now: 9 -- the same lost
  update, with volatile.

  volatile promises a write is seen.
  It does not make read-subtract-
  write one step.""",
        narration=(
            "The popular half-fix is the word volatile. Surely that "
            "helps? [[slnc 300]] It does not. Both threads read ten, "
            "both write nine, exactly as before. [[slnc 300]] Volatile "
            "promises that when one thread writes, other threads see it. "
            "That is visibility. It does not promise that read, "
            "subtract and write happen as one step. That is atomicity, "
            "and it is a different promise."
        ),
    ),
    dict(
        key="05-caller-lock", kind="console", title="The Caller Holds The Lock",
        body="""THREE. The caller holds the lock.
  one caller took the lock;
  one forgot.

  stock now: 9 -- the careful
  caller's lock protected nothing.""",
        narration=(
            "Next idea: put a lock beside the count, and ask every "
            "caller to take it first. [[slnc 300]] In this demo, one "
            "checkout thread takes the lock and sells. Another checkout "
            "thread forgets, and sells anyway. Both read ten. Both write "
            "nine. [[slnc 300]] Four careful callers protect nothing if "
            "a fifth forgets. A rule that callers must remember is a "
            "rule that will eventually be broken."
        ),
    ),
    dict(
        key="06-pattern", kind="bullets", title="The Pattern — The Object Owns Its Lock",
        body=[
            "The lock is a private field.",
            "Every public method takes it itself.",
            "",
            "Waiting is private too: a condition",
            "the object owns.",
            "",
            "There is no way in, except safely.",
        ],
        narration=(
            "The pattern moves the responsibility. The lock becomes a "
            "private field of the stock object. Every public method "
            "takes that lock itself, does its work, and lets go. "
            "[[slnc 300]] A caller cannot forget, because a caller never "
            "touches the lock. There is no way in except the safe way. "
            "[[slnc 300]] In Java, that is a reentrant lock and a "
            "condition, both private."
        ),
    ),
    dict(
        key="07-wait-signal", kind="console", title="Waiting And Signalling",
        body="""FOUR. The pattern.
  8 threads x 25000 sales from
  200000: 0 left.

  a thread waited for 3 items, was
  signalled by the thread that
  added them, and took them.""",
        narration=(
            "Eight checkout threads each sell twenty-five thousand "
            "items, from a stock of two hundred thousand. Zero left. "
            "Not one update lost. [[slnc 300]] Waiting is inside the "
            "object too. A taker thread asks for three items and finds "
            "none, so it waits on the object's own condition, letting "
            "go of the lock while it waits. [[slnc 300]] A delivery "
            "thread adds three and signals. The taker wakes, takes the "
            "lock again, and takes its three. It never polled and never "
            "slept."
        ),
    ),
    dict(
        key="08-if-while", kind="console", title="Cost One — wait In A Loop",
        body="""FIVE. if, not while.
  with if:    stock ends at -1

  with while: stock ends at 0, and
  1 taker is still waiting,
  correctly.""",
        narration=(
            "Now the bill. First cost: waiting must sit in a loop. "
            "[[slnc 300]] Two taker threads are waiting, one item each. "
            "One item is added, and both are woken. [[slnc 300]] If the "
            "code checks with a plain if, both proceed. One item, two "
            "sales. The count ends at minus one. [[slnc 300]] With a "
            "while loop, the woken thread checks again, sees the item is "
            "gone, and goes back to waiting. Being woken means stock may "
            "be there. It does not mean stock is there."
        ),
    ),
    dict(
        key="09-nested", kind="console", title="Cost Two — Nested Monitors",
        body="""SIX. Nested monitors.
  two monitors locked in
  opposite orders.

  deadlock detected by the JVM:
  true.
  broken by interrupting both.""",
        narration=(
            "Second cost. One transfer thread moves stock from monitor "
            "A to monitor B. It holds A, then asks for B. [[slnc 300]] "
            "At the same moment, another thread moves stock from B to A. "
            "It holds B, then asks for A. [[slnc 300]] Each holds what "
            "the other needs. Both wait forever. The Java virtual "
            "machine detects it, and this demo breaks it by interrupting "
            "both threads. Real code has no such rescue."
        ),
    ),
    dict(
        key="10-callout", kind="console", title="Cost Three — Calling Out",
        body="""SIX, continued. A callout.
  unknown code called while
  holding the lock, asking
  another thread for the stock.

  timed out: true, after 206ms.""",
        narration=(
            "Third cost. Suppose the monitor, while holding its lock, "
            "calls some other code it does not own, such as a listener. "
            "[[slnc 300]] That listener asks a second thread to read the "
            "stock, and waits for the answer. The second thread needs "
            "the lock. The monitor is holding it, and is waiting for the "
            "listener. [[slnc 300]] Nobody can move. This demo gives up "
            "after two hundred milliseconds. The rule: never call code "
            "you do not own while holding your lock."
        ),
    ),
    dict(
        key="11-harness", kind="code", title="How The Demo Forces The Race",
        body="""Rendezvous bothRead =
    new Rendezvous("both-read", 2);

PlainStock stock =
    new PlainStock(10, bothRead::meet);

// each sale reads, then meets, then writes.
// neither writes until both have read.""",
        narration=(
            "None of this is left to luck. The plain stock takes a hook "
            "that runs between the read and the write. The demo passes "
            "in a rendezvous, a meeting point that will not let either "
            "thread through until both have arrived. [[slnc 300]] So "
            "both threads have read ten before either writes nine. "
            "For the two takers, the demo waits until the condition's "
            "own wait queue shows two waiters before adding the item. No "
            "sleeping, no hoping."
        ),
    ),
    dict(
        key="12-scheduler", kind="bullets", title="What The Scheduler Really Does",
        body=[
            "Each failure is bought by pinning",
            "one fact: both have read, both",
            "are waiting, both hold a lock.",
            "",
            "Everything else, the JVM chooses.",
        ],
        narration=(
            "The same honest admission as every project here. Each "
            "failure you heard was bought by pinning one fact on "
            "purpose: both threads have read, both takers are waiting, "
            "both transfers hold their first lock. [[slnc 300]] The "
            "Java scheduler still chooses everything else, including "
            "which woken taker runs first. The sales timing is a real "
            "measurement and changes between machines. A passing test "
            "proves the forced scenario, not safety under every "
            "schedule."
        ),
    ),
    dict(
        key="13-bill", kind="bullets", title="The Bill, And When It Is Too Much",
        body=[
            "The lock is a bottleneck by design.",
            "wait needs a loop.",
            "Two monitors can deadlock.",
            "",
            "For one counter, use AtomicInteger.",
            "Use a monitor when several fields",
            "change together, or threads must wait.",
        ],
        narration=(
            "Here is the bill in one place. [[slnc 300]] The lock is a "
            "bottleneck by design: one thread inside at a time. Waiting "
            "needs a loop. Two monitors can deadlock, and calling out "
            "while holding the lock can too. [[slnc 300]] And when is "
            "it too much? For a single counter, an atomic integer is "
            "simpler and faster. A monitor earns its place when several "
            "fields must change together, or when threads must wait for "
            "a condition."
        ),
    ),
    dict(
        key="14-outro", kind="outro", title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Try fixing act six by always",
            "locking the monitors in the same order.",
        ],
        narration=(
            "That's the Monitor Object. [[slnc 250]] If you take one "
            "sentence away, take this one: a lock the caller must "
            "remember will eventually be forgotten, so let the object "
            "own it. [[slnc 350]] The full source, the written notes, "
            "the diagrams and an animated walkthrough are all in the "
            "repository, running offline with nothing installed but a "
            "Java development kit. [[slnc 300]] If you try one "
            "exercise, fix the nested monitors by always locking them in "
            "the same order, and watch the deadlock disappear. [[slnc "
            "300]] If this helped, a like genuinely does help other "
            "people find it, and subscribe if you would like the rest of "
            "the series. [[slnc 250]] Thanks for watching."
        ),
    ),
]
