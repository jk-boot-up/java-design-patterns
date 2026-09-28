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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Active Object pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An active object has its own '
            'thread. [[slnc 300]] When you call it, your call becomes a '
            'message in its mailbox. [[slnc 300]] The call returns '
            'straight away, with a promise of the answer later. [[slnc '
            "400]] And because only one thread ever touches the object's "
            'data, it needs no lock at all. [[slnc 600]] Think of a busy '
            'chef with an order rail. [[slnc 300]] Waiters clip orders to '
            'the rail, and walk away at once. [[slnc 300]] The chef cooks '
            'them one at a time, in order. [[slnc 700]] This pattern is a '
            'capstone. [[slnc 300]] Nothing in it is new. [[slnc 300]] It '
            'combines four ideas from earlier concurrency videos. [[slnc '
            '500]] By the end, you will know why callers never wait. '
            '[[slnc 300]] And what it costs: a mailbox that can back up, '
            'errors that arrive late, and a limit on how much one worker '
            'can do.'
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
            "Here is the scenario. [[slnc 400]] An online store's stock "
            'count changes from several places at once. [[slnc 400]] '
            'Checkout reserves stock. [[slnc 300]] Returns add stock '
            'back. [[slnc 300]] And a back-office import corrects the '
            'count, which is slow work. [[slnc 500]] All of them change '
            'the same number. [[slnc 300]] So something must stop them '
            'colliding.'
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
            'The usual answer is a monitor. [[slnc 300]] The object owns '
            'a lock, and only one thread may enter at a time. [[slnc '
            '300]] It is correct. [[slnc 500]] But listen to what a '
            'shared lock does. [[slnc 400]] The import thread takes the '
            'lock, and starts its slow work. [[slnc 300]] Then a checkout '
            'thread tries to reserve one item. [[slnc 300]] It cannot get '
            'in, so it waits. [[slnc 500]] A real customer is now stuck '
            'behind a back-office job. [[slnc 300]] And the lock cannot '
            'tell the difference between them.'
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
            'The pattern turns the object into something that works on '
            'its own. [[slnc 400]] It gets its own thread, and its own '
            'mailbox, which is a queue of messages. [[slnc 500]] When you '
            'call reserve, the object does not do the work right away. '
            '[[slnc 300]] It packs your request into a message, drops it '
            'in the mailbox, and immediately hands you a future. [[slnc '
            '300]] A future is a promise of a result that will arrive '
            "later. [[slnc 500]] The object's one worker thread takes "
            'messages one at a time, in order. [[slnc 300]] And it '
            'completes each future as it goes.'
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
            'Now the same scene, with an active object. [[slnc 400]] The '
            'slow import is running on the worker. [[slnc 300]] The '
            'checkout thread calls reserve. [[slnc 300]] The call returns '
            'at once. [[slnc 300]] Its future says: not done yet. [[slnc '
            '500]] The import finishes, and the stock is fifty. [[slnc '
            '300]] Then the worker takes the reserve message, and applies '
            'it. [[slnc 300]] The stock is now forty-nine, and the future '
            'is completed. [[slnc 500]] The checkout thread was never '
            'blocked. [[slnc 300]] And the results arrived in the order '
            'the messages were sent.'
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
            'Now the surprising part. [[slnc 400]] Four caller threads '
            'each send twenty-five thousand restock messages. [[slnc '
            '300]] The final stock is exactly one hundred thousand. '
            '[[slnc 300]] Not a single update is lost. [[slnc 500]] Look '
            'for the lock. [[slnc 300]] There is none. [[slnc 300]] The '
            'stock is a plain number, not even marked volatile. [[slnc '
            '500]] Why is it safe? [[slnc 300]] Because only the worker '
            'thread ever reads or writes it. [[slnc 300]] Safety comes '
            'from there being exactly one worker.'
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
            'This pattern is a capstone, so here is what it is made of. '
            '[[slnc 500]] The mailbox is a queue, from the Producer '
            'Consumer pattern. [[slnc 300]] The worker is a thread, from '
            'the Thread Pool pattern. [[slnc 300]] The answer is a '
            'future, from the Future and Promise pattern. [[slnc 300]] '
            'And one party owning the data comes from the Monitor Object '
            'pattern. [[slnc 500]] Nothing here is new. [[slnc 300]] What '
            'is new is putting them together. [[slnc 300]] If any of '
            'those four is unfamiliar, its own video explains it.'
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
            'Now the costs. [[slnc 300]] First: the mailbox can back up. '
            '[[slnc 500]] The worker is busy with one slow message. '
            '[[slnc 300]] Meanwhile, callers send ten thousand more. '
            '[[slnc 300]] All ten thousand are now waiting in the '
            'mailbox. [[slnc 500]] Nothing refused them, and nothing '
            'slowed the callers down. [[slnc 300]] If the worker is '
            'slower than its callers, the queue just keeps growing. '
            '[[slnc 300]] A real system needs a limit on the queue, and a '
            'decision about what to do when it is full.'
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
            'The second cost: everything is asynchronous, including '
            'errors. [[slnc 500]] When a message fails, the error does '
            'not appear where the message was sent. [[slnc 300]] Instead, '
            'its future fails, later, when someone asks for the result. '
            "[[slnc 500]] And the error's stack trace belongs to the "
            'worker thread. [[slnc 300]] The method that sent the message '
            'does not appear anywhere in it. [[slnc 300]] So debugging '
            'means working out who sent the message that failed.'
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
            'The third cost, measured. [[slnc 400]] Each message here '
            'costs fifty microseconds of real work. [[slnc 300]] And one '
            'worker does all of it. [[slnc 500]] With one caller, the '
            'object handles about nineteen thousand eight hundred '
            'messages per second. [[slnc 300]] With four callers, about '
            'nineteen thousand nine hundred. [[slnc 500]] Four times the '
            'callers, and the same rate. [[slnc 300]] The limit is the '
            'single worker, not the callers. [[slnc 300]] That is the '
            'price of having no lock.'
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
            'How does the demo make these scenes happen reliably? [[slnc '
            '400]] Nothing is left to luck. [[slnc 500]] The slow import '
            'holds the worker at a gate. [[slnc 300]] And it signals, '
            'through a latch, that it has started. [[slnc 400]] The demo '
            'waits for that signal, so the worker is proven to be busy. '
            '[[slnc 300]] Only then does it call reserve. [[slnc 300]] '
            'And the call returns while the worker is still held. [[slnc '
            '500]] The speed test uses real work, not sleeping. [[slnc '
            '300]] Each message spins for fifty microseconds.'
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
            'A quick, honest note about this demo. [[slnc 400]] Each '
            'scene is pinned in place. [[slnc 300]] The worker is held at '
            'a gate, the mailbox is counted while it is held, and the '
            'error is raised on the worker. [[slnc 500]] But the '
            'operating system still decides when each caller thread runs. '
            '[[slnc 300]] The speeds are real measurements, and they '
            'change from machine to machine. [[slnc 300]] A passing test '
            'proves the forced scene, not every possible timing.'
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
            'Where does this idea lead? [[slnc 400]] Actor systems are '
            'active objects, where the mailbox is the main feature. '
            '[[slnc 300]] Event loops, like those in Node or Netty, are '
            'one worker and a mailbox. [[slnc 300]] This video names '
            'them, but does not teach them. [[slnc 500]] And when is it '
            'too much? [[slnc 300]] For data that rarely changes, a '
            'simple monitor with a lock is easier. [[slnc 300]] An active '
            'object earns its place when callers must never wait, or when '
            'the work is slow.'
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
            "That's the Active Object pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] An '
            'active object trades a lock for a queue, and that queue has '
            'to be watched. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Give the mailbox a size limit. [[slnc 300]] Then '
            'decide what a caller should experience when it is full. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
