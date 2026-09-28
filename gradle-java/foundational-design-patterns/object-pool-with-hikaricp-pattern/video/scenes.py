"""Scene definitions for the Object Pool with HikariCP teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Object Pool with HikariCP',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Object Pool pattern, in Java, using HikariCP. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] An object pool '
            'keeps a few expensive objects, lends them out, and takes '
            'them back. [[slnc 600]] Think of the trolleys at a '
            'supermarket. [[slnc 300]] You borrow one, use it, and return '
            'it to the bay for the next shopper. [[slnc 700]] This is the '
            'framework version of the Object Pool video. [[slnc 300]] '
            'That one built a pool by hand, and found four costs. [[slnc '
            '500]] HikariCP is the database connection pool inside most '
            'Java applications. [[slnc 300]] By the end, you will know '
            'which of those costs a real library solves, and which it '
            'cannot.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Object Pool, the hand-built video,', 'found four costs: a small object', 'pooled is slower, a returned object', 'carries old state, a leak hangs', 'the application, sizing is a guess.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Object Pool video. [[slnc 400]] That '
            'one found four costs. [[slnc 300]] A small pooled object is '
            'slower than creating it. [[slnc 300]] A returned object '
            'carries its old state. [[slnc 300]] A leak hangs the '
            'application. [[slnc 300]] And choosing the size is a guess. '
            '[[slnc 500]] This video is about database connections, the '
            'one thing clearly worth pooling. [[slnc 300]] We will not '
            'teach the pattern again.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new:', 'HikariCP and H2.', '', 'HikariCP is a JDBC connection pool.', 'Closing a connection returns it.', '', 'H2 is a database that runs in', 'memory, so nothing is installed.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Two things are new in this project. [[slnc 400]] First, '
            'HikariCP, a database connection pool. [[slnc 300]] You ask '
            'it for a connection, use it, and close it. [[slnc 300]] But '
            'closing does not really close it. [[slnc 300]] It gives it '
            'back to the pool. [[slnc 500]] Second, H2, a database that '
            'runs in memory, so nothing needs installing. [[slnc 500]] '
            'And one promise. [[slnc 300]] If you skip this video, you '
            'lose none of the pattern. [[slnc 300]] This one is about the '
            'tool.'
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
            'First demo: it opens only what is needed. [[slnc 400]] Ten '
            'payments, one after another. [[slnc 300]] The pool is '
            'allowed to hold two connections. [[slnc 500]] How many did '
            'it open? [[slnc 300]] Just one. [[slnc 300]] The payments '
            'ran one at a time, so one was enough. [[slnc 500]] And '
            'closing the connection each time did not close it. [[slnc '
            '300]] It returned it to the pool.'
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
            'Second demo: the dirty return, from the hand-built video. '
            '[[slnc 400]] Ada changes two connection settings: auto '
            'commit off, and read only on. [[slnc 300]] Then she returns '
            'the connection. [[slnc 500]] Grace borrows the very same '
            'connection. [[slnc 300]] Auto commit is back on. [[slnc '
            '300]] And read only is back off. [[slnc 500]] The pool reset '
            'the settings it knows about, on the way back in. [[slnc '
            '300]] That is the reset the hand-built video had to write by '
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
            'But not everything is reset. [[slnc 400]] Ada sets a '
            'variable inside the database session itself, and returns the '
            'connection. [[slnc 500]] Grace borrows it, and reads that '
            'variable. [[slnc 300]] It says: Ada Lovelace. [[slnc 500]] '
            'The security bug from the hand-built video is still '
            'possible. [[slnc 300]] The pool can only reset what it can '
            'see. [[slnc 300]] And state inside the database session is '
            'invisible to it.'
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
            'Third demo: running out, with a timeout. [[slnc 400]] Two '
            'borrowers take both connections, and never return them. '
            '[[slnc 300]] A third caller waits. [[slnc 500]] After about '
            'three hundred milliseconds, it receives a clear error. '
            '[[slnc 300]] Connection is not available, the request timed '
            'out. [[slnc 300]] Total two, active two, idle zero. [[slnc '
            '500]] The timeout was already a setting. [[slnc 300]] But '
            'its default is thirty seconds, so set it yourself. [[slnc '
            '300]] There is also a leak detection setting, which logs who '
            'never returned a connection.'
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
            'Fourth demo: choosing the size is still a guess. [[slnc '
            '400]] Four payments arrive at once, each needing fifty '
            'milliseconds. [[slnc 500]] With a pool of one, they queue, '
            'and it takes over two hundred milliseconds. [[slnc 300]] '
            'With a pool of four, it takes about fifty. [[slnc 500]] A '
            'pool of fifty opens fifty connections, and keeps them idle, '
            "for just four payments. [[slnc 300]] HikariCP's own "
            'documentation recommends small pools. [[slnc 300]] More is '
            'not faster.'
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
            'Fifth demo: what pooling actually buys. [[slnc 400]] Opening '
            'a new database connection each time: about thirty-eight '
            'microseconds. [[slnc 300]] Borrowing one from the pool: '
            'about one and a half. [[slnc 500]] And this is H2, in '
            'memory, where connections are cheap. [[slnc 300]] A real '
            'database, across a network, costs far more. [[slnc 300]] '
            'That is why this is the one place the pattern is clearly '
            'right. [[slnc 300]] The exact timings vary by machine.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Pool connections, threads and', 'native handles.', '', 'Use a library that has already', 'fixed the hard parts.', '', 'Never pool ordinary objects.', 'Never write your own connection', 'pool.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Pool connections, '
            'threads, and handles to the operating system. [[slnc 300]] '
            'Use a library that has already solved the hard parts. [[slnc '
            '300]] Never pool ordinary objects. [[slnc 300]] And never '
            'write your own connection pool. [[slnc 500]] You have just '
            'heard how many things there are to get right.'
        ),
    ),
    dict(
        key='11-met', kind='bullets', title='Where You Have Met This',
        body=['Every Spring Boot application with', 'a database uses HikariCP.', '', 'Every DataSource is a pool.'],
        narration=(
            'Where have you met this before? [[slnc 400]] Every Spring '
            'Boot application with a database uses HikariCP. [[slnc 300]] '
            'Every data source is a pool. [[slnc 300]] And now you know '
            'what happens when you close a connection.'
        ),
    ),
    dict(
        key='12-versions', kind='bullets', title='What Was Used',
        body=['HikariCP and H2: the versions from', "Spring Boot 4.1.1's bill of materials.", '', 'Spring Boot itself is not used.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] HikariCP '
            'and H2, at the versions listed by Spring Boot four point one '
            'point one. [[slnc 300]] But Spring Boot itself is not used '
            'here.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the pool, the', 'exception message, the statistics.', '', 'The database is H2 in memory.', 'Timings vary by machine.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything here is real. [[slnc 300]] The pool, its error '
            'messages, and its statistics. [[slnc 300]] The only stand-in '
            'is the database, H2, in memory. [[slnc 300]] The timings '
            'vary by machine, and no test depends on them.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Set the leak detection threshold', 'and see what it logs.'],
        narration=(
            "That's the Object Pool, with HikariCP. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Use a '
            'library that has solved the hard parts, and still reset what '
            'it cannot see. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Switch on the leak detection setting. [[slnc 300]] And '
            'see what it logs. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
