"""Scene definitions for the Publisher-Subscriber with Redis teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of Redis's words in plain
language before using Redis's name for it, and never points at a picture the
listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Publisher-Subscriber with Redis',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Publisher '
            'Subscriber pattern in Java, using a real server called Redis. '
            '[[slnc 250]] It is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] Here is the plain definition, in '
            'general words. One part of a system announces that something '
            'happened, once, to a named place. Any number of other parts '
            'can listen at that place. The one announcing never learns who '
            'they are. [[slnc 350]] Now the same thing in our online '
            'store. When an order is placed, the order service announces '
            'it once. Inventory, email, analytics and loyalty points each '
            'hear it and do their own work, and the order service does '
            'not have to know any of them by name. [[slnc 300]] By the '
            'end you will have seen Redis copy one order to a program '
            'running in a different process, tell the publisher how many '
            'heard it, keep nothing for a listener that arrives late, and '
            'cut off a listener that falls too far behind.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order is placed.', 'Several services care:',
              'inventory, email, analytics, loyalty.', '',
              'The partner project built the topic', 'inside one Java program.', '',
              'This time the topic lives in Redis,', 'a separate program, and every',
              'listener has its own connection.'],
        narration=(
            'Here is the scenario. An order is placed, and several '
            'services care about it. Inventory reserves the stock. Email '
            'sends the confirmation. Analytics counts the sale. Loyalty '
            'adds points. [[slnc 300]] The hand-built partner project in '
            'this course already built this, with the topic as an object '
            'inside one Java program. This time the topic lives in Redis, '
            'a separate program, and every listener reaches it over a '
            'network connection of its own. That changes more than you '
            'might expect.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='The Order Service Calls Each One',
        body="""ONE. The order service calls each one.
  inventory [ORD-1], email [ORD-1],
  analytics [ORD-1].

  the order service knows 3 services
  by name. a fourth, loyalty points,
  means editing it.""",
        narration=(
            'First, the version without the pattern. The order service '
            'calls inventory, then email, then analytics, each by name, '
            'and each one handles order one. [[slnc 250]] It works. But '
            'the order service now knows three services by name. When a '
            'fourth one, loyalty points, wants to hear about orders, '
            'somebody has to edit the order service to add it.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="Redis's Words",
        body=['Publish: announce a message', 'under a name, once.', '',
              'Channel: the name it goes out under,', 'here orders.placed.', '',
              'Subscribe: ask Redis to send you', 'everything on a name, from now on.', '',
              'Redis keeps no copy. Like live radio.'],
        narration=(
            'Redis brings a few words with it, and each one is simpler '
            'than it sounds. Think of a live radio station. The presenter '
            'speaks once, and every radio tuned in at that moment hears '
            'it. [[slnc 250]] Announcing a message once is what Redis '
            'calls publishing. [[slnc 200]] The frequency it goes out on '
            'is what Redis calls a channel. It is just a name. Here the '
            'name is orders dot placed. [[slnc 200]] And tuning in, '
            'asking Redis to send you everything on that name from now '
            'on, is what Redis calls subscribing. [[slnc 250]] One more '
            'thing about live radio. If your radio was off, there is no '
            'recording. Redis works the same way, and that will matter '
            'later.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='Publish Once, Redis Fans It Out',
        body="""TWO. Publish once, and Redis fans it out.
  published OrderPlaced ORD-1 once.
  Redis answered: 3 receivers.
  inventory [ORD-1], email [ORD-1],
  analytics [ORD-1].

  loyalty starts as a separate Java process.
  ORD-2 is published: 4 receivers.
  the loyalty process printed [ORD-2]
  and exited with code 0.
  the order service was not changed.""",
        narration=(
            'Second, the pattern, on a real Redis server. The demo starts '
            'Redis in a container, a small sealed box it switches on and '
            'off itself. Inventory, email and analytics each open their '
            'own connection and subscribe. The order service publishes '
            'order one, once. [[slnc 250]] Redis answers it with a '
            'number: three receivers. And each of the three services '
            'gets order one. [[slnc 300]] Now loyalty points joins, and '
            'it is not even in the same program. The demo starts it as a '
            'second Java process, with its own memory. Order two is '
            'published, and Redis answers four receivers. The loyalty '
            'process prints order two, and exits cleanly. The order '
            'service was not changed at all.'
        ),
    ),
    dict(
        key='06-count', kind='code', title='The Publisher Gets A Number',
        body="""public long publish(OrderEvent event) {
    // Redis hands it to every listener
    // on this channel, right now, and
    // answers with how many that was.
    return redis.publish(
        event.channel(), event.text());
}""",
        narration=(
            'Here is the whole of the publishing side. The order service '
            'hands one message to Redis under a channel name, and Redis '
            'answers with a single number: how many listeners it handed '
            'the message to, at that instant. [[slnc 300]] That number '
            'is new. In the partner project the publisher was told '
            'nothing at all. Here it learns how many heard. It still '
            'does not learn who they were, or whether any of them '
            'finished the work.'
        ),
    ),
    dict(
        key='07-three', kind='console', title='A Subscriber That Arrives Late',
        body="""THREE. A subscriber that arrives late.
  3 orders published while only email
  listened. Redis answered: [1, 1, 1].
  loyalty starts listening, and ORD-4
  is published: 2 receivers.

  email saw [ORD-1, ORD-2, ORD-3, ORD-4].
  loyalty saw [ORD-4].

  there is no reading from the start.
  keys in the database: 0.""",
        narration=(
            'Third, a subscriber that arrives late. Only email is '
            'listening, and three orders are published. Redis answers '
            'one, one and one. Then loyalty starts listening, and order '
            'four is published, to two receivers. [[slnc 250]] Email saw '
            'all four orders. Loyalty saw only order four. [[slnc 250]] '
            'In the partner project, a late subscriber could read the '
            'topic from the start, because the topic kept a log. Redis '
            'has no log for this. It stored none of the four orders. The '
            'number of keys in its database is zero. Orders one, two and '
            'three were never coming.'
        ),
    ),
    dict(
        key='08-four', kind='console', title='Each Takes What It Wants',
        body="""FOUR. Each takes what it wants.
  OrderPlaced ORD-1 reached 2 receivers.
  OrderCancelled ORD-1 reached 1.

  email listened to orders.placed:
  [OrderPlaced ORD-1].

  analytics listened to orders.*:
  [OrderPlaced ORD-1,
   OrderCancelled ORD-1].""",
        narration=(
            'Fourth, each service takes only what it wants. Email '
            'subscribes to one exact name, orders dot placed. Analytics '
            'subscribes with a star in the name, orders dot star, which '
            'matches every name that starts with orders. Redis calls that '
            'a pattern subscription. [[slnc 250]] Order one is placed, and '
            'reaches two receivers. Then order one is cancelled, and that '
            'reaches only one. Email got the placed order. Analytics got '
            'both.'
        ),
    ),
    dict(
        key='09-pile', kind='diagram', title='A Pile For Every Listener',
        body=None,
        narration=(
            'Before the fifth act, one more idea. Picture a busy kitchen '
            'sending plates out to several tables. The kitchen never waits '
            'for a slow table. Plates that a table has not taken yet stack '
            'up on a shelf by the kitchen door, one shelf per table. '
            '[[slnc 250]] Redis does exactly this. What a listener has '
            'not read yet waits in a pile that Redis keeps for that one '
            'listener. Redis calls the pile the output buffer. '
            '[[slnc 250]] And the pile has a limit. Out of the box it is '
            'thirty two megabytes, or eight megabytes if that lasts for '
            'sixty seconds. Past the limit, Redis does not slow down, and '
            'it does not wait. It closes that listener\'s connection.'
        ),
    ),
    dict(
        key='10-five', kind='console', title='A Subscriber That Cannot Keep Up',
        body="""FIVE. A subscriber that cannot keep up.
  this demo lowers the limit to 1mb.
  analytics stops reading. orders go out
  in rounds of 1000 until Redis acts.

  more than 10,000 orders later, Redis
  cut analytics off. listeners cut off
  for falling behind: 1.
  first order: 2 receivers. last: 1.
  email received every one.
  analytics got some of them, not all.""",
        narration=(
            'Fifth, the headline of this video. The demo lowers the limit '
            'to one megabyte, so the point arrives in seconds. Email and '
            'analytics both listen. Then analytics stops reading, the way '
            'a stuck service would. The order service publishes orders '
            'in rounds of one thousand, a flash sale, until Redis acts. '
            '[[slnc 300]] More than ten thousand orders later, Redis '
            'cuts analytics off. Its own counter of listeners cut off '
            'for falling behind reads one. The first order reached two '
            'receivers. The last reached one. Email kept up, and '
            'received every one. [[slnc 250]] When analytics starts '
            'reading again, it gets some of the orders, not all, and '
            'then its connection ends. The rest were thrown away with '
            'the pile. The exact counts depend on the machine, so the '
            'demo describes them rather than printing them.'
        ),
    ),
    dict(
        key='11-why', kind='bullets', title='Why Redis Cuts It Off',
        body=['The other choices are worse:', '',
              '✗ wait for the slow listener,', '   and slow down every publisher;',
              '✗ keep piling up, until Redis', '   runs out of memory.', '',
              '✓ cut the one slow listener off,', '   and keep everyone else going.', '',
              'The publisher is never told.'],
        narration=(
            'Why would Redis do that? Because the other two choices are '
            'worse. It could wait for the slow listener, and then one '
            'stuck service would slow down every publisher in the shop. '
            'Or it could keep piling up messages until Redis itself runs '
            'out of memory, and then everyone loses. [[slnc 250]] So it '
            'cuts off the one listener that fell behind, and keeps '
            'everyone else going. [[slnc 250]] Notice who is not told. '
            'The publisher was never slowed down, and never warned. The '
            'only trace is a counter inside Redis, and a smaller number '
            'in the answer to the next publish.'
        ),
    ),
    dict(
        key='12-six', kind='console', title='The Bill',
        body="""SIX. The bill.
  email was down when ORD-1 was placed.
  Redis told the order service:
  0 receivers.
  email came back and got: [].

  the count says how many were listening.
  not which ones, and not whether any
  finished the work.

  1 container and 2 Java processes.""",
        narration=(
            'Sixth, the bill. Email is down when order one is placed. '
            'Redis tells the order service zero receivers. When email '
            'comes back, it gets nothing. There is nothing to catch up '
            'from. [[slnc 250]] At least the publisher can see the zero. '
            'But the count only says how many connections were listening. '
            'It does not say which ones, and it does not say whether any '
            'of them finished the work. [[slnc 250]] And Redis is a '
            'separate program to run and to watch. This demo needed one '
            'container and two Java processes.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the shape right: publish once,', 'nobody named, each subscriber',
              'choosing what it hears.', '',
              'It left out three things.', '',
              'A listener in another process.', 'A backlog that is not kept at all.',
              'A limit on how far behind you fall.'],
        narration=(
            'The hand-built partner project got the shape right. The '
            'publisher announces once and names nobody. A new subscriber '
            'joins without the publisher changing. Each subscriber picks '
            'what it hears. All of that is true on Redis. [[slnc 300]] '
            'It left out three things. A listener in a different process, '
            'because everything lived in one program. A backlog: the '
            'partner project kept a log, so a late or slow subscriber '
            'could catch up, and Redis keeps none. And a limit: the '
            'partner project let a slow subscriber fall behind for ever, '
            'while Redis cuts it off.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Redis Pub/Sub is for news that', 'is worth nothing if it is late.', '',
              '1. Subscribe before you need it.', '',
              '2. Keep every listener reading,', '   and watch the cut-off counter.', '',
              '3. If a missed order matters,', '   use something that keeps a log.'],
        narration=(
            'Here is my verdict, plainly. Redis publishing is for news '
            'that is worth nothing if it arrives late: a live price, a '
            'stock level refresh, a signal to clear a cache. [[slnc 250]] '
            'One. Subscribe before you need it, because nothing is kept '
            'for a latecomer. [[slnc 200]] Two. Keep every listener '
            'reading. Hand slow work to a queue of its own, and watch '
            'the counter of listeners cut off. [[slnc 200]] Three. If a '
            'missed order would matter, use a tool that keeps a log, '
            'not live radio.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Redis 8.10.2 on Alpine, Jedis 8.0.1,', 'Testcontainers 2.0.5, in a container',
              'the demo starts and stops itself.', '',
              'Too much if every listener is in', 'one program: an in-memory topic',
              'costs nothing to run.', '',
              'Too little if a lost order matters.'],
        narration=(
            'What is real here? The server is Redis, version eight point '
            'ten point two, the newest release, in a small Alpine Linux '
            'container that the demo starts at the beginning and stops at '
            'the end. The Java client is Jedis, version eight point zero '
            'point one. Nothing is installed and nothing is left running. '
            'You need a container runtime, such as Docker Desktop, '
            'switched on before you start. Every number in this video '
            'comes from the program\'s own output, and two runs one '
            'after the other print the same thing. [[slnc 300]] So when '
            'is this the wrong tool? If every listener lives in one '
            'program, a topic in memory costs nothing to run. And if a '
            'lost order matters, Redis publishing is too little, because '
            'it keeps nothing.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Publisher Subscriber with Redis. [[slnc 250]] If you "
            'take one sentence away, take this one: Redis hands each '
            'message to whoever is listening at that instant, tells the '
            'publisher how many that was, keeps nothing, and cuts off a '
            'listener that falls too far behind. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository. [[slnc 300]] If you '
            'try one exercise, raise the limit in the fifth act to eight '
            'megabytes, guess whether analytics is still cut off, and then '
            'run it. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
