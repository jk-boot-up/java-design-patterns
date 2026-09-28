"""Scene definitions for the Monitor Object teaching video.

Each scene has: key, title, kind, body, narration.

Narration names the threads, speaks counts and outcomes out loud, and never
points at a picture the listener cannot see.
"""

SCENES = [
    dict(
        key="01-poster", kind="poster", title="Monitor Object", body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Monitor Object pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A monitor object owns its '
            'own lock, and its own waiting. [[slnc 300]] So every one of '
            'its methods runs safely, and no caller can forget to be '
            'careful. [[slnc 600]] Think of a shop with one fitting room, '
            'and an attendant at the door. [[slnc 300]] Customers never '
            'lock the door themselves. [[slnc 300]] The attendant lets '
            'one person in at a time. [[slnc 700]] In our online store, '
            'many threads change the stock count of a product. [[slnc '
            '500]] By the end, you will know why volatile does not stop a '
            'lost update. [[slnc 300]] Why a lock held by the caller is '
            'weaker than a lock the object owns. [[slnc 300]] Why waiting '
            'must sit in a loop. [[slnc 300]] And how a correct monitor '
            'can still deadlock.'
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
            'Here is the scenario. [[slnc 400]] An online store keeps one '
            'number for each product: how many are in stock. [[slnc 400]] '
            'Many checkout threads reduce that number, one sale at a '
            'time. [[slnc 300]] A delivery thread adds to it when new '
            'stock arrives. [[slnc 500]] And a checkout that wants three '
            'items, when only two are left, should wait for the delivery, '
            'not simply fail.'
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
            'First demo: a plain number. [[slnc 400]] Selling one item '
            'takes three steps. [[slnc 300]] Read the count, subtract '
            'one, and write the answer back. [[slnc 500]] Two checkout '
            'threads both read ten. [[slnc 300]] Both subtract one. '
            '[[slnc 300]] Both write nine. [[slnc 500]] Two items left '
            'the shelf, but the count says only one did. [[slnc 300]] '
            'That is called a lost update. [[slnc 300]] And this demo '
            'makes it happen every time.'
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
            'A popular half-fix is the keyword volatile. [[slnc 300]] '
            'Surely that helps? [[slnc 500]] It does not. [[slnc 300]] '
            'Both threads still read ten, and both still write nine. '
            '[[slnc 500]] Volatile promises that when one thread writes, '
            'other threads will see it. [[slnc 300]] That is called '
            'visibility. [[slnc 400]] It does not promise that read, '
            'subtract, and write happen as one step. [[slnc 300]] That is '
            'called atomicity, and it is a different promise.'
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
            'Next idea: put a lock next to the count, and ask every '
            'caller to take it first. [[slnc 500]] In this demo, one '
            'checkout thread takes the lock, and sells. [[slnc 300]] '
            'Another checkout thread forgets the lock, and sells anyway. '
            '[[slnc 300]] Both read ten, and both write nine. [[slnc '
            '500]] Four careful callers protect nothing, if a fifth one '
            'forgets. [[slnc 300]] A rule that every caller must remember '
            'will eventually be broken.'
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
            'The pattern moves the responsibility. [[slnc 400]] The lock '
            'becomes a private field, inside the stock object. [[slnc '
            '300]] Every public method takes that lock itself, does its '
            'work, and lets go. [[slnc 500]] A caller cannot forget, '
            'because a caller never touches the lock. [[slnc 300]] There '
            'is no way in, except the safe way. [[slnc 500]] Waiting is '
            'private too. [[slnc 300]] In Java, that means a private '
            'Reentrant Lock, and a private Condition.'
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
            'Now the pattern, running. [[slnc 400]] Eight checkout '
            'threads each sell twenty-five thousand items, from a stock '
            'of two hundred thousand. [[slnc 300]] The final count is '
            'zero. [[slnc 300]] Not one update was lost. [[slnc 600]] '
            'Waiting happens inside the object too. [[slnc 300]] A thread '
            'asks for three items, but there are none. [[slnc 300]] So it '
            "waits on the object's own condition, and lets go of the lock "
            'while it waits. [[slnc 400]] Then a delivery thread adds '
            'three items, and sends a signal. [[slnc 300]] The waiting '
            'thread wakes, takes the lock again, and takes its three '
            'items. [[slnc 300]] It never kept checking, and it never '
            'guessed how long to sleep.'
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
            'Now the costs. [[slnc 300]] The first: waiting must sit '
            'inside a loop. [[slnc 500]] Two threads are waiting, for one '
            'item each. [[slnc 300]] One item is added, and both are '
            'woken. [[slnc 500]] If the code checks with a single if '
            'statement, both carry on. [[slnc 300]] One item, two sales, '
            'and the count ends at minus one. [[slnc 500]] With a while '
            'loop, the second thread checks again, sees the item is gone, '
            'and goes back to waiting. [[slnc 300]] Being woken means '
            'stock might be there. [[slnc 300]] It does not mean stock is '
            'there.'
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
            'The second cost: two monitors can deadlock. [[slnc 400]] One '
            'thread moves stock from monitor A to monitor B. [[slnc 300]] '
            'It holds A, and asks for B. [[slnc 400]] At the same moment, '
            'another thread moves stock from B to A. [[slnc 300]] It '
            'holds B, and asks for A. [[slnc 500]] Each holds what the '
            'other needs. [[slnc 300]] Both wait forever. [[slnc 400]] '
            'Java detects it, and this demo breaks it by interrupting '
            'both threads. [[slnc 300]] Real code has no such rescue.'
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
            'The third cost: calling out while holding the lock. [[slnc '
            '400]] Suppose the monitor, while holding its lock, calls '
            'some outside code, like a listener. [[slnc 400]] That '
            'listener asks another thread to read the stock, and waits '
            'for the answer. [[slnc 300]] But that other thread needs the '
            'lock. [[slnc 300]] And the monitor is holding the lock, '
            'while it waits for the listener. [[slnc 500]] Nobody can '
            'move. [[slnc 300]] This demo gives up after about two '
            'hundred milliseconds. [[slnc 400]] The rule: never call code '
            'you do not own, while holding your lock.'
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
            'How does the demo make these failures happen reliably? '
            '[[slnc 400]] Nothing is left to luck. [[slnc 500]] The plain '
            'stock accepts a hook that runs between reading and writing. '
            '[[slnc 300]] The demo plugs in a meeting point, which '
            'releases neither thread until both have arrived. [[slnc '
            '300]] So both threads have read ten, before either one '
            'writes nine. [[slnc 500]] For the two waiting threads, the '
            'demo checks that both are really waiting, before it adds the '
            'item. [[slnc 300]] No sleeping, and no hoping.'
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
            'A quick, honest note about this demo. [[slnc 400]] Each '
            'failure was made repeatable by pinning one fact on purpose. '
            '[[slnc 300]] Both threads have read. [[slnc 200]] Both are '
            'waiting. [[slnc 200]] Both hold a lock. [[slnc 500]] Java '
            'still decides everything else, such as which woken thread '
            'runs first. [[slnc 300]] The timing numbers are real '
            'measurements, and they vary by machine. [[slnc 300]] A '
            'passing test proves the forced scene, not safety under every '
            'possible timing.'
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
            'Here are the costs, all in one place. [[slnc 400]] The lock '
            'is a bottleneck by design, because only one thread can be '
            'inside at a time. [[slnc 300]] Waiting needs a loop. [[slnc '
            '300]] Two monitors can deadlock. [[slnc 300]] And calling '
            'out while holding the lock can deadlock too. [[slnc 500]] So '
            'when is it too much? [[slnc 300]] For a single counter, an '
            'Atomic Integer is simpler, and faster. [[slnc 300]] A '
            'monitor earns its place when several fields must change '
            'together, or when threads must wait for a condition.'
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
            "That's the Monitor Object pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A lock '
            'that callers must remember will eventually be forgotten, so '
            'let the object own it. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Fix the nested monitors, by always locking them '
            'in the same order. [[slnc 300]] Then run it, and listen for '
            'the deadlock to disappear. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
