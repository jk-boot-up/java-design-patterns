"""Scene definitions for the Object Pool teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Object Pool',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Object Pool '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: keep '
            'a few objects that are expensive to create, lend them out, '
            'and take them back, so the cost of creating them is paid '
            'once. [[slnc 350]] This is the second project in the '
            'foundational category. It is one of the most over-applied '
            'ideas in Java, so this video shows the pattern working, and '
            'then shows four ways it goes wrong, with evidence. In our '
            'online store, the expensive thing is a connection to the '
            'payment gateway. [[slnc 300]] By the end you will know the '
            'one kind of object worth pooling, why pooling a small one '
            'makes things slower, and I will give you my verdict plainly.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The payment gateway connection takes', '200 milliseconds to establish.', '', 'A checkout makes payments.', '', 'How many connections should it make?'],
        narration=(
            'Here is the scenario. In the online store, a connection to '
            'the payment gateway takes two hundred milliseconds to '
            'establish. That is a network handshake. [[slnc 300]] The '
            'checkout makes payments. The question: how many connections '
            'should it make?'
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
            'The simplest answer: a new connection for every payment. Ten '
            'payments. Ten connections opened. Two thousand and '
            'seventy-five milliseconds. [[slnc 300]] Every payment paid '
            'the full two hundred millisecond handshake. It is simple, '
            'and correct, and slow.'
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
            'The pattern: a pool. Open a few connections, once, up front. '
            'Lend one out for each payment, and take it back afterwards. '
            '[[slnc 300]] Ten payments. Two connections opened. Four '
            'hundred and twelve milliseconds, including opening the pool. '
            'About a fifth of the time. [[slnc 300]] And this is the '
            'right use of the pattern. The expensive part is outside the '
            'Java virtual machine: a network handshake.'
        ),
    ),
    dict(
        key='05-warning', kind='bullets', title='Now, The Bill',
        body=['Pooling is one of the most', 'over-applied ideas in Java.', '', 'Four ways it goes wrong,', 'each one demonstrated.'],
        narration=(
            'Now the bill, and here it is larger than the benefit, in '
            'most cases. Pooling is one of the most over-applied ideas in '
            'Java. There are four ways it goes wrong, and each one is '
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
            'First cost. Try pooling a small object: a receipt, with '
            'three fields. Twenty million operations. Allocating one, '
            'forced onto the heap: about two nanoseconds. Borrowing one '
            'from a pool: about six and a half. [[slnc 300]] The pool is '
            'nearly three times slower. It creates four objects, against '
            'twenty million, and still loses. [[slnc 300]] The reason: '
            'the pool adds a lock, and moves objects through shared '
            'memory. The Java allocator is little more than moving a '
            'pointer.'
        ),
    ),
    dict(
        key='07-method', kind='bullets', title='How This Was Measured',
        body=['Same work per operation.', 'Five warm-up rounds, discarded.', 'Nine rounds, median reported.', '', 'Allocation measured twice: as plain', 'code, and forced onto the heap.', '', 'The pool is compared against the', 'one that cannot be optimised away.'],
        narration=(
            'A claim like that needs its method. Each version does the '
            'same work. Five warm-up rounds are thrown away. Nine '
            'measured rounds follow, and the median is reported. [[slnc '
            '300]] Allocation is measured twice. As plain code, the '
            'compiler can sometimes remove it entirely, which is why it '
            'reads under a nanosecond. That would be an unfair '
            'comparison. So it is also measured with every object stored '
            'where it cannot be removed. The pool is compared against '
            'that one. [[slnc 300]] The numbers vary by machine. The '
            'direction, and a ratio of about three, held on every run.'
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
            'Second cost. A returned object carries its old state. [[slnc '
            '300]] Ada pays, and the connection goes back. Grace borrows '
            'that very connection, and asks who used it last. Ada '
            'Lovelace. [[slnc 300]] That is a security bug, not a '
            'performance one, and it is the failure that actually happens '
            'in the field. The fix is a reset when the connection is '
            'returned. Every pool needs one.'
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
            'Third cost. A leaked object is never returned. Two callers '
            'borrow both connections, and never give them back. [[slnc '
            '300]] A third payment arrives. In this demo it waits three '
            'hundred milliseconds, and gives up, rescued by a timeout. '
            'Without that timeout, it would wait forever. The application '
            'hangs. That is worse than a slow start.'
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
            'Fourth cost. The size is a guess, and it can be wrong in '
            'both directions. Four payments at the same moment, each '
            'needing fifty milliseconds. [[slnc 300]] A pool of one: they '
            'queue, and it takes two hundred and eighteen. A pool of '
            'four: fifty-eight. [[slnc 300]] A pool of fifty: fifty '
            'connections opened, and forty-six sitting idle, held open, '
            'for four payments.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Pool what is expensive outside', 'the JVM:', 'connections, threads, native handles.', '', 'Pool nothing else.', '', "A thread pool is the pattern's other", 'clearly correct use.'],
        narration=(
            'Here is my verdict, plainly. Pool the things that are '
            'expensive outside the Java virtual machine: connections, '
            'threads, native handles. Pool nothing else. [[slnc 300]] '
            'That is why connection pools and thread pools exist, and '
            'general object pools do not. A thread pool, from the '
            "concurrency category, is this same idea, and the pattern's "
            'other clearly correct use.'
        ),
    ),
    dict(
        key='12-recognise', kind='bullets', title='How To Recognise It',
        body=['A class called Pool, with borrow', 'and release.', '', 'Every JDBC DataSource.', 'ExecutorService: a pool of threads.', '', 'A stack of reusable objects with', 'a reset call, avoiding garbage.'],
        narration=(
            'How do you recognise this in code you did not write? A class '
            'called pool, with borrow and release. Every J D B C data '
            'source is a connection pool. Every executor service is a '
            'pool of threads. And be suspicious of a stack of reusable '
            'objects, with a reset call, in code claiming to avoid '
            'garbage collection. That is usually the slow version.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The handshake is simulated by a', 'sleep, standing in for a network.', '', 'The benchmark is real, hand-rolled,', 'and its method is written down.', '', 'Timings vary by machine.'],
        narration=(
            'The same honest admission as everywhere in this course. The '
            'handshake is simulated with a sleep, standing in for a '
            'network. The benchmark is real, but it is hand-rolled, not a '
            'professional harness, and its method is written down so you '
            'can check it. The timings vary by machine. The direction '
            'does not.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['For anything cheap to create,', 'which is nearly everything.'],
        narration=(
            'So when is a pool too much? For anything cheap to create. '
            'Which is nearly everything.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Change the receipt to hold a big', 'array, and see if the ordering changes.'],
        narration=(
            "That's the Object Pool. [[slnc 250]] If you take one "
            'sentence away, take this one: pool what is expensive outside '
            'the Java virtual machine, and nothing else. [[slnc 350]] The '
            'full source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, change the receipt to hold a large '
            'array, and see whether the ordering changes, and why. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
