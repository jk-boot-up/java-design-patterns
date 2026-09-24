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
            'Hello, and welcome. This video explains the Idempotent '
            'Consumer pattern in Java, using a real Kafka broker and a '
            'real Postgres database. [[slnc 250]] It is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] Here is the '
            'plain definition, in general words. A message can arrive '
            'more than once. So the receiver writes down the id of every '
            'message it has handled, in the same step as the work itself, '
            'and when a message turns up whose id is already written '
            'down, it does nothing. [[slnc 350]] Now the same thing in our '
            'online store. Every time a customer places an order, '
            'checkout sends a message, and the notifications service '
            'queues one confirmation email. If that message arrives twice, '
            'the customer must still get exactly one email. [[slnc 300]] '
            'By the end you will have seen Kafka hand the same three '
            'orders to a second copy of the service, a list of ids in '
            'memory fail to notice, and two copies working on the same '
            'order at the same time, with the database deciding which one '
            'wins.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Checkout sends one message per order.', '',
              'Notifications queues one email', 'for each, in its own database.', '',
              'Several copies of notifications', 'run at once, and restart on', 'every deploy.', '',
              'Goal: exactly one email per order.'],
        narration=(
            'Here is the scenario. When a customer places an order, '
            'checkout sends a message saying so. The notifications service '
            'reads each message and queues one confirmation email, as a '
            'row in its own database. [[slnc 300]] Several copies of the '
            'notifications service run at the same time, and every time a '
            'new version is deployed, they are stopped and started again. '
            '[[slnc 250]] The shop wants exactly one email per order. None '
            'missing, and none sent twice.'
        ),
    ),
    dict(
        key='03-words', kind='bullets', title="Kafka's Words",
        body=['A notebook the till writes in,', 'one line per sale: the topic.', '',
              'Each line has a numbered place,', 'from 0: the offset.', '',
              'One service, however many copies:', 'a consumer group.', '',
              'The bookmark the group asks to be', 'written: committing the offset.'],
        narration=(
            'Before the demo, a few words, in plain language first. '
            'Picture a shared notebook. The till writes one line in it for '
            'every sale, and the back office reads down it with a '
            'bookmark. [[slnc 250]] In Kafka the notebook is called a '
            'topic. Every message sits at a numbered place in it, counting '
            'from zero, and Kafka calls that number the offset. '
            '[[slnc 250]] A service reading the topic is a consumer group, '
            'however many copies of it are running. The broker keeps each '
            'group\'s bookmark: the place it has reached. A copy has to '
            'ask for the bookmark to be moved, and Kafka calls that '
            'committing the offset. Until it is moved, Kafka assumes '
            'nothing after it was handled.'
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
            'Act one. Checkout places three orders, and Kafka puts them at '
            'places zero, one and two. Copy A of the notifications service '
            'is handed all three, and queues three confirmation emails. '
            'Then it crashes, before asking Kafka to move the bookmark. '
            'So Kafka has written down no place at all for the group. '
            '[[slnc 300]] Copy B joins the same group, and Kafka hands it '
            'the same three orders again, at the same places, zero, one '
            'and two. Nothing on them says they are repeats. Kafka has no '
            'such mark. [[slnc 250]] Six deliveries for three orders, and '
            'six emails. This is what Kafka means by at least once.'
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
            'Act two. Copy A now keeps a list of the ids it has handled, '
            'in its own memory. It handles three orders, remembers three '
            'ids, and crashes before moving the bookmark. [[slnc 250]] '
            'Copy B is handed the same three orders. Its list starts with '
            'no ids at all, so it queues all three emails again. Six '
            'emails. [[slnc 300]] This is the most important find in the '
            'video. On Kafka, an order is only handed out again because a '
            'copy stopped. So the repeat always lands on a copy whose '
            'memory is new. A list in memory never even sees the '
            'duplicate it was written to catch.'
        ),
    ),
    dict(
        key='06-postgres-words', kind='bullets', title="Postgres's Words",
        body=['A group of changes kept together', 'or thrown away together:', 'a transaction.', '',
              'A column no two rows may share:', 'a primary key.', '',
              'A second writer of the same key', 'waits for the first: a lock.'],
        narration=(
            'The fix needs three words from the database, again in plain '
            'language first. A group of changes that are kept together, '
            'or thrown away together, is a transaction. Nothing in it is '
            'visible to anyone else until it is committed. [[slnc 250]] '
            'A column that no two rows may share is a primary key. '
            '[[slnc 250]] And when two writers try to write the same key '
            'at the same moment, the database makes the second one wait '
            'for the first to finish. That waiting is a lock.'
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
            'Act three is the pattern. Copy A writes each order\'s id into '
            'a table of handled messages, where the id is the primary key, '
            'and writes the email beside it, in one transaction. Then it '
            'crashes before moving the bookmark. [[slnc 250]] Copy B is '
            'handed the same three orders. For each one it tries to write '
            'the id, and Postgres says the id is already there. So copy B '
            'skips all three and queues none. [[slnc 250]] Six deliveries, '
            'three emails, three ids. The table outlived the copy that '
            'wrote it.'
        ),
    ),
    dict(
        key='08-diagram', kind='diagram', title='Where The Memory Lives',
        body=None,
        narration=(
            'Here is the whole arrangement in words. Kafka keeps the '
            'orders, and each group\'s bookmark. A copy of the service is '
            'handed orders starting from the bookmark. For each order, it '
            'opens one database transaction, writes the id first, then '
            'the email, and commits. Only after that commit does it ask '
            'Kafka to move the bookmark. [[slnc 300]] If it dies before '
            'the bookmark moves, the order goes out again, to another '
            'copy, and the id is waiting for it. The id and the email '
            'land together, or not at all.'
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
            'Act four moves the crash. First, the id is written after the '
            'email, as a second step. Copy A queues the email for order '
            'one, and dies before writing the id. One email, no id. Copy '
            'B is handed the order, finds no id, and queues the email '
            'again. Two emails for one order. [[slnc 300]] Now the id and '
            'the email go in one transaction, and copy A dies before the '
            'commit. Its connection drops, and Postgres throws the whole '
            'transaction away. No email, no id. Copy B handles the order '
            'properly: one email, one id. [[slnc 250]] Exactly once, from '
            'a broker that only promises at least once.'
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
            'commit. The copy opens a transaction and inserts the message '
            'id, asking Postgres to write nothing if the id is already '
            'there. Postgres answers with how many rows it wrote. One row '
            'means the order is new, so the email is queued in the same '
            'transaction. Zero rows means it was handled already. '
            '[[slnc 250]] Then the transaction commits, and only after '
            'that does the copy ask Kafka to move the bookmark.'
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
            'Act five is something the plain-Java version could never '
            'show. Kafka gives every copy a patience limit: how long it '
            'may go without asking for more orders before Kafka decides '
            'it is stuck. Kafka calls it max poll interval, and its '
            'default is five minutes. Here it is three seconds. '
            '[[slnc 300]] Copy A is handed order one, writes the id and '
            'the email, and is slow to commit. After three seconds, Kafka '
            'hands the same order to copy B. Now two copies are working on '
            'one order. [[slnc 250]] Copy B tries to write the same id, '
            'and Postgres makes it wait, on copy A\'s lock. Copy A '
            'commits. Postgres tells copy B the id is taken, and copy B '
            'skips it. One email. [[slnc 250]] Then copy A asks Kafka to '
            'move the bookmark, and Kafka refuses. Copy A no longer owns '
            'that order. A check done in Java would have let both copies '
            'through. Only the primary key could decide.'
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
            'Act six is the bill. The table cannot keep every id for '
            'ever, so a cleanup job deletes old ones. Three orders placed '
            'two days ago are handled, and their three ids stored. The '
            'cleanup keeps ids for twenty four hours, and deletes all '
            'three. [[slnc 250]] But a topic keeps its orders for a set '
            'time too, and this one keeps them for one hundred and sixty '
            'eight hours: seven days, Kafka\'s default. An operator moves '
            'the group\'s bookmark back to the start, to replay it. Three '
            'orders are handed out again, and with their ids gone, three '
            'more emails are queued. Six in all. [[slnc 300]] So keep the '
            'ids at least as long as Kafka keeps the orders. And there '
            'are two more systems to run: two containers, a broker and a '
            'database, for one email per order.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['The plain-Java version got the', 'whole pattern right.', '',
              'It left out: the repeat goes to a', 'different copy, with no mark on it.', '',
              'Two copies can hold the same', 'order at the same time.', '',
              "Kafka's retention sets the", "cleanup window's floor."],
        narration=(
            'How does this compare with the plain-Java version earlier in '
            'the course? It got the whole pattern right. The list in '
            'memory that loses at a restart, the crash between the work '
            'and the id, and the single transaction that fixes both all '
            'hold here. [[slnc 250]] What it left out is what Kafka adds. '
            'The repeat goes to a different copy, with no mark on it. Two '
            'copies can hold the same order at the same moment. And the '
            'cleanup window is no longer a free guess: the topic\'s '
            'retention sets its floor.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Assume every message comes twice,', 'to a different copy.', '',
              'The id is the primary key, in the', 'same database as the work.', '',
              'Write the id first, in the same', 'transaction as the work.', '',
              'Commit the transaction, then', 'the offset.'],
        narration=(
            'The verdict. Behind Kafka, assume every message will be '
            'handed out twice, and to a different copy. Keep the ids in a '
            'table in the same database as the work, with the id as the '
            'primary key. [[slnc 250]] Write the id first, inside the same '
            'transaction as the work, and let the database\'s answer '
            'decide whether to go on. Commit the transaction, and only '
            'then move the bookmark. And keep the ids at least as long as '
            'the topic keeps the messages.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real Here',
        body=['Kafka 4.3.1 and Postgres 18.6,', 'each in a container the demo', 'starts and stops.', '',
              'kafka-clients 4.3.1, the Postgres', 'driver 42.7.13, Testcontainers 2.0.5.', '',
              'Every number comes from the', "program's own output.", '',
              'If the work is safe to repeat,', 'skip the table.'],
        narration=(
            'What is real here? The broker is Kafka, version four point '
            'three point one, and the database is Postgres, version '
            'eighteen point six, both the newest releases, each in a '
            'container that the demo starts at the beginning and stops at '
            'the end. The one thing you need is a container runtime, such '
            'as Docker Desktop, switched on before you start. [[slnc 250]] '
            'Every number in this video comes from the program\'s own '
            'output, and two runs print the same thing. [[slnc 250]] And '
            'when is this too much? If the work is naturally safe to '
            'repeat, such as setting an order\'s status to shipped, there '
            'is nothing to deduplicate, and no table is needed.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Idempotent Consumer with Kafka. [[slnc 250]] If you "
            'take one sentence away, take this one: Kafka will hand the '
            'same order to two copies, one after a crash or both at once, '
            'and only an id written in the same transaction as the work '
            'sees both of them. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository. [[slnc 300]] If you try one exercise, remove '
            'the primary key from the table of handled ids, run act five, '
            'and count the emails. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
