"""Scene definitions for the Double-Checked Locking teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Double-Checked Locking',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Double-Checked '
            'Locking pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'double checked locking creates a shared object lazily. It '
            'checks for the object first without a lock, and only takes '
            'the lock, and checks again, when it looks missing. [[slnc '
            '350]] This is another project in the concurrency category, '
            'whose subject is how threads share work and state without '
            'corrupting either. In our online store, the shared thing '
            'that is expensive to build is the price list. [[slnc 300]] '
            'By the end you will see two threads each build the price '
            'list, see the lock-every-time fix and its cost, see the '
            'double check take the lock once, see why the field must be '
            'volatile, see the simplest correct way, and see the bill, '
            'which is that it is ceremony with one way to be subtly '
            'wrong.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The price list is expensive to', 'build.', '', 'So the shop builds it the first', 'time anyone asks.', '', 'Many threads ask, and the first', 'few may ask together.', '', 'How do we build it once?'],
        narration=(
            'Here is the scenario. The price list is expensive to build, '
            'so the shop builds it the first time anyone asks. Many '
            'threads ask, and the first few may ask at the same moment. '
            '[[slnc 300]] The question: how do we build it exactly once?'
        ),
    ),
    dict(
        key='03-naive', kind='console', title='Check, Then Create',
        body="""ONE. Check, then create.
  two threads ask together.
  both see it is missing.
  price lists built: 2.

  each holds a different one.""",
        narration=(
            'First, check, then create. Two threads ask for the shared '
            'price list at the same moment, before it exists. Both see '
            'that it is missing. Both build one. Two price lists were '
            'built, and each thread holds a different one. One of them is '
            'thrown away, and the expensive build was done twice.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Look for the object, without a', 'lock.', '', 'If it is missing, take the lock.', '', 'Look again, in case someone else', 'built it while you waited.', '', 'Only then build it.'],
        narration=(
            'The pattern. Look for the object, without a lock. If it is '
            'missing, take the lock. Then look again, in case someone '
            'else built it while you waited. Only then, build it. Once it '
            'is built, nobody takes the lock again.'
        ),
    ),
    dict(
        key='05-sync', kind='console', title='Lock Every Time',
        body="""TWO. Lock every time.
  the same race: built 1.

  1000 calls after it exists:
  the lock taken 1000 times.""",
        narration=(
            'Second, lock every time. The same two threads, with the lock '
            'taken on every call: one is built. That is correct. But a '
            'thousand calls, long after the price list was built, take '
            'the lock a thousand times. Every caller waits its turn, to '
            'be told something that never changes.'
        ),
    ),
    dict(
        key='06-dcl', kind='console', title='Check, Lock, Check Again',
        body="""THREE. Check twice.
  the same race: built 1.
  the second thread waited,
  looked again, found it.

  1000 calls: 1 lock taken.""",
        narration=(
            'Third, check, lock, check again. The same race builds one. '
            'The second thread waited for the lock, looked again, and '
            'found it already built. And a thousand calls take the lock '
            'once. After that, no call waits for anyone.'
        ),
    ),
    dict(
        key='07-vol', kind='console', title='Why It Must Be Volatile',
        body="""FOUR. Volatile.
  the field is volatile: true.

  without it, a thread could see
  the reference before the
  object is built.

  it cannot be shown on demand:
  a test guards the rule.""",
        narration=(
            'Fourth, why the field must be volatile. It is. Without it, '
            'the Java memory model lets one thread see the reference '
            'before it sees the object fully built. That failure cannot '
            'be produced on demand. It depends on the processor and the '
            'compiler. So it is not demonstrated here. A test guards the '
            'rule instead.'
        ),
    ),
    dict(
        key='08-holder', kind='console', title='The Simplest Correct Way',
        body="""FIVE. A holder.
  before anyone asks: 0 built.
  after two calls: 1 built,
  the same one.

  the JVM does it once, on first
  use. no lock, no volatile.""",
        narration=(
            'Fifth, the simplest correct way. Before anyone asks, nothing '
            'is built. After two calls, one is built, and both got the '
            "same one. The JVM builds a class's static state once, when "
            'the class is first used. There is no lock to write, and no '
            'volatile to forget.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  double-checked: 29 lines.
  holder: 10 lines.

  ceremony, with one way to be
  subtly wrong.

  use it only where the holder
  cannot be used.""",
        narration=(
            'Last, the bill. The double checked version is twenty nine '
            'lines. The holder is ten. Double checked locking is ceremony '
            'with one way to be subtly wrong. It earns its place only '
            'where the holder idiom cannot be used, for example, when '
            'creation needs an argument. And an uncontended lock is '
            'cheap. Measure before deciding the lock on every call is a '
            'problem.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A volatile static field, an if (x', '== null), a synchronized block,', '', 'A private static nested Holder', 'class with one field.', '', 'Lazy<T> and Suppliers.memoize in', 'libraries.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'volatile static field, an if (x == null), a synchronized '
            'block, and another if (x == null). A private static nested '
            'Holder class with one field. Lazy<T> and Suppliers.memoize '
            'in libraries. A comment that says why the field is volatile.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Prefer the class holder idiom, or', 'an enum, for a lazy shared object.', 'If creation needs an argument or', 'can fail and be retried, use', 'double-checked locking, with a', 'volatile field, a local variable,', 'and a test that guards the', 'volatile. If you have not measured', 'the lock as a problem, take the'],
        narration=(
            'Here is my verdict, plainly. Prefer the class holder idiom, '
            'or an enum, for a lazy shared object. If creation needs an '
            'argument or can fail and be retried, use double-checked '
            'locking, with a volatile field, a local variable, and a test '
            'that guards the volatile. If you have not measured the lock '
            'as a problem, take the lock on every call.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. Every number quoted comes from '
            "this program's own output. Nothing depends on a clock, so "
            'every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['Nearly always. Most lazy', 'initialisation can use a holder,', 'an eager static, or a lock on', 'every call, and the cost of a', 'wrong double check is a bug you', 'cannot reproduce.'],
        narration=(
            'So when is it too much? Nearly always. Most lazy '
            'initialisation can use a holder, an eager static, or a lock '
            'on every call, and the cost of a wrong double check is a bug '
            'you cannot reproduce.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Double-Checked Locking. [[slnc 250]] If you take one "
            'sentence away, take this one: double-checked locking saves '
            'the lock after the build, and costs a rule you can break '
            'without seeing it. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'remove the volatile keyword and explain why a test cannot '
            'fail, and what that means. [[slnc 300]] If this helped, a '
            'like genuinely does help other people find it, and subscribe '
            'if you would like the rest of the series. [[slnc 250]] '
            'Thanks for watching.'
        ),
    ),
]
