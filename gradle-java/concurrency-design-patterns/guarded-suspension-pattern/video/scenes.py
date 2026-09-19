"""Scene definitions for the Guarded Suspension teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Guarded Suspension',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Guarded '
            'Suspension pattern in Java, and it is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'guarded suspension makes a thread wait until a condition is '
            'true before it carries on. It sleeps, rather than asking '
            'again and again, and it checks the condition again when it '
            'wakes. [[slnc 350]] This is another project in the '
            'concurrency category, whose subject is how threads share '
            'work and state without corrupting either. In our online '
            "store, the picker's job is to wait until an order arrives, "
            'and then take it. [[slnc 300]] By the end you will see a '
            'picker that keeps asking use a processor for nothing, see '
            'one that sleeps, see why the guard must be checked again '
            'after waking, see a wake-up that arrived too early, see a '
            'wait with a limit, and see the bill, which is that every '
            'waiter is woken for one order.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Orders arrive in an inbox at', 'unpredictable times.', '', 'Pickers take them out.', '', 'When there are none, a picker', 'must wait.', '', 'How?'],
        narration=(
            'Here is the scenario. Orders arrive in an inbox at '
            'unpredictable times. Pickers take them out. When there are '
            'none, a picker must wait. [[slnc 300]] The question: how '
            'should it wait?'
        ),
    ),
    dict(
        key='03-spin', kind='console', title='Waiting By Asking',
        body="""ONE. Asking.
  the picker asks whether an
  order has come, over and over.
  more than a million times,
  and none has come.

  a processor busy for nothing.""",
        narration=(
            'First, waiting by asking. The picker asks the inbox whether '
            'an order has come, over and over. No order has come, and it '
            'has already asked more than a million times. It took the '
            'order when one arrived. But the whole time, it kept a '
            'processor busy doing nothing.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A guard: a condition that must be', 'true before the thread goes on.', '', 'If it is false, the thread sleeps.', '', 'Whoever makes it true wakes it.', '', 'On waking, check the guard again,', 'in a loop.'],
        narration=(
            'The pattern. A guard: a condition that must be true before '
            'the thread goes on. If it is false, the thread sleeps. '
            'Whoever makes it true wakes it. And on waking, the thread '
            'checks the guard again, in a loop.'
        ),
    ),
    dict(
        key='05-sleep', kind='console', title='Waiting By Sleeping',
        body="""TWO. Sleeping.
  the picker's thread:
  WAITING.
  no processor used.

  an order arrives: woken,
  and takes ORD-1.""",
        narration=(
            "Second, waiting by sleeping. The picker's thread is in the "
            'waiting state. It is using no processor, and it has asked '
            'nothing. An order arrives. The picker is woken, and takes '
            'it.'
        ),
    ),
    dict(
        key='06-while', kind='console', title='Ask Again After Waking',
        body="""THREE. Ask again.
  two pickers, one order.
  guard with if: they took
  ORD-1 and null.
  guard with while: ORD-1 only.

  the second picker looked,
  found nothing, and waited.""",
        narration=(
            'Third, ask again after waking. Two pickers wait, and one '
            'order arrives. With the guard checked with an if, both are '
            'woken, and one of them takes nothing: null. With a while, '
            'the second picker wakes, looks again, finds nothing, and '
            'goes back to waiting. One word is the difference.'
        ),
    ),
    dict(
        key='07-early', kind='console', title='The Order Came First',
        body="""FOUR. Too early.
  the order was already there.
  a picker that waits without
  looking: WAITING, though an
  order is there.

  looking first: takes it.""",
        narration=(
            'Fourth, the order came first. The order was already there, '
            'and the notification that announced it has come and gone. A '
            'picker that waits without looking first goes to sleep, '
            'though an order is sitting there. A picker that checks the '
            'guard before it waits takes the order at once. A '
            'notification is not a message. It is only a nudge.'
        ),
    ),
    dict(
        key='08-limit', kind='console', title='Wait, But Not For Ever',
        body="""FIVE. A limit.
  no order: gives up after
  100 ms.
  an order there: ORD-1.

  wait a while, and tell me if
  it was not true.""",
        narration=(
            'Fifth, wait, but not forever. With no order coming, the '
            'picker gives up after a hundred milliseconds, and gets '
            'nothing. With an order there, it takes it at once. A limit '
            'turns wait until it is true into wait a while, and tell me '
            'if it was not.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  20 pickers waiting.
  1 order, notifyAll:
  20 woke, 1 took it,
  19 went back to sleep.

  a wait for something that is
  never sent lasts for ever.""",
        narration=(
            'Last, the bill. Twenty pickers are waiting, and one order '
            'arrives. Notify all wakes all twenty. One takes the order. '
            'Nineteen go back to sleep. And a thread that waits for '
            'something nobody will ever send waits forever. Every wait '
            'needs a plan for how it ends.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['while (!condition) { wait(); }, or', 'condition.await() in a loop.', '', 'BlockingQueue.take(),', 'CountDownLatch.await(),', '', 'notify and notifyAll beside a', 'state change.'],
        narration=(
            'How do you recognise this in code you did not write? while '
            '(!condition) { wait(); }, or condition.await() in a loop. '
            'BlockingQueue.take(), CountDownLatch.await(), Future.get(). '
            'notify and notifyAll beside a state change. A synchronized '
            'method that starts with a while.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use guarded suspension when a', 'thread cannot go on until a', 'condition holds. Prefer a blocking', 'queue or a condition object from', 'the standard library to writing', 'wait and notify yourself. If you', 'do write it, check the guard in a', 'while loop, before waiting and', 'after waking, change the state'],
        narration=(
            'Here is my verdict, plainly. Use guarded suspension when a '
            'thread cannot go on until a condition holds. Prefer a '
            'blocking queue or a condition object from the standard '
            'library to writing wait and notify yourself. If you do write '
            'it, check the guard in a while loop, before waiting and '
            'after waking, change the state under the same lock you wait '
            'on, and give the wait a limit.'
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
        body=['Writing wait and notify by hand is', 'rarely right when a blocking queue', 'does it. And where the caller can', 'give up, balking is simpler than', 'waiting.'],
        narration=(
            'So when is it too much? Writing wait and notify by hand is '
            'rarely right when a blocking queue does it. And where the '
            'caller can give up, balking is simpler than waiting.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Guarded Suspension. [[slnc 250]] If you take one "
            'sentence away, take this one: guarded suspension makes a '
            'thread sleep until a guard is true, and the guard must be '
            'checked again after every wake. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, change notifyAll to notify, and '
            'find the case where a picker is never woken. [[slnc 300]] If '
            'this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
