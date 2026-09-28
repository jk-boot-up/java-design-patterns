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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Transactional Outbox pattern in Java, using a real Postgres '
            'database, a real Kafka broker, and a tool called Debezium in '
            'between. [[slnc 300]] This video is presented by Jayasekhar '
            'Konduru. [[slnc 600]] First, a simple definition. [[slnc '
            '300]] When you must save something, and also tell others '
            'about it, do not do two separate things that can half '
            'happen. [[slnc 300]] Save the message in your own database, '
            'beside the record, in one single save. [[slnc 300]] And let '
            'something else send it out later. [[slnc 600]] Think of an '
            'office out-tray. [[slnc 300]] You file your copy and drop '
            'the letter in the tray, in one action. [[slnc 300]] The post '
            'room sends it later. [[slnc 700]] In our online store, when '
            'a customer checks out, the orders service saves the order, '
            'and an order placed message, together. [[slnc 300]] And '
            'Debezium sends that message on. [[slnc 500]] By the end, you '
            'will hear a message sent for a row that was already deleted. '
            '[[slnc 300]] A database keeping its history for a reader '
            'that was switched off. [[slnc 300]] And the same message '
            'sent twice.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The Orders service saves each order', 'in its own Postgres database.', '',
              'Notifications, stock and shipping', 'hear about it through Kafka.', '',
              'Goal: every saved order announced,', 'nothing announced that was not saved,',
              "and each order's events in order."],
        narration=(
            'Here is the scenario. [[slnc 400]] When a customer checks '
            'out, the orders service saves the order in its own database. '
            '[[slnc 300]] That database is Postgres. [[slnc 500]] The '
            'rest of the shop, notifications, stock, and shipping, hears '
            'about new orders through a message broker. [[slnc 300]] That '
            'broker is Kafka. [[slnc 600]] The shop wants three things. '
            '[[slnc 300]] Every saved order is announced. [[slnc 300]] '
            'Nothing is announced that was not saved. [[slnc 300]] And '
            "each order's events, placed, paid, and shipped, are heard in "
            'the order they happened.'
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
            'First demo: two writes, and one crash. [[slnc 400]] There is '
            'no outbox yet. [[slnc 300]] Checkout saves the order in '
            'Postgres, and then sends the message to Kafka itself. [[slnc '
            '600]] The program dies between the two. [[slnc 300]] Order '
            'one is in Postgres. [[slnc 300]] Kafka has no message. '
            '[[slnc 300]] The customer is charged, and nobody is told. '
            '[[slnc 600]] So swap the two lines. [[slnc 300]] Send first, '
            'then save, and die in between. [[slnc 300]] Now Kafka has '
            'one message, and order two is not in Postgres. [[slnc 300]] '
            'The shop has announced an order that does not exist. [[slnc '
            '500]] Two systems, two steps, and no transaction that covers '
            'both.'
        ),
    ),
    dict(
        key='04-log-words', kind='bullets', title="Postgres's Words",
        body=['A journal of every change, written', 'before any table: the WAL.', '',
              'Readable from outside when started', 'with wal_level=logical.', '',
              'A bookmark kept for one reader:', 'a replication slot.', '',
              'Postgres keeps every page the', 'reader has not confirmed.'],
        narration=(
            'Before the fix, some words, in plain language. [[slnc 500]] '
            'Picture an office where every piece of paper is first copied '
            'into a journal, automatically. [[slnc 500]] Postgres has '
            'exactly that. [[slnc 300]] Before it changes any table, it '
            'writes the change into a journal on disk. [[slnc 300]] So it '
            'can recover after a crash. [[slnc 300]] Postgres calls it '
            'the write-ahead log. [[slnc 600]] Normally, only Postgres '
            'reads it. [[slnc 300]] But with one setting switched on, an '
            'outside program can read the changes too. [[slnc 600]] That '
            'outside reader gets a bookmark in the journal. [[slnc 300]] '
            'Postgres calls that bookmark a replication slot. [[slnc '
            '300]] And Postgres keeps every page of the journal that the '
            'reader has not yet confirmed.'
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
            'Debezium is that outside reader. [[slnc 300]] It holds the '
            'bookmark, receives every saved change, and turns each one '
            'into a message. [[slnc 300]] This is called change data '
            'capture. [[slnc 600]] One part of Debezium takes each new '
            'row in the outbox table, and turns it into one clean '
            "message. [[slnc 300]] The order I D becomes the message's "
            "key. [[slnc 300]] And the row's own I D travels with the "
            'message, as a label. [[slnc 600]] Debezium also writes down '
            'how far through the journal it has read. [[slnc 600]] '
            'Usually, Debezium runs as a program of its own. [[slnc 300]] '
            "Here, it runs inside the demo's own Java program. [[slnc "
            '300]] That saves a third container, and it reads the journal '
            'in exactly the same way.'
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
            'Second demo: one transaction, and Debezium sends. [[slnc '
            '400]] Postgres is started with its journal readable from '
            'outside. [[slnc 300]] Debezium, version three point six, '
            'runs inside the program, and holds its bookmark. [[slnc '
            '600]] Checkout now writes each order, and a row in the '
            'outbox table, in one transaction. [[slnc 300]] And it saves '
            'them together. [[slnc 300]] Checkout has no Kafka code at '
            'all. [[slnc 500]] Three orders, and three outbox rows. '
            '[[slnc 300]] Debezium reads the three saves from the '
            'journal, and sends three messages. [[slnc 600]] Then order '
            'four writes both rows. [[slnc 300]] But the card is '
            'declined, and the whole transaction is undone. [[slnc 300]] '
            'Order five saves after it. [[slnc 500]] Kafka now holds four '
            'messages, and not one for order four. [[slnc 300]] The '
            'journal only passes on work that was actually saved. [[slnc '
            '300]] So an order and its message live or die together.'
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
            'Third demo, and this is the headline of the video. [[slnc '
            '400]] This time, each transaction writes the outbox row. '
            '[[slnc 300]] And then deletes it again, before saving. '
            '[[slnc 600]] Three orders. [[slnc 300]] The outbox table '
            'ends up with no rows at all. [[slnc 300]] And Kafka still '
            'receives three messages. [[slnc 600]] Debezium never looked '
            'at the table. [[slnc 300]] It read the inserts from the '
            'journal, where they were written before the delete. [[slnc '
            '500]] A relay that reads the table, like the one in the '
            'plain Java version, would have found nothing to send. [[slnc '
            '300]] Debezium recommends working this way. [[slnc 300]] '
            'Because then the outbox table never needs cleaning.'
        ),
    ),
    dict(
        key='08-diagram', kind='diagram', title='Where Each Piece Lives',
        body=None,
        narration=(
            'Here is where each piece lives, in words. [[slnc 500]] '
            'Checkout writes to Postgres, and to nothing else. [[slnc '
            '300]] Postgres writes every change into its journal first. '
            '[[slnc 300]] And it keeps the journal for the bookmark. '
            '[[slnc 500]] Debezium receives the saved outbox changes. '
            '[[slnc 300]] And it forwards each one to Kafka, keyed by the '
            'order. [[slnc 600]] Only after Kafka accepts a message does '
            'Debezium write down how far it has read. [[slnc 300]] That '
            'order of steps matters, and the fifth demo shows why.'
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
            'Fourth demo: Debezium is down. [[slnc 400]] Debezium is '
            'stopped, so the bookmark has no reader. [[slnc 300]] '
            'Checkout does not notice. [[slnc 300]] It takes three '
            'orders, and Kafka receives nothing. [[slnc 600]] Meanwhile, '
            'Postgres keeps every page of the journal that Debezium has '
            'not confirmed. [[slnc 300]] And the amount it keeps keeps '
            'growing. [[slnc 300]] By default, there is no limit at all. '
            '[[slnc 600]] Debezium starts again, carries on from its '
            'bookmark, and sends all three orders. [[slnc 300]] Nothing '
            'was lost. [[slnc 300]] And nobody wrote any retry code. '
            '[[slnc 600]] But remember that missing limit. [[slnc 300]] '
            'If Debezium is switched off and forgotten, Postgres keeps '
            'its journal until the disk is full.'
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
            "On the checkout's side, the whole pattern is one "
            'transaction. [[slnc 500]] Switch off automatic saving. '
            '[[slnc 300]] Insert the order: order one, customer one, a '
            'total of twenty-nine pounds ninety-five, status placed. '
            '[[slnc 500]] Insert the outbox row. [[slnc 300]] Its type is '
            'order placed, and it carries the order. [[slnc 300]] Then '
            'save once, for both rows. [[slnc 600]] What matters most is '
            'what is missing. [[slnc 300]] Checkout never connects to '
            'Kafka. [[slnc 300]] Debezium reads the saved rows from the '
            'journal.'
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
            'Fifth demo: sent, but not written down. [[slnc 400]] '
            'Debezium sends orders one and two to Kafka. [[slnc 300]] '
            'Then it dies, before writing down how far it has read. '
            '[[slnc 300]] Kafka holds two messages. [[slnc 600]] Debezium '
            'starts again, from the last place it wrote down. [[slnc '
            '300]] The bookmark still holds those two changes, because '
            'they were never confirmed. [[slnc 300]] So Debezium sends '
            'both again. [[slnc 600]] Four messages, for two orders. '
            '[[slnc 300]] Each pair carries the same message I D. [[slnc '
            '500]] Delivery is at least once. [[slnc 300]] That is the '
            'price of writing down after sending. [[slnc 300]] Writing '
            'down first would risk losing a message forever. [[slnc 300]] '
            'And the unchanging I D is what lets a reader throw away the '
            'second copy.'
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
            'Sixth demo: ordering, and the bill. [[slnc 400]] Three '
            'orders are placed, then paid, then shipped. [[slnc 300]] '
            'Each step is its own transaction, and the orders take turns. '
            '[[slnc 300]] Nine saves in all. [[slnc 600]] Kafka splits '
            'the topic into three lanes, read side by side. [[slnc 300]] '
            'It calls them partitions. [[slnc 300]] The order I D picks '
            'the lane. [[slnc 300]] And order is kept within a lane, '
            'never across lanes. [[slnc 500]] Order one lands alone in '
            'one lane: placed, paid, shipped. [[slnc 300]] Orders two and '
            'three share another lane, taking turns. [[slnc 300]] And '
            'each keeps its own order. [[slnc 600]] Then the bill. [[slnc '
            '300]] Two containers. [[slnc 300]] Postgres started with its '
            'journal readable from outside. [[slnc 300]] And one '
            'bookmark, with no limit on how much it keeps. [[slnc 300]] '
            'So when Debezium is retired, the bookmark must be deleted '
            'too. [[slnc 300]] The demo deletes it.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['The plain-Java version got the', 'whole pattern right.', '',
              'It left out: Debezium reads the log,', 'not the table.', '',
              'The slot keeps the log for its', 'reader, with no limit.', '',
              'Order is kept per key, and only', 'per key.'],
        narration=(
            'How does this compare with the plain Java version? [[slnc '
            '400]] It got the whole pattern right. [[slnc 300]] Both ways '
            'the two separate writes can fail. [[slnc 300]] The message '
            'saved beside the order, in one transaction. [[slnc 300]] '
            'Checkout carrying on while the sender is away. [[slnc 300]] '
            'And the duplicate when the sender dies at the wrong moment. '
            '[[slnc 300]] All of that holds here. [[slnc 600]] What it '
            'left out is what a real database journal adds. [[slnc 500]] '
            'Debezium reads the journal, not the table. [[slnc 300]] So a '
            'deleted row is still sent. [[slnc 300]] The bookmark keeps '
            'the journal for its reader, with no limit. [[slnc 300]] An '
            'undone transaction never appears at all. [[slnc 300]] And '
            'order is kept per key, and only per key.'
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
            'So, here is the verdict. [[slnc 400]] Save to one system '
            'only: the order, and its outbox row, in one transaction. '
            '[[slnc 300]] Let change data capture carry the message out, '
            "from the database's own journal. [[slnc 500]] Key each "
            "message by its order, so one order's messages stay in order. "
            '[[slnc 500]] Watch the bookmark, and raise an alert when it '
            'stops moving. [[slnc 300]] Delete it when Debezium is '
            'retired. [[slnc 500]] And make every reader forgive a '
            'duplicate, by remembering the message I Ds it has already '
            'handled.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real Here',
        body=['Postgres 18.6 and Kafka 4.3.1, each', 'in a container the demo starts', 'and stops.', '',
              'Debezium 3.6.3.Final, embedded:', 'no third container.', '',
              'Every number comes from the', "program's own output.", '',
              'Cannot enable logical decoding?', 'Poll the table instead.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'database is Postgres, version eighteen point six. [[slnc '
            '300]] The broker is Kafka, version four point three point '
            'one. [[slnc 300]] Each runs in a container that the demo '
            'starts and stops by itself. [[slnc 300]] Debezium is version '
            'three point six point three, running inside the demo. [[slnc '
            '300]] You just need Docker switched on first. [[slnc 300]] '
            "Every number you heard comes from the program's own output. "
            '[[slnc 600]] So, when is this too much? [[slnc 300]] If you '
            "cannot make your database's journal readable from outside, "
            'use a relay that checks the outbox table on a timer instead. '
            '[[slnc 300]] It gives the same guarantee, at the price of a '
            'table to clean.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Transactional Outbox, with Debezium. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] '
            'Save to your own database only, and let its journal carry '
            'the message out, so an order and its message can never be '
            'separated, and the only price is a message that may arrive '
            'twice. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Crash Debezium after sending one message, instead of '
            'two. [[slnc 300]] Guess the counts first, and then run it. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
