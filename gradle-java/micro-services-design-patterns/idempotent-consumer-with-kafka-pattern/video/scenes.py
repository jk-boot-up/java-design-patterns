"""Scene definitions for the Idempotent Consumer with Kafka teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of Kafka's and Postgres's words
in plain language before using the tool's name for it, and never points at a
picture the listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Idempotent Consumer with Kafka',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Idempotent Consumer pattern in Java, using a real Kafka '
            'broker and a real Postgres database. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A message can arrive more '
            'than once. [[slnc 300]] So the receiver writes down the I D '
            'of every message it handles, in the same step as the work '
            'itself. [[slnc 300]] When a message arrives whose I D is '
            'already written down, it does nothing. [[slnc 700]] In our '
            'online store, every time a customer places an order, '
            'checkout sends a message. [[slnc 300]] The notifications '
            'service then queues one confirmation email. [[slnc 300]] If '
            'that message arrives twice, the customer must still get '
            'exactly one email. [[slnc 500]] By the end, you will hear '
            'Kafka hand the same three orders to a second copy of the '
            'service. [[slnc 300]] A list of I Ds in memory fail to '
            'notice. [[slnc 300]] And two copies working on the same '
            'order at once, with the database deciding which one wins.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Checkout sends one message per order.', '',
              'Notifications queues one email', 'for each, in its own database.', '',
              'Several copies of notifications', 'run at once, and restart on', 'every deploy.', '',
              'Goal: exactly one email per order.'],
        narration=(
            'Here is the scenario. [[slnc 400]] When a customer places an '
            'order, checkout sends a message saying so. [[slnc 300]] The '
            'notifications service reads each message. [[slnc 300]] And '
            'it queues one confirmation email, as a row in its own '
            'database. [[slnc 600]] Several copies of the notifications '
            'service run at the same time. [[slnc 300]] And every time a '
            'new version is released, they are stopped and started again. '
            '[[slnc 500]] The shop wants exactly one email per order. '
            '[[slnc 300]] None missing, and none sent twice.'
        ),
    ),
    dict(
        key='03-words', kind='bullets', title="Kafka's Words",
        body=['A notebook the till writes in,', 'one line per sale: the topic.', '',
              'Each line has a numbered place,', 'from 0: the offset.', '',
              'One service, however many copies:', 'a consumer group.', '',
              'The bookmark the group asks to be', 'written: committing the offset.'],
        narration=(
            'Before the demo, a few words, in plain language. [[slnc '
            '400]] Picture a shared notebook. [[slnc 300]] The till '
            'writes one line in it for every sale. [[slnc 300]] And the '
            'back office reads down it, with a bookmark. [[slnc 600]] In '
            'Kafka, the notebook is called a topic. [[slnc 300]] Every '
            'message sits at a numbered place in it, counting from zero. '
            '[[slnc 300]] That number is called the offset. [[slnc 600]] '
            'A service reading the topic is called a consumer group, '
            'however many copies of it are running. [[slnc 300]] Kafka '
            "keeps each group's bookmark: the place it has reached. "
            '[[slnc 300]] A copy must ask for the bookmark to be moved. '
            '[[slnc 300]] That is called committing the offset. [[slnc '
            '300]] Until it is moved, Kafka assumes nothing after it was '
            'handled.'
        ),
    ),
    dict(
        key='04-one', kind='console', title='Kafka Sends It Again',
        body="""ONE. Kafka sends it again.
  checkout places 3 orders,
  at places 0, 1, 2.

  copy A is handed 3, queues 3 emails,
  and crashes before writing its place.
  place written down: none.

  copy B is handed places 0, 1, 2 again.
  nothing on them says they are repeats.
  deliveries: 6 for 3 orders.
  confirmation emails queued: 6.""",
        narration=(
            'First demo: Kafka sends it again. [[slnc 400]] Checkout '
            'places three orders, and Kafka puts them at places zero, '
            'one, and two. [[slnc 500]] Copy A of the notifications '
            'service is handed all three. [[slnc 300]] It queues three '
            'confirmation emails. [[slnc 300]] Then it crashes, before '
            'asking Kafka to move the bookmark. [[slnc 300]] So Kafka has '
            'no bookmark for the group at all. [[slnc 600]] Copy B joins '
            'the same group. [[slnc 300]] And Kafka hands it the same '
            'three orders again, at the same places. [[slnc 300]] Nothing '
            'on them says they are repeats. [[slnc 300]] Kafka has no '
            'such mark. [[slnc 500]] Six deliveries, for three orders. '
            '[[slnc 300]] And six emails. [[slnc 300]] This is what Kafka '
            'means by at least once.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='A List Of Ids In Memory',
        body="""TWO. A list of ids in memory.
  copy A keeps a list of handled ids
  in memory. it handles 3 orders,
  remembers 3 ids, and crashes.

  copy B is handed the same 3.
  its list starts with 0 ids.
  confirmation emails queued: 6.

  the list died with copy A.""",
        narration=(
            'Second demo: a list of I Ds in memory. [[slnc 400]] Copy A '
            'now keeps a list of the I Ds it has handled, in its own '
            'memory. [[slnc 300]] It handles three orders, remembers '
            'three I Ds, and crashes before moving the bookmark. [[slnc '
            '600]] Copy B is handed the same three orders. [[slnc 300]] '
            'Its list starts empty. [[slnc 300]] So it queues all three '
            'emails again. [[slnc 300]] Six emails. [[slnc 600]] This is '
            'the most important finding in the video. [[slnc 300]] On '
            'Kafka, an order is only handed out again because a copy '
            'stopped. [[slnc 300]] So the repeat always lands on a copy '
            'with fresh, empty memory. [[slnc 300]] A list in memory '
            'never even sees the duplicate it was meant to catch.'
        ),
    ),
    dict(
        key='06-postgres-words', kind='bullets', title="Postgres's Words",
        body=['A group of changes kept together', 'or thrown away together:', 'a transaction.', '',
              'A column no two rows may share:', 'a primary key.', '',
              'A second writer of the same key', 'waits for the first: a lock.'],
        narration=(
            'The fix needs three database words, in plain language. '
            '[[slnc 500]] A group of changes that are kept together, or '
            'thrown away together, is called a transaction. [[slnc 300]] '
            'Nothing in it is visible to anyone else until it is '
            'committed. [[slnc 500]] A column that no two rows may share '
            'is called a primary key. [[slnc 500]] And when two writers '
            'try to write the same key at the same moment, the database '
            'makes the second one wait. [[slnc 300]] That waiting is '
            'caused by a lock.'
        ),
    ),
    dict(
        key='07-three', kind='console', title='A Table, One Transaction',
        body="""THREE. A table of ids, same transaction.
  copy A writes each id and its email
  in one database transaction.
  it handles 3 and crashes before
  writing down its place.

  copy B is handed the same 3.
  the table already holds their ids,
  so B skips 3 and queues 0.

  deliveries: 6. emails queued: 3.
  ids stored: 3.""",
        narration=(
            'Third demo: the pattern. [[slnc 400]] Copy A writes each '
            "order's I D into a table of handled messages. [[slnc 300]] "
            'The I D is the primary key. [[slnc 300]] And the email is '
            'written beside it, in the same transaction. [[slnc 300]] '
            'Then copy A crashes, before moving the bookmark. [[slnc '
            '600]] Copy B is handed the same three orders. [[slnc 300]] '
            'For each one, it tries to write the I D. [[slnc 300]] And '
            'Postgres says the I D is already there. [[slnc 300]] So copy '
            'B skips all three, and queues no emails. [[slnc 600]] Six '
            'deliveries, three emails, and three I Ds. [[slnc 300]] The '
            'table outlived the copy that wrote it.'
        ),
    ),
    dict(
        key='08-diagram', kind='diagram', title='Where The Memory Lives',
        body=None,
        narration=(
            'Here is the whole setup, in words. [[slnc 400]] Kafka keeps '
            "the orders, and each group's bookmark. [[slnc 300]] A copy "
            'of the service is handed orders, starting from the bookmark. '
            '[[slnc 500]] For each order, it opens one database '
            'transaction. [[slnc 300]] It writes the I D first, then the '
            'email, and commits. [[slnc 300]] Only after that does it ask '
            'Kafka to move the bookmark. [[slnc 600]] If it crashes '
            'before the bookmark moves, the order goes out again, to '
            'another copy. [[slnc 300]] And the I D is already waiting '
            'for it. [[slnc 300]] The I D and the email are saved '
            'together, or not at all.'
        ),
    ),
    dict(
        key='09-four', kind='console', title='Where The Crash Lands',
        body="""FOUR. Where the crash lands.
  id written after the email:
  A dies before writing the id.
  emails: 1, ids: 0.
  copy B queues it again.
  emails for ORD-1: 2.

  id and email in one transaction:
  A dies before the commit.
  emails: 0, ids: 0.
  copy B handles it. emails: 1, ids: 1.""",
        narration=(
            'Fourth demo: where the crash lands. [[slnc 400]] First, the '
            'I D is written after the email, as a separate step. [[slnc '
            '300]] Copy A queues the email for order one. [[slnc 300]] '
            'Then it crashes before writing the I D. [[slnc 300]] One '
            'email, and no I D. [[slnc 300]] Copy B is handed the order, '
            'finds no I D, and queues the email again. [[slnc 300]] Two '
            'emails, for one order. [[slnc 600]] Now the I D and the '
            'email go in one transaction. [[slnc 300]] Copy A crashes '
            'before the commit. [[slnc 300]] Its connection drops, and '
            'Postgres throws the whole transaction away. [[slnc 300]] No '
            'email, and no I D. [[slnc 300]] Copy B handles the order '
            'properly: one email, one I D. [[slnc 500]] Exactly once, '
            'from a broker that only promises at least once.'
        ),
    ),
    dict(
        key='10-code', kind='code', title='The Pattern In Two Statements',
        body="""// id first, inside the transaction
