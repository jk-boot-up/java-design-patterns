"""Scene definitions for the Object Pool with HikariCP teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Object Pool with HikariCP',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Object Pool '
            'pattern with HikariCP, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Object Pool video. That one built a '
            'pool by hand, and found four costs. HikariCP is the '
            'connection pool inside most Java applications, and the '
            'mature answer to several of them. [[slnc 350]] The plain '
            'definition, in short: keep a few expensive objects, lend '
            'them out, and take them back. [[slnc 300]] By the end you '
            'will see which costs a real library solves, and which it '
            'cannot.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Object Pool, the hand-built video,', 'found four costs: a small object', 'pooled is slower, a returned object', 'carries old state, a leak hangs', 'the application, sizing is a guess.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'This video assumes the Object Pool video. If you have not '
            'seen it, start there. It builds a pool by hand, and finds '
            'four costs. A small pooled object is slower than allocating '
            'it. A returned object carries its old state. A leak hangs '
            'the application. And sizing is a guess. [[slnc 300]] This '
            'one is about connections, the one thing worth pooling. It '
            'does not teach the pattern again.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new:', 'HikariCP and H2.', '', 'HikariCP is a JDBC connection pool.', 'Closing a connection returns it.', '', 'H2 is a database that runs in', 'memory, so nothing is installed.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line, two new things. HikariCP is a '
            'database connection pool. You ask it for a connection, use '
            'it, and close it. Closing does not close it. It gives it '
            'back. H two is a database that runs in memory, so nothing '
            'needs installing. [[slnc 300]] And a promise: skipping this '
            'video loses none of the pattern. The hand-built one teaches '
            'all of it.'
        ),
    ),
    dict(
        key='04-demand', kind='console', title='It Opens What Demand Needs',
        body="""ONE. The pool.
  10 payments, one at a time,
  through a pool that may hold
  2.

  connections opened: 1

  close() returned it each
  time.""",
        narration=(
            'Ten payments, one after another, through a pool that is '
            'allowed to hold two connections. How many did it open? One. '
            'The payments ran one at a time, so one was enough. It opens '
            'what demand needs, up to the maximum. Closing the connection '
            'each time did not close it. It returned it.'
        ),
    ),
    dict(
        key='05-dirty', kind='console', title='The Dirty Return',
        body="""TWO. Dirty return.
  Ada sets autoCommit false,
  readOnly true, and returns.

  Grace gets the same connection:
  autoCommit true,
  readOnly false.

  the reset the partner had to
  write.""",
        narration=(
            'The dirty return, from the hand-built video. One borrower '
            'sets auto commit to false, and read only to true, and '
            'returns the connection. The next borrower gets the very same '
            'connection. Auto commit is true. Read only is false. [[slnc '
            '300]] The pool reset the settings it knows about, on the way '
            'back. That is the reset the partner project had to write by '
            'hand.'
        ),
    ),
    dict(
        key='06-remains', kind='console', title='What It Cannot Reset',
        body="""  but a session variable Ada
  set in the database:

  Grace reads it:
  Ada Lovelace

  the security bug is still
  possible.

  the pool cannot reset what
  it cannot see.""",
        narration=(
            'But not everything. Ada sets a session variable, inside the '
            'database, and returns the connection. Grace borrows it, and '
            'reads the variable. Ada Lovelace. [[slnc 300]] The security '
            'bug from the hand-built video is still possible. The pool '
            'can only reset what it can see. State that lives inside the '
            'database session is invisible to it.'
        ),
    ),
    dict(
        key='07-exhaust', kind='console', title='Exhaustion, With A Timeout',
        body="""THREE. Exhaustion.
  two borrowers never return.

  a third caller waited 316ms:
  SQLTransientConnection
  Exception

  Connection is not available,
  request timed out after
  306ms (total=2, active=2,
  idle=0, waiting=0)""",
        narration=(
            'Exhaustion. Two borrowers take both connections and never '
            'return them. A third caller waits, and after about three '
            'hundred milliseconds, it gets an exception with a message '
            'worth reading: connection is not available, request timed '
            'out. Total two, active two, idle zero. [[slnc 300]] The '
            'timeout was already a setting. The hand-built pool needed '
            'one you had to remember. Its default here is thirty seconds, '
            'so set it. A leak detection setting can also log who never '
            'returned a connection.'
        ),
    ),
    dict(
        key='08-size', kind='console', title='Sizing Is Still A Guess',
        body="""FOUR. Sizing.
  4 payments at once, 50ms:
  pool of 1: 223ms
  pool of 4:  53ms

  a pool of 50 opens 50
  connections and keeps them
  idle.

  small pools are recommended.""",
        narration=(
            'Sizing is still a guess. Four payments at once, each needing '
            'fifty milliseconds. A pool of one: they queue. Two hundred '
            'and twenty-three. A pool of four: fifty-three. [[slnc 300]] '
            'A pool of fifty opens fifty connections, and keeps them '
            "idle, for four payments. HikariCP's own documentation argues "
            'for small pools. More is not faster.'
        ),
    ),
    dict(
        key='09-buys', kind='console', title='What Pooling Buys',
        body="""FIVE. What it buys.
  a new connection each time:
  about 38 microseconds

  borrowing:
  about 1.6 microseconds

  in-memory H2 is cheap.
  a network database costs far
  more.""",
        narration=(
            'What does pooling buy, on real database connections? Opening '
            'a new one each time: about thirty-eight microseconds. '
            'Borrowing from the pool: about one and a half. [[slnc 300]] '
            'And this is in-memory H two, whose connections are cheap. A '
            'real database over a network costs far more. That is why '
            'this is the one place the pattern is right. The timings vary '
            'by machine.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Pool connections, threads and', 'native handles.', '', 'Use a library that has already', 'fixed the hard parts.', '', 'Never pool ordinary objects.', 'Never write your own connection', 'pool.'],
        narration=(
            'My verdict, plainly. Pool connections, threads and native '
            'handles. Use a library that has already fixed the hard '
            'parts. Never pool ordinary objects. And never write your own '
            'connection pool. [[slnc 300]] You have just seen how many '
            'parts there are to get right.'
        ),
    ),
    dict(
        key='11-met', kind='bullets', title='Where You Have Met This',
        body=['Every Spring Boot application with', 'a database uses HikariCP.', '', 'Every DataSource is a pool.'],
        narration=(
            'You have met this. Every Spring Boot application with a '
            'database uses HikariCP. Every data source is a pool. Now you '
            'know what it is doing when you close a connection.'
        ),
    ),
    dict(
        key='12-versions', kind='bullets', title='What Was Used',
        body=['HikariCP and H2: the versions from', "Spring Boot 4.1.1's bill of materials.", '', 'Spring Boot itself is not used.'],
        narration=(
            'For the record. HikariCP and H two, at the versions from '
            "Spring Boot four point one point one's bill of materials. "
            'Spring Boot itself is not used in this video.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the pool, the', 'exception message, the statistics.', '', 'The database is H2 in memory.', 'Timings vary by machine.'],
        narration=(
            'The same honest admission as everywhere in this course, and '
            'short. Everything is real: the pool, the exception message, '
            'and the statistics. The only stand-in is the database, H two '
            'in memory. The timings vary by machine, and no test asserts '
            'one.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Set the leak detection threshold', 'and see what it logs.'],
        narration=(
            "That's the Object Pool with HikariCP. [[slnc 250]] If you "
            'take one sentence away, take this one: use a library that '
            'has fixed the hard parts, and still reset what it cannot '
            'see. [[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, set the '
            'leak detection threshold, and see what it logs. [[slnc 300]] '
            'If this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
