"""Scene definitions for the Execute Around teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Execute Around',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Execute Around pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Execute Around puts the '
            'setting up, and the cleaning up, in one method. [[slnc 300]] '
            'The caller only hands in the work that goes in the middle. '
            '[[slnc 600]] Think of a car wash. [[slnc 300]] The machine '
            'always opens the gate at the start, and closes it at the '
            'end. [[slnc 300]] You only drive through the middle. [[slnc '
            '700]] In our online store, every piece of code that reads '
            'orders must open a database connection, and close it again. '
            '[[slnc 300]] And someone always forgets, when something goes '
            'wrong. [[slnc 500]] In this video, a connection leaks on a '
            'failure. [[slnc 300]] Then the closing moves into one place. '
            '[[slnc 300]] We will get results out, undo a failed '
            'transaction, measure time, and then hear the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Every query needs a connection.', '', 'Every connection must be', 'closed,', '', 'whether the query works', 'or fails.', '', 'Who does the closing?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Every query to the order '
            'database needs a connection. [[slnc 300]] And every '
            'connection must be closed, whether the query works, or '
            'fails. [[slnc 500]] So here is the question. [[slnc 300]] '
            'Who does the closing?'
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
            'First, the naive way: open, use, and close, by hand. [[slnc '
            '400]] The query breaks. [[slnc 300]] And the line that would '
            'close the connection came after it, so it never runs. [[slnc '
            '500]] Connections still open: one. [[slnc 300]] Repeat that '
            'on every failure, and the connection pool runs dry.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One method opens, runs the', 'work, and closes.', '', 'The caller passes only the', 'work, as a lambda.', '', 'The closing sits in a finally', 'block, once.'],
        narration=(
            'Now, the pattern. [[slnc 400]] One method opens the '
            'connection, runs the work, and closes it. [[slnc 300]] The '
            'caller passes in only the work, as a lambda. [[slnc 500]] '
            'The closing sits in a finally block, written once.'
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
            'Second demo: the caller only gives the work. [[slnc 400]] '
            'The same failure: the query breaks. [[slnc 500]] Connections '
            'opened: one. [[slnc 300]] Still open: none. [[slnc 500]] The '
            'closing lives in one place, in a finally block. [[slnc 300]] '
            'So it cannot be forgotten.'
        ),
    ),
    dict(
        key='06-result', kind='console', title='Getting An Answer Out',
        body="""THREE. An answer out.
  a string came out.
  a number came out: 15.
  still open: 0.""",
        narration=(
            'Third demo: getting an answer out. [[slnc 400]] The work can '
            'return a value. [[slnc 300]] Here, it returns the rows for '
            'an order. [[slnc 300]] And here, it returns a number: '
            'fifteen. [[slnc 500]] And still, no connections are left '
            'open.'
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
            'Fourth demo: all or nothing. [[slnc 400]] A customer has '
            'fifty pounds of credit. [[slnc 300]] Two purchases of thirty '
            'pounds each are made, inside one transaction. [[slnc 300]] '
            'The second fails, because there is not enough credit. [[slnc '
            '500]] Afterwards, the balance is still fifty pounds. [[slnc '
            '300]] The first purchase was undone too. [[slnc 500]] A '
            'single purchase of thirty pounds, which works, leaves twenty '
            'pounds.'
        ),
    ),
    dict(
        key='08-timed', kind='console', title='The Same Shape, For Measuring',
        body="""FIVE. For measuring.
  receipt sent in 5 ticks.
  a failing job: still measured:
  9 ticks.""",
        narration=(
            'Fifth demo: the same shape, for measuring time. [[slnc 400]] '
            'Sending a receipt took five ticks. [[slnc 500]] And a job '
            'that fails, because the mail server timed out, is still '
            'measured. [[slnc 300]] Nine ticks. [[slnc 300]] Because the '
            'measuring also sits in a finally block.'
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
            'Finally, the costs. [[slnc 400]] First, the caller let the '
            'connection out of the block, and used it later. [[slnc 300]] '
            'By then, it was closed. [[slnc 300]] The pattern cannot stop '
            "that. [[slnc 500]] Second, the caller's code now lives "
            'inside a lambda. [[slnc 300]] It cannot return early from '
            'the outer method. [[slnc 300]] And it cannot throw a checked '
            'exception without extra help. [[slnc 500]] Third, with two '
            'resources, the blocks nest one inside the other. [[slnc '
            '300]] And the real work drifts further and further to the '
            'right.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['JdbcTemplate.query(...) and', 'TransactionTemplate.execute(...)', '', 'try (var in = ...) { ... }, the', "language's own version.", '', 'Files.lines used inside a block,', 'lock.lock(); try { ... } finally {'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            "[[slnc 400]] In Spring, look for the JDBC template's query "
            "method, and the transaction template's execute method. "
            '[[slnc 300]] In Java itself, look for try-with-resources, '
            "which is the language's own version. [[slnc 300]] Look for a "
            'lock, followed by try, and an unlock in a finally block. '
            '[[slnc 300]] And look for methods that take a lambda named '
            'work, callback, or action.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use execute around wherever', 'something must be undone or', 'finished after use: connections,', 'files, locks, transactions,', 'timers. Put the clean-up in a', 'finally block, once. Do not let', 'the resource leave the block. For', 'plain files and streams, try-with-', "resources is the language's own"],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use Execute Around '
            'wherever something must be undone, or finished, after use. '
            '[[slnc 300]] Connections, files, locks, transactions, and '
            'timers. [[slnc 500]] Put the cleaning up in a finally block, '
            'once. [[slnc 300]] And do not let the resource escape from '
            'the block. [[slnc 500]] For simple files and streams, '
            "try-with-resources is the language's own form of this "
            'pattern.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] Time "
            'is counted in ticks, not by the clock, so every run gives '
            'the same result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a resource used once, in one', 'place, try with resources is', 'enough. Write your own around', 'method when many callers repeat', 'the same set-up and clean-up.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a resource used '
            'once, in one place, try-with-resources is enough. [[slnc '
            '400]] Write your own execute around method when many callers '
            'repeat the same setting up, and cleaning up.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Execute Around pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] '
            'Execute Around puts the opening and closing in one place, '
            'and the price is work trapped in a lambda, and a resource '
            'that can still escape. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Add a method that retries the work up to three '
            'times. [[slnc 300]] All around the same connection. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
