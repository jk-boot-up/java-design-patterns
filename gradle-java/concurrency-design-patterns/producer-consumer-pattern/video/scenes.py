"""Scene definitions for the Producer-Consumer teaching video.

Each scene has: key, title, kind, body, narration.

This is the hardest audio-only category in the course: an interleaving is
naturally drawn, not spoken. So narration names the threads -- "the
checkout thread", "the packer thread" -- says what each one does in
order, and speaks timings and counts out loud rather than pointing at a
picture. It is also the category's reference project, so it introduces the
determinism harness every later project in the category reuses.
"""

SCENES = [
    dict(
        key="01-poster",
        kind="poster",
        title="Producer-Consumer",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Producer Consumer pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A queue with a size limit '
            'sits between the code that produces work and the code that '
            'consumes it. [[slnc 300]] Each side works at its own pace. '
            '[[slnc 300]] And the limit is chosen on purpose, not '
            'discovered by accident. [[slnc 600]] Think of a conveyor '
            "belt between a bakery's oven and its packing table. [[slnc "
            '300]] The oven puts loaves on, the packers take them off. '
            '[[slnc 300]] And the belt only holds so many. [[slnc 700]] '
            'In our online store, checkout accepts orders, and a packing '
            'step wraps each one for the courier. [[slnc 300]] But '
            'packing is slower than orders arrive. [[slnc 500]] By the '
            'end, you will know why a queue with no limit is not a safer '
            'fix. [[slnc 300]] And you will hear, in real numbers, what '
            'it costs to give every order its own thread. [[slnc 300]] '
            'Every failure in this video is forced to happen, on every '
            'run, with no guessing about timing.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "Checkout accepts orders. A packing step wraps",
            "each one for the courier -- and packing is",
            "slower than orders arrive.",
            "",
            "That gap -- arrivals faster than processing --",
            "is this entire project's subject.",
            "",
            "The shared question every project in this",
            "category asks: who is holding the thread,",
            "and for how long?",
        ],
        narration=(
            'Here is the scenario, and it stays the same for the whole '
            'video. [[slnc 400]] Checkout accepts an order. [[slnc 300]] '
            'A packing step wraps it, labels it, and hands it to the '
            'courier. [[slnc 300]] And packing takes longer than an order '
            'takes to arrive. [[slnc 500]] That gap, between how fast '
            'orders arrive and how fast they are packed, is the whole '
            'subject. [[slnc 300]] Every version of the code answers the '
            'same question differently. [[slnc 300]] Who is holding a '
            'thread, and for how long, while that gap is absorbed?'
        ),
    ),
    dict(
        key="03-inline",
        kind="console",
        title="Naive One — The Checkout Thread Packs Itself",
        body="""ONE. No queue at all.
  checkout(ord-1) returned after 49ms
  checkout(ord-2) returned after 50ms
  checkout(ord-3) returned after 50ms

  every customer behind order one waited for
  order one's pack to finish.""",
        narration=(
            'First version: no queue at all. [[slnc 400]] The checkout '
            'thread packs the order itself, before replying to the '
            'customer. [[slnc 500]] Each checkout takes about fifty '
            'milliseconds. [[slnc 300]] Not because checkout is slow, but '
            'because the whole packing job happens inside that one call. '
            '[[slnc 500]] The shopper pays that cost directly. [[slnc '
            '300]] Every customer behind order one waits for a warehouse '
            'job they have never heard of.'
        ),
    ),
    dict(
        key="04-thread-per-order",
        kind="console",
        title="Naive Two — A Thread Per Order",
        body="""TWO. A thread per order.
  created 2,000 real threads in 96.8ms
  (48.4 microseconds each)

  100,000 threads: ~4,838ms of creation
  cost alone -- before a single one has
  packed anything.

  each thread also holds a stack. That is
  where OutOfMemoryError comes from.""",
        narration=(
            'The obvious fix: hand each order to a brand new thread, and '
            'reply at once. [[slnc 300]] It works. [[slnc 300]] The '
            "shopper is never held up. [[slnc 500]] So let's measure the "
            'real cost. [[slnc 300]] Two thousand real threads are '
            'created in under a hundred milliseconds, about forty-eight '
            'microseconds each. [[slnc 400]] On a busy day of one hundred '
            'thousand orders, that is almost five seconds, just creating '
            'threads, before any packing happens. [[slnc 500]] And every '
            'thread holds its own memory, whether it is busy or not. '
            '[[slnc 300]] That is where the famous error comes from: out '
            'of memory, unable to create a new thread. [[slnc 300]] The '
            'demo does not trigger it on purpose, but the numbers point '
            'straight at it.'
        ),
    ),
    dict(
        key="05-the-bound",
        kind="bullets",
        title="The Pattern: A Bound, Chosen On Purpose",
        body=[
            "A queue between checkout and packing.",
            "Each side runs at its own pace.",
            "",
            "The bound is not an implementation detail.",
            "It is the whole point.",
            "",
            "An unbounded queue is the thread-per-order",
            "failure again, wearing a nicer name.",
        ],
        narration=(
            'So here is the fix, in one sentence. [[slnc 400]] A queue '
            'sits between checkout and packing, and each side works at '
            'its own pace, up to a limit. [[slnc 500]] That limit is not '
            'a detail you can skip. [[slnc 300]] It is the whole point of '
            'the pattern. [[slnc 500]] A queue with no limit is not '
            'safer. [[slnc 300]] It is the thread-per-order problem '
            'again, with a nicer name. [[slnc 300]] Nothing ever says no. '
            '[[slnc 300]] It just fails later, and more expensively.'
        ),
    ),
    dict(
        key="06-capacity",
        kind="console",
        title="The Queue At Capacity, Forced Rather Than Hoped For",
        body="""THREE. The bounded queue.
  the packer thread takes one order and is
  held there -- parked, not guessed at.

  three more orders fill the queue to its
  capacity of three.

  a fourth, offered with a 150ms patience:
  REJECTED -- the queue never had room.""",
        narration=(
            'Third demo: the queue, full, and on purpose. [[slnc 400]] '
            'The packer thread takes one order, and is deliberately held '
            'at a gate. [[slnc 300]] Not guessed at with a sleep. [[slnc '
            '400]] Only when a latch confirms the packer is really stuck, '
            'are three more orders added. [[slnc 300]] That fills the '
            'queue to its limit of three. [[slnc 500]] Then a fourth '
            'order is offered, with a patience of one hundred and fifty '
            'milliseconds. [[slnc 300]] Nothing frees a place in that '
            'time, because the packer is still held. [[slnc 300]] So the '
            'fourth order is refused. [[slnc 300]] On every single run.'
        ),
    ),
    dict(
        key="07-two-shutdowns",
        kind="bullets",
        title="Two Shutdowns, And They Are Not The Same Event",
        body=[
            "Clean: a poison pill, enqueued like any",
            "other order. Everything ahead of it is",
            "drained first.",
            "",
            "Abrupt: interrupt the packer thread.",
            "Whatever was still queued is simply",
            "never reached.",
        ],
        narration=(
            'There are two ways to stop this system, and they are not the '
            'same. [[slnc 500]] A clean shutdown puts a special stop '
            'order, called a poison pill, into the queue, like any other '
            'order. [[slnc 300]] Because it waits in the same queue, '
            'everything ahead of it is still packed first. [[slnc 500]] '
            'An abrupt shutdown interrupts the packer thread directly. '
            '[[slnc 300]] Anything still waiting in the queue is simply '
            'never reached. [[slnc 500]] Mixing these up is a real, '
            'common bug. [[slnc 300]] Stopping a service with a raw '
            'interrupt quietly drops all the work that was queued.'
        ),
    ),
    dict(
        key="08-clean-shutdown",
        kind="console",
        title="Clean Shutdown",
        body="""FOUR. Clean shutdown.
  4 orders queued, then the poison pill.

  packed before stopping: 4 of 4""",
        narration=(
            'Fourth demo: a clean shutdown. [[slnc 400]] Four real orders '
            'are queued. [[slnc 300]] Then the poison pill is queued '
            'behind them. [[slnc 500]] The packer takes and packs all '
            'four, in order. [[slnc 300]] Only then does it take the '
            'pill, and stop. [[slnc 300]] Four out of four, every time.'
        ),
    ),
    dict(
        key="09-abrupt-shutdown",
        kind="console",
        title="Abrupt Shutdown",
        body="""FIVE. Abrupt shutdown.
  1 order held mid-pack, 4 more queued
  behind it.

  the packer thread is interrupted, not
  signalled to drain.

  orders lost, still in the queue: 4""",
        narration=(
            'Fifth demo: an abrupt shutdown. [[slnc 400]] One order is '
            'held in the middle of packing. [[slnc 300]] Four more orders '
            'wait in the queue behind it. [[slnc 500]] This time, instead '
            'of a poison pill, the packer thread is interrupted. [[slnc '
            '500]] Four orders are still in the queue. [[slnc 300]] Never '
            'taken. [[slnc 300]] The packer is gone, and those orders are '
            'lost.'
        ),
    ),
    dict(
        key="10-why-no-sleep",
        kind="quote",
        title="Why Nothing In This Project Sleeps",
        body=[
            "A sleep-based test is a bet on how fast one",
            "machine happens to be, on one particular day.",
            "",
            "It usually wins. \"Usually\" is exactly",
            "what this category refuses to ship.",
            "",
            "A gate, a latch, a barrier: certainty,",
            "not a guess.",
        ],
        narration=(
            'Every timing in this video was forced, not guessed. [[slnc '
            '300]] Here is why that matters. [[slnc 500]] The easy way to '
            'test a full queue is to sleep for a moment, and hope the '
            'packer has reached the gate by then. [[slnc 300]] That '
            'usually works, on the machine that wrote it. [[slnc 500]] '
            'But usually is not good enough. [[slnc 300]] A test that '
            'passes most of the time will fail one day, on a slower or '
            'busier machine. [[slnc 500]] Gates, latches, and barriers do '
            'not hope. [[slnc 300]] They wait for certainty, and only '
            'carry on once it exists.'
        ),
    ),
    dict(
        key="11-lost-update",
        kind="code",
        title="The Harness's Own Proof",
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
            'Here is that technique in its smallest form. [[slnc 400]] '
            'Two threads run the same code. [[slnc 300]] Each reads a '
            'shared value, ten, into its own variable. [[slnc 500]] Then '
            'both meet at a meeting point, which releases neither until '
            'both have arrived. [[slnc 300]] Only then does each write '
            'back its value, minus one. [[slnc 500]] Run it twenty times, '
            'and the result is nine, twenty times. [[slnc 300]] Not '
            'eight, which two honest subtractions should give. [[slnc '
            '300]] Because both read ten before either wrote, one '
            'subtraction is lost, every single run. [[slnc 400]] The same '
            'meeting point held the packer in place in the earlier demos.'
        ),
    ),
    dict(
        key="12-scheduler",
        kind="bullets",
        title="What The Scheduler Really Does",
        body=[
            "This project pins one interleaving, deliberately.",
            "",
            "The real JVM scheduler chooses none of this",
            "freely elsewhere -- it is free to run these",
            "threads in any order, on any machine.",
            "",
            "A passing test proves the forced interleaving",
            "behaves as shown. Not that every schedule does.",
        ],
        narration=(
            'A quick, honest note, needed in every concurrency video. '
            '[[slnc 400]] Every repeatable result here was made '
            'repeatable on purpose, with a gate or a latch. [[slnc 500]] '
            'Outside these tests, the operating system runs threads in '
            'whatever order it likes, on any machine, on any day. [[slnc '
            '500]] So a passing test here proves one thing. [[slnc 300]] '
            'The one forced timing produces exactly the result you heard. '
            '[[slnc 300]] It does not prove the design is safe under '
            'every possible timing.'
        ),
    ),
    dict(
        key="13-bill",
        kind="bullets",
        title="The Bill",
        body=[
            "Ordering across multiple producers is not",
            "guaranteed -- only FIFO for one of each side.",
            "",
            "A full queue with 'block' is back-pressure",
            "reaching all the way to checkout again --",
            "one layer removed, easier to miss.",
            "",
            "Choosing the bound has no free answer.",
        ],
        narration=(
            "Every pattern has a cost, so here is this one's. [[slnc "
            '500]] First, order is only guaranteed with one producer and '
            'one consumer. [[slnc 300]] Add a second producer, and two '
            'orders can be taken in either order. [[slnc 500]] Second, if '
            'a full queue makes checkout wait, checkout becomes slow '
            'again when the queue fills. [[slnc 300]] The original '
            'problem is back, one step removed, and only under heavy '
            'load. [[slnc 500]] Third, choosing the limit has no free '
            'answer. [[slnc 300]] Too small, and normal bursts get '
            'refused. [[slnc 300]] Too large, and you have quietly '
            'rebuilt the unlimited queue.'
        ),
    ),
    dict(
        key="14-too-much",
        kind="bullets",
        title="When This Is Too Much",
        body=[
            "Worth it: producing and consuming genuinely",
            "happen at different, independent rates --",
            "most real systems with any I/O at all.",
            "",
            "Not worth it: two pieces of code that always",
            "run in lockstep. A queue between them is",
            "ceremony with no decision behind it.",
        ],
        narration=(
            'So, when is this pattern worth it? [[slnc 400]] When '
            'producing and consuming really do happen at different '
            'speeds. [[slnc 300]] That describes most real systems that '
            'read or write anything. [[slnc 500]] It is not worth it '
            'between two pieces of code that always run in step. [[slnc '
            '300]] A queue between them is ceremony, with no real '
            'decision behind it.'
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Try replacing a latch with a",
            "sleep, and run the test fifty times to see how many",
            "of them it takes before it fails.",
        ],
        narration=(
            "That's the Producer Consumer pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'queue with no limit is not safer, it is the thread-per-order '
            'failure with a nicer name. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Replace a latch in one of the tests '
            'with a sleep. [[slnc 300]] Then run the test fifty times, '
            'and count how many runs it takes to fail. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
