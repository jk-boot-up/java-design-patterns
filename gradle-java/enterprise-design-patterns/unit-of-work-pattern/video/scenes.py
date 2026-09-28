"""Scene definitions for the Unit of Work teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Unit of Work',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Unit of Work pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A unit of work keeps a list '
            'of everything that changed. [[slnc 300]] What is new, what '
            'was changed, and what was removed. [[slnc 300]] Then it '
            'writes it all together at the end, in one step, or not at '
            'all. [[slnc 600]] Think of an online shopping basket. [[slnc '
            '300]] You add and remove items freely. [[slnc 300]] Nothing '
            'is charged until you press pay, and then it all happens at '
            'once. [[slnc 700]] In our online store, the question is: '
            'what happens when placing an order writes seven things, and '
            'the seventh fails? [[slnc 500]] By the end, you will know '
            'what half an order looks like. [[slnc 300]] What a '
            'transaction fixes, and what it still costs. [[slnc 300]] And '
            'how a unit of work does better.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Placing an order writes:', 'one order row, three line rows,', 'and three stock decrements.', '', 'The third stock update fails.', '', 'What is left behind?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Placing an order writes '
            'one order row, three order line rows, and three stock '
            'updates. [[slnc 300]] Seven writes in total. [[slnc 500]] '
            'And the third stock update, for the monitor, fails. [[slnc '
            '500]] So here is the question. [[slnc 300]] What is left '
            'behind in the database?'
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
            'changes. [[slnc 400]] The order is written. [[slnc 300]] '
            "Then the keyboard's stock, and its line. [[slnc 300]] Then "
            "the mouse's stock, and its line. [[slnc 300]] Then the "
            "monitor's stock update is rejected. [[slnc 500]] What is "
            'left? [[slnc 300]] One order, with only two of its three '
            'lines. [[slnc 300]] Keyboard stock down by two, mouse stock '
            'down by one, and the monitor untouched. [[slnc 500]] Nothing '
            'knows it is broken. [[slnc 300]] And nothing can undo it, '
            'because the writes have already happened.'
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
            'The second approach is the one experienced developers reach '
            'for: wrap it all in a transaction. [[slnc 300]] And it '
            'mostly works. [[slnc 500]] The failure rolls everything '
            'back. [[slnc 300]] No orders, no lines, and all three stock '
            'levels back to ten. [[slnc 500]] The cost is time. [[slnc '
            '300]] The transaction, and its locks, stay open for the '
            'whole calculation. [[slnc 300]] Including a slow check made '
            'for every line. [[slnc 300]] Here, that is twenty-two ticks '
            'of time. [[slnc 300]] And other customers wait on those '
            'locks.'
        ),
    ),
    dict(
        key='05-pattern', kind='bullets', title='The Pattern',
        body=['Change the objects. Register each change:', 'new, dirty, or removed.', '', 'Nothing touches the database yet.', '', 'At commit, write everything, in one', 'short transaction.'],
        narration=(
            'Now, the pattern. [[slnc 400]] It keeps a list. [[slnc 300]] '
            'As the objects change, each change is registered: new, '
            'changed, or removed. [[slnc 500]] Nothing touches the '
            'database yet. [[slnc 300]] The slow checks happen now, with '
            'no locks held. [[slnc 500]] Only at the end, called commit, '
            'does it write everything, in one short transaction.'
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
            'Third demo: nothing is written until commit. [[slnc 400]] '
            'After changing every object, there have been zero database '
            'operations. [[slnc 300]] Seven changes are registered, and '
            'waiting. [[slnc 500]] Then commit writes them. [[slnc 300]] '
            'The order first, then its lines, then the stock updates. '
            '[[slnc 500]] The database was locked for seven ticks, not '
            'twenty-two. [[slnc 300]] Because the slow work was already '
            'done.'
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
            'Fourth demo: all of it, or none. [[slnc 400]] The same '
            "failure again. [[slnc 300]] The monitor's stock update is "
            'rejected, during commit. [[slnc 500]] The transaction rolls '
            'back. [[slnc 300]] And the database is exactly as it was '
            'before. [[slnc 300]] No orders, no lines, and all stock '
            'levels at ten. [[slnc 500]] All of the order, or none of it. '
            '[[slnc 300]] The customer never saw half an order.'
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
            'Now the costs. [[slnc 300]] The first: the order of writes '
            'matters. [[slnc 500]] Written in the order they were '
            'registered, the lines came before their order. [[slnc 300]] '
            'And the database refused, because a line pointed at an order '
            'that did not exist yet. [[slnc 500]] So the unit of work '
            'must know that parents come before children. [[slnc 300]] '
            'And it must sort its changes before writing them.'
        ),
    ),
    dict(
        key='09-dirty', kind='bullets', title='Cost Two: Knowing What Changed',
        body=['It must know what is dirty:', 'either check every field of every object,', 'or be told.', '', 'This project is told, through', 'registerDirty.'],
        narration=(
            'The second cost: knowing what changed. [[slnc 400]] There '
            'are two ways. [[slnc 300]] Check every field of every '
            'object, which is slow. [[slnc 300]] Or be told, which puts '
            'the burden on the calling code. [[slnc 500]] This project is '
            'told. [[slnc 300]] The caller says, register dirty, meaning, '
            'this object changed. [[slnc 300]] Forget to say it, and the '
            'change is never written.'
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
            'Fifth demo: the third cost, memory and the database '
            'disagree. [[slnc 400]] Until commit, memory says the '
            'keyboard has eight in stock. [[slnc 300]] The database still '
            'says ten. [[slnc 500]] The whole list of changes lives in '
            'memory. [[slnc 300]] So a huge bulk update is a memory '
            'problem too. [[slnc 300]] And anything reading the database '
            'in the meantime sees the old picture.'
        ),
    ),
    dict(
        key='11-toydb', kind='bullets', title='The Toy Database',
        body=['Rows, a counter, and a write', 'that can be told to fail.', '', 'This project adds begin, rollback,', 'and a foreign key check.', '', 'Every count came from its counter.'],
        narration=(
            'A word about the database in these demos. [[slnc 400]] It is '
            'a toy. [[slnc 300]] Rows, an operation counter, and a write '
            'that can be told to fail, on demand. [[slnc 500]] For this '
            'project, it also learned to begin and roll back a '
            "transaction. [[slnc 300]] And to check that a line's order "
            'really exists. [[slnc 300]] Every count in this video came '
            'from its counter.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['@Transactional is a unit of work.', 'A flush is its commit.', '', 'The persistence context tracks what', 'changed, and writes it when the', 'transaction ends.'],
        narration=(
            'You have met this pattern before. [[slnc 400]] In Spring, '
            'the at Transactional annotation starts a unit of work. '
            '[[slnc 300]] The persistence context tracks what changed. '
            '[[slnc 300]] And writes it all when the transaction ends, in '
            'an order it works out for you. [[slnc 500]] Writing out '
            'those changes is called a flush. [[slnc 300]] If a write '
            'ever happened at a moment you did not expect, that was the '
            'unit of work choosing when to commit.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The pattern is real.', 'The database is a stand-in: no locks,', 'no other users.', '', 'The ticks are a model of lock time,', 'not a measurement.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'pattern is real. [[slnc 300]] The database is a stand-in, '
            'with no real locks, and no other users. [[slnc 500]] The '
            'ticks are a model of how long locks are held, not a real '
            'measurement. [[slnc 300]] What is real is the shape. [[slnc '
            '300]] Slow work outside the transaction, and writes inside a '
            'short one.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['One write needs no unit of work.', '', 'It earns its place when one business', 'action must write several rows together.'],
        narration=(
            'So, when is this too much? [[slnc 400]] A single write does '
            'not need a unit of work. [[slnc 300]] It would just be '
            'ceremony. [[slnc 500]] It earns its place when one business '
            'action must write several rows together. [[slnc 300]] And '
            'when half of them would be worse than none.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add registerRemoved and use it', 'to cancel an order.'],
        narration=(
            "That's the Unit of Work pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Do the '
            'slow work first, then write everything once, or not at all. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] Add '
            'removal to the unit of work. [[slnc 300]] And use it to '
            'cancel an order. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
