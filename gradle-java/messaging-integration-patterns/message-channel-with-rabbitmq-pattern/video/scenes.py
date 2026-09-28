"""Scene definitions for the Message Channel with RabbitMQ teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of the broker's words in plain
language before using RabbitMQ's name for it, and never points at a picture the
listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Message Channel with RabbitMQ',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Message Channel pattern, in Java, using a real message '
            'broker called RabbitMQ. [[slnc 300]] This video is presented '
            'by Jayasekhar Konduru. [[slnc 600]] First, a simple '
            'definition. [[slnc 300]] A message channel is a named place '
            'that one system puts messages into, and another system takes '
            'them out of. [[slnc 300]] Because the messages wait in '
            'between, the two systems do not need to be running at the '
            'same moment. [[slnc 600]] In our online store, the shop '
            'takes orders, and the warehouse picks them off the shelf. '
            '[[slnc 300]] So the shop drops a pick order into a channel, '
            'and goes straight back to selling. [[slnc 300]] And the '
            'warehouse takes the order out whenever it is ready. [[slnc '
            '500]] By the end, you will hear a broker hold orders for a '
            'warehouse that is not even running. [[slnc 300]] Hand an '
            'order out again, when a picker crashes. [[slnc 300]] Share '
            'orders between a slow picker and a fast one. [[slnc 300]] '
            'And come back from its own restart, with some orders kept, '
            'and others gone.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The shop takes orders.', 'The warehouse picks them.', '',
              'Two systems, two teams.', 'Not always up at the same time.', '',
              'The partner project put a queue', 'between them, inside one program.', '',
              'This time the queue is its own', 'program, with its own restart.'],
        narration=(
            'Here is the scenario. [[slnc 400]] The shop takes orders, '
            'and the warehouse picks them. [[slnc 300]] They are two '
            'separate systems, run by two separate teams. [[slnc 300]] '
            'And they are not always running at the same time. [[slnc '
            '500]] The warehouse goes down for maintenance, restarts '
            'after an update, and sometimes crashes in the middle of an '
            'order. [[slnc 500]] The hand-built partner video put a queue '
            'between them, inside one program. [[slnc 300]] This time, '
            'the queue lives in a program of its own, with its own '
            'restarts. [[slnc 300]] And that changes three things.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='Checkout Calls The Warehouse',
        body="""ONE. Checkout calls the warehouse.
  the warehouse is down for maintenance.

  orders placed: 3.
  checkouts that failed: 3.

  selling did not need the warehouse
  to answer yet.""",
        narration=(
            'First, with no channel at all. [[slnc 400]] The warehouse is '
            'down for maintenance. [[slnc 300]] Checkout calls it '
            'directly, three times. [[slnc 300]] And all three checkouts '
            'fail. [[slnc 500]] The shop cannot sell while another system '
            'is away. [[slnc 300]] Even though the customer only needed '
            'to hear that the order was placed.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="The Broker's Words",
        body=['A broker is a program that holds', 'messages for other programs.', '',
              'A queue is its shelf: a named place', 'where messages wait, in order.', '',
              'An exchange is its counter: it', 'decides which shelf a message', 'goes on.', '',
              'Here the queue is the channel.'],
        narration=(
            'A real broker brings a few words with it. [[slnc 300]] Each '
            'one is simpler than it sounds. [[slnc 500]] Think of a post '
            'office. [[slnc 300]] You hand a parcel over the counter, and '
            'walk away. [[slnc 300]] The post office keeps it on a shelf, '
            'until the person it is for collects it. [[slnc 500]] The '
            'post office is the broker: a separate program whose job is '
            'to hold messages for other programs. [[slnc 300]] In this '
            'video, the broker is RabbitMQ. [[slnc 500]] The shelf is '
            'called a queue: a named place where messages wait, in the '
            'order they arrived. [[slnc 300]] In this pattern, the queue '
            'is the channel. [[slnc 500]] And the counter is called an '
            'exchange. [[slnc 300]] It decides which shelf a message goes '
            'on. [[slnc 300]] Here we only use the simplest one, which '
            'puts a message on the queue it is addressed to.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='A Real Channel Between Them',
        body="""TWO. A real channel between them.
  RabbitMQ is running in a container.

  checkout sends 3 pick orders
  and carries on.

  the warehouse takes each once:
  ORD-1, ORD-2, ORD-3.
  left waiting: 0.""",
        narration=(
            'Second demo: a real channel. [[slnc 400]] The demo starts a '
            'RabbitMQ broker, in a container that it switches on and off '
            'by itself. [[slnc 500]] Checkout sends three pick orders to '
            'a queue. [[slnc 300]] And carries on, without waiting for '
            'anyone. [[slnc 500]] The warehouse is listening. [[slnc '
            '300]] It is handed each order once: order one, order two, '
            'order three. [[slnc 300]] When it has finished, nothing is '
            'left waiting.'
        ),
    ),
    dict(
        key='06-three', kind='console', title='Nobody Is Listening Yet',
        body="""THREE. Nobody is listening yet.
  the warehouse is not running.
  no receiver exists anywhere.

  checkout sends 3, and none fail.
  the broker is holding: 3.

  the warehouse starts afterwards:
  ORD-1, ORD-2, ORD-3, in order.""",
        narration=(
            'Third demo, and this is something the hand-built version '
            'could never show. [[slnc 400]] The warehouse is not running '
            'at all. [[slnc 300]] There is no receiver anywhere. [[slnc '
            '500]] Checkout sends three orders, and none of them fail. '
            '[[slnc 300]] Because checkout is only talking to the broker. '
            '[[slnc 300]] The broker holds all three. [[slnc 500]] Some '
            'time later, the warehouse starts up. [[slnc 300]] And it is '
            'handed the waiting orders, in order: one, two, three. [[slnc '
            '500]] In the hand-built version, the channel lived inside '
            'the sender. [[slnc 300]] So a receiver could be away, but '
            'could never simply not exist yet.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='Where The Message Lives',
        body=None,
        narration=(
            'Here is the whole picture, in words. [[slnc 400]] There are '
            'now three programs, not one. [[slnc 300]] The shop, which '
            'sends and carries on. [[slnc 300]] The broker, which holds '
            'the queue. [[slnc 300]] And the warehouse, which takes an '
            'order, picks it, and then says it is done. [[slnc 500]] '
            'Inside the broker, there is one more place a message can be: '
            'its disk. [[slnc 300]] Only messages marked to be saved go '
            'there. [[slnc 500]] And the rule that holds it all together '
            'is this. [[slnc 300]] The broker only forgets an order when '
            'the warehouse says it is done with it.'
        ),
    ),
    dict(
        key='08-four', kind='console', title='Saying Done',
        body="""FOUR. Saying done.
  a picker takes ORD-1 and crashes
  before saying it is done.
  the broker puts it back.
  waiting again: 1.

  a second picker gets the same ORD-1,
  marked as seen before: true.
  deliveries: 2, orders picked: 1,
  waiting: 0.""",
        narration=(
            'Fourth demo: saying done. [[slnc 400]] A good post office '
            'only hands over a parcel when it is signed for. [[slnc 300]] '
            "Until then, it is still the post office's parcel. [[slnc "
            '300]] In RabbitMQ, that signature is called an '
            'acknowledgement. [[slnc 300]] It is the receiver telling the '
            'broker that it has finished with a message. [[slnc 600]] A '
            'picker takes order one, and crashes before saying it is '
            'done. [[slnc 300]] The broker kept its own copy, so it puts '
            'the order back. [[slnc 300]] One order is waiting again. '
            '[[slnc 500]] A second picker is handed that same order. '
            '[[slnc 300]] And the broker marks it as seen before, so the '
            'picker knows it might be a repeat. [[slnc 300]] This picker '
            'says done, and only then does the broker forget it. [[slnc '
            '500]] No order was lost. [[slnc 300]] The price is that a '
            'receiver can see the same order twice, and must be written '
            'to cope with that.'
        ),
    ),
    dict(
        key='09-shared', kind='console', title='Two Pickers, One Queue',
        body="""  two pickers share one channel,
  one slow and one fast.
  checkout sends 10 orders.

  no limit on unfinished orders:
  slow picker 5, fast picker 5.
  the fast one stands idle.

  a limit of 1 unfinished order each:
  the fast picker took most of them.""",
        narration=(
            'Now, two pickers share one queue. [[slnc 400]] One is slow, '
            'because its shelves are at the far end of the building. '
            '[[slnc 300]] The other is fast. [[slnc 300]] Checkout sends '
            'ten orders. [[slnc 500]] The broker has a setting for how '
            'many unfinished orders it will give one picker, before '
            'waiting for it to say done. [[slnc 300]] It is called '
            'prefetch. [[slnc 300]] And by default, there is no limit. '
            '[[slnc 500]] With no limit, the broker hands out all ten at '
            'once, taking turns. [[slnc 300]] Five go to the slow picker, '
            'and five to the fast one. [[slnc 300]] The fast one finishes '
            'quickly, then stands idle, while the slow one works through '
            'its pile. [[slnc 500]] With a limit of one, the broker waits '
            'for each picker to say done, before giving it the next '
            'order. [[slnc 300]] So the fast picker keeps coming back for '
            'more. [[slnc 300]] And it takes most of the orders.'
        ),
    ),
    dict(
        key='10-five', kind='console', title='Written To Disk, Or Not',
        body="""FIVE. Written to disk, or only memory.
  two channels hold 3 orders each.
  one: written to disk.
  one: held in memory only.

  the broker is stopped and started.
  written to disk: 3 still waiting.
  held in memory only: 0.""",
        narration=(
            'Fifth demo: the broker restarts. [[slnc 400]] There are two '
            'queues, and the broker has been told to keep both queues '
            'across a restart. [[slnc 300]] Each queue gets the same '
            'three orders. [[slnc 500]] The only difference is a mark on '
            "each message. [[slnc 300]] One queue's messages are marked "
            "to be saved to disk. [[slnc 300]] The other's are only held "
            'in memory. [[slnc 500]] Then the broker is stopped, and '
            'started again. [[slnc 300]] Both queues come back. [[slnc '
            '300]] The first still holds three orders. [[slnc 300]] The '
            'second holds none. [[slnc 600]] That is the surprise in this '
            'project. [[slnc 300]] Keeping an order safe takes two '
            'settings, not one. [[slnc 300]] And a queue that came back '
            'empty looks, from outside, exactly like a quiet day.'
        ),
    ),
    dict(
        key='11-settings', kind='code', title='Two Settings, Not One',
        body="""// the queue is written down
