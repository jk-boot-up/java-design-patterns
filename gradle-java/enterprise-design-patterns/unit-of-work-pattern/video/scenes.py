"""Scene definitions for the Unit of Work teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Unit of Work',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Unit of Work '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: keep '
            'a list of everything that changed, new, changed and removed, '
            'and write it all together at the end, in one step, or not at '
            'all. [[slnc 350]] This is the third project in the '
            'enterprise category. In our online store, the question is '
            'what happens when placing an order writes seven things, and '
            'the seventh fails. [[slnc 300]] By the end you will know '
            'what half an order looks like, what a transaction fixes, '
            'what it still costs, and how a unit of work does better.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Placing an order writes:', 'one order row, three line rows,', 'and three stock decrements.', '', 'The third stock update fails.', '', 'What is left behind?'],
        narration=(
            'Here is the scenario. In the online store, placing an order '
            'writes an order row, three line rows, and three stock '
            'decrements. That is seven writes. [[slnc 300]] And the third '
            "stock update, the last product's, fails. [[slnc 300]] The "
            'question is: what is left behind in the database?'
        ),
    ),
    dict(
        key='03-wreckage', kind='console', title='Each Object Saves Itself',
        body="""ONE. Each object saves itself.
  orders: 1
  order lines: 2 of 3
  stock: keyboard 8, mouse 9,
  monitor 10 (was 10, 10, 10)

  nothing knows it is broken.""",
        narration=(
            'First, the naive way: each object saves itself as it '
            'changes. [[slnc 300]] The order is written. Then the '
            "keyboard's stock, and its line. Then the mouse's stock, and "
            "its line. Then the monitor's stock is rejected. [[slnc 300]] "
            'What is left: one order, with two lines out of three. '
            'Keyboard stock down by two, mouse down by one, monitor '
            'untouched. Nothing anywhere knows it is broken, and nothing '
            'can undo it, because the writes have already happened.'
        ),
    ),
    dict(
        key='04-transaction', kind='console', title='Wrap It In A Transaction',
        body="""TWO. A transaction.
  orders: 0, lines: 0,
  stock: 10, 10, 10

  the cost: open for 22 ticks,
  including every slow check.""",
        narration=(
            'The second naive version is the one experienced developers '
            'reach for: wrap it all in a transaction. And it mostly '
            'works. The failure rolls everything back. Orders zero, lines '
            'zero, stock back to ten, ten, ten. [[slnc 300]] The cost is '
            'time. The transaction, and the locks it holds, stay open for '
            'the whole computation, including the slow check made for '
            'each line. Here that is twenty-two ticks. Other customers '
            'wait on those locks.'
        ),
    ),
    dict(
        key='05-pattern', kind='bullets', title='The Pattern',
        body=['Change the objects. Register each change:', 'new, dirty, or removed.', '', 'Nothing touches the database yet.', '', 'At commit, write everything, in one', 'short transaction.'],
        narration=(
            'The pattern keeps a list. As the objects change, each change '
            'is registered: new, dirty or removed. [[slnc 300]] Nothing '
            'touches the database. The slow checks happen now, with no '
            'locks held. [[slnc 300]] Only at commit does it write '
            'everything, in one short transaction.'
        ),
    ),
    dict(
        key='06-nothing', kind='console', title='Nothing Until Commit',
        body="""THREE. The pattern.
  after changing every object:
  0 database operations,
  7 changes registered.

  locked for 7 ticks, not 22.""",
        narration=(
            'Watch the counter. After changing every object, zero '
            'database operations. Seven changes registered, waiting. '
            '[[slnc 300]] Then commit writes them, the order first, then '
            'its lines, then the stock updates. And the database was '
            'locked for seven ticks, not twenty-two. The slow work was '
            'already done.'
        ),
    ),
    dict(
        key='07-all-or-none', kind='console', title='All Of It, Or None',
        body="""FOUR. The same failure.
  commit failed: UPDATE
  products id=3

  orders: 0, lines: 0,
  stock: 10, 10, 10

  all of the order, or none.""",
        narration=(
            'Now the same failure. The third stock update is rejected '
            'during commit. [[slnc 300]] The transaction rolls back, and '
            'the database is exactly as it was. Orders zero, lines zero, '
            'stock ten, ten, ten. [[slnc 300]] All of the order, or none '
            'of it. And the customer never saw half an order.'
        ),
    ),
    dict(
        key='08-ordering', kind='console', title='Cost One: Order Of Writes',
        body="""FIVE. Order of writes.
  written as registered,
  the lines came before
  their order:
  foreign key: no row in
  orders

  the unit of work sorts them.""",
        narration=(
            'Now the bill. First, the order of writes matters. [[slnc '
            '300]] Written in the order they were registered, the lines '
            'came before their order, and the database refused: a line '
            'pointed at an order that did not exist yet. [[slnc 300]] The '
            'unit of work has to know that parents come before children, '
            'and sort its changes before it writes.'
        ),
    ),
    dict(
        key='09-dirty', kind='bullets', title='Cost Two: Knowing What Changed',
        body=['It must know what is dirty:', 'either check every field of every object,', 'or be told.', '', 'This project is told, through', 'registerDirty.'],
        narration=(
            'Second cost. The unit of work has to know what actually '
            'changed. There are two ways. Check every field of every '
            'object, which is slow. Or be told, which puts the burden on '
            'the caller. [[slnc 300]] This project is told. The caller '
            'says registerDirty. Forget to say it, and the change is '
            'never written.'
        ),
    ),
    dict(
        key='10-memory', kind='console', title='Cost Three: Memory Disagrees',
        body="""SIX. Memory.
  in memory, the keyboard
  has 8 in stock.

  in the database, it still
  has 10.

  7 changes held in memory.""",
        narration=(
            'Third cost. Until commit, memory and the database disagree. '
            'The keyboard has eight in stock in memory, and ten in the '
            'database. [[slnc 300]] And the whole change set lives in '
            'memory, so a huge bulk update is a memory problem too. '
            'Something reading the database in the meantime sees the old '
            'world.'
        ),
    ),
    dict(
        key='11-toydb', kind='bullets', title='The Toy Database',
        body=['Rows, a counter, and a write', 'that can be told to fail.', '', 'This project adds begin, rollback,', 'and a foreign key check.', '', 'Every count came from its counter.'],
        narration=(
            'A word about the database in these demos. It is a toy: rows, '
            'an operation counter, and a write that can be told to fail '
            'on demand. [[slnc 300]] For this project it also learned to '
            'begin and roll back a transaction, and to check a foreign '
            'key. Every count in this video came from its counter.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['@Transactional is a unit of work.', 'A flush is its commit.', '', 'The persistence context tracks what', 'changed, and writes it when the', 'transaction ends.'],
        narration=(
            'You have met this one. The transactional annotation is a '
            'unit of work. The persistence context tracks what changed, '
            'and writes it when the transaction ends, in an order it '
            'works out for you. [[slnc 300]] A flush is the commit. If a '
            'write ever happened at a moment you did not expect, that was '
            'the unit of work choosing when to commit.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The pattern is real.', 'The database is a stand-in: no locks,', 'no other users.', '', 'The ticks are a model of lock time,', 'not a measurement.'],
        narration=(
            'The same honest admission as everywhere in this course. The '
            'pattern is real. The database is a stand-in, with no real '
            'locks and no other users. [[slnc 300]] The ticks are a model '
            'of how long locks are held, not a measurement. What is real '
            'is the shape: slow work outside the transaction, writes '
            'inside a short one.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['One write needs no unit of work.', '', 'It earns its place when one business', 'action must write several rows together.'],
        narration=(
            'So when is it too much? A single write needs no unit of '
            'work. It is ceremony. [[slnc 300]] It earns its place when '
            'one business action must write several rows together, and '
            'half of them is worse than none.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add registerRemoved and use it', 'to cancel an order.'],
        narration=(
            "That's the Unit of Work. [[slnc 250]] If you take one "
            'sentence away, take this one: do the slow work first, then '
            'write everything once, or not at all. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, add removal to the unit of work and '
            'use it to cancel an order. [[slnc 300]] If this helped, a '
            'like genuinely does help other people find it, and subscribe '
            'if you would like the rest of the series. [[slnc 250]] '
            'Thanks for watching.'
        ),
    ),
]
