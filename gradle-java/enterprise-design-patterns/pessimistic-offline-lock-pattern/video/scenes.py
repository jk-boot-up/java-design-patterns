"""Scene definitions for the Pessimistic Offline Lock teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Pessimistic Offline Lock',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Pessimistic '
            'Offline Lock pattern in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] The plain '
            'definition: a pessimistic offline lock makes a person take a '
            'lock on a record before editing it. Nobody else can edit it '
            'until the lock is let go, so the clash is prevented instead '
            'of detected. [[slnc 350]] This is another project in the '
            'enterprise category, whose subject is how a business '
            'application organises its logic, its data and its requests. '
            'In our online store, two clerks want to edit the same '
            'product, and we would rather they did not clash at all. '
            '[[slnc 300]] By the end you will see a lock stop a clash '
            'before it starts, see edits that overwrite nothing, and see '
            'the three bills: waiting, a lock nobody let go of, and two '
            'people each waiting for the other. I will also show how much '
            'to lock.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Two clerks want to edit the', 'same product.', '', 'An edit takes several minutes.', '', 'A clash would throw away a lot', 'of work.', '', 'Stop the clash before it starts?'],
        narration=(
            'Here is the scenario. In the online store, two clerks want '
            'to edit the same product. An edit takes several minutes, and '
            'a clash would throw away a lot of work. [[slnc 300]] The '
            'question: can we stop the clash before it starts?'
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
            'First, lock, then edit. Clerk A asks for the lock on the '
            'blue mug, and gets it. Clerk B asks, and is refused, and '
            'told who holds it: A. Clerk B never starts an edit that '
            'could have been thrown away.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Take a lock before you edit.', '', 'Only the holder may write.', '', 'Everyone else is refused, and', 'told who holds it.', '', 'Let go when you are done, or the', 'lock expires.'],
        narration=(
            'The pattern. Take a lock before you edit. Only the holder '
            'may write. Everyone else is refused, and told who holds it. '
            'You let go when you are done, or the lock expires by itself.'
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
            'Second, no lost update. Clerk A raises the price and lets '
            'go. Then B takes the lock, and reads the product. It already '
            'has the new price. B saves the stock count on top of it. '
            'Nothing was overwritten, and nothing needed retrying.'
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
            'Third, the first bill. While clerk A edits, clerk B tries '
            'once a minute, and is refused three times. In that time B '
            'has done nothing useful. A lock trades lost updates for '
            'waiting.'
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
            'Fourth, a lock nobody let go of. Clerk A goes to lunch '
            'without letting go. B is refused straight away, and again '
            'after ten minutes. After sixteen minutes the lock has '
            'expired, and B gets it. [[slnc 300]] When A comes back and '
            'saves, A is refused, because A no longer holds the lock. An '
            'expiry solves the lunch, and creates a new problem for A.'
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
            'Fifth, two clerks each waiting for the other. A holds the '
            'mug and now needs the tea. B holds the tea and now needs the '
            'mug. Neither can move, until a lock expires. That is a '
            'deadlock. [[slnc 300]] The fix is a rule: everyone takes '
            'locks in the same order. Then A takes both, and B is stopped '
            'at the first, holding nothing, and simply waits.'
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
            'Last, how much to lock. One lock on the whole catalogue: A '
            'gets it, and B, editing a completely different product, is '
            'refused. A lock per product: A gets the mug, and B gets the '
            'tea. The smaller the thing locked, the fewer people wait. '
            'But the more things you lock, the more there is to forget, '
            'and to deadlock on.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A lock or checkout step before an', 'edit, and an unlock or checkin', '', 'A locks table or a locked_by and', 'locked_until column.', '', 'SELECT ... FOR UPDATE held across', 'a long session, which is a warning'],
        narration=(
            'How do you recognise this in code you did not write? A lock '
            'or checkout step before an edit, and an unlock or checkin '
            'after. A locks table or a locked_by and locked_until column. '
            'SELECT ... FOR UPDATE held across a long session, which is a '
            "warning sign. A message such as 'this record is being edited "
            "by someone else'."
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a pessimistic lock when a', 'conflict would throw away a lot of', 'work, when edits are long, and', 'when it is acceptable that people', 'sometimes wait. Lock the smallest', 'thing that keeps the data safe,', 'always give a lock an expiry, take', 'locks in a fixed order, and refuse', 'a write from anyone who no longer'],
        narration=(
            'Here is my verdict, plainly. Use a pessimistic lock when a '
            'conflict would throw away a lot of work, when edits are '
            'long, and when it is acceptable that people sometimes wait. '
            'Lock the smallest thing that keeps the data safe, always '
            'give a lock an expiry, take locks in a fixed order, and '
            'refuse a write from anyone who no longer holds the lock. Use '
            'an optimistic lock where clashes are rare and retrying is '
            'cheap.'
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
        body=['Where conflicts are rare and edits', 'short, a lock is waiting and', 'bookkeeping for nothing. A long', "database lock held across a user's", 'thinking time is almost always a', 'mistake.'],
        narration=(
            'So when is it too much? Where conflicts are rare and edits '
            'short, a lock is waiting and bookkeeping for nothing. A long '
            "database lock held across a user's thinking time is almost "
            'always a mistake.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Pessimistic Offline Lock. [[slnc 250]] If you take "
            'one sentence away, take this one: a pessimistic lock '
            'prevents the clash, and the price is waiting, forgotten '
            'locks and deadlocks. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, add a way for a lock holder to renew its '
            'lock, and decide how many times it may. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
