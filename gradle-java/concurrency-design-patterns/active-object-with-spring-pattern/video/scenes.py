"""Scene definitions for the Active Object with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Active Object with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Active Object pattern, in Java, using Spring Boot. [[slnc '
            '300]] This video is presented by Jayasekhar Konduru. [[slnc '
            '600]] First, a simple definition. [[slnc 300]] An active '
            'object has its own thread. [[slnc 300]] A call to it becomes '
            'a message in a mailbox, and returns straight away with a '
            'promise of the answer. [[slnc 300]] Because only one thread '
            'owns the data, no lock is needed. [[slnc 600]] Think of a '
            'post box. [[slnc 300]] You drop your letter in, and walk '
            'away. [[slnc 300]] One postal worker empties it and handles '
            'each letter in turn. [[slnc 700]] This is the framework '
            'version of the Active Object video, with the same shop '
            'stock. [[slnc 400]] We will build an active object from a '
            'Spring bean and a one-thread executor, with no lock. [[slnc '
            '300]] Then we will hear the two ways that guarantee breaks: '
            'a call that skips the proxy, and a read that skips the '
            'mailbox.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Active Object, the hand-built video,', 'built an object with its own thread and', 'mailbox, and no lock.', '', 'It showed: a mailbox that backs up,', 'errors that arrive late, and a', 'throughput ceiling.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Active Object video. [[slnc 400]] '
            'That one builds an object with its own thread and mailbox, '
            'by hand, with no lock. [[slnc 300]] And it shows three '
            'costs: a mailbox that backs up, errors that arrive late, and '
            'a limit on speed. [[slnc 500]] If you are new to the '
            'pattern, watch that one first. [[slnc 400]] Here, we ask '
            'what Spring Boot does with the same idea.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'An @Async bean, on a executor with', 'exactly one thread, is an active object.', '', "The executor's queue is the mailbox.", '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            'At its heart, Spring is a container that creates your '
            'objects. [[slnc 500]] A bean whose methods are marked at '
            'Async, running on an executor with exactly one thread, is an '
            "active object. [[slnc 300]] The executor's queue is the "
            'mailbox. [[slnc 500]] And one promise. [[slnc 300]] If you '
            'skip this video, you lose none of the pattern. [[slnc 300]] '
            'This one is about the tool.'
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
            'First demo: no lock at all. [[slnc 400]] Four callers each '
            'send five thousand restock messages. [[slnc 300]] The final '
            'stock is exactly twenty thousand. [[slnc 500]] Look for the '
            'lock. [[slnc 300]] There is none. [[slnc 300]] The stock is '
            'a plain number, not even marked volatile. [[slnc 400]] It is '
            'safe because every change runs on one thread, the inventory '
            'thread. [[slnc 300]] And the executor has exactly one.'
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
            'Second demo: the mailbox. [[slnc 400]] The worker is busy '
            'with one slow message. [[slnc 300]] Callers send ten '
            'thousand more. [[slnc 300]] All ten thousand wait, and '
            'nothing refuses them. [[slnc 500]] Now limit the queue to '
            'three. [[slnc 300]] The fourth waiting message is refused, '
            'with a Task Rejected exception. [[slnc 400]] In the '
            'hand-built video, that limit was a cost. [[slnc 300]] Here, '
            'it is just a setting.'
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
            'Third demo: a failure that belongs to Spring. [[slnc 400]] '
            'The worker reads the stock, which is zero, and holds on to '
            'that value. [[slnc 500]] Meanwhile, a caller adds five '
            'items. [[slnc 300]] But it calls the method on this, meaning '
            'on the same object, directly. [[slnc 300]] A call on this '
            "skips Spring's proxy. [[slnc 300]] So it runs on the "
            "caller's own thread, not the worker. [[slnc 500]] Then the "
            'worker writes what it read, plus ten. [[slnc 300]] The final '
            'stock is ten, not fifteen. [[slnc 300]] Five items vanished. '
            '[[slnc 500]] Two threads touched a plain field, so the '
            'lock-free guarantee is gone. [[slnc 300]] And nothing '
            'complained.'
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
            'Fourth demo: a read. [[slnc 400]] A restock of five items is '
            'waiting in the mailbox, behind a slow message. [[slnc 500]] '
            "A getter that reads the field directly, from the caller's "
            'thread, says zero. [[slnc 400]] A read sent as a message '
            'waits its turn, behind the restock. [[slnc 300]] And it says '
            'five. [[slnc 500]] The direct read raced the worker, and '
            'lost. [[slnc 300]] In an active object, reads must be '
            'messages too.'
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
            'Fifth demo: errors arrive later. [[slnc 400]] A failing '
            'message does not throw where it was sent. [[slnc 300]] '
            'Instead, its future fails, later. [[slnc 400]] And the '
            "error's stack trace belongs to the inventory thread. [[slnc "
            '300]] The method that sent the message appears nowhere in '
            'it. [[slnc 300]] So debugging means finding out who sent the '
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
            'Last demo: one worker is a limit. [[slnc 400]] Every message '
            'costs fifty microseconds of real work. [[slnc 400]] With one '
            'caller, about nineteen thousand messages per second. [[slnc '
            '300]] With four callers, about the same. [[slnc 500]] Four '
            'times the callers, and the same rate. [[slnc 300]] The limit '
            'is the single worker, exactly as in the hand-built video. '
            '[[slnc 300]] That is the price of having no lock. [[slnc '
            '300]] The numbers vary from machine to machine.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Use it when callers must not wait.', 'Route every access, reads too,', 'through the proxy.', '', 'Bound the mailbox.', '', 'Never give the executor a second', 'thread.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use it when callers '
            'must not wait, and one owner for the data is enough. [[slnc '
            '300]] Send every access through the proxy, including reads. '
            '[[slnc 300]] Put a limit on the mailbox. [[slnc 300]] And '
            'never give the executor a second thread.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Async with a named single-thread', 'executor.', '', 'A service with mutable fields, no', 'synchronized, and methods that all', 'return futures.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for an at Async method that names an executor '
            'with exactly one thread. [[slnc 300]] A service with '
            'changing fields, no synchronized keyword anywhere, and '
            'methods that all return futures. [[slnc 300]] And a comment '
            'that says, only ever called from the worker thread.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['A single-thread executor named for', 'the thing it protects.', '', 'Actor libraries take this idea much', 'further.'],
        narration=(
            'Where have you met this before? [[slnc 300]] As a '
            'single-thread executor, named after the thing it protects. '
            '[[slnc 300]] Actor libraries take the same idea much '
            'further.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] No web server, '
            'no database, and no web library.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's executor,", 'its proxy, and its exceptions.', '', 'Every wait is a latch or a gate.', 'The throughput numbers are measured', 'and vary by machine.'],
        narration=(
            "A quick, honest note about this demo. [[slnc 300]] Spring's "
            'executor, its proxy, and its errors are all real. [[slnc '
            '300]] Every wait uses a latch or a gate. [[slnc 300]] The '
            'speed numbers are real measurements, and they vary by '
            'machine.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For state that changes rarely, a', 'synchronized method is simpler.', '', 'It earns its place when callers must', 'not wait.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For data that '
            'changes rarely, a simple synchronized method is easier. '
            '[[slnc 300]] An active object earns its place when callers '
            'must not wait.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Give the executor two threads', 'and see what breaks.'],
        narration=(
            "That's Active Object with Spring. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] An '
            'active object trades a lock for a queue, and the guarantee '
            'only holds for calls that go through the queue. [[slnc 500]] '
            'The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Give the executor '
            'two threads, and run the first demo again. [[slnc 300]] Then '
            'work out which guarantee you just gave up. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
