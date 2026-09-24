"""Scene definitions for the Transactional Outbox with Debezium teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of Postgres's, Debezium's and
Kafka's words in plain language before using the tool's name for it, and never
points at a picture the listener cannot see. Every figure is the output of
`./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Transactional Outbox with Debezium',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Transactional '
            'Outbox pattern in Java, using a real Postgres database, a real '
            'Kafka broker, and Debezium in between. [[slnc 250]] It is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] Here '
            'is the plain definition, in general words. When you have to '
            'save something and also tell others about it, do not do two '
            'separate things that can half happen. Save the message in '
            'your own database, beside the record, in the same single '
            'save, and let something else send it later. [[slnc 350]] Now '
            'the same thing in our online store. When a customer checks '
            'out, the Orders service saves the order, and the rest of the '
            'shop must hear that the order was placed. So the service saves '
            'the order and an order placed message together, and a tool '
            'called Debezium sends the message on. [[slnc 300]] By the end '
            'you will have seen an event sent for a row that was already '
            'deleted, a database keeping its log for a reader that was '
            'switched off, and the same event sent twice.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The Orders service saves each order', 'in its own Postgres database.', '',
              'Notifications, stock and shipping', 'hear about it through Kafka.', '',
              'Goal: every saved order announced,', 'nothing announced that was not saved,',
              "and each order's events in order."],
        narration=(
            'Here is the scenario. When a customer checks out, the Orders '
            'service saves the order in its own database. That database is '
            'Postgres. [[slnc 250]] The rest of the shop, notifications, '
            'stock and shipping, hears about new orders through a message '
            'broker. That broker is Kafka. [[slnc 300]] The shop wants '
            'three things. Every saved order is announced. Nothing is '
            'announced that was not saved. And each order\'s events, '
            'placed, paid and shipped, are heard in the order they '
            'happened.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='Two Writes, One Crash',
        body="""ONE. Two writes, one crash.
  save, then send.
  the process dies in between.
  ORD-1 in Postgres: yes.
  events in Kafka: 0.

  swap the lines: send, then save,
  and die in between.
  events in Kafka: 1.
  ORD-2 in Postgres: no.""",
        narration=(
            'Act one, the two lines everybody writes first. There is no '
            'outbox yet. The checkout saves the order in Postgres, and '
            'then sends the event to Kafka itself. [[slnc 250]] The '
            'process dies between the two. Order one is in Postgres. Kafka '
            'has no event. The customer is charged, and nobody is told. '
            '[[slnc 300]] So swap the two lines. Send first, then save, '
            'and die in between. Now Kafka has one event, and order two is '
            'not in Postgres. The shop has announced an order that does not '
            'exist. [[slnc 250]] Two systems, two steps, and no transaction '
            'that covers both.'
        ),
    ),
    dict(
        key='04-log-words', kind='bullets', title="Postgres's Words",
        body=['A journal of every change, written', 'before any table: the WAL.', '',
              'Readable from outside when started', 'with wal_level=logical.', '',
              'A bookmark kept for one reader:', 'a replication slot.', '',
              'Postgres keeps every page the', 'reader has not confirmed.'],
        narration=(
            'Before the fix, some words, in plain language first. Picture '
            'an office where every piece of paper that touches any desk is '
            'first copied into a journal, automatically, by the building. '
            '[[slnc 250]] Postgres has exactly that. Before it changes any '
            'table, it writes the change into a journal on disk, so that '
            'it can recover after a crash. Postgres calls it the write '
            'ahead log. [[slnc 250]] Normally only Postgres reads it. But '
            'start Postgres with one setting, wal level logical, and an '
            'outside program can read the changes back as rows. '
            '[[slnc 250]] That outside reader gets a bookmark in the '
            'journal, which Postgres calls a replication slot. And Postgres '
            'keeps every page of the journal that the reader has not yet '
            'confirmed.'
        ),
    ),
    dict(
        key='05-debezium-words', kind='bullets', title="Debezium's Words",
        body=['A reader of the journal that turns', 'each change into a message:',
              'change data capture. Debezium.', '',
              'One outbox row in, one event out:', 'the outbox event router.', '',
              'How far it has read, written down:', 'its offset.', '',
              'Here it runs inside our own program.'],
        narration=(
            'Debezium is that outside reader. It holds the bookmark, is '
            'sent every committed change, and turns each one into a '
            'message. This is called change data capture. [[slnc 250]] Its '
            'outbox event router takes each new row in the outbox table and '
            'makes one clean event out of it. The order id becomes the '
            'message key, and the row\'s id travels with the message as a '
            'label, which Kafka calls a header. [[slnc 250]] Debezium also '
            'writes down how far through the journal it has read, and '
            'calls that its offset. [[slnc 250]] Debezium usually runs in '
            'a program of its own. Here it runs inside the demo\'s own Java '
            'program, as a library, which Debezium calls the embedded '
            'engine. That saves a third container, and it reads the same '
            'journal in the same way.'
        ),
    ),
    dict(
        key='06-two', kind='console', title='One Transaction, And Debezium Sends',
        body="""TWO. One transaction, Debezium sends.
  wal_level logical. Debezium 3.6.3.Final.
  slot orders_outbox. slot active: yes.

  order and outbox row, one transaction.
  no Kafka code at all.
  orders: 3, outbox rows: 3.
  events in Kafka: 3.

  ORD-4: card declined, rolled back.
  events in Kafka: 4. events for ORD-4: 0.""",
        narration=(
            'Act two, the pattern. Postgres runs with wal level logical. '
            'Debezium, version three point six point three, runs inside '
            'the program and holds its bookmark, the replication slot. '
            '[[slnc 250]] The checkout now writes each order and a row in '
            'the outbox table, in one transaction, and commits. It has no '
            'Kafka code at all. Three orders, three outbox rows. Debezium '
            'reads the three commits from the journal and sends three '
            'events. [[slnc 300]] Then order four writes both rows, the '
            'card is declined, and the whole transaction is rolled back. '
            'Order five commits after it. Kafka now holds four events, and '
            'not one for order four. The journal only hands over work that '
            'was committed, so an order and its event live or die '
            'together.'
        ),
    ),
    dict(
        key='07-three', kind='console', title='The Log, Not The Table',
        body="""THREE. The log, not the table.
  each transaction writes the outbox
  row and deletes it again before
  committing.

  orders: 3.
  outbox rows: 0.
  events in Kafka: 3.

  a relay reading the table would find
  nothing. Debezium read the log.""",
        narration=(
            'Act three is the headline of this video. This time each '
            'transaction writes the outbox row, and then deletes it again, '
            'before it commits. [[slnc 250]] Three orders. The outbox table '
            'ends with no rows at all. And Kafka still receives three '
            'events. [[slnc 300]] Debezium never looked at the table. It '
            'read the inserts from the journal, where they were written '
            'before the delete. A relay that reads the table, like the one '
            'in the plain-Java version, would have found nothing to send. '
            'Debezium itself recommends this way of working, because the '
            'outbox table then never needs cleaning.'
        ),
    ),
    dict(
        key='08-diagram', kind='diagram', title='Where Each Piece Lives',
        body=None,
        narration=(
            'Here is where each piece lives, in words. The checkout writes '
            'to Postgres, and to nothing else. Postgres writes every change '
            'into its journal first, and keeps the journal for the slot. '
            'Debezium, inside the demo\'s program, is sent the committed '
            'outbox changes and forwards each one to Kafka, keyed by the '
            'order. [[slnc 300]] Only after Kafka accepts an event does '
            'Debezium write down how far it has read. That order of steps '
            'matters, and act five shows why.'
        ),
    ),
    dict(
        key='09-four', kind='console', title='Debezium Is Down',
        body="""FOUR. Debezium is down.
  Debezium is stopped.
  slot active: no.
  the checkout still takes 3 orders.
  orders: 3. events in Kafka: 0.

  log kept for the slot:
  grew while it was down. limit: -1.

  Debezium starts again and sends 3:
  ORD-1, ORD-2, ORD-3.""",
        narration=(
            'Act four. Debezium is stopped, so the bookmark has no reader. '
            'The checkout does not notice. It takes three orders, and '
            'Kafka receives nothing. [[slnc 250]] Meanwhile Postgres keeps '
            'every page of its journal that Debezium has not confirmed, '
            'and the amount it keeps for the slot grows. The setting that '
            'caps it is minus one, which means no cap at all. [[slnc 300]] '
            'Debezium starts again, carries on from its bookmark, and sends '
            'all three: orders one, two and three. Nothing was lost, and '
            'nobody wrote a retry. [[slnc 250]] Keep that minus one in '
            'mind. A Debezium that is switched off and forgotten makes '
            'Postgres keep its journal until the disk is full.'
        ),
    ),
    dict(
        key='10-code', kind='code', title='The Pattern In One Transaction',
        body="""c.setAutoCommit(false);
