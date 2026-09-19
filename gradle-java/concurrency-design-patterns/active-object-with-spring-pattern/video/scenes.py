"""Scene definitions for the Active Object with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Active Object with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Active Object '
            'pattern with Spring Boot, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Active Object video. That one built '
            'an object with its own thread and mailbox by hand, so calls '
            'become messages that return a future at once, with no lock '
            'at all, and showed its costs: a mailbox that backs up, '
            'errors that arrive late, and a throughput ceiling. This one '
            'shows the same idea inside Spring Boot. [[slnc 350]] The '
            'plain definition, in short: an object gets its own thread, '
            'and a call to it becomes a message that returns straight '
            'away with a promise of the answer, so one thread owns the '
            'state and it needs no lock. [[slnc 300]] By the end you will '
            'see an active object built from a bean and a one-thread '
            'executor, with a plain field and no lock, then see the two '
            'ways that guarantee breaks: a call that skips the proxy, and '
            'a read that skips the mailbox.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Active Object, the hand-built video,', 'built an object with its own thread and', 'mailbox, and no lock.', '', 'It showed: a mailbox that backs up,', 'errors that arrive late, and a', 'throughput ceiling.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Active Object video. If you have not '
            'seen it, start there. It builds an object with its own '
            'thread and mailbox by hand, with no lock, and shows three '
            'costs: a mailbox that backs up, errors that arrive late, and '
            'a throughput ceiling. [[slnc 300]] This one uses the same '
            'example. It does not teach the pattern again. It shows what '
            'Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'An @Async bean, on a executor with', 'exactly one thread, is an active object.', '', "The executor's queue is the mailbox.", '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'is a framework whose core is a container that creates your '
            'objects. An async bean, given an executor with exactly one '
            "thread, is an active object: the executor's queue is the "
            'mailbox. [[slnc 300]] And a promise: skipping this video '
            'loses none of the pattern. The hand-built one teaches all of '
            'it.'
        ),
    ),
    dict(
        key='04-nolock', kind='console', title='No Lock At All',
        body="""ONE. No lock.
  4 callers x 5000 restocks:
  stock 20000.

  the stock field is a plain
  int: no lock, not volatile.

  every change ran on the one
  inventory- thread.""",
        narration=(
            'First, the point of the pattern. Four callers each send five '
            'thousand restocks. The final stock is exactly twenty '
            'thousand. [[slnc 300]] Look for the lock, and there is none. '
            'The stock is a plain int, not even volatile. It is safe '
            'because every change runs on one thread, the inventory '
            'thread, and the executor has exactly one.'
        ),
    ),
    dict(
        key='05-mailbox', kind='console', title='The Mailbox',
        body="""TWO. The mailbox.
  the worker is busy. callers
  send 10000 more.

  waiting in the mailbox: 10000
  nothing refused them.

  a mailbox of 3: the fourth
  waiting is refused:
  TaskRejectedException.""",
        narration=(
            "The mailbox is the executor's queue. The worker is busy on "
            'one slow message, and callers send ten thousand more. All '
            'ten thousand wait. Nothing refuses them. [[slnc 300]] Bound '
            'the queue to three, and the fourth waiting message is '
            'refused with a task rejected exception. That is the '
            "partner's cost, and here it is a setting."
        ),
    ),
    dict(
        key='06-this', kind='console', title='A Call That Skips The Proxy',
        body="""THREE. Through this.
  the worker read stock 0 and
  is holding it.

  a caller adds 5 through this,
  on its own thread.

  the worker writes 0 + 10.
  final stock: 10, not 15.""",
        narration=(
            "Now a failure that is Spring's own. The worker has read the "
            'stock, and is holding that value at a gate. A caller adds '
            "five, through this, and it runs on the caller's own thread, "
            'because a call on this skips the proxy. [[slnc 300]] Then '
            'the worker writes what it read, plus ten. Final stock: ten, '
            'not fifteen. Five items vanished. With two threads changing '
            'a plain field, the lock-free design is gone, and nothing '
            'complains.'
        ),
    ),
    dict(
        key='07-read', kind='console', title='A Read That Skips The Mailbox',
        body="""FOUR. A read.
  a restock of 5 is waiting.

  a getter that reads the field
  directly says: 0.

  a read sent as a message,
  behind the restock, says: 5.

  reads are messages too.""",
        narration=(
            'Fourth, a read. A restock of five is waiting behind a slow '
            'message. A getter that reads the field directly, from the '
            "caller's thread, says zero. [[slnc 300]] A read sent as a "
            'message, queued behind the restock, waits its turn, and says '
            'five. The direct read raced the worker, and lost. In an '
            'active object, reads are messages too.'
        ),
    ),
    dict(
        key='08-errors', kind='console', title='Errors Arrive Later',
        body="""FIVE. Errors.
  cause: stock feed unavailable
  [raised on inventory-1]

  the calling method appears
  nowhere in that trace.""",
        narration=(
            'Fifth, errors. A failing message does not throw where it was '
            'sent. Its future fails, later, and the stack trace belongs '
            'to the inventory thread. The method that sent the message '
            'appears nowhere in it. Debugging means finding who sent the '
            'message that failed.'
        ),
    ),
    dict(
        key='09-ceiling', kind='console', title='One Worker Is A Ceiling',
        body="""SIX. The ceiling.
  each message costs 50
  microseconds of work.

  1 caller:  ~19000 per second
  4 callers: ~19000 per second

  the ceiling is the worker.""",
        narration=(
            'Last, the ceiling. Every message costs fifty microseconds of '
            'real work. One caller: about nineteen thousand a second. '
            'Four callers: the same. [[slnc 300]] Four times the callers, '
            'the same rate. The ceiling is the worker, exactly as in the '
            'hand-built video. That is the price of having no lock. The '
            'numbers vary by machine.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Use it when callers must not wait.', 'Route every access, reads too,', 'through the proxy.', '', 'Bound the mailbox.', '', 'Never give the executor a second', 'thread.'],
        narration=(
            'My verdict, plainly. Use it when callers must not wait, and '
            'one owner for the state is enough. Route every access, reads '
            'included, through the proxy. Bound the mailbox. And never '
            'give the executor a second thread.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Async with a named single-thread', 'executor.', '', 'A service with mutable fields, no', 'synchronized, and methods that all', 'return futures.'],
        narration=(
            'How do you recognise this in code you did not write? An '
            'async method naming an executor that has exactly one thread. '
            'A service with mutable fields, no synchronized keyword '
            'anywhere, and methods that all return futures. And a comment '
            'saying, only ever called from the worker thread.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['A single-thread executor named for', 'the thing it protects.', '', 'Actor libraries take this idea much', 'further.'],
        narration=(
            'You have met this as a single thread executor, named for the '
            'thing it protects. Actor libraries take the same idea much '
            'further.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. No web '
            'server, no database, and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's executor,", 'its proxy, and its exceptions.', '', 'Every wait is a latch or a gate.', 'The throughput numbers are measured', 'and vary by machine.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            "Everything is real: Spring's executor, its proxy, and its "
            'exceptions. Every wait is a latch or a gate. The throughput '
            'numbers are measured, and vary by machine.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For state that changes rarely, a', 'synchronized method is simpler.', '', 'It earns its place when callers must', 'not wait.'],
        narration=(
            'So when is it too much? For state that changes rarely, a '
            'synchronized method is simpler. An active object earns its '
            'place when callers must not wait.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Give the executor two threads', 'and see what breaks.'],
        narration=(
            "That's Active Object with Spring. [[slnc 250]] If you take "
            'one sentence away, take this one: an active object trades a '
            'lock for a queue, and the guarantee holds only for the calls '
            'that go through it. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository. [[slnc 300]] If you try one exercise, '
            'give the executor two threads, and rerun the first act, and '
            'see which guarantee you just gave up. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
