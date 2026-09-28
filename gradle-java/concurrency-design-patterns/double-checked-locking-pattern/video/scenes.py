"""Scene definitions for the Double-Checked Locking teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Double-Checked Locking',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Double-Checked Locking pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Double-checked '
            'locking creates a shared object only when it is first '
            'needed. [[slnc 300]] It checks for the object first, without '
            'a lock. [[slnc 300]] Only if the object looks missing does '
            'it take the lock, and check again. [[slnc 600]] Think of the '
            'last person leaving an office. [[slnc 300]] You glance at '
            'the lights on the way out. [[slnc 300]] Only if they look '
            'on, do you walk back and check properly before switching '
            'them off. [[slnc 700]] In our online store, the price list '
            'is expensive to build. [[slnc 500]] In this video, two '
            'threads will build it twice. [[slnc 300]] We will try '
            'locking every time, then checking twice. [[slnc 300]] We '
            'will hear why one field must be volatile, and the simplest '
            'correct way to do it. [[slnc 300]] And then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The price list is expensive to', 'build.', '', 'So the shop builds it the first', 'time anyone asks.', '', 'Many threads ask, and the first', 'few may ask together.', '', 'How do we build it once?'],
        narration=(
            "Here is the scenario. [[slnc 400]] The shop's price list is "
            'expensive to build. [[slnc 300]] So the shop builds it the '
            'first time anyone asks for it. [[slnc 500]] Many threads ask '
            'for it. [[slnc 300]] And the first few may ask at exactly '
            'the same moment. [[slnc 500]] So here is the question. '
            '[[slnc 300]] How do we build it exactly once?'
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
            'First, the naive way: check, then create. [[slnc 400]] Two '
            'threads ask for the price list at the same moment, before it '
            'exists. [[slnc 300]] Both see that it is missing. [[slnc '
            '300]] So both build one. [[slnc 500]] Two price lists were '
            'built. [[slnc 300]] And each thread holds a different one. '
            '[[slnc 300]] One is thrown away, and the expensive work was '
            'done twice.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Look for the object, without a', 'lock.', '', 'If it is missing, take the lock.', '', 'Look again, in case someone else', 'built it while you waited.', '', 'Only then build it.'],
        narration=(
            'Now, the pattern. [[slnc 400]] First, look for the object, '
            'without a lock. [[slnc 300]] If it is missing, take the '
            'lock. [[slnc 300]] Then look again, in case another thread '
            'built it while you were waiting. [[slnc 300]] Only then, '
            'build it. [[slnc 500]] Once it exists, nobody takes the lock '
            'again.'
        ),
    ),
    dict(
        key='05-sync', kind='console', title='Lock Every Time',
        body="""TWO. Lock every time.
  the same race: built 1.

  1000 calls after it exists:
  the lock taken 1000 times.""",
        narration=(
            'Second demo: lock every time. [[slnc 400]] The same two '
            'threads, but now every call takes the lock. [[slnc 300]] '
            'Only one price list is built. [[slnc 300]] That is correct. '
            '[[slnc 500]] But then a thousand calls arrive, long after '
            'the price list exists. [[slnc 300]] And the lock is taken a '
            'thousand times. [[slnc 400]] Every caller waits its turn, '
            'just to be told something that never changes.'
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
            'Third demo: check, lock, and check again. [[slnc 400]] The '
            'same race builds just one price list. [[slnc 400]] The '
            'second thread waited for the lock. [[slnc 300]] Then it '
            'looked again, and found the list already built. [[slnc 500]] '
            'And a thousand calls take the lock only once. [[slnc 300]] '
            'After that, no call waits for anyone.'
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
            'Fourth: why the field must be marked volatile. [[slnc 400]] '
            'In this project, it is. [[slnc 500]] Without volatile, '
            "Java's memory rules allow a strange thing. [[slnc 300]] One "
            'thread could see the reference to the price list, before the '
            'price list is fully built. [[slnc 500]] That failure cannot '
            'be produced on demand. [[slnc 300]] It depends on the '
            'processor and the compiler. [[slnc 300]] So it is not '
            'demonstrated here. [[slnc 300]] Instead, a test checks that '
            'the field stays volatile.'
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
            'Fifth demo: the simplest correct way, called the holder '
            'idiom. [[slnc 400]] Before anyone asks, nothing is built. '
            '[[slnc 300]] After two calls, one is built, and both callers '
            'got the same one. [[slnc 500]] How? [[slnc 300]] Java builds '
            "a class's static data once, when the class is first used. "
            '[[slnc 300]] So the price list sits in a small holder class, '
            'and Java does the rest. [[slnc 400]] There is no lock to '
            'write, and no volatile to forget.'
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
            'Finally, the cost. [[slnc 400]] The double-checked version '
            'is twenty-nine lines. [[slnc 300]] The holder version is '
            'ten. [[slnc 500]] Double-checked locking is ceremony, with '
            'one way to be quietly wrong. [[slnc 300]] It only earns its '
            'place where the holder cannot be used. [[slnc 300]] For '
            'example, when building the object needs an argument. [[slnc '
            '500]] And remember, a lock that nobody else is holding is '
            'cheap. [[slnc 300]] Measure before deciding that locking on '
            'every call is a problem.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A volatile static field, an if (x', '== null), a synchronized block,', '', 'A private static nested Holder', 'class with one field.', '', 'Lazy<T> and Suppliers.memoize in', 'libraries.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a volatile static field, an if statement '
            'checking for null, a synchronized block, and then the same '
            'null check again. [[slnc 300]] Look for a small private '
            'static class called Holder, with one field. [[slnc 300]] '
            'Look for helpers like Lazy, or memoize, in libraries. [[slnc '
            '300]] And look for a comment explaining why the field is '
            'volatile.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Prefer the class holder idiom, or', 'an enum, for a lazy shared object.', 'If creation needs an argument or', 'can fail and be retried, use', 'double-checked locking, with a', 'volatile field, a local variable,', 'and a test that guards the', 'volatile. If you have not measured', 'the lock as a problem, take the'],
        narration=(
            'So, here is the verdict. [[slnc 400]] For a shared object '
            'built on first use, prefer the holder idiom, or an enum. '
            '[[slnc 500]] If building the object needs an argument, or '
            'can fail and be retried, use double-checked locking. [[slnc '
            '300]] With a volatile field, a local variable, and a test '
            'that guards the volatile. [[slnc 500]] And if you have not '
            'measured the lock as a problem, simply take the lock on '
            'every call.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['Nearly always. Most lazy', 'initialisation can use a holder,', 'an eager static, or a lock on', 'every call, and the cost of a', 'wrong double check is a bug you', 'cannot reproduce.'],
        narration=(
            'So, when is this too much? [[slnc 400]] Nearly always. '
            '[[slnc 300]] Most objects built on first use can use a '
            'holder, an eagerly built static, or a lock on every call. '
            '[[slnc 300]] And a wrong double check causes a bug you '
            'cannot reproduce.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Double-Checked Locking. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Double-checked '
            'locking saves the lock after the object is built, and costs '
            'a rule you can break without ever seeing it fail. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Remove the '
            'volatile keyword. [[slnc 300]] Then explain why no test can '
            'fail, and what that means for your code. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
