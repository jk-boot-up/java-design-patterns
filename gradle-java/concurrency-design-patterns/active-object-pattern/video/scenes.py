"""Scene definitions for the Active Object teaching video.

Each scene has: key, title, kind, body, narration.

This is the category's capstone. It names the four projects its parts came
from and teaches none of them again. Narration names the threads, speaks
counts and outcomes out loud, and never points at a picture.
"""

SCENES = [
    dict(
        key="01-poster", kind="poster", title="Active Object", body=None,
        narration=(
            "Hello, and welcome. This video explains the Active Object "
            "pattern in Java, and it is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] The plain definition: an "
            "object gets its own thread, and a call to it becomes a "
            "message that returns straight away with a promise of the "
            "answer. Because one thread owns the state, the object needs "
            "no lock. [[slnc 350]] This is the sixth and last project in "
            "the concurrency category, and it is a capstone. Nothing in "
            "it is new. It is four earlier ideas, assembled. [[slnc 300]] "
            "By the end you will know what those four are, why callers "
            "never wait, and what the design costs: a mailbox that can "
            "back up, errors that arrive late, and a ceiling on how much "
            "one worker can do."
        ),
    ),
    dict(
        key="02-scenario", kind="bullets", title="The Scenario",
        body=[
            "An online store's stock changes from",
            "several places at once.",
            "",
            "Checkout reserves stock. Returns add it",
            "back. A back-office import corrects the count,",
            "and the import is slow.",
        ],
        narration=(
            "Here is the scenario. An online store's stock count changes "
            "from several places at once. [[slnc 300]] Checkout reserves "
            "stock. Returns add it back. And a back-office import "
            "corrects the count, which is slow work. [[slnc 300]] All "
            "of them touch the same number, so something has to keep "
            "them from colliding."
        ),
    ),
    dict(
        key="03-monitor", kind="console", title="A Monitor — The Caller Waits",
        body="""ONE. A monitor.
  the import holds the lock.
  the checkout thread state:
  WAITING

  a customer is waiting behind
  a back-office import.""",
        narration=(
            "The answer from the last video was a monitor: the object "
            "owns a lock. It is correct. But watch what a shared lock "
            "does. [[slnc 300]] The import thread takes the lock and "
            "starts its slow work. A checkout thread calls reserve. It "
            "cannot get in, so it waits. Its state is waiting. "
            "[[slnc 300]] A customer is standing behind a back-office "
            "job, and the monitor cannot tell the two apart."
        ),
    ),
    dict(
        key="04-pattern", kind="bullets", title="The Pattern — A Thread And A Mailbox",
        body=[
            "The object gets its own thread.",
            "A call becomes a message in its mailbox.",
            "The call returns a future at once.",
            "",
            "One worker takes messages one at a time.",
        ],
        narration=(
            "The pattern turns the object into something that works on "
            "its own. It gets its own thread, and its own mailbox, a "
            "queue of messages. [[slnc 300]] When you call reserve, the "
            "object does not do the work. It packs the request into a "
            "message, drops it in the mailbox, and returns a future "
            "straight away. [[slnc 300]] Its one worker thread takes "
            "the messages one at a time, in order, and completes each "
            "future as it goes."
        ),
    ),
    dict(
        key="05-returns", kind="console", title="The Call Returns At Once",
        body="""TWO. An active object.
  the import is running.
  reserve(1) has already returned.
  its result is ready yet: false

  import done: stock 50
  reserve done, later, in order:
  stock 49""",
        narration=(
            "Same scene, with an active object. The import is running "
            "on the worker. The checkout thread calls reserve. It "
            "returns at once. Its future says not done yet. [[slnc 300]] "
            "The import finishes. Stock is fifty. The worker takes the "
            "reserve message next, applies it, and completes the "
            "future. Stock is forty-nine. [[slnc 300]] The checkout "
            "thread was never blocked, and the answers arrived in the "
            "order the messages were sent."
        ),
    ),
    dict(
        key="06-no-lock", kind="console", title="No Lock At All",
        body="""THREE. One thread owns the state.
  4 callers x 25000 restocks:
  stock 100000

  the stock field has no lock and
  is not volatile. only the thread
  inventory-worker touches it.""",
        narration=(
            "Now the surprising part. Four caller threads each send "
            "twenty-five thousand restocks. The final stock is exactly "
            "one hundred thousand. Not one update lost. [[slnc 300]] "
            "Look for the lock, and there is none. The stock field is "
            "a plain number, not even volatile. Only the worker thread "
            "ever reads or writes it. [[slnc 300]] Mutual exclusion "
            "here comes from there being exactly one worker."
        ),
    ),
    dict(
        key="07-made-of", kind="bullets", title="What It Is Made Of",
        body=[
            "A queue of messages:   Producer-Consumer.",
            "A worker thread:       Thread Pool.",
            "A future for the answer: Future and Promise.",
            "State owned by one party: Monitor Object.",
            "",
            "Nothing new. The assembly is.",
        ],
        narration=(
            "This pattern is a capstone, so here is what it is made "
            "of. [[slnc 300]] The mailbox is the queue from the "
            "Producer-Consumer video. The worker is a thread, from the "
            "Thread Pool video. The answer is a future, from the Future "
            "and Promise video. And one party owning the state comes "
            "from the Monitor Object video. [[slnc 300]] If any of "
            "those is unfamiliar, go back to that video. This one only "
            "covers what putting them together adds."
        ),
    ),
    dict(
        key="08-backup", kind="console", title="Cost One — The Mailbox Backs Up",
        body="""FOUR. The mailbox backs up.
  worker busy on one slow message;
  callers sent 10000 more.

  messages waiting in the
  mailbox: 10000

  nothing refused them.""",
        narration=(
            "Now the bill. First cost: the mailbox can back up. "
            "[[slnc 300]] The worker is busy on one slow message. "
            "Callers send ten thousand more. All ten thousand are "
            "waiting in the mailbox. [[slnc 300]] Nothing refused them, "
            "and nothing slowed the callers down. If the worker is "
            "slower than its callers, the queue just grows. A real "
            "system needs a bound and a decision about what to do when "
            "it is full."
        ),
    ),
    dict(
        key="09-errors", kind="console", title="Cost Two — Errors Arrive Later",
        body="""FIVE. Errors arrive later.
  cause: stock feed unavailable
  [raised on inventory-worker]

  the calling method appears
  nowhere in that trace: true""",
        narration=(
            "Second cost. Everything is asynchronous, including "
            "errors. [[slnc 300]] A message fails. It does not throw "
            "where it was sent. Its future fails, later, when someone "
            "asks for the result. [[slnc 300]] The stack trace belongs "
            "to the worker thread. The method that sent the message "
            "appears nowhere in it. Debugging means working out who "
            "sent the message that failed."
        ),
    ),
    dict(
        key="10-ceiling", kind="console", title="Cost Three — One Worker Is A Ceiling",
        body="""SIX. One worker is a ceiling.
  each message costs 50
  microseconds of work.

  1 caller:  19832 per second
  4 callers: 19919 per second

  the ceiling is the worker.""",
        narration=(
            "Third cost, measured. Every message here costs fifty "
            "microseconds of real work, and one worker does all of it. "
            "[[slnc 300]] One caller: about nineteen thousand eight "
            "hundred messages a second. Four callers: about nineteen "
            "thousand nine hundred. [[slnc 300]] Four times the "
            "callers, the same rate. The ceiling is the worker, not the "
            "callers. That is the price of having no lock."
        ),
    ),
    dict(
        key="11-harness", kind="code", title="How The Demo Forces It",
        body="""Gate slow = new Gate();
CountDownLatch started = new CountDownLatch(1);

inventory.importCorrection(50, () -> {
    started.countDown();
    slow.awaitOpen();     // worker held here
});
started.await();          // now it is busy
inventory.reserve(1);     // returns at once""",
        narration=(
            "None of this is left to luck. The slow import parks the "
            "worker on a gate, and tells a latch it has started. "
            "[[slnc 300]] The demo waits for that latch, so the worker "
            "is proven to be busy, and only then calls reserve. The "
            "call returns while the worker is still held. [[slnc 300]] "
            "The ceiling uses real work, not sleeping: each message "
            "spins for fifty microseconds."
        ),
    ),
    dict(
        key="12-scheduler", kind="bullets", title="What The Scheduler Really Does",
        body=[
            "Each scenario pins what it needs:",
            "the worker is held, the mailbox is counted.",
            "",
            "The rates are real measurements",
            "and change between machines.",
        ],
        narration=(
            "The same honest admission as every project here. Each "
            "scenario pins what it needs: the worker is held on a "
            "gate, the mailbox is counted while it is held, the error "
            "is raised on the worker. [[slnc 300]] The scheduler still "
            "chooses when each caller thread runs. The rates are real "
            "measurements and change between machines. A passing test "
            "proves the forced scenario, not every possible schedule."
        ),
    ),
    dict(
        key="13-leads", kind="bullets", title="Where This Leads, And When It Is Too Much",
        body=[
            "Actors: active objects with mailboxes.",
            "Event loops: one worker and a mailbox.",
            "",
            "Too much for state that rarely changes:",
            "a monitor is simpler.",
        ],
        narration=(
            "Where does this idea go? Actor systems are active objects "
            "where the mailbox is the main feature. Event loops, like "
            "those in Node or Netty, are one worker and a mailbox. "
            "This video names them and teaches neither. [[slnc 300]] "
            "And when is it too much? For state that rarely changes, a "
            "monitor is simpler. An active object earns its place when "
            "callers must not wait, or when the work is slow."
        ),
    ),
    dict(
        key="14-outro", kind="outro", title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Try giving the mailbox a bound,",
            "and decide what happens when it is full.",
        ],
        narration=(
            "That's the Active Object. [[slnc 250]] If you take one "
            "sentence away, take this one: an active object trades a "
            "lock for a queue, and the queue has to be watched. "
            "[[slnc 350]] The full source, the written notes, the "
            "diagrams and an animated walkthrough are all in the "
            "repository, running offline with nothing installed but a "
            "Java development kit. [[slnc 300]] If you try one "
            "exercise, give the mailbox a bound, and decide what a "
            "caller should see when it is full. [[slnc 300]] If this "
            "helped, a like genuinely does help other people find it, "
            "and subscribe if you would like the rest of the series. "
            "[[slnc 250]] Thanks for watching."
        ),
    ),
]
