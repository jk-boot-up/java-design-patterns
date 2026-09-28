"""Scene definitions for the Unit of Work with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Unit of Work with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Unit of Work pattern, in Java, using Spring. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A unit of work '
            'collects all the changes, and writes them together at the '
            'end. [[slnc 300]] Or not at all. [[slnc 600]] Think of a '
            'bank transfer. [[slnc 300]] Money must leave one account and '
            'arrive in the other, together. [[slnc 300]] Never just one '
            'half. [[slnc 700]] This is the framework version of the Unit '
            'of Work video, with the very same order. [[slnc 500]] We '
            'will hear the writes arrive at the end, not where the code '
            'is. [[slnc 300]] And meet three failures that belong to '
            'Spring itself. [[slnc 300]] An error that saves anyway, a '
            'write nobody asked for, and an annotation that does nothing.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Unit of Work, the hand-built video,', 'built the mechanism from plain Java.', '', 'This video uses the same order:', 'three lines, and the third stock', 'update fails.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Unit of Work video. [[slnc 400]] '
            'That one builds the mechanism by hand. [[slnc 300]] Register '
            'the changes, write them at the end, and undo everything on '
            'failure. [[slnc 500]] Here, we use the same order: three '
            'lines, where the third stock update fails. [[slnc 300]] We '
            'will not teach the pattern again. [[slnc 300]] Instead, we '
            'ask what Spring does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['Three things are new: Spring Boot,', 'Hibernate, and H2.', '', 'Spring creates and wires your objects.', 'Hibernate turns objects into SQL.', 'H2 is a database that runs in memory.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Three things are new in this project. [[slnc 400]] Spring, '
            "which creates the application's objects, and connects them. "
            '[[slnc 300]] Hibernate, which turns work on objects into '
            'database commands. [[slnc 300]] And H2, a database that runs '
            'in memory, so nothing needs installing. [[slnc 500]] And one '
            'promise. [[slnc 300]] If you skip this video, you lose none '
            'of the pattern. [[slnc 300]] This one is about the tool.'
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
            'First demo: no transaction at all. [[slnc 400]] Every step '
            'saves on its own. [[slnc 300]] And the third stock update '
            'fails. [[slnc 500]] What was saved? [[slnc 300]] One order, '
            'with two of its three lines. [[slnc 300]] Keyboard stock '
            'down to eight, mouse down to nine, and the monitor '
            'untouched. [[slnc 500]] Half an order. [[slnc 300]] The same '
            'problem as the hand-built video, now in Spring.'
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
            'Second demo: one annotation, at Transactional, on the place '
            'order method. [[slnc 500]] Listen to the counts. [[slnc '
            '300]] Inside the method, after changing three objects, '
            'nothing has been written yet. [[slnc 300]] Zero inserts, and '
            'zero updates. [[slnc 500]] After the method returns, two '
            'inserts and one update appear. [[slnc 300]] The writes '
            'happened at the end, not where the code is. [[slnc 500]] And '
            'now the same failure leaves no orders, and no lines. [[slnc '
            '300]] All of the order, or none of it. [[slnc 300]] The '
            'whole hand-built class is replaced by one annotation.'
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
            "Third demo: the first of Spring's own failures. [[slnc 400]] "
            'The same stock failure, but now declared as a checked '
            'exception. [[slnc 300]] That is the kind of error the '
            'compiler makes you handle. [[slnc 500]] What was saved? '
            '[[slnc 300]] One order, two lines, and stock of eight, nine, '
            'and ten. [[slnc 300]] Half an order, even with the at '
            "Transactional annotation. [[slnc 500]] Spring's default rule "
            'is this. [[slnc 300]] Undo on unchecked errors. [[slnc 300]] '
            'But save anyway on checked ones. [[slnc 300]] Nothing in the '
            'code says so.'
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
            'Fourth demo: the fix. [[slnc 400]] One setting on the '
            'annotation, called rollback for, naming the checked '
            'exception. [[slnc 500]] Now the same failure undoes '
            'everything. [[slnc 300]] No orders, no lines, and all stock '
            'back to ten. [[slnc 500]] But someone had to know to write '
            'that setting. [[slnc 300]] And nobody is warned when they '
            'forget.'
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
            'Fifth demo: a write nobody asked for. [[slnc 400]] Changes '
            'are normally held until the end. [[slnc 500]] Before '
            "changing a product's stock: zero updates written. [[slnc "
            '300]] After changing it: still zero, held back. [[slnc 500]] '
            'Then an unrelated query runs, counting products. [[slnc '
            '300]] Now one update has been written. [[slnc 500]] '
            'Hibernate wrote the change first, so the query would see it. '
            '[[slnc 300]] This is called a flush. [[slnc 300]] The write '
            'happened at a line that says nothing about writing. [[slnc '
            '300]] And if that write fails, it fails there, not at the '
            'end.'
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
            'Last demo: the annotation that does nothing. [[slnc 400]] '
            'The at Transactional annotation works because Spring wraps '
            'the object in a proxy. [[slnc 300]] The proxy begins and '
            'ends the transaction. [[slnc 500]] Now one method calls '
            'another method on the same object, directly, through this. '
            '[[slnc 300]] That call skips the proxy. [[slnc 300]] So the '
            'annotation on the second method is never seen. [[slnc 500]] '
            'The write fails, because there is no transaction. [[slnc '
            '300]] The error says: no entity manager with an actual '
            'transaction available. [[slnc 300]] What was saved: one '
            'order, and no lines. [[slnc 500]] This is one of the most '
            'common Spring errors there is.'
        ),
    ),
    dict(
        key='10-why', kind='bullets', title='Why These Surprise People',
        body=['The annotation hides the mechanism.', '', 'The mechanism still has rules:', 'checked exceptions commit,', 'queries flush,', 'and only calls through the proxy', 'count.'],
        narration=(
            'So why do these surprise people? [[slnc 400]] The annotation '
            'hides the mechanism. [[slnc 300]] But the mechanism still '
            'has rules. [[slnc 500]] Checked exceptions save anyway. '
            '[[slnc 300]] Queries can trigger writes. [[slnc 300]] And '
            'only calls that go through the proxy count. [[slnc 500]] '
            'None of those rules are visible in the code you wrote.'
        ),
    ),
    dict(
        key='11-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Transactional method in a', 'Spring application.', '', 'And the error in act six is one', 'of the most common there is.'],
        narration=(
            'Where have you met this before? [[slnc 400]] In every at '
            'Transactional method in a Spring application. [[slnc 300]] '
            'And the error from the last demo is one of the most common '
            'there is. [[slnc 500]] Now you know why it happens, not just '
            'how to make it stop.'
        ),
    ),
    dict(
        key='12-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', 'Hibernate and H2: the versions', 'that release manages.', '', 'No web server, no web starter.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] With whichever '
            'versions of Hibernate and H2 that release includes. [[slnc '
            '300]] There is no web server here. [[slnc 300]] This video '
            'is about the transaction, not the web.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's proxy,", "Hibernate's flush, and the counts", "from Hibernate's own statistics.", '', 'The database is H2 in memory.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            "Everything here is real. [[slnc 300]] The proxy is Spring's. "
            "[[slnc 300]] The flush is Hibernate's. [[slnc 300]] And the "
            "counts come from Hibernate's own statistics. [[slnc 400]] "
            'The only stand-in is the database, H2, in memory.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a single write, the annotation', 'is not needed.', '', 'It earns its place when one business', 'action writes several rows together.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a single write, '
            'the annotation is not needed at all. [[slnc 300]] It earns '
            'its place when one business action writes several rows '
            'together.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Make the stock failure extend', 'Exception and see what changes.'],
        narration=(
            "That's Unit of Work with Spring. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] An '
            'annotation hides the mechanism, but the mechanism still has '
            'rules. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Make the stock failure a checked exception. [[slnc '
            '300]] And listen for what changes in the second demo. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
