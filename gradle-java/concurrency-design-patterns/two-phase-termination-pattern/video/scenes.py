"""Scene definitions for the Two-Phase Termination teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Two-Phase Termination',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Two-Phase '
            'Termination pattern in Java, and it is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'two phase termination stops a thread in two steps. First the '
            'thread is asked to stop, and it finishes what it is doing, '
            'and tidies up. Then the caller waits for it to end, for a '
            'limited time. [[slnc 350]] This is another project in the '
            'concurrency category, whose subject is how threads share '
            'work and state without corrupting either. In our online '
            'store, the job is shutting down the order worker without '
            'losing or damaging an order. [[slnc 300]] By the end you '
            'will see a worker stopped mid-order and leave the order half '
            'written, see it asked to stop and finish the order, see a '
            'sleeping worker need waking, see cleanup run on the way out, '
            'see a worker that will not stop, and see the bill, which is '
            'the orders still waiting.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The order worker writes each order', 'as three lines.', '', 'The shop is shut down for an', 'upgrade.', '', 'The worker is in the middle of', 'an order.', '', 'How do we stop it?'],
        narration=(
            'Here is the scenario. The order worker writes each order as '
            'three lines. The shop is shut down for an upgrade, and the '
            'worker is in the middle of an order. [[slnc 300]] The '
            'question: how do we stop it?'
        ),
    ),
    dict(
        key='03-plug', kind='console', title='Pull The Plug',
        body="""ONE. The plug.
  the ledger is closed while
  ORD-1 is half written.
  lines: line 1 only.

  left half written: true.""",
        narration=(
            'First, pull the plug. The shop shuts down, and closes the '
            'ledger, while order one is half written. Only line one was '
            'written. The worker tries to write line two, and finds the '
            'ledger closed. The order is left half written, with a line '
            'one, and no line two or three.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Phase one: ask it to stop.', '', 'It finishes what it is doing,', 'tidies up, and ends.', '', 'Phase two: wait for it to end,', 'for a limited time.', '', 'Then decide what to do if it', 'did not.'],
        narration=(
            'The pattern. Phase one: ask the thread to stop. It finishes '
            'what it is doing, tidies up, and ends. Phase two: wait for '
            'it to end, for a limited time. Then decide what to do if it '
            'did not.'
        ),
    ),
    dict(
        key='05-ask', kind='console', title='Ask It To Stop, And Let It Finish',
        body="""TWO. Ask, and let it finish.
  stop requested mid-order.
  the worker finishes ORD-1:
  3 lines.
  it starts no other.

  half written: false.""",
        narration=(
            'Second, ask it to stop, and let it finish. Stop is requested '
            'while order one is half written, and order two is waiting. '
            'The worker finishes order one, all three lines, and starts '
            'nothing else. It ends. Three lines in the ledger, all of '
            "order one's, none of order two's. Nothing is half written."
        ),
    ),
    dict(
        key='06-wake', kind='console', title='A Worker That Is Asleep',
        body="""THREE. Asleep.
  a flag alone: the worker is
  still WAITING.

  a flag and an interrupt:
  it ends.""",
        narration=(
            'Third, a worker that is asleep. A stop request that only '
            'sets a flag does nothing to a worker that is waiting for an '
            'order. It is still waiting. The same request, with an '
            'interrupt to wake it, and the worker ends. A flag is not '
            'enough for a thread that is not looking at it.'
        ),
    ),
    dict(
        key='07-tidy', kind='console', title='Tidy Up On The Way Out',
        body="""FOUR. Tidy up.
  interrupted while waiting.
  did its cleanup run: true.

  the cleanup is in a finally
  block: it runs however the
  worker ends.""",
        narration=(
            'Fourth, tidy up on the way out. The worker is interrupted '
            'while it is waiting. Did its cleanup run? Yes. The cleanup '
            'is in a finally block, so it runs however the worker ends: '
            'finished, interrupted, or failed.'
        ),
    ),
    dict(
        key='08-stuck', kind='console', title='A Worker That Will Not Stop',
        body="""FIVE. Will not stop.
  stuck in something that
  ignores the request.
  200 ms later: not ended,
  still alive.

  phase two has a time limit.
  there is no safe way to force
  it.""",
        narration=(
            'Fifth, a worker that will not stop. It is stuck in something '
            'that ignores the request. After waiting two hundred '
            'milliseconds, it has not ended, and is still alive. That is '
            'why phase two has a time limit. What happens next is a '
            'decision: report it, wait longer, or restart the process. '
            'Java gives no safe way to force a thread to stop.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  stopped with 5 orders waiting.
  finished 1, pending 5.

  the 5 were accepted from
  customers, and not done.

  a stop needs a policy.
  it took as long as the order in
  progress.""",
        narration=(
            'Last, the bill. The worker was stopped with five orders '
            'still waiting: one finished, five pending. Those five were '
            'accepted from customers, and have not been done. A stop '
            'needs a policy: finish them first, hand them to another '
            'worker, or save them. And shutting down took as long as the '
            'order in progress. Stopping is never instant.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A volatile boolean stopRequested', 'checked at the top of a loop.', '', 'ExecutorService.shutdown()', 'followed by', '', 'Thread.interrupt() followed by', 'Thread.join(timeout).'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'volatile boolean stopRequested checked at the top of a loop. '
            'ExecutorService.shutdown() followed by '
            'awaitTermination(timeout, unit). Thread.interrupt() followed '
            'by Thread.join(timeout). Shutdown hooks and '
            'graceful-shutdown settings in servers and frameworks.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Stop threads in two phases: ask,', 'then wait with a limit. Let a', 'worker finish the unit of work it', 'is in, and check for the request', 'between units. Wake it if it may', 'be waiting. Put cleanup in a', 'finally block. Decide what happens', 'to the queued work, and to a', 'worker that does not end. Never'],
        narration=(
            'Here is my verdict, plainly. Stop threads in two phases: '
            'ask, then wait with a limit. Let a worker finish the unit of '
            'work it is in, and check for the request between units. Wake '
            'it if it may be waiting. Put cleanup in a finally block. '
            'Decide what happens to the queued work, and to a worker that '
            'does not end. Never force-stop a thread.'
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
        body=['For a thread that holds no state', 'and whose work can be repeated,', 'stopping at once is fine, and a', 'daemon thread can simply be left.', 'The pattern matters where a stop', 'can damage something.'],
        narration=(
            'So when is it too much? For a thread that holds no state and '
            'whose work can be repeated, stopping at once is fine, and a '
            'daemon thread can simply be left. The pattern matters where '
            'a stop can damage something.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Two-Phase Termination. [[slnc 250]] If you take one "
            'sentence away, take this one: two-phase termination stops a '
            'thread by asking and then waiting, and the price is that '
            'stopping takes as long as the work in progress. [[slnc 350]] '
            'The full source, the written notes, the diagrams and an '
            'animated walkthrough are all in the repository, running '
            'offline with nothing installed but a Java development kit. '
            '[[slnc 300]] If you try one exercise, make the worker finish '
            'its queued orders before stopping, and decide how long it '
            'may take. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