queueDeclare(name, true, ...);

// this message is written down too
basicPublish("", name,
    PERSISTENT_TEXT_PLAIN, body);

// this one lives in memory only
basicPublish("", name,
    TEXT_PLAIN, body);""",
        narration=(
            'In the code, the difference is small enough to miss. [[slnc '
            '400]] When the queue is created, one setting says whether '
            'the queue itself survives a restart. [[slnc 500]] Then, on '
            'every single send, a second setting says whether that '
            'message is saved to disk as well. [[slnc 500]] The two sends '
            'in the last demo differ in one argument, and nothing else. '
            '[[slnc 300]] A restart is the only moment you find out which '
            'one you wrote.'
        ),
    ),
    dict(
        key='12-six', kind='console', title='The Bill',
        body="""SIX. The bill.
  room for 5, given 8:
  5 accepted, 3 refused.

  the sender learns only that the
  broker took the message.

  1 container for 1 shop
  and 1 warehouse.""",
        narration=(
            'Finally, the costs. [[slnc 400]] A RabbitMQ queue has no '
            'size limit, unless you give it one. [[slnc 300]] And when '
            'you do, by default it makes room by quietly throwing away '
            'the oldest message. [[slnc 500]] So this queue is given room '
            'for five, and told to refuse new messages instead. [[slnc '
            '300]] And checkout asks the broker for a receipt on every '
            'send. [[slnc 300]] This is called a publisher confirm. '
            '[[slnc 500]] Eight orders are sent. [[slnc 300]] Five are '
            'accepted, and three are refused. [[slnc 300]] And checkout '
            'hears about every refusal. [[slnc 300]] Without the '
            'receipts, those three would have simply vanished. [[slnc '
            '600]] Two more costs remain. [[slnc 300]] The shop only '
            'learns that the broker took an order, never whether the '
            'warehouse picked it. [[slnc 300]] And the broker is a third '
            'system to run, secure, update, and watch.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the shape right: send and', 'carry on, each order once, in order,',
              'a limit, and no news of the work.', '',
              'It left out three things.', '',
              'A receiver that does not exist yet.', 'A message handed out, not finished.',
              'A restart, and what it keeps.'],
        narration=(
            'The hand-built partner video got the main shape right. '
            '[[slnc 400]] The sender puts a message in, and carries on. '
            '[[slnc 300]] The receiver takes each one once, in order. '
            '[[slnc 300]] A channel needs a limit. [[slnc 300]] And the '
            'sender hears nothing about the work itself. [[slnc 300]] All '
            'of that is true on RabbitMQ too. [[slnc 600]] But it left '
            'out three things, and they are why this video exists. [[slnc '
            '400]] A receiver that does not exist yet. [[slnc 300]] A '
            'message that has been handed out, but not finished. [[slnc '
            '300]] And a restart of the channel itself, and what it '
            'keeps.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Use a channel when two systems', 'live on different schedules.', '',
              'Then say three things out loud:', '',
              '1. Write down the queue', '   and every message.',
              '2. Say done after the work,', '   and cope with a repeat.',
              '3. Give it a limit, and', '   ask for receipts.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a channel when two '
            'systems live on different schedules. [[slnc 500]] Then, on a '
            'real broker, settle three things, because the broker will '
            'not assume any of them. [[slnc 500]] One. [[slnc 200]] Save '
            'the queue, and save every message, if a restart must not '
            'lose orders. [[slnc 400]] Two. [[slnc 200]] Only say done '
            'after the work is finished. [[slnc 300]] And make the '
            'receiver safe against seeing the same order twice. [[slnc '
            '400]] Three. [[slnc 200]] Give the queue a limit, choose '
            'what happens when it is reached, and ask for receipts.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['RabbitMQ 4.3.6, Java client 5.36.0,', 'Testcontainers 2.0.5, in a container',
              'the demo starts and stops itself.', '',
              'Too much if both systems are always', 'up and the caller needs the answer',
              'now, or if losing a waiting order', 'on a restart is fine.', '',
              'A broker is a third system to run.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'broker is RabbitMQ, version four point three point six, the '
            'newest release. [[slnc 300]] It runs in a container that the '
            'demo starts and stops by itself. [[slnc 300]] Nothing is '
            'installed, and nothing is left running. [[slnc 300]] You '
            'just need Docker switched on first. [[slnc 500]] Every '
            "number you heard comes from the program's own output. [[slnc "
            '600]] So, when is this too much? [[slnc 300]] If both '
            'systems are always running, and the caller needs the answer '
            'now, a direct call is simpler. [[slnc 300]] If losing a '
            'waiting order in a restart is acceptable, a queue inside the '
            'program costs nothing to run. [[slnc 500]] A broker earns '
            'its place only when the sender and receiver truly live on '
            'different schedules.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's the Message Channel, with RabbitMQ. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] A '
            'broker only forgets an order when the receiver says it is '
            'done, and only keeps it through a restart if both the queue '
            'and the message were saved. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Change the restart demo so both queues '
            'keep their orders in memory only. [[slnc 300]] Guess both '
            'numbers, and then run it. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
