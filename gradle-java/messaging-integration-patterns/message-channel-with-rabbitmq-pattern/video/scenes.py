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
            'Hello, and welcome. This video explains the Message Channel '
            'pattern in Java, using a real message broker called RabbitMQ. '
            '[[slnc 250]] It is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] Here is the plain definition, in '
            'general words. A message channel is a named place that one '
            'system puts messages into, and another system takes them out '
            'of. Because the messages wait in between, neither system has '
            'to be running at the same moment as the other. [[slnc 350]] '
            'Now the same thing in our online store. The shop takes '
            'orders, and the warehouse picks them off the shelf. They are '
            'two separate systems. So the shop drops a pick order into a '
            'channel and goes straight back to selling, and the warehouse '
            'takes the order out whenever it is ready. [[slnc 300]] By '
            'the end you will have seen a broker hold orders for a '
            'warehouse that is not even running, hand an order out again '
            'when a picker crashes, and come back from its own restart '
            'with some orders kept and others gone.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The shop takes orders.', 'The warehouse picks them.', '',
              'Two systems, two teams.', 'Not always up at the same time.', '',
              'The partner project put a queue', 'between them, inside one program.', '',
              'This time the queue is its own', 'program, with its own restart.'],
        narration=(
            'Here is the scenario. The shop takes orders, and the '
            'warehouse picks them. They are two separate systems, run by '
            'two separate teams, and they are not always up at the same '
            'time. The warehouse goes down for maintenance, restarts after '
            'an update, and sometimes crashes half way through an order. '
            '[[slnc 300]] The hand-built partner project already put a '
            'queue between them, but that queue lived inside the same '
            'program as the shop and the warehouse. This time the queue '
            'lives in a program of its own, which has its own restarts, '
            'and that changes three things.'
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
            'First, the version without a channel. The warehouse system is '
            'down for maintenance. Checkout calls it directly, three '
            'times, and all three checkouts fail. [[slnc 250]] That is a '
            'shop that cannot sell while another system is away, even '
            'though selling did not need the warehouse to answer yet. The '
            'customer only needed to be told the order was placed.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="The Broker's Words",
        body=['A broker is a program that holds', 'messages for other programs.', '',
              'A queue is its shelf: a named place', 'where messages wait, in order.', '',
              'An exchange is its counter: it', 'decides which shelf a message', 'goes on.', '',
              'Here the queue is the channel.'],
        narration=(
            'A real broker brings a few words with it, and each one is '
            'simpler than it sounds. Think of a post office. You hand a '
            'parcel over the counter and walk away, and the post office '
            'keeps it on a shelf until the person it is for comes to '
            'collect it. [[slnc 250]] The post office is the broker: a '
            'separate program whose whole job is to hold messages for '
            'other programs. RabbitMQ is the broker in this video. '
            '[[slnc 250]] The shelf is what RabbitMQ calls a queue: a '
            'named place where messages wait, in the order they arrived. '
            'In this pattern, the queue is the channel. [[slnc 250]] And '
            'the counter is what RabbitMQ calls an exchange: the part '
            'that decides which shelf a message goes on. We only use the '
            'simplest one, which puts a message on the queue it is '
            'addressed to, so it never has a real decision to make.'
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
            'Second, a real channel. The demo starts a RabbitMQ broker in '
            'a container, a small sealed box the demo switches on and off '
            'itself. Checkout sends three pick orders to a queue and '
            'carries on without waiting for anyone. [[slnc 250]] The '
            'warehouse is listening, and it is handed each order once: '
            'order one, order two, order three. When it has finished, '
            'nothing is left waiting.'
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
            'Third, and this is the act the partner project could never '
            'stage. The warehouse is not running at all. There is no '
            'receiver anywhere. Checkout sends three orders, and none of '
            'them fail, because checkout is only talking to the broker. '
            '[[slnc 250]] The broker is holding all three. Some time '
            'later the warehouse starts up, and it is handed the backlog '
            'in the order it went in: one, two, three. [[slnc 250]] In '
            'the partner project the channel lived inside the sender, so '
            'the receiver could be away, but it could never simply not '
            'exist yet.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='Where The Message Lives',
        body=None,
        narration=(
            'Here is the whole picture in words. There are three '
            'programs now, not one. The shop, which sends and carries on. '
            'The broker, which holds the queue. And the warehouse, which '
            'takes an order, picks it, and then says it is done. '
            '[[slnc 250]] Inside the broker there is one more place a '
            'message can be: its disk. Only messages marked to be written '
            'down go there. [[slnc 250]] The rule that holds the whole '
            'thing together is this. The broker forgets an order only '
            'when the warehouse says it is done with it.'
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
            'Fourth, saying done. Back to the post office: a good one '
            'hands a parcel over only when it is signed for, so an '
            'unsigned parcel is still the post office\'s parcel. The '
            'signature is what RabbitMQ calls an acknowledgement: the '
            'receiver telling the broker it has finished with a message. '
            '[[slnc 300]] A picker takes order one, and crashes before it '
            'says it is done. The broker had kept its own copy, so it '
            'puts the order back, and one order is waiting again. '
            '[[slnc 250]] A second picker is handed the same order one, '
            'and the broker marks it as seen before, so the picker can '
            'tell it might be a repeat. This picker says done, and only '
            'then does the broker forget it. Two deliveries, one order '
            'picked, nothing waiting. [[slnc 250]] No order was lost. The '
            'price is that a receiver can see the same order twice, and '
            'has to be written to cope with that.'
        ),
    ),
    dict(
        key='09-five', kind='console', title='Written To Disk, Or Not',
        body="""FIVE. Written to disk, or only memory.
  two channels hold 3 orders each.
  one: written to disk.
  one: held in memory only.

  the broker is stopped and started.
  written to disk: 3 still waiting.
  held in memory only: 0.""",
        narration=(
            'Fifth, the broker restarts. Two queues, and the broker has '
            'been told to keep both queues across a restart. RabbitMQ '
            'calls a queue like that durable. Each queue is given the '
            'same three orders. The only difference is a mark on each '
            'message. One queue\'s messages are marked to be written to '
            'disk, which RabbitMQ calls persistent. The other\'s are held '
            'in memory only. [[slnc 300]] Then the broker program is '
            'stopped and started again. Both queues come back. The first '
            'still holds three orders. The second holds none. '
            '[[slnc 300]] That is the surprise in this project. Keeping '
            'an order safe is two settings, not one. And a queue that '
            'came back empty looks, from the outside, exactly like a '
            'quiet day.'
        ),
    ),
    dict(
        key='10-settings', kind='code', title='Two Settings, Not One',
        body="""// the queue is written down
queueDeclare(name, true, ...);

// this message is written down too
basicPublish("", name,
    PERSISTENT_TEXT_PLAIN, body);

// this one lives in memory only
basicPublish("", name,
    TEXT_PLAIN, body);""",
        narration=(
            'In the code, the difference is small enough to miss. When '
            'the queue is created, one setting says whether the queue '
            'itself is written down. Then, on every single send, a '
            'second setting says whether that message is written down '
            'as well. [[slnc 250]] The two sends in the fifth act differ '
            'in one argument and nothing else. A restart is the only '
            'moment you find out which one you wrote.'
        ),
    ),
    dict(
        key='11-six', kind='console', title='The Bill',
        body="""SIX. The bill.
  room for 5, given 8:
  5 accepted, 3 refused.

  the sender learns only that the
  broker took the message.

  1 container for 1 shop
  and 1 warehouse.""",
        narration=(
            'Last, the bill. A RabbitMQ queue has no limit at all unless '
            'you give it one. And when you do give it one, its default is '
            'to make room by quietly throwing away the oldest message. '
            '[[slnc 250]] So this queue is given room for five, and told '
            'to refuse new messages instead. And checkout asks the broker '
            'for a receipt on every send, which RabbitMQ calls a '
            'publisher confirm. Eight orders are sent. Five are accepted '
            'and three refused, and checkout hears about every refusal. '
            'Without the receipts, those three would simply have '
            'vanished. [[slnc 300]] Two more costs do not go away. The '
            'shop now learns only that the broker took an order, never '
            'whether the warehouse picked it. And the broker is a third '
            'system to run, secure, upgrade and watch. Here, that is one '
            'container, for one shop and one warehouse.'
        ),
    ),
    dict(
        key='12-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the shape right: send and', 'carry on, each order once, in order,',
              'a limit, and no news of the work.', '',
              'It left out three things.', '',
              'A receiver that does not exist yet.', 'A message handed out, not finished.',
              'A restart, and what it keeps.'],
        narration=(
            'The hand-built partner project got the shape right. The '
            'sender puts a message in and carries on. The receiver takes '
            'each one once, in order. A channel needs a limit. And the '
            'sender hears nothing about the work itself. All of that is '
            'true on RabbitMQ, with the same numbers. [[slnc 300]] It '
            'left out three things, and they are the three this video is '
            'for. A receiver that does not exist yet, because the channel '
            'lived inside the sender. A message that has been handed out '
            'but is not finished, because taking it from a list removed '
            'it for good. And a restart of the channel itself, and the '
            'question of what it keeps.'
        ),
    ),
    dict(
        key='13-verdict', kind='bullets', title='The Verdict',
        body=['Use a channel when two systems', 'live on different schedules.', '',
              'Then say three things out loud:', '',
              '1. Write down the queue', '   and every message.',
              '2. Say done after the work,', '   and cope with a repeat.',
              '3. Give it a limit, and', '   ask for receipts.'],
        narration=(
            'Here is my verdict, plainly. Use a channel when two systems '
            'live on different schedules. Then, on a real broker, say '
            'three things out loud, because the broker will not assume '
            'any of them. [[slnc 250]] One. Write down the queue, and '
            'write down every message, if a restart must not lose '
            'orders. [[slnc 200]] Two. Say done only after the work is '
            'finished, and make the receiver safe against seeing the '
            'same order twice. [[slnc 200]] Three. Give the queue a '
            'limit, choose what happens at it, and ask for receipts, so '
            'the sender hears the answer.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['RabbitMQ 4.3.6, in a container', 'the demo starts and stops itself.', '',
              'The Java client 5.36.0, and', 'Testcontainers 2.0.5.', '',
              'Every number quoted comes from', "the program's own output, and",
              'two runs print the same thing.'],
        narration=(
            'What is real here? The broker is RabbitMQ, version four '
            'point three point six, the newest release, running in a '
            'container that the demo starts at the beginning and stops '
            'at the end. Nothing is installed and nothing is left '
            'running. The one thing you need is a container runtime, '
            'such as Docker Desktop, switched on before you start. '
            '[[slnc 250]] Every number quoted in this video comes from '
            'the program\'s own output, and two runs one after the other '
            'print exactly the same thing.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['If both systems are always up and', 'the caller needs the answer now,', 'call directly.', '',
              'If losing a waiting order on a', 'restart is fine, a queue inside', 'the program costs nothing.', '',
              'A broker is a third system to run.'],
        narration=(
            'So when is this too much? If both systems are always up '
            'together, and the caller needs the answer now, a direct call '
            'is simpler and tells you more. If losing a waiting order on '
            'a restart is acceptable, a queue inside the program, like '
            'the partner project\'s, costs nothing to run. [[slnc 250]] A '
            'broker is a third system to install, secure, upgrade and '
            'watch. It earns that only when the sender and the receiver '
            'genuinely live on different schedules.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Message Channel with RabbitMQ. [[slnc 250]] If you "
            'take one sentence away, take this one: a broker forgets an '
            'order only when the receiver says it is done, and keeps it '
            'through a restart only if both the queue and the message '
            'were written down. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository. [[slnc 300]] If you try one '
            'exercise, change the fifth act so both queues send their '
            'orders in memory only, guess both numbers, and then run it. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