insert into orders
  values ('ORD-1', 'customer-1', 2995,
          'placed');
insert into outbox
  values ('ORD-1/OrderPlaced', 'order',
          'ORD-1', 'OrderPlaced', payload);
c.commit();

// no Kafka here. Debezium reads the log.""",
        narration=(
            'The whole pattern, on the checkout\'s side, is one '
            'transaction. Switch off automatic commits. Insert the order: '
            'order one, customer one, a total of two thousand nine hundred '
            'and ninety five pence, status placed. [[slnc 250]] Insert the '
            'outbox row: its id is order one, slash, order placed. Its '
            'type is order placed, and its payload is the order. Then '
            'commit, once, for both rows. [[slnc 300]] What matters most '
            'is what is missing. The checkout never opens a connection to '
            'Kafka. Debezium reads the committed rows from the journal.'
        ),
    ),
    dict(
        key='11-five', kind='console', title='Sent, But Not Written Down',
        body="""FIVE. Sent, but not written down.
  Debezium sends ORD-1 and ORD-2,
  then dies before writing down how
  far it has read.
  events in Kafka: 2. slot active: no.

  it starts again from the last place
  it wrote down, and sends both again.
  events in Kafka: 4 for 2 orders.

  ORD-1/OrderPlaced arrived 2 times,
  ORD-2/OrderPlaced arrived 2 times.""",
        narration=(
            'Act five. Debezium sends orders one and two to Kafka, and '
            'then dies, before writing down how far it has read. Kafka '
            'holds two events. [[slnc 250]] Debezium starts again, from '
            'the last place it wrote down. The slot still holds those two '
            'changes, because they were never confirmed, and hands them '
            'over again. Debezium sends both again. [[slnc 300]] Four '
            'events for two orders. Each pair carries the same event id. '
            'Delivery is at least once. It is the price of writing down '
            'after sending, and the alternative, writing down first, would '
            'risk losing an event for good. The unchanging id is what lets '
            'a reader throw the second copy away.'
        ),
    ),
    dict(
        key='12-six', kind='console', title='Order Per Key, And The Bill',
        body="""SIX. Order per key, and the bill.
  3 orders placed, paid and shipped.
  9 commits. order-events has 3 partitions.
  ORD-1: partition 1, placed, paid, shipped.
  ORD-2: partition 2, placed, paid, shipped.
  ORD-3: partition 2, placed, paid, shipped.

  the bill: 2 containers,
  wal_level logical, 1 replication slot.
  limit -1. slot exists now: no.""",
        narration=(
            'Act six. Three orders are placed, then paid, then shipped. '
            'Each step is its own transaction, and the orders take turns. '
            'Nine commits. [[slnc 250]] Kafka splits the topic into three '
            'lanes that are read side by side. It calls them partitions. '
            'The order id picks the lane, and order is kept within a lane, '
            'never across lanes. [[slnc 250]] Order one lands alone on '
            'partition one: placed, paid, shipped. Orders two and three '
            'share partition two, taking turns, and each keeps its own '
            'order. [[slnc 300]] Then the bill. Two containers. Postgres '
            'started with wal level logical. And one replication slot, '
            'with no limit on what it keeps, so retiring Debezium means '
            'dropping the slot. The demo drops it, and the slot is gone.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['The plain-Java version got the', 'whole pattern right.', '',
              'It left out: Debezium reads the log,', 'not the table.', '',
              'The slot keeps the log for its', 'reader, with no limit.', '',
              'Order is kept per key, and only', 'per key.'],
        narration=(
            'How does this compare with the plain-Java version earlier in '
            'the course? It got the whole pattern right. Both halves of '
            'the dual write failing, the message saved beside the order in '
            'one transaction, checkout carrying on while the sender is '
            'away, and the duplicate when the sender dies at the wrong '
            'moment. All of that holds here. [[slnc 250]] What it left out '
            'is what a real database log adds. Debezium reads the log, not '
            'the table, so a deleted row is still sent. The slot keeps the '
            'log for its reader, with no limit. A rolled back transaction '
            'never appears at all. And order is kept per key, and only per '
            'key.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Commit to one system only:', 'the order and its outbox row.', '',
              'Let change data capture carry', 'the message out, from the log.', '',
              'Key each event by its order.', '',
              'Watch the slot. Drop it when', 'Debezium is retired.', '',
              'Make every reader forgive a duplicate.'],
        narration=(
            'The verdict. Commit to one system only: the order and its '
            'outbox row, in one transaction. Let change data capture carry '
            'the message out, from the database\'s own log. [[slnc 250]] '
            'Key each event by its order, so that one order\'s events stay '
            'in order. [[slnc 250]] Watch the slot, and alert when it '
            'stops moving. Drop it when Debezium is retired. [[slnc 250]] '
            'And make every reader of the topic forgive a duplicate, by '
            'remembering the event ids it has already handled.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real Here',
        body=['Postgres 18.6 and Kafka 4.3.1, each', 'in a container the demo starts', 'and stops.', '',
              'Debezium 3.6.3.Final, embedded:', 'no third container.', '',
              'Every number comes from the', "program's own output.", '',
              'Cannot enable logical decoding?', 'Poll the table instead.'],
        narration=(
            'What is real here? The database is Postgres, version eighteen '
            'point six, and the broker is Kafka, version four point three '
            'point one, each in a container that the demo starts at the '
            'beginning and stops at the end. Debezium is version three '
            'point six point three, the newest general release, running '
            'inside the demo, so there is no third container. The one '
            'thing you need is a container runtime, such as Docker '
            'Desktop, switched on before you start. [[slnc 250]] Every '
            'number in this video comes from the program\'s own output, and '
            'two runs print the same thing. [[slnc 250]] And when is this '
            'too much? If you cannot start your database with logical '
            'decoding, a relay that polls the outbox table on a timer gives '
            'the same guarantee, at the price of a table to clean.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Transactional Outbox with Debezium. [[slnc 250]] If "
            'you take one sentence away, take this one: commit to your own '
            'database only, and let its log carry the message out, so an '
            'order and its event can never part, and the only price is an '
            'event that may arrive twice. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository. [[slnc 300]] If you try one exercise, '
            'crash Debezium after sending one event instead of two, and '
            'predict the counts before you run it. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
