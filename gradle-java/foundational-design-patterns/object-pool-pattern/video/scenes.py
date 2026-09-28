"""Scene definitions for the Object Pool teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Object Pool',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Object Pool pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An object pool keeps a few '
            'objects that are expensive to create. [[slnc 300]] It lends '
            'them out, and takes them back. [[slnc 300]] So the cost of '
            'creating them is paid only once. [[slnc 600]] Think of a '
            'bike rental scheme. [[slnc 300]] The city does not build a '
            'new bike for every ride. [[slnc 300]] You borrow one, ride, '
            'and return it for the next person. [[slnc 700]] This pattern '
            'is one of the most over-used ideas in Java. [[slnc 300]] So '
            'this video shows it working, and then four ways it goes '
            'wrong, with evidence. [[slnc 500]] In our online store, the '
            'expensive thing is a connection to the payment gateway. '
            '[[slnc 300]] By the end, you will know the one kind of '
            'object worth pooling. [[slnc 300]] And why pooling a small '
            'object makes things slower.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The payment gateway connection takes', '200 milliseconds to establish.', '', 'A checkout makes payments.', '', 'How many connections should it make?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Opening a connection to '
            'the payment gateway takes two hundred milliseconds. [[slnc '
            '300]] That is a network handshake. [[slnc 500]] The checkout '
            'makes many payments. [[slnc 300]] So here is the question. '
            '[[slnc 300]] How many connections should it open?'
        ),
    ),
    dict(
        key='03-naive', kind='console', title='A Connection Per Payment',
        body="""ONE. A new connection each.
  10 payments:
  10 connections opened,
  2075ms.

  every payment paid a 200ms
  handshake.

  simple, correct, slow.""",
        narration=(
            'First, the simplest way: a new connection for every payment. '
            '[[slnc 400]] Ten payments. [[slnc 300]] Ten connections '
            'opened. [[slnc 300]] About two seconds in total. [[slnc '
            '500]] Every payment paid the full two hundred millisecond '
            'handshake. [[slnc 300]] It is simple, correct, and slow.'
        ),
    ),
    dict(
        key='04-pool', kind='console', title='The Pattern: A Pool',
        body="""TWO. A pool of two.
  10 payments:
  2 connections opened,
  412ms,
  including opening the pool.

  the right use: the cost is
  outside the JVM.""",
        narration=(
            'Second demo: the pattern, a pool. [[slnc 400]] Open a few '
            'connections once, at the start. [[slnc 300]] Lend one out '
            'for each payment, and take it back afterwards. [[slnc 500]] '
            'Ten payments. [[slnc 300]] Only two connections opened. '
            '[[slnc 300]] About four hundred milliseconds, including '
            'opening the pool. [[slnc 300]] Roughly a fifth of the time. '
            '[[slnc 500]] And this is the right use of the pattern. '
            '[[slnc 300]] The expensive part happens outside Java, in a '
            'network handshake.'
        ),
    ),
    dict(
        key='05-warning', kind='bullets', title='Now, The Bill',
        body=['Pooling is one of the most', 'over-applied ideas in Java.', '', 'Four ways it goes wrong,', 'each one demonstrated.'],
        narration=(
            'Now the costs. [[slnc 300]] And here, in most cases, they '
            'are bigger than the benefit. [[slnc 500]] Pooling is one of '
            'the most over-used ideas in Java. [[slnc 300]] There are '
            'four ways it goes wrong. [[slnc 300]] And each one is '
            'demonstrated.'
        ),
    ),
    dict(
        key='06-small', kind='console', title='Cost One: It Is Slower',
        body="""THREE. A small object.
  allocating, forced onto
  the heap: 2.19 ns
  pooling: 6.44 ns

  the pool is 2.9 times
  slower.

  objects created:
  20 million against 4.""",
        narration=(
            'Third demo: the first cost, it can be slower. [[slnc 400]] '
            "Let's try pooling a small object: a receipt, with three "
            'fields. [[slnc 300]] Twenty million operations. [[slnc 500]] '
            'Creating a new receipt each time takes about two '
            'nanoseconds. [[slnc 300]] Borrowing one from a pool takes '
            'about six and a half. [[slnc 500]] The pool is nearly three '
            'times slower. [[slnc 300]] It creates only four objects, '
            'instead of twenty million, and it still loses. [[slnc 500]] '
            'Why? [[slnc 300]] The pool needs a lock, and moves objects '
            'through shared memory. [[slnc 300]] Java creating a small '
            'object is little more than moving a pointer.'
        ),
    ),
    dict(
        key='07-method', kind='bullets', title='How This Was Measured',
        body=['Same work per operation.', 'Five warm-up rounds, discarded.', 'Nine rounds, median reported.', '', 'Allocation measured twice: as plain', 'code, and forced onto the heap.', '', 'The pool is compared against the', 'one that cannot be optimised away.'],
        narration=(
            'A claim like that needs a careful method, so here it is. '
            '[[slnc 400]] Each version does exactly the same work. [[slnc '
            '300]] Five warm-up rounds are thrown away. [[slnc 300]] Then '
            'nine measured rounds, and the middle result is reported. '
            '[[slnc 500]] Creating objects is measured in a way the '
            'compiler cannot optimise away. [[slnc 300]] So the '
            'comparison is fair. [[slnc 500]] The exact numbers vary by '
            'machine. [[slnc 300]] But the direction, and a ratio of '
            'about three, held on every run.'
        ),
    ),
    dict(
        key='08-dirty', kind='console', title='Cost Two: A Dirty Return',
        body="""FOUR. A dirty return.
  Grace borrows the connection
  Ada just returned.

  last card holder:
  Ada Lovelace

  a security bug.
  with a reset: null.""",
        narration=(
            'Fourth demo: the second cost, a dirty return. [[slnc 400]] A '
            'returned object still carries its old state. [[slnc 500]] '
            'Ada pays, and her connection goes back to the pool. [[slnc '
            '300]] Then Grace borrows that very same connection, and asks '
            'who used it last. [[slnc 300]] The answer is: Ada Lovelace. '
            '[[slnc 500]] That is a security bug, not a speed problem. '
            '[[slnc 300]] And it is the failure that really happens in '
            'the field. [[slnc 500]] The fix is to reset each connection '
            'when it is returned. [[slnc 300]] Every pool needs one.'
        ),
    ),
    dict(
        key='09-leak', kind='console', title='Cost Three: A Leak',
        body="""FIVE. A leak.
  two borrowers never return
  their connections.

  a third payment waited 310ms
  and got nothing.

  without the timeout: waits
  forever.""",
        narration=(
            'Fifth demo: the third cost, a leak. [[slnc 400]] A leaked '
            'object is borrowed, and never returned. [[slnc 300]] Two '
            'callers borrow both connections, and never give them back. '
            '[[slnc 500]] Then a third payment arrives. [[slnc 300]] '
            'Here, it waits about three hundred milliseconds, and gives '
            'up, thanks to a timeout. [[slnc 300]] Without that timeout, '
            'it would wait forever. [[slnc 300]] And the whole '
            'application would hang.'
        ),
    ),
    dict(
        key='10-size', kind='console', title='Cost Four: Sizing Is A Guess',
        body="""SIX. Sizing.
  4 payments at once:
  pool of 1:  218ms
  pool of 4:   58ms

  pool of 50: 50 connections
  opened, 46 idle.""",
        narration=(
            'Last demo: the fourth cost, sizing is a guess. [[slnc 400]] '
            'And it can be wrong in both directions. [[slnc 500]] Four '
            'payments arrive at once, each needing fifty milliseconds. '
            '[[slnc 300]] With a pool of one, they queue, and it takes '
            'over two hundred milliseconds. [[slnc 300]] With a pool of '
            'four, it takes under sixty. [[slnc 300]] With a pool of '
            'fifty, fifty connections are opened, and forty-six sit idle, '
            'held open, for just four payments.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Pool what is expensive outside', 'the JVM:', 'connections, threads, native handles.', '', 'Pool nothing else.', '', "A thread pool is the pattern's other", 'clearly correct use.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Pool the things that '
            'are expensive outside Java. [[slnc 300]] Connections, '
            'threads, and handles to the operating system. [[slnc 300]] '
            'And pool nothing else. [[slnc 500]] That is why connection '
            'pools and thread pools exist, and general object pools do '
            'not. [[slnc 300]] A thread pool is this same idea, and the '
            "pattern's other clearly correct use."
        ),
    ),
    dict(
        key='12-recognise', kind='bullets', title='How To Recognise It',
        body=['A class called Pool, with borrow', 'and release.', '', 'Every JDBC DataSource.', 'ExecutorService: a pool of threads.', '', 'A stack of reusable objects with', 'a reset call, avoiding garbage.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a class called pool, with borrow and '
            'release methods. [[slnc 300]] Every J D B C data source is a '
            'connection pool. [[slnc 300]] Every executor service is a '
            'pool of threads. [[slnc 500]] And be suspicious of a stack '
            'of reusable objects, with a reset method, in code that '
            'claims to avoid garbage collection. [[slnc 300]] That is '
            'usually the slow version.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The handshake is simulated by a', 'sleep, standing in for a network.', '', 'The benchmark is real, hand-rolled,', 'and its method is written down.', '', 'Timings vary by machine.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'network handshake is simulated, with a short sleep. [[slnc '
            '300]] The speed test is real, but hand-made, not a '
            'professional tool. [[slnc 300]] And its method is written '
            'down, so you can check it. [[slnc 500]] The timings vary by '
            'machine. [[slnc 300]] The direction does not.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['For anything cheap to create,', 'which is nearly everything.'],
        narration=(
            'So, when is a pool too much? [[slnc 400]] For anything that '
            'is cheap to create. [[slnc 300]] Which is nearly everything.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Change the receipt to hold a big', 'array, and see if the ordering changes.'],
        narration=(
            "That's the Object Pool pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Pool what is '
            'expensive outside Java, and nothing else. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Change the receipt so it '
            'holds a large array. [[slnc 300]] Then see whether the '
            'winner changes, and work out why. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