insert into handled_messages
  (message_id, order_placed_at)
  values (?, ?)
  on conflict (message_id) do nothing;

// 1 row: new. 0 rows: done already
if (rows == 1) queueConfirmation(order);

connection.commit();
consumer.commitSync(); // only now""",
        narration=(
            'In the code, the whole pattern is two statements and a '
            'commit. [[slnc 500]] The copy opens a transaction, and '
            'inserts the message I D. [[slnc 300]] It asks Postgres to '
            'write nothing if the I D is already there. [[slnc 300]] '
            'Postgres answers with how many rows it wrote. [[slnc 500]] '
            'One row means the order is new. [[slnc 300]] So the email is '
            'queued, in the same transaction. [[slnc 300]] Zero rows '
            'means it was already handled. [[slnc 500]] Then the '
            'transaction commits. [[slnc 300]] And only then does the '
            'copy ask Kafka to move the bookmark.'
        ),
    ),
    dict(
        key='11-five', kind='console', title='Two Copies At Once',
        body="""FIVE. Two copies at once.
  copy A is handed ORD-1 and is slow.
  after 3 seconds, Kafka decides A is
  stuck and hands the order to copy B.

  B writes the same id; Postgres waits.
  sessions waiting on a lock: 1.
  A commits. queued by B: 0.
  emails for ORD-1: 1.

  A asks for its place to be written.
  Kafka refuses: CommitFailedException""",
        narration=(
            'Fifth demo, and this is something the plain Java version '
            'could never show. [[slnc 500]] Kafka gives every copy a '
            'patience limit. [[slnc 300]] It is how long a copy may go '
            'without asking for more orders, before Kafka decides it is '
            'stuck. [[slnc 300]] By default it is five minutes. [[slnc '
            '300]] Here, it is three seconds. [[slnc 600]] Copy A is '
            'handed order one. [[slnc 300]] It writes the I D and the '
            'email, but is slow to commit. [[slnc 300]] After three '
            'seconds, Kafka hands the same order to copy B. [[slnc 300]] '
            'Now two copies are working on one order. [[slnc 600]] Copy B '
            'tries to write the same I D. [[slnc 300]] And Postgres makes '
            "it wait, on copy A's lock. [[slnc 300]] Copy A commits. "
            '[[slnc 300]] Postgres tells copy B the I D is taken, so copy '
            'B skips it. [[slnc 300]] One email. [[slnc 600]] Then copy A '
            'asks Kafka to move the bookmark, and Kafka refuses. [[slnc '
            '300]] Copy A no longer owns that order. [[slnc 500]] A check '
            'done in Java would have let both copies through. [[slnc '
            "300]] Only the database's primary key could decide."
        ),
    ),
    dict(
        key='12-six', kind='console', title='The Bill',
        body="""SIX. The bill.
  3 orders placed two days ago.
  ids stored: 3. cleanup keeps ids
  for 24 hours, and deletes 3.

  this topic keeps orders for 168 hours.
  an operator replays the group.
  handed again: 3. emails queued: 6.

  keep ids as long as Kafka keeps orders.
  2 containers, for 1 email per order.""",
        narration=(
            'Sixth demo: the bill. [[slnc 400]] The table cannot keep '
            'every I D forever. [[slnc 300]] So a clean-up job deletes '
            'old ones. [[slnc 500]] Three orders placed two days ago are '
            'handled, and their three I Ds stored. [[slnc 300]] The '
            'clean-up keeps I Ds for one day. [[slnc 300]] So it deletes '
            'all three. [[slnc 600]] But a topic also keeps its orders '
            'for a set time. [[slnc 300]] This one keeps them for seven '
            "days, which is Kafka's default. [[slnc 500]] An operator "
            "moves the group's bookmark back to the start, to replay it. "
            '[[slnc 300]] Three orders are handed out again. [[slnc 300]] '
            'Their I Ds are gone, so three more emails are queued. [[slnc '
            '300]] Six in total. [[slnc 600]] So keep the I Ds at least '
            'as long as Kafka keeps the orders. [[slnc 500]] And there '
            'are two more systems to run, a broker and a database, for '
            'one email per order.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['The plain-Java version got the', 'whole pattern right.', '',
              'It left out: the repeat goes to a', 'different copy, with no mark on it.', '',
              'Two copies can hold the same', 'order at the same time.', '',
              "Kafka's retention sets the", "cleanup window's floor."],
        narration=(
            'How does this compare with the plain Java version? [[slnc '
            '400]] It got the whole pattern right. [[slnc 300]] The list '
            'in memory that is lost on restart. [[slnc 300]] The crash '
            'between the work and the I D. [[slnc 300]] And the single '
            'transaction that fixes both. [[slnc 300]] All of that holds '
            'here. [[slnc 600]] What it left out is what Kafka adds. '
            '[[slnc 500]] The repeat goes to a different copy, with no '
            'mark on it. [[slnc 300]] Two copies can hold the same order '
            'at the same moment. [[slnc 300]] And the clean-up window is '
            'no longer a free guess. [[slnc 300]] How long the topic '
            'keeps messages sets its minimum.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Assume every message comes twice,', 'to a different copy.', '',
              'The id is the primary key, in the', 'same database as the work.', '',
              'Write the id first, in the same', 'transaction as the work.', '',
              'Commit the transaction, then', 'the offset.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Behind Kafka, assume '
            'every message will be handed out twice, to a different copy. '
            '[[slnc 500]] Keep the I Ds in a table, in the same database '
            'as the work. [[slnc 300]] With the I D as the primary key. '
            '[[slnc 500]] Write the I D first, inside the same '
            "transaction as the work. [[slnc 300]] Let the database's "
            'answer decide whether to carry on. [[slnc 500]] Commit the '
            'transaction, and only then move the bookmark. [[slnc 500]] '
            'And keep the I Ds at least as long as the topic keeps the '
            'messages.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real Here',
        body=['Kafka 4.3.1 and Postgres 18.6,', 'each in a container the demo', 'starts and stops.', '',
              'kafka-clients 4.3.1, the Postgres', 'driver 42.7.13, Testcontainers 2.0.5.', '',
              'Every number comes from the', "program's own output.", '',
              'If the work is safe to repeat,', 'skip the table.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'broker is Kafka, version four point three point one. [[slnc '
            '300]] The database is Postgres, version eighteen point six. '
            '[[slnc 300]] Both are the newest releases. [[slnc 300]] Each '
            'runs in a container that the demo starts and stops by '
            'itself. [[slnc 300]] You just need Docker switched on first. '
            "[[slnc 500]] Every number you heard comes from the program's "
            'own output. [[slnc 600]] So, when is this too much? [[slnc '
            '300]] If the work is naturally safe to repeat, like setting '
            "an order's status to shipped, there is nothing to guard "
            'against. [[slnc 300]] And no table is needed.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Idempotent Consumer, with Kafka. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Kafka '
            'will hand the same order to two copies, one after a crash or '
            'both at once, and only an I D written in the same '
            'transaction as the work catches both. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Remove the primary key '
            'from the table of handled I Ds. [[slnc 300]] Run the fifth '
            'demo, and count the emails. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
