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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Publisher-Subscriber pattern in Java, using a real server '
            'called Redis. [[slnc 300]] This video is presented by '
            'Jayasekhar Konduru. [[slnc 600]] First, a simple definition. '
            '[[slnc 300]] One part of a system announces that something '
            'happened, once, to a named place. [[slnc 300]] Any number of '
            'other parts can listen at that place. [[slnc 300]] And the '
            'one announcing never learns who they are. [[slnc 700]] In '
            'our online store, when an order is placed, the order service '
            'announces it once. [[slnc 300]] Inventory, email, analytics, '
            'and loyalty points each hear it, and do their own work. '
            '[[slnc 300]] The order service does not need to know any of '
            'them by name. [[slnc 500]] By the end, you will hear Redis '
            'pass one order to a program running separately. [[slnc 300]] '
            'Tell the publisher how many heard it. [[slnc 300]] Keep '
            'nothing for a listener that arrives late. [[slnc 300]] And '
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
            'Here is the scenario. [[slnc 400]] An order is placed, and '
            'several services care about it. [[slnc 300]] Inventory '
            'reserves the stock. [[slnc 200]] Email sends the '
            'confirmation. [[slnc 200]] Analytics counts the sale. [[slnc '
            '200]] Loyalty adds points. [[slnc 600]] The plain Java '
            'version built this with the topic as an object inside one '
            'Java program. [[slnc 300]] This time, the topic lives in '
            'Redis, a separate program. [[slnc 300]] And every listener '
            'reaches it over its own network connection. [[slnc 300]] '
            'That changes more than you might expect.'
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
            'First demo: without the pattern. [[slnc 400]] The order '
            'service calls inventory, then email, then analytics, each by '
            'name. [[slnc 300]] Each one handles order one. [[slnc 500]] '
            'It works. [[slnc 300]] But the order service now knows three '
            'services by name. [[slnc 300]] When loyalty points wants to '
            'hear about orders, someone must edit the order service.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="Redis's Words",
        body=['Publish: announce a message', 'under a name, once.', '',
              'Channel: the name it goes out under,', 'here orders.placed.', '',
              'Subscribe: ask Redis to send you', 'everything on a name, from now on.', '',
              'Redis keeps no copy. Like live radio.'],
        narration=(
            'Redis brings a few words with it. [[slnc 300]] Each is '
            'simpler than it sounds. [[slnc 500]] Think of a live radio '
            'station. [[slnc 300]] The presenter speaks once, and every '
            'radio tuned in at that moment hears it. [[slnc 500]] '
            'Announcing a message once is what Redis calls publishing. '
            '[[slnc 300]] The frequency it goes out on is called a '
            'channel. [[slnc 300]] It is just a name. [[slnc 300]] Here, '
            'the name is orders dot placed. [[slnc 300]] And tuning in, '
            'to hear everything on that name from now on, is called '
            'subscribing. [[slnc 600]] One more thing about live radio. '
            '[[slnc 300]] If your radio was off, there is no recording. '
            '[[slnc 300]] Redis works the same way, and that will matter '
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
            'Second demo: publish once, and Redis passes it on. [[slnc '
            '400]] The demo starts Redis in a container, a small sealed '
            'box it switches on and off by itself. [[slnc 500]] '
            'Inventory, email, and analytics each connect, and subscribe. '
            '[[slnc 300]] The order service publishes order one, once. '
            '[[slnc 300]] Redis answers with a number: three receivers. '
            '[[slnc 300]] And each of the three services gets order one. '
            '[[slnc 600]] Now loyalty points joins. [[slnc 300]] And it '
            'is not even in the same program. [[slnc 300]] The demo '
            'starts it as a second Java program, with its own memory. '
            '[[slnc 500]] Order two is published, and Redis answers: four '
            'receivers. [[slnc 300]] The loyalty program receives order '
            'two. [[slnc 300]] And the order service was not changed at '
            'all.'
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
            'Here is the whole of the publishing side. [[slnc 400]] The '
            'order service hands one message to Redis, under a channel '
            'name. [[slnc 300]] And Redis answers with one number. [[slnc '
            '300]] How many listeners it handed the message to, at that '
            'moment. [[slnc 600]] That number is new. [[slnc 300]] In the '
            'plain Java version, the publisher was told nothing. [[slnc '
            '300]] Here, it learns how many heard. [[slnc 500]] But it '
            'still does not learn who they were. [[slnc 300]] Or whether '
            'any of them finished the work.'
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
            'Third demo: a subscriber that arrives late. [[slnc 400]] '
            'Only email is listening. [[slnc 300]] Three orders are '
            'published. [[slnc 300]] Redis answers: one receiver each '
            'time. [[slnc 500]] Then loyalty starts listening. [[slnc '
            '300]] And order four is published, to two receivers. [[slnc '
            '600]] Email saw all four orders. [[slnc 300]] Loyalty saw '
            'only order four. [[slnc 600]] In the plain Java version, a '
            'late subscriber could read from the start, because the topic '
            'kept a history. [[slnc 300]] Redis keeps no history here. '
            '[[slnc 300]] It stored none of the four orders. [[slnc 300]] '
            'Orders one, two, and three were never coming.'
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
            'Fourth demo: each service takes only what it wants. [[slnc '
            '400]] Email subscribes to one exact name: orders dot placed. '
            '[[slnc 500]] Analytics subscribes with a star in the name: '
            'orders dot star. [[slnc 300]] That matches every name '
            'starting with orders. [[slnc 300]] Redis calls that a '
            'pattern subscription. [[slnc 600]] Order one is placed, and '
            'reaches two receivers. [[slnc 300]] Then order one is '
            'cancelled, and that reaches only one. [[slnc 500]] Email got '
            'the placed order. [[slnc 300]] Analytics got both.'
        ),
    ),
    dict(
        key='09-pile', kind='diagram', title='A Pile For Every Listener',
        body=None,
        narration=(
            'Before the fifth demo, one more idea. [[slnc 400]] Picture a '
            'busy kitchen sending plates to several tables. [[slnc 300]] '
            'The kitchen never waits for a slow table. [[slnc 300]] '
            'Plates a table has not taken yet stack up on a shelf by the '
            'door. [[slnc 300]] One shelf per table. [[slnc 600]] Redis '
            'does exactly this. [[slnc 300]] Messages a listener has not '
            'read yet wait in a pile that Redis keeps for that one '
            'listener. [[slnc 300]] Redis calls it the output buffer. '
            '[[slnc 600]] And the pile has a limit. [[slnc 300]] By '
            'default, thirty-two megabytes. [[slnc 300]] Past that limit, '
            'Redis does not slow down, and it does not wait. [[slnc 300]] '
            "It closes that listener's connection."
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
            'Fifth demo, and this is the headline of the video. [[slnc '
            '400]] The demo lowers the limit to one megabyte, so the '
            'effect shows up in seconds. [[slnc 500]] Email and analytics '
            'are both listening. [[slnc 300]] Then analytics stops '
            'reading, just as a stuck service would. [[slnc 300]] The '
            'order service publishes orders in rounds of a thousand, like '
            'a flash sale. [[slnc 600]] More than ten thousand orders '
            'later, Redis cuts analytics off. [[slnc 300]] The first '
            'order reached two receivers. [[slnc 300]] The last reached '
            'only one. [[slnc 300]] Email kept up, and received every '
            'order. [[slnc 600]] When analytics starts reading again, it '
            'gets some of the orders, not all. [[slnc 300]] Then its '
            'connection ends. [[slnc 300]] The rest were thrown away with '
            'the pile. [[slnc 500]] The exact counts depend on the '
            'machine, so the demo describes them instead of printing '
            'them.'
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
            'Why would Redis do that? [[slnc 300]] Because the other two '
            'choices are worse. [[slnc 600]] It could wait for the slow '
            'listener. [[slnc 300]] Then one stuck service would slow '
            'down every publisher in the shop. [[slnc 500]] Or it could '
            'keep piling up messages, until Redis itself runs out of '
            'memory. [[slnc 300]] Then everyone loses. [[slnc 600]] So it '
            'cuts off the one listener that fell behind. [[slnc 300]] And '
            'it keeps everyone else going. [[slnc 600]] Notice who is not '
            'told. [[slnc 300]] The publisher was never slowed down, and '
            'never warned. [[slnc 300]] The only trace is a counter '
            'inside Redis. [[slnc 300]] And a smaller number in the '
            'answer to the next publish.'
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
            'Sixth demo: the bill. [[slnc 400]] Email is down when order '
            'one is placed. [[slnc 300]] Redis tells the order service: '
            'zero receivers. [[slnc 500]] When email comes back, it gets '
            'nothing. [[slnc 300]] There is nothing to catch up from. '
            '[[slnc 600]] At least the publisher can see the zero. [[slnc '
            '300]] But the count only says how many were listening. '
            '[[slnc 300]] Not which ones. [[slnc 300]] And not whether '
            'any of them finished the work. [[slnc 600]] And Redis is one '
            'more program to run and watch.'
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
            'The plain Java version got the shape right. [[slnc 400]] The '
            'publisher announces once, and names nobody. [[slnc 300]] A '
            'new subscriber joins without the publisher changing. [[slnc '
            '300]] And each subscriber picks what it hears. [[slnc 300]] '
            'All of that is true on Redis. [[slnc 600]] But it left out '
            'three things. [[slnc 500]] First, a listener in a different '
            'program, because everything lived in one program. [[slnc '
            '400]] Second, the history. [[slnc 300]] The plain version '
            'kept a history, so a late or slow subscriber could catch up. '
            '[[slnc 300]] Redis keeps none. [[slnc 400]] And third, a '
            'limit. [[slnc 300]] The plain version let a slow subscriber '
            'fall behind forever. [[slnc 300]] Redis cuts it off.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Redis Pub/Sub is for news that', 'is worth nothing if it is late.', '',
              '1. Subscribe before you need it.', '',
              '2. Keep every listener reading,', '   and watch the cut-off counter.', '',
              '3. If a missed order matters,', '   use something that keeps a log.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Redis publishing is '
            'for news that is worthless if it arrives late. [[slnc 300]] '
            'A live price. [[slnc 200]] A stock level refresh. [[slnc '
            '200]] Or a signal to clear a cache. [[slnc 600]] One. [[slnc '
            '200]] Subscribe before you need it, because nothing is kept '
            'for a latecomer. [[slnc 400]] Two. [[slnc 200]] Keep every '
            'listener reading. [[slnc 300]] Hand slow work to a separate '
            'queue. [[slnc 300]] And watch the counter of listeners that '
            'were cut off. [[slnc 400]] Three. [[slnc 200]] If a missed '
            'order would matter, use a tool that keeps a history. [[slnc '
            '300]] Not live radio.'
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
            'A quick, honest note about this demo. [[slnc 400]] The '
            'server is Redis, version eight point ten point two, the '
            'newest release. [[slnc 300]] It runs in a container that the '
            'demo starts and stops by itself. [[slnc 300]] The Java '
            'client is called Jedis. [[slnc 300]] You just need Docker '
            'switched on first. [[slnc 300]] Every number you heard comes '
            "from the program's own output. [[slnc 600]] So, when is this "
            'the wrong tool? [[slnc 300]] If every listener lives in one '
            'program, a topic in memory costs nothing to run. [[slnc '
            '300]] And if a lost order matters, Redis publishing is too '
            'little, because it keeps nothing.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Publisher-Subscriber, with Redis. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Redis '
            'hands each message to whoever is listening at that moment, '
            'tells the publisher how many that was, keeps nothing, and '
            'cuts off a listener that falls too far behind. [[slnc 500]] '
            'The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Raise the limit in '
            'the fifth demo to eight megabytes. [[slnc 300]] Guess '
            'whether analytics is still cut off, and then run it. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
