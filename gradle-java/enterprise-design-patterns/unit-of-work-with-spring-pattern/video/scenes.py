"""Scene definitions for the Unit of Work with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Unit of Work with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Unit of Work '
            'pattern with Spring, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Unit of Work video. That one built '
            'the pattern by hand. This one shows the very same order '
            'going through one annotation. [[slnc 350]] The plain '
            'definition, in short: collect all the changes, and write '
            'them together at the end, or not at all. [[slnc 300]] By the '
            'end you will see the writes arrive at commit, not where the '
            'code is, and meet the failures that belong to Spring itself: '
            'a checked exception that commits anyway, a flush nobody '
            'wrote, and an annotation that does nothing.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Unit of Work, the hand-built video,', 'built the mechanism from plain Java.', '', 'This video uses the same order:', 'three lines, and the third stock', 'update fails.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'This video assumes the Unit of Work video. If you have not '
            'seen it, start there. It builds the mechanism by hand: '
            'register the changes, write them at commit, roll back to '
            'nothing. [[slnc 300]] This one uses the same order: three '
            'lines, where the third stock update fails. It does not teach '
            'the pattern again. It shows what Spring does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['Three things are new: Spring Boot,', 'Hibernate, and H2.', '', 'Spring creates and wires your objects.', 'Hibernate turns objects into SQL.', 'H2 is a database that runs in memory.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first annotation, three new things. Spring '
            'creates the objects of an application, and wires them '
            'together. Hibernate turns operations on objects into S Q L. '
            'H two is a database that runs in memory, so nothing needs '
            'installing. [[slnc 300]] And a promise: skipping this video '
            'loses none of the pattern. The hand-built one teaches all of '
            'it.'
        ),
    ),
    dict(
        key='04-no-tx', kind='console', title='No Transaction',
        body="""ONE. No transaction.
  the third stock update failed

  committed: orders 1, lines 2,
  stock keyboard 8, mouse 9,
  monitor 10

  the partner's first act,
  with Spring.""",
        narration=(
            'First, with no transaction around the order. Every step '
            'commits on its own. The third stock update fails. [[slnc '
            '300]] What is committed: one order. Two lines. Keyboard '
            'stock down to eight, mouse stock down to nine, monitor '
            'untouched. Half an order. The very first act of the Unit of '
            'Work video, now in Spring.'
        ),
    ),
    dict(
        key='05-annotation', kind='console', title='One Annotation',
        body="""TWO. @Transactional.
  inside the method, after
  changing three objects:
  inserts written 0,
  updates written 0.

  after it returned:
  inserts 2, updates 1.

  the same failure: orders 0,
  lines 0. none of it.""",
        narration=(
            'Now the one annotation: transactional, on the place method. '
            'Watch the counts. Inside the method, after changing three '
            'objects, inserts written: zero. Updates written: zero. '
            '[[slnc 300]] After the method returned: two inserts, one '
            'update. The writes appeared at commit, not where the code '
            'is. [[slnc 300]] And the same failure now leaves orders '
            'zero, lines zero. All of the order, or none of it. That '
            'whole hand-built class is one annotation.'
        ),
    ),
    dict(
        key='06-checked', kind='console', title='The Checked Exception',
        body="""THREE. A checked exception.
  the same failure, declared
  as a checked exception.

  committed: orders 1, lines 2,
  stock 8, 9, 10

  half an order committed,
  under @Transactional.""",
        narration=(
            "Now the failures that are Spring's own. The same failure, "
            'but declared as a checked exception, one the compiler makes '
            'you handle. [[slnc 300]] Committed: one order, two lines, '
            'stock eight, nine, ten. Half an order. Under the '
            "transactional annotation. [[slnc 300]] Spring's default: "
            'roll back on unchecked exceptions and errors. Commit on '
            'checked ones. Nothing in the code says so. The annotation '
            'looks the same.'
        ),
    ),
    dict(
        key='07-rollbackfor', kind='console', title='rollbackFor',
        body="""FOUR. rollbackFor.
  @Transactional(
    rollbackFor =
    StockFailureChecked.class)

  committed: orders 0, lines 0,
  stock 10, 10, 10

  someone has to know to write
  it.""",
        narration=(
            'The fix is one attribute: rollback for, naming the checked '
            'exception. Now the same failure rolls everything back. '
            'Orders zero, lines zero, stock ten, ten, ten. [[slnc 300]] '
            'But the default had to be overridden, in the annotation, by '
            'someone who knew. Nobody is warned when they forget.'
        ),
    ),
    dict(
        key='08-flush', kind='console', title='A Flush Nobody Wrote',
        body="""FIVE. A flush.
  updates before the change: 0
  after changing a stock: 0
  after an unrelated query: 1

  Hibernate wrote it first.

  the write happened at a line
  that says nothing about
  writing.""",
        narration=(
            'Second failure. Changes are held until commit. But look at '
            'this. Updates written before the change: zero. After '
            "changing a product's stock: still zero, held back. [[slnc "
            '300]] Then an unrelated query runs, counting products. '
            'Updates written: one. Hibernate wrote the change first, so '
            'that the query would see it. [[slnc 300]] The write happened '
            'at a line that says nothing about writing. And if that write '
            'fails, it fails there, not at the end.'
        ),
    ),
    dict(
        key='09-proxy', kind='console', title='The Annotation That Does Nothing',
        body="""SIX. A call on this.
  placeViaThis() calls
  placeLines(), which is
  @Transactional, on this.

  TransactionRequiredException:
  No EntityManager with actual
  transaction available

  committed: orders 1, lines 0""",
        narration=(
            'Third failure. The transactional annotation works because '
            'Spring wraps the object in a proxy. The proxy begins and '
            'commits the transaction. [[slnc 300]] Now a method calls '
            'another method on the same object, through this. That call '
            'skips the proxy. The annotation on the second method is '
            'never seen. [[slnc 300]] The write fails, for want of a '
            'transaction. Transaction required exception: no entity '
            'manager with actual transaction available. Committed: one '
            'order, no lines. One of the most common Spring errors there '
            'is.'
        ),
    ),
    dict(
        key='10-why', kind='bullets', title='Why These Surprise People',
        body=['The annotation hides the mechanism.', '', 'The mechanism still has rules:', 'checked exceptions commit,', 'queries flush,', 'and only calls through the proxy', 'count.'],
        narration=(
            'So why do these surprise people? The annotation hides the '
            'mechanism. But the mechanism still has rules. Checked '
            'exceptions commit. Queries can flush. And only calls that go '
            'through the proxy count. [[slnc 300]] None of those rules '
            'are visible in the code you wrote.'
        ),
    ),
    dict(
        key='11-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Transactional method in a', 'Spring application.', '', 'And the error in act six is one', 'of the most common there is.'],
        narration=(
            'You have met this. Every transactional method in a Spring '
            'application. And the error in act six is one of the most '
            'common Spring errors there is. [[slnc 300]] Now you know why '
            'it happens, not just how to make it stop.'
        ),
    ),
    dict(
        key='12-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', 'Hibernate and H2: the versions', 'that release manages.', '', 'No web server, no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. '
            'Hibernate and H two are whichever versions that release '
            'manages. There is no web server and no web starter in this '
            'project. It is about the transaction boundary, not H T T P.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's proxy,", "Hibernate's flush, and the counts", "from Hibernate's own statistics.", '', 'The database is H2 in memory.'],
        narration=(
            'The same honest admission as everywhere in this course, and '
            "again short. Everything is real. The proxy is Spring's. The "
            "flush is Hibernate's. The counts come from Hibernate's own "
            'statistics. The only stand-in is the database, H two in '
            'memory.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a single write, the annotation', 'is not needed.', '', 'It earns its place when one business', 'action writes several rows together.'],
        narration=(
            'So when is it too much? For a single write, the annotation '
            'is not needed at all. It earns its place when one business '
            'action writes several rows together.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Make the stock failure extend', 'Exception and see what changes.'],
        narration=(
            "That's Unit of Work with Spring. [[slnc 250]] If you take "
            'one sentence away, take this one: an annotation hides the '
            'mechanism, and the mechanism still has rules. [[slnc 350]] '
            'The full source, the written notes, the diagrams and an '
            'animated walkthrough are all in the repository. [[slnc 300]] '
            'If you try one exercise, make the stock failure extend '
            'Exception instead, and see what changes in act two. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
