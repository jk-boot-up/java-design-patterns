"""Scene definitions for the Execute Around teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Execute Around',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Execute Around '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'execute around puts the set up and the clean up in one '
            'method. The caller hands in only the work in the middle. '
            '[[slnc 350]] This is another project in the foundational '
            'category, whose subject is how an object gets hold of '
            'another, and how small idioms shape everyday Java. In our '
            'online store, every piece of code that reads orders must '
            'open a connection and close it again, and someone always '
            'forgets on the error path. [[slnc 300]] By the end you will '
            'see a connection leak on a failure, see the closing done in '
            'one place, see a result come out, see a transaction undone '
            'on failure, see the same shape used for timing, and see the '
            'bill, which is a resource that escapes and a caller trapped '
            'in a lambda.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Every query needs a connection.', '', 'Every connection must be', 'closed,', '', 'whether the query works', 'or fails.', '', 'Who does the closing?'],
        narration=(
            'Here is the scenario. Every query to the order database '
            'needs a connection, and every connection must be closed, '
            'whether the query works or fails. [[slnc 300]] The question: '
            'who does the closing?'
        ),
    ),
    dict(
        key='03-hand', kind='console', title='Open, Use, Close, By Hand',
        body="""ONE. By hand.
  the query broke; the code
  that would close the
  connection came after it.
  still open: 1.

  repeat on every failure and
  the pool runs dry.""",
        narration=(
            'First, open, use, close, by hand. The query broke, and the '
            'code that would close the connection was after it. '
            'Connections still open: one. Repeat that on every failure, '
            'and the pool runs dry.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One method opens, runs the', 'work, and closes.', '', 'The caller passes only the', 'work, as a lambda.', '', 'The closing sits in a finally', 'block, once.'],
        narration=(
            'The pattern. One method opens, runs the work, and closes. '
            'The caller passes only the work, as a lambda. The closing '
            'sits in a finally block, once.'
        ),
    ),
    dict(
        key='05-around', kind='console', title='The Caller Gives The Work',
        body="""TWO. The caller gives the work.
  the same failure.
  opened: 1, still open: 0.

  the closing is in one place,
  in a finally block.""",
        narration=(
            'Second, the caller gives the work, and the pool does the '
            'rest. The same failure: the query broke. Connections opened: '
            'one. Still open: none. The closing is in one place, in a '
            'finally block, and cannot be forgotten.'
        ),
    ),
    dict(
        key='06-result', kind='console', title='Getting An Answer Out',
        body="""THREE. An answer out.
  a string came out.
  a number came out: 15.
  still open: 0.""",
        narration=(
            'Third, getting an answer out. A string came out: the rows '
            'for an order. A number came out: fifteen. Still open: none.'
        ),
    ),
    dict(
        key='07-tx', kind='console', title='All Or Nothing',
        body="""FOUR. All or nothing.
  2 purchases of 3000 from 5000:
  the second failed.
  balance: 5000. the first was
  undone too.

  one purchase: 2000.""",
        narration=(
            'Fourth, all or nothing. Two purchases of three thousand from '
            'a credit of five thousand: the second failed, with not '
            'enough credit. The balance afterwards is five thousand. The '
            'first purchase was undone too. One purchase of three '
            'thousand that works leaves two thousand.'
        ),
    ),
    dict(
        key='08-timed', kind='console', title='The Same Shape, For Measuring',
        body="""FIVE. For measuring.
  receipt sent in 5 ticks.
  a failing job: still measured:
  9 ticks.""",
        narration=(
            'Fifth, the same shape, for measuring. Receipt sent, in five '
            'ticks. And a failing job: the mail server timed out, and it '
            'was still measured: nine ticks.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  a connection let out of the
  block, and used later: closed.

  work in a lambda: no early
  return, no checked exception.

  two resources: blocks nest,
  work drifts right.""",
        narration=(
            'Last, the bill. The caller let the connection out of the '
            'block, and used it later: connection one is closed. The '
            "block cannot stop that. The caller's code is now inside a "
            'lambda: it cannot return early, and it cannot throw a '
            'checked exception without help. And with two resources the '
            'blocks nest, one inside the other, so the real work drifts '
            'to the right.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['JdbcTemplate.query(...) and', 'TransactionTemplate.execute(...)', '', 'try (var in = ...) { ... }, the', "language's own version.", '', 'Files.lines used inside a block,', 'lock.lock(); try { ... } finally {'],
        narration=(
            'How do you recognise this in code you did not write? '
            'JdbcTemplate.query(...) and TransactionTemplate.execute(...) '
            "in Spring. try (var in = ...) { ... }, the language's own "
            'version. Files.lines used inside a block, lock.lock(); try { '
            '... } finally { lock.unlock(); }. A method that takes a '
            'lambda named work, callback or action.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use execute around wherever', 'something must be undone or', 'finished after use: connections,', 'files, locks, transactions,', 'timers. Put the clean-up in a', 'finally block, once. Do not let', 'the resource leave the block. For', 'plain files and streams, try-with-', "resources is the language's own"],
        narration=(
            'Here is my verdict, plainly. Use execute around wherever '
            'something must be undone or finished after use: connections, '
            'files, locks, transactions, timers. Put the clean-up in a '
            'finally block, once. Do not let the resource leave the '
            'block. For plain files and streams, try-with-resources is '
            "the language's own form of it."
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
        body=['For a resource used once, in one', 'place, try with resources is', 'enough. Write your own around', 'method when many callers repeat', 'the same set-up and clean-up.'],
        narration=(
            'So when is it too much? For a resource used once, in one '
            'place, try with resources is enough. Write your own around '
            'method when many callers repeat the same set-up and '
            'clean-up.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Execute Around. [[slnc 250]] If you take one sentence "
            'away, take this one: execute around puts the opening and '
            'closing in one place, and the price is that the work is '
            'trapped in a lambda, and the resource can still escape. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add a method that retries the work up to three times, around '
            'the same connection. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
