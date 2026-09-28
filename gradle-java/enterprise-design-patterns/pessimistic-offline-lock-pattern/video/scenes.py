"""Scene definitions for the Pessimistic Offline Lock teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Pessimistic Offline Lock',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Pessimistic Offline Lock pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A pessimistic lock '
            'makes a person take a lock on a record before editing it. '
            '[[slnc 300]] Nobody else can edit it until the lock is '
            'released. [[slnc 300]] So a clash is prevented, instead of '
            'detected. [[slnc 600]] Think of a meeting room booking. '
            '[[slnc 300]] Once you have booked the room, nobody else can '
            'use it until your booking ends. [[slnc 700]] In our online '
            'store, two clerks want to edit the same product. [[slnc '
            '300]] And we would rather they did not clash at all. [[slnc '
            '500]] In this video, a lock stops a clash before it starts. '
            '[[slnc 300]] Then we hear the costs: waiting, a forgotten '
            'lock, and two people each waiting for the other. [[slnc '
            '300]] And we learn how much to lock.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Two clerks want to edit the', 'same product.', '', 'An edit takes several minutes.', '', 'A clash would throw away a lot', 'of work.', '', 'Stop the clash before it starts?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Two clerks want to edit '
            'the same product. [[slnc 300]] An edit takes several '
            'minutes. [[slnc 300]] And a clash would throw away a lot of '
            'work. [[slnc 500]] So here is the question. [[slnc 300]] Can '
            'we stop the clash before it even starts?'
        ),
    ),
    dict(
        key='03-first', kind='console', title='Lock First, Then Edit',
        body="""ONE. Lock first.
  A asks: got the lock.
  B asks: refused, locked
  by A.

  the clash was stopped before
  B could start editing.""",
        narration=(
            'First demo: lock first, then edit. [[slnc 400]] Clerk A asks '
            'for the lock on the blue mug, and gets it. [[slnc 300]] '
            'Clerk B asks, and is refused. [[slnc 300]] And B is told who '
            'holds the lock: clerk A. [[slnc 500]] Clerk B never starts '
            'an edit that might have been thrown away.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Take a lock before you edit.', '', 'Only the holder may write.', '', 'Everyone else is refused, and', 'told who holds it.', '', 'Let go when you are done, or the', 'lock expires.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Take a lock before you edit. '
            '[[slnc 300]] Only the lock holder may save changes. [[slnc '
            '300]] Everyone else is refused, and told who holds it. '
            '[[slnc 500]] Release the lock when you are done. [[slnc '
            '300]] Or it expires by itself.'
        ),
    ),
    dict(
        key='05-safe', kind='console', title='No Lost Update',
        body="""TWO. No lost update.
  A raises the price, lets go.
  B locks, reads: price 1200.
  B saves stock 40.

  nothing was overwritten.""",
        narration=(
            'Second demo: no lost update. [[slnc 400]] Clerk A raises the '
            'price, and releases the lock. [[slnc 300]] Then clerk B '
            'takes the lock, and reads the product. [[slnc 300]] It '
            'already shows the new price, twelve pounds. [[slnc 500]] '
            'Clerk B saves the stock count, on top of it. [[slnc 300]] '
            'Nothing was overwritten. [[slnc 300]] And nothing needed '
            'retrying.'
        ),
    ),
    dict(
        key='06-wait', kind='console', title='The Bill: Waiting',
        body="""THREE. Waiting.
  B tries once a minute:
  3 refusals.

  B has done nothing useful.

  a lock trades lost updates
  for waiting.""",
        narration=(
            'Third demo: the first cost, waiting. [[slnc 400]] While '
            'clerk A edits, clerk B tries once a minute. [[slnc 300]] And '
            'is refused three times. [[slnc 500]] In all that time, clerk '
            'B has done nothing useful. [[slnc 300]] A lock swaps lost '
            'updates for waiting.'
        ),
    ),
    dict(
        key='07-forgot', kind='console', title='The Bill: A Lock Nobody Let Go Of',
        body="""FOUR. Forgotten.
  A goes to lunch.
  10 minutes: still locked.
  16 minutes: expired, B in.

  A comes back and saves:
  refused, no longer the
  holder.""",
        narration=(
            'Fourth demo: a lock nobody released. [[slnc 400]] Clerk A '
            'goes to lunch, without releasing the lock. [[slnc 500]] '
            'Clerk B is refused straight away. [[slnc 300]] And again, '
            'after ten minutes. [[slnc 300]] After sixteen minutes, the '
            'lock has expired, and clerk B gets it. [[slnc 500]] When '
            'clerk A comes back and saves, A is refused. [[slnc 300]] '
            'Because A no longer holds the lock. [[slnc 500]] An expiry '
            'solves the lunch problem, but creates a new problem for '
            'clerk A.'
        ),
    ),
    dict(
        key='08-dead', kind='console', title='The Bill: Each Waiting For The Other',
        body="""FIVE. A deadlock.
  A holds mug, needs tea.
  B holds tea, needs mug.
  neither can move.

  fixed order: A took both,
  B held nothing and waits.""",
        narration=(
            'Fifth demo: two clerks, each waiting for the other. [[slnc '
            '400]] Clerk A holds the lock on the mug, and now needs the '
            'tea. [[slnc 300]] Clerk B holds the lock on the tea, and now '
            'needs the mug. [[slnc 500]] Neither can move, until a lock '
            'expires. [[slnc 300]] That is called a deadlock. [[slnc '
            '600]] The fix is a simple rule: everyone takes locks in the '
            'same order. [[slnc 300]] Then clerk A takes both. [[slnc '
            '300]] And clerk B is stopped at the first one, holding '
            'nothing, and simply waits.'
        ),
    ),
    dict(
        key='09-size', kind='console', title='How Much To Lock',
        body="""SIX. How much.
  one lock on the catalogue:
  B, on another product,
  refused.

  a lock per product: both
  work.

  smaller: less waiting,
  more locks to manage.""",
        narration=(
            'Last demo: how much to lock. [[slnc 400]] With one lock on '
            'the whole catalogue, clerk A gets it. [[slnc 300]] And clerk '
            'B, editing a completely different product, is refused. '
            '[[slnc 500]] With one lock per product, clerk A gets the '
            'mug, and clerk B gets the tea. [[slnc 300]] Both can work. '
            '[[slnc 500]] The smaller the thing you lock, the fewer '
            'people wait. [[slnc 300]] But the more locks you have, the '
            'more there are to forget, and to deadlock on.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A lock or checkout step before an', 'edit, and an unlock or checkin', '', 'A locks table or a locked_by and', 'locked_until column.', '', 'SELECT ... FOR UPDATE held across', 'a long session, which is a warning'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a lock, or check-out step, before an '
            'edit, and an unlock, or check-in, after. [[slnc 300]] Look '
            'for a locks table, or columns saying who locked a record, '
            'and until when. [[slnc 300]] Look for a database lock held '
            'across a long session, which is a warning sign. [[slnc 300]] '
            'And a message like: this record is being edited by someone '
            'else.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a pessimistic lock when a', 'conflict would throw away a lot of', 'work, when edits are long, and', 'when it is acceptable that people', 'sometimes wait. Lock the smallest', 'thing that keeps the data safe,', 'always give a lock an expiry, take', 'locks in a fixed order, and refuse', 'a write from anyone who no longer'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a pessimistic lock '
            'when a conflict would throw away a lot of work. [[slnc 300]] '
            'When edits take a long time. [[slnc 300]] And when it is '
            'acceptable for people to wait sometimes. [[slnc 500]] Lock '
            'the smallest thing that keeps the data safe. [[slnc 300]] '
            'Always give a lock an expiry. [[slnc 300]] Take locks in a '
            'fixed order. [[slnc 300]] And refuse a save from anyone who '
            'no longer holds the lock. [[slnc 500]] Use an optimistic '
            'lock instead, where clashes are rare, and retrying is cheap.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every result you '
            "heard comes from the program's own output. [[slnc 300]] Time "
            'is simulated, not read from the clock, so every run gives '
            'the same result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['Where conflicts are rare and edits', 'short, a lock is waiting and', 'bookkeeping for nothing. A long', "database lock held across a user's", 'thinking time is almost always a', 'mistake.'],
        narration=(
            'So, when is this too much? [[slnc 400]] Where conflicts are '
            'rare and edits are short, a lock is waiting and bookkeeping '
            'for nothing. [[slnc 400]] And a database lock held while a '
            'person thinks is almost always a mistake.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Pessimistic Offline Lock. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'pessimistic lock prevents the clash, and the price is '
            'waiting, forgotten locks, and deadlocks. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Add a way for a lock '
            'holder to renew their lock. [[slnc 300]] And decide how many '
            'times they may do it. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
