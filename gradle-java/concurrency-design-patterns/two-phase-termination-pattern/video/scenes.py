"""Scene definitions for the Two-Phase Termination teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Two-Phase Termination',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Two-Phase Termination pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Two-phase '
            'termination stops a thread in two steps. [[slnc 300]] First, '
            'the thread is asked to stop. [[slnc 300]] It finishes what '
            'it is doing, and tidies up. [[slnc 300]] Second, the caller '
            'waits for it to end, but only for a limited time. [[slnc '
            '600]] Think of closing a shop for the night. [[slnc 300]] '
            'You lock the front door to new customers. [[slnc 300]] Then '
            'you let the people inside finish paying, before you switch '
            'off the lights. [[slnc 700]] In our online store, we must '
            'shut down the order worker, without losing or damaging an '
            'order. [[slnc 500]] In this video, a worker stopped suddenly '
            'leaves an order half written. [[slnc 300]] Then a worker '
            'asked politely finishes it. [[slnc 300]] We will wake a '
            'sleeping worker, run cleanup on the way out, and meet a '
            'worker that will not stop. [[slnc 300]] And then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The order worker writes each order', 'as three lines.', '', 'The shop is shut down for an', 'upgrade.', '', 'The worker is in the middle of', 'an order.', '', 'How do we stop it?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The order worker writes '
            'each order as three lines in a ledger. [[slnc 400]] The shop '
            'is being shut down for an upgrade. [[slnc 300]] And the '
            'worker is in the middle of an order. [[slnc 500]] So here is '
            'the question. [[slnc 300]] How do we stop it?'
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
            'First, the crude way: pull the plug. [[slnc 400]] The shop '
            'shuts down, and closes the ledger, while order one is half '
            'written. [[slnc 500]] Only line one was written. [[slnc '
            '300]] The worker tries to write line two, and finds the '
            'ledger closed. [[slnc 500]] So order one is left half '
            'written. [[slnc 300]] A line one, with no line two or three.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Phase one: ask it to stop.', '', 'It finishes what it is doing,', 'tidies up, and ends.', '', 'Phase two: wait for it to end,', 'for a limited time.', '', 'Then decide what to do if it', 'did not.'],
        narration=(
            'Now, the pattern, in two phases. [[slnc 500]] Phase one: ask '
            'the thread to stop. [[slnc 300]] It finishes what it is '
            'doing, tidies up, and ends. [[slnc 500]] Phase two: wait for '
            'it to end, for a limited time. [[slnc 300]] Then decide what '
            'to do, if it did not.'
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
            'Second demo: ask it to stop, and let it finish. [[slnc 400]] '
            'The stop request arrives while order one is half written. '
            '[[slnc 300]] And order two is waiting. [[slnc 500]] The '
            'worker finishes order one, all three lines. [[slnc 300]] '
            'Then it starts nothing new, and ends. [[slnc 500]] The '
            'ledger holds three lines, all from order one. [[slnc 300]] '
            'None from order two. [[slnc 300]] And nothing is half '
            'written.'
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
            'Third demo: a worker that is asleep. [[slnc 400]] The worker '
            'is waiting for an order to arrive. [[slnc 500]] A stop '
            'request that only sets a flag does nothing. [[slnc 300]] The '
            'worker is still asleep, and never looks at the flag. [[slnc '
            '500]] The same request, plus an interrupt to wake the worker '
            'up, and the worker ends. [[slnc 400]] A flag is not enough '
            'for a thread that is not looking at it.'
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
            'Fourth demo: tidy up on the way out. [[slnc 400]] The worker '
            'is interrupted while it is waiting. [[slnc 300]] Did its '
            'cleanup run? [[slnc 300]] Yes. [[slnc 500]] The cleanup sits '
            'in a finally block. [[slnc 300]] So it runs however the '
            'worker ends. [[slnc 300]] Finished, interrupted, or failed.'
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
            'Fifth demo: a worker that will not stop. [[slnc 400]] It is '
            'stuck inside something that ignores the stop request. [[slnc '
            '500]] After waiting two hundred milliseconds, it has not '
            'ended. [[slnc 300]] It is still alive. [[slnc 500]] That is '
            'why phase two has a time limit. [[slnc 300]] What happens '
            'next is a decision. [[slnc 300]] Report it, wait longer, or '
            'restart the whole program. [[slnc 400]] Java gives no safe '
            'way to force a thread to stop.'
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
            'Finally, the cost. [[slnc 400]] The worker was stopped with '
            'five orders still waiting. [[slnc 300]] One order was '
            'finished, and five are still pending. [[slnc 500]] Those '
            'five were accepted from customers, and have not been done. '
            '[[slnc 300]] So a stop needs a policy. [[slnc 300]] Finish '
            'them first, hand them to another worker, or save them for '
            'later. [[slnc 500]] And shutting down took as long as the '
            'order in progress. [[slnc 300]] Stopping is never instant.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A volatile boolean stopRequested', 'checked at the top of a loop.', '', 'ExecutorService.shutdown()', 'followed by', '', 'Thread.interrupt() followed by', 'Thread.join(timeout).'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a volatile flag, like stop requested, checked '
            "at the top of a loop. [[slnc 300]] Look for an executor's "
            'shutdown, followed by await termination with a time limit. '
            "[[slnc 300]] Look for a thread's interrupt, followed by join "
            'with a time limit. [[slnc 300]] And look for graceful '
            'shutdown settings in servers and frameworks.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Stop threads in two phases: ask,', 'then wait with a limit. Let a', 'worker finish the unit of work it', 'is in, and check for the request', 'between units. Wake it if it may', 'be waiting. Put cleanup in a', 'finally block. Decide what happens', 'to the queued work, and to a', 'worker that does not end. Never'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Stop threads in two '
            'phases: ask, and then wait, with a time limit. [[slnc 500]] '
            'Let a worker finish the piece of work it is doing. [[slnc '
            '300]] And check for the stop request between pieces. [[slnc '
            '300]] Wake it up, if it might be waiting. [[slnc 300]] Put '
            'cleanup in a finally block. [[slnc 300]] Decide what happens '
            'to the queued work, and to a worker that does not end. '
            '[[slnc 400]] And never force a thread to stop.'
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
        body=['For a thread that holds no state', 'and whose work can be repeated,', 'stopping at once is fine, and a', 'daemon thread can simply be left.', 'The pattern matters where a stop', 'can damage something.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a thread that '
            'holds nothing important, and whose work can simply be '
            'repeated, stopping at once is fine. [[slnc 300]] A '
            'background daemon thread can just be left to end with the '
            'program. [[slnc 400]] This pattern matters wherever a sudden '
            'stop could damage something.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Two-Phase Termination. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Two-phase '
            'termination stops a thread by asking, and then waiting, and '
            'the price is that stopping takes as long as the work in '
            'progress. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Make the worker finish all its queued orders before it '
            'stops. [[slnc 300]] And decide how long it should be allowed '
            'to take. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
