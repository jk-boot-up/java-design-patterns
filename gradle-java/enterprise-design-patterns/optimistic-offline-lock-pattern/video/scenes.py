"""Scene definitions for the Optimistic Offline Lock teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Optimistic Offline Lock',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Optimistic '
            'Offline Lock pattern in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] The plain '
            'definition: an optimistic offline lock lets people edit '
            'without locking anything. It detects a clash only when '
            'someone saves, by checking that the row has not changed '
            'since it was read. [[slnc 350]] This is another project in '
            'the enterprise category, whose subject is how a business '
            'application organises its logic, its data and its requests. '
            'In our online store, two clerks edit the same product at the '
            'same time. [[slnc 300]] By the end you will see two clerks '
            'silently overwrite each other, see a version number stop it, '
            'see how a retry keeps both changes, and see the three bills: '
            'a conflict that was not one, a busy row where most of the '
            'work is repeated, and a long edit lost at the last moment.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Two clerks open the same product.', '', 'One raises the price.', 'One counts the stock.', '', 'Each edits for a while, then', 'saves the whole row.', '', 'What happens to the first save?'],
        narration=(
            'Here is the scenario. In the online store, two clerks open '
            'the same product. One raises the price. The other counts the '
            'stock. Each edits for a while, and then saves the whole row. '
            "[[slnc 300]] The question: what happens to the first clerk's "
            'change?'
        ),
    ),
    dict(
        key='03-lww', kind='console', title='No Lock: The Last Write Wins',
        body="""ONE. The last write wins.
  A raises the price to 12.00.
  B counts 40 in stock.

  the row: price 10.00,
  stock 40.

  A's price vanished, with
  no error.""",
        narration=(
            'First, no lock. Both clerks read the same row. Clerk A '
            'raises the price to twelve pounds and saves. Clerk B counts '
            'forty in stock, and saves the whole row, with the old price '
            "still in it. The row now says ten pounds. Clerk A's change "
            'vanished, and nobody was told.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Nothing is locked while people', 'work.', '', 'Every row carries a version.', '', 'A save succeeds only if the row', 'still has the version that was', 'read.', '', 'Otherwise: refused.'],
        narration=(
            'The pattern. Nothing is locked while people work. Every row '
            'carries a version. A save succeeds only if the row still has '
            'the version that was read. If not, it is refused, and the '
            'writer must look again.'
        ),
    ),
    dict(
        key='05-version', kind='console', title='A Version On Every Row',
        body="""TWO. A version.
  A saves: accepted. version 2.
  B saves: refused, changed by
  someone else.

  the row: price 12.00,
  stock 50.""",
        narration=(
            'Second, a version on every row. Clerk A saves, and the row '
            'moves to version two. Clerk B saves, but was working from '
            'version one, and is refused: changed by someone else since '
            'you read it. The twelve pound price survives.'
        ),
    ),
    dict(
        key='06-retry', kind='console', title='Reload, Reapply, Save',
        body="""THREE. Retry.
  B is refused, reloads,
  reapplies the stock count,
  and saves: 2 attempts.

  price 12.00, stock 40.
  both changes survived.""",
        narration=(
            'Third, reload, reapply, save. Clerk B is refused, and '
            'reloads the row. Now it shows the new price. Clerk B '
            'reapplies the stock count, and saves. Two attempts, and both '
            'changes survive.'
        ),
    ),
    dict(
        key='07-field', kind='console', title='The Version Is Per Row',
        body="""FOUR. Per row.
  price and stock: different
  fields.
  second save: refused.

  a conflict that was not one.""",
        narration=(
            'Fourth, the first bill. One clerk changed the price and '
            'another changed the stock. Different fields, and no real '
            'clash. But the second save is refused, because the version '
            'belongs to the whole row. A version for each field would let '
            'both through, at the cost of more bookkeeping.'
        ),
    ),
    dict(
        key='08-busy', kind='console', title='The Bill: A Busy Row',
        body="""FIVE. A busy row.
  10 clerks add one each.
  final stock: 10.
  saves attempted: 19.
  refused: 9.

  nothing lost, most work
  repeated.""",
        narration=(
            'Fifth, a busy row. Ten clerks each add one to the stock of '
            'the same product. Nothing is lost, and the stock ends at '
            'ten. But nineteen saves were attempted, and nine were '
            'refused. Nine of the ten did their work twice. A row that '
            'everyone wants is a row where most of the effort is '
            'repeated.'
        ),
    ),
    dict(
        key='09-late', kind='console', title='The Bill: You Find Out At The End',
        body="""SIX. Found at the end.
  5 changes in a long session.
  on save: changed by someone
  else.

  all 5 discarded.

  the cost is paid when the
  conflict is found.""",
        narration=(
            'Last, the second bill. A user makes five changes over a long '
            'session. On saving, they are told the row changed. All five '
            'changes are discarded, and the user learns it only now. The '
            'cost of a conflict is paid at the moment it is found, which '
            'is the end.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A version column, and WHERE id = ?', 'AND version = ? in an update.', '', '@Version in JPA and Hibernate.', '', 'An OptimisticLockException or an', 'HTTP 409 or 412 in the API.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'version column, and WHERE id = ? AND version = ? in an '
            'update. @Version in JPA and Hibernate. An '
            'OptimisticLockException or an HTTP 409 or 412 in the API. '
            'If-Match and ETag headers on a web request.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use an optimistic lock when', 'conflicts are rare, edits are', 'short, and it is cheap to try', 'again: most web applications. Keep', 'the version in the row, check it', 'in the update, retry by reloading,', 'and tell the user honestly when', 'their change cannot be applied.', 'Use a pessimistic lock when a'],
        narration=(
            'Here is my verdict, plainly. Use an optimistic lock when '
            'conflicts are rare, edits are short, and it is cheap to try '
            'again: most web applications. Keep the version in the row, '
            'check it in the update, retry by reloading, and tell the '
            'user honestly when their change cannot be applied. Use a '
            'pessimistic lock when a conflict is expensive, or a session '
            'is long.'
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
        body=['Where conflicts are frequent and', 'costly, retrying wastes work and a', 'lock is kinder. Where only one', 'writer exists, a version is pure', 'overhead.'],
        narration=(
            'So when is it too much? Where conflicts are frequent and '
            'costly, retrying wastes work and a lock is kinder. Where '
            'only one writer exists, a version is pure overhead.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Optimistic Offline Lock. [[slnc 250]] If you take one "
            'sentence away, take this one: an optimistic lock costs '
            'nothing until there is a clash, and then the clash is paid '
            'for in repeated work or lost edits. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, change the store so the version is '
            'per field, and see which conflicts disappear. [[slnc 300]] '
            'If this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
