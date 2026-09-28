"""Scene definitions for the Optimistic Offline Lock teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Optimistic Offline Lock',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Optimistic Offline Lock pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] An optimistic lock '
            'lets people edit without locking anything. [[slnc 300]] It '
            'only detects a clash when someone saves. [[slnc 300]] By '
            'checking that the data has not changed since it was read. '
            '[[slnc 600]] Think of editing a shared document offline. '
            '[[slnc 300]] When you reconnect, the app checks whether '
            'someone else changed it meanwhile, before accepting your '
            'version. [[slnc 700]] In our online store, two clerks edit '
            'the same product at the same time. [[slnc 500]] In this '
            'video, they silently overwrite each other. [[slnc 300]] Then '
            'a version number stops it, and a retry keeps both changes. '
            '[[slnc 300]] And then we hear three costs.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Two clerks open the same product.', '', 'One raises the price.', 'One counts the stock.', '', 'Each edits for a while, then', 'saves the whole row.', '', 'What happens to the first save?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Two clerks open the same '
            'product. [[slnc 300]] One raises its price. [[slnc 300]] The '
            'other counts its stock. [[slnc 500]] Each one edits for a '
            'while, and then saves the whole product row. [[slnc 500]] So '
            'here is the question. [[slnc 300]] What happens to the first '
            "clerk's change?"
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
            'First, no lock at all. [[slnc 400]] Both clerks read the '
            'same row. [[slnc 300]] Clerk A raises the price to twelve '
            'pounds, and saves. [[slnc 300]] Clerk B counts forty in '
            'stock, and saves the whole row, with the old price still in '
            'it. [[slnc 500]] The row now says ten pounds. [[slnc 300]] '
            "Clerk A's change has vanished. [[slnc 300]] And nobody was "
            'told. [[slnc 300]] The last one to save simply wins.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Nothing is locked while people', 'work.', '', 'Every row carries a version.', '', 'A save succeeds only if the row', 'still has the version that was', 'read.', '', 'Otherwise: refused.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Nothing is locked while '
            'people work. [[slnc 300]] But every row carries a version '
            'number. [[slnc 500]] A save only succeeds if the row still '
            'has the version that was read. [[slnc 300]] If not, the save '
            'is refused. [[slnc 300]] And the person saving must look '
            'again.'
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
            'Second demo: a version on every row. [[slnc 400]] Clerk A '
            'saves, and the row moves to version two. [[slnc 500]] Clerk '
            'B saves. [[slnc 300]] But clerk B was working from version '
            'one. [[slnc 300]] So the save is refused, with the message: '
            'changed by someone else since you read it. [[slnc 500]] The '
            'twelve pound price survives.'
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
            'Third demo: reload, reapply, and save. [[slnc 400]] Clerk B '
            'is refused, and reloads the row. [[slnc 300]] Now it shows '
            'the new price of twelve pounds. [[slnc 300]] Clerk B '
            'reapplies the stock count of forty, and saves again. [[slnc '
            '500]] Two attempts in total. [[slnc 300]] And both changes '
            'survive: price twelve pounds, stock forty.'
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
            'Fourth demo, and the first cost. [[slnc 400]] One clerk '
            'changed the price. [[slnc 300]] Another changed the stock. '
            '[[slnc 300]] Different fields, so there was no real clash. '
            '[[slnc 500]] But the second save is still refused. [[slnc '
            '300]] Because the version number belongs to the whole row. '
            '[[slnc 300]] It is a conflict that was not really a '
            'conflict. [[slnc 500]] A version for each field would let '
            'both through, but at the cost of more bookkeeping.'
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
            'Fifth demo: a busy row. [[slnc 400]] Ten clerks each add one '
            'to the stock of the same product. [[slnc 500]] Nothing is '
            'lost, and the stock ends at ten. [[slnc 300]] But nineteen '
            'saves were attempted, and nine were refused. [[slnc 500]] '
            'Nine of the ten clerks did their work twice. [[slnc 300]] On '
            'a row everyone wants, most of the effort gets repeated.'
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
            'Last demo: the second cost, you only find out at the end. '
            '[[slnc 400]] A user makes five changes, over a long editing '
            'session. [[slnc 300]] When they save, they are told the row '
            'has changed. [[slnc 500]] All five changes are thrown away. '
            '[[slnc 300]] And the user only learns this now, at the very '
            'end. [[slnc 500]] The cost of a conflict is paid at the '
            'moment it is found.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A version column, and WHERE id = ?', 'AND version = ? in an update.', '', '@Version in JPA and Hibernate.', '', 'An OptimisticLockException or an', 'HTTP 409 or 412 in the API.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a version column, and an update that '
            'checks both the I D and the version. [[slnc 300]] Look for '
            'the at Version annotation in J P A, or Hibernate. [[slnc '
            '300]] Look for an Optimistic Lock Exception, or a web '
            'service answering four hundred and nine, meaning conflict. '
            '[[slnc 300]] And look for web requests using the If Match '
            'header, with an E Tag.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use an optimistic lock when', 'conflicts are rare, edits are', 'short, and it is cheap to try', 'again: most web applications. Keep', 'the version in the row, check it', 'in the update, retry by reloading,', 'and tell the user honestly when', 'their change cannot be applied.', 'Use a pessimistic lock when a'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use an optimistic lock '
            'when conflicts are rare, edits are short, and trying again '
            'is cheap. [[slnc 300]] That describes most web applications. '
            '[[slnc 500]] Keep the version in the row. [[slnc 300]] Check '
            'it in the update. [[slnc 300]] Retry by reloading. [[slnc '
            '300]] And tell the user honestly when their change cannot be '
            'applied. [[slnc 500]] Use a pessimistic lock instead, when a '
            'conflict is expensive, or an editing session is long.'
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
        body=['Where conflicts are frequent and', 'costly, retrying wastes work and a', 'lock is kinder. Where only one', 'writer exists, a version is pure', 'overhead.'],
        narration=(
            'So, when is this too much? [[slnc 400]] Where conflicts are '
            'frequent and costly, retrying wastes work, and a lock is '
            'kinder. [[slnc 400]] And where there is only ever one '
            'writer, a version number is pure overhead.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Optimistic Offline Lock. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] An '
            'optimistic lock costs nothing until there is a clash, and '
            'then the clash is paid for in repeated work, or lost edits. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] '
            'Change the store, so the version is kept per field instead '
            'of per row. [[slnc 300]] Then see which conflicts disappear. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
