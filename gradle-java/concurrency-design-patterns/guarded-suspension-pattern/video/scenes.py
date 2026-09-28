"""Scene definitions for the Guarded Suspension teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Guarded Suspension',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Guarded Suspension pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Guarded suspension makes a '
            'thread wait until a condition is true, before it carries on. '
            '[[slnc 300]] It sleeps, instead of asking again and again. '
            '[[slnc 300]] And when it wakes, it checks the condition once '
            'more. [[slnc 600]] Think of waiting for a parcel. [[slnc '
            '300]] You do not open the front door every ten seconds. '
            '[[slnc 300]] You wait until the doorbell rings, and then you '
            'check who it is. [[slnc 700]] In our online store, a '
            'warehouse picker must wait until an order arrives, and then '
            'take it. [[slnc 500]] In this video, a picker that keeps '
            'asking will waste a processor. [[slnc 300]] Then one will '
            'sleep instead. [[slnc 300]] We will hear why the condition '
            'must be checked again after waking, and what a wait with a '
            'time limit gives you. [[slnc 300]] And then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Orders arrive in an inbox at', 'unpredictable times.', '', 'Pickers take them out.', '', 'When there are none, a picker', 'must wait.', '', 'How?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Orders arrive in an '
            'inbox, at unpredictable times. [[slnc 300]] Pickers take '
            'them out, one at a time. [[slnc 400]] When the inbox is '
            'empty, a picker must wait. [[slnc 500]] So here is the '
            'question. [[slnc 300]] How should it wait?'
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
            'First, the naive way: waiting by asking. [[slnc 400]] The '
            'picker asks the inbox, has an order come yet? [[slnc 300]] '
            'Over and over. [[slnc 400]] No order has come, and it has '
            'already asked more than a million times. [[slnc 500]] When '
            'an order finally arrives, it takes it. [[slnc 300]] But the '
            'whole time, it kept a processor busy, doing nothing useful.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A guard: a condition that must be', 'true before the thread goes on.', '', 'If it is false, the thread sleeps.', '', 'Whoever makes it true wakes it.', '', 'On waking, check the guard again,', 'in a loop.'],
        narration=(
            'Now, the pattern. [[slnc 400]] There is a guard: a condition '
            'that must be true before the thread carries on. [[slnc 300]] '
            'Here, the guard is: there is an order in the inbox. [[slnc '
            '500]] If the guard is false, the thread sleeps. [[slnc 300]] '
            'Whoever makes it true wakes the thread. [[slnc 300]] And '
            'when the thread wakes, it checks the guard again, in a loop.'
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
            "Second demo: waiting by sleeping. [[slnc 400]] The picker's "
            'thread is now in the waiting state. [[slnc 300]] It uses no '
            'processor, and asks nothing. [[slnc 500]] Then an order '
            'arrives. [[slnc 300]] The picker is woken, and takes the '
            'order.'
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
            'Third demo: check again after waking. [[slnc 400]] Two '
            'pickers are waiting, and one order arrives. [[slnc 500]] If '
            'the guard is checked with a single if statement, both '
            'pickers are woken. [[slnc 300]] One takes the order. [[slnc '
            '300]] And the other takes nothing at all, an empty result. '
            '[[slnc 500]] If the guard is checked with a while loop, the '
            'second picker wakes, looks again, and finds nothing. [[slnc '
            '300]] So it goes back to waiting. [[slnc 500]] One word, if '
            'or while, makes the difference.'
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
            'Fourth demo: the order came first. [[slnc 400]] An order is '
            'already in the inbox. [[slnc 300]] And the signal that '
            'announced it has already come and gone. [[slnc 500]] A '
            'picker that goes straight to sleep, without looking first, '
            'sleeps forever, even though an order is sitting there. '
            '[[slnc 400]] A picker that checks the guard before waiting '
            'takes the order at once. [[slnc 500]] A wake-up signal is '
            'not a message. [[slnc 300]] It is only a nudge, and it can '
            'be missed.'
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
            'Fifth demo: wait, but not forever. [[slnc 400]] With no '
            'order coming, the picker gives up after one hundred '
            'milliseconds, and gets nothing. [[slnc 400]] With an order '
            'waiting, it takes it at once. [[slnc 500]] A time limit '
            'changes, wait until it is true, into, wait a while, and tell '
            'me if it was not.'
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
            'Finally, the cost. [[slnc 400]] Twenty pickers are waiting, '
            'and one order arrives. [[slnc 300]] The signal called notify '
            'all wakes all twenty. [[slnc 300]] One takes the order. '
            '[[slnc 300]] Nineteen go back to sleep. [[slnc 500]] And a '
            'thread that waits for something nobody will ever send, waits '
            'forever. [[slnc 300]] Every wait needs a plan for how it '
            'ends.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['while (!condition) { wait(); }, or', 'condition.await() in a loop.', '', 'BlockingQueue.take(),', 'CountDownLatch.await(),', '', 'notify and notifyAll beside a', 'state change.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a while loop around a call to wait, or to a '
            "condition's await. [[slnc 300]] Look for a blocking queue's "
            "take method, a count down latch's await, or a future's get. "
            '[[slnc 300]] Look for notify or notify all, right next to a '
            'change of state. [[slnc 300]] And a synchronized method that '
            'starts with a while loop.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use guarded suspension when a', 'thread cannot go on until a', 'condition holds. Prefer a blocking', 'queue or a condition object from', 'the standard library to writing', 'wait and notify yourself. If you', 'do write it, check the guard in a', 'while loop, before waiting and', 'after waking, change the state'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use guarded suspension '
            'when a thread cannot carry on until a condition is true. '
            '[[slnc 500]] Prefer ready-made tools, like a blocking queue, '
            'over writing wait and notify yourself. [[slnc 500]] If you '
            'do write it yourself, follow four rules. [[slnc 300]] Check '
            'the guard in a while loop. [[slnc 300]] Check it before '
            'waiting, and again after waking. [[slnc 300]] Change the '
            'state under the same lock you wait on. [[slnc 300]] And give '
            'every wait a time limit.'
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
        body=['Writing wait and notify by hand is', 'rarely right when a blocking queue', 'does it. And where the caller can', 'give up, balking is simpler than', 'waiting.'],
        narration=(
            'So, when is this too much? [[slnc 400]] Writing wait and '
            'notify by hand is rarely right when a blocking queue already '
            'does it. [[slnc 400]] And where the caller can simply give '
            'up, the Balking pattern is simpler than waiting.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Guarded Suspension. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Guarded suspension '
            'makes a thread sleep until its guard is true, and the guard '
            'must be checked again after every wake. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Change notify all to plain '
            'notify. [[slnc 300]] Then find the situation where a picker '
            'is never woken. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
