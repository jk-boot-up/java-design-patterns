"""Scene definitions for the Cache-Aside with Redis teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of Redis's words in plain
language before using Redis's name for it, and never points at a picture the
listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Cache-Aside with Redis',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Cache-Aside pattern in Java, using a real cache server '
            'called Redis. [[slnc 300]] This video is presented by '
            'Jayasekhar Konduru. [[slnc 600]] First, a simple definition. '
            '[[slnc 300]] Cache-aside means you ask a fast copy first. '
            '[[slnc 300]] If the copy has nothing, you fetch the real '
            'answer yourself. [[slnc 300]] And you leave a copy behind, '
            'for the next person. [[slnc 600]] In our online store, every '
            'product page needs a price, and prices live in the database. '
            '[[slnc 300]] So the shop asks the cache for the price first. '
            '[[slnc 300]] If the cache has nothing, the shop reads the '
            'database, and writes the price into the cache on the way '
            'back. [[slnc 500]] By the end, you will hear a second shop '
            'find the cache already filled. [[slnc 300]] A price removed '
            'by the cache on its own clock. [[slnc 300]] One ordinary '
            'write that makes an old price last forever. [[slnc 300]] And '
            'fifty requests rushing at the database, with nobody '
            'arranging it.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Every product page needs a price.', 'Prices live in the database.', '',
              'Ten products get most of the views.', 'Their prices rarely change.', '',
              'The shop runs as more than one', 'process, on a busy day.', '',
              'This time the cache is its own', 'program, shared by every shop.'],
        narration=(
            'Here is the scenario. [[slnc 400]] Every product page needs '
            'a price. [[slnc 300]] The prices live in the database, which '
            'holds the truth. [[slnc 300]] Ten products get most of the '
            'views, and their prices rarely change. [[slnc 300]] On a '
            'busy day, the shop runs as more than one program, and all of '
            'them read the same database. [[slnc 600]] The plain Java '
            'version of this project also used a cache. [[slnc 300]] But '
            "that cache lived inside the shop's own program, with a clock "
            'the demo moved by hand. [[slnc 500]] This time, the cache is '
            'a program of its own, shared by every shop. [[slnc 300]] '
            'With a clock that nobody in the shop controls. [[slnc 300]] '
            'And that changes three things.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='No Cache',
        body="""ONE. No cache.
  1000 product page views
  over 10 popular products:

  1000 database reads.""",
        narration=(
            'First, with no cache. [[slnc 400]] Every product page reads '
            'the database. [[slnc 300]] A thousand page views, over ten '
            'popular products, cost a thousand database reads. [[slnc '
            '500]] Only ten different rows were ever read. [[slnc 300]] '
            'The database answered the same ten questions, a hundred '
            'times each.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="Redis's Words",
        body=['Redis is a separate program that', 'keeps small data in memory.', '',
              'A key is the name of a note.', 'Its value is what the note says.', '',
              'key:   product:SKU-0', 'value: 1000   (a price in pence)', '',
              'Every shop reads the same notes.'],
        narration=(
            'Redis brings a few words with it, and each is simpler than '
            'it sounds. [[slnc 500]] Think of a whiteboard by the door of '
            'a busy restaurant kitchen. [[slnc 300]] The recipes live in '
            'a thick book in the office, and walking there is slow. '
            '[[slnc 300]] So one cook writes the answer on the board. '
            '[[slnc 300]] And the next cook reads the board, instead of '
            'walking. [[slnc 500]] Redis is the whiteboard. [[slnc 300]] '
            'It is a separate program that keeps small pieces of data in '
            'memory, and answers over the network. [[slnc 500]] Each note '
            'has a name, which Redis calls a key. [[slnc 300]] And what '
            'the note says is called its value. [[slnc 300]] Here, the '
            "key is the product's code, and the value is its price: ten "
            'pounds. [[slnc 500]] And every cook in the kitchen reads the '
            'same board.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='Look Aside, In Redis',
        body="""TWO. Look aside, in Redis.
  Redis is running in a container.

  the same 1000 views:
  10 database reads,
  990 cache hits, 10 misses.

  Redis now holds 10 keys,
  each with a 60 second expiry.""",
        narration=(
            'Second demo: the pattern, with Redis. [[slnc 400]] The demo '
            'starts Redis in a container, a small sealed box that the '
            'demo switches on and off by itself. [[slnc 500]] The shop '
            'asks Redis for the price first. [[slnc 300]] If Redis has '
            'nothing, that is a miss. [[slnc 300]] So the shop reads the '
            'database, and writes the price into Redis, to be thrown away '
            'after sixty seconds. [[slnc 500]] The same thousand views '
            'now cost only ten database reads. [[slnc 300]] Ten misses, '
            'one for each product. [[slnc 300]] And nine hundred and '
            'ninety hits. [[slnc 300]] Redis now holds ten keys.'
        ),
    ),
    dict(
        key='06-three', kind='console', title='Another Process Can See It',
        body="""THREE. Another process can see it.
  a second shop: a separate Java process.

  cache in its own memory, first 10 views:
    10 database reads, 0 cache hits.
  cache in Redis, first 10 views:
    0 database reads, 10 cache hits.

  redis-cli GET product:SKU-0: 1000.
  price changed to 1600, key deleted once.
  copies left for any process: 0.""",
        narration=(
            'Third demo, and this is something the plain Java version '
            'could never show. [[slnc 400]] The first shop has viewed all '
            'ten products. [[slnc 300]] Then a second shop starts, as a '
            'separate Java program, with its own memory. [[slnc 500]] '
            'With a cache inside its own memory, its first ten views cost '
            "ten database reads. [[slnc 300]] The first shop's work is no "
            'use to it. [[slnc 500]] With the same Redis, its first ten '
            'views cost no database reads at all. [[slnc 300]] Ten hits. '
            "[[slnc 500]] Then a third program, Redis's own command-line "
            'tool, asks for the same key. [[slnc 300]] And it is told: '
            'ten pounds. [[slnc 500]] Finally, the first shop changes '
            'that price to sixteen pounds, and deletes the key, once. '
            '[[slnc 300]] No copy is left anywhere, so every shop reads '
            'the new price next time.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='Where The Price Lives',
        body=None,
        narration=(
            'Here is the whole setup, in words. [[slnc 400]] There are '
            'two shop programs, one Redis, and one database. [[slnc 500]] '
            'Each shop asks Redis first. [[slnc 300]] On a miss, the shop '
            'itself reads the database. [[slnc 300]] Then it writes the '
            'price into Redis. [[slnc 500]] Redis never reads the '
            'database. [[slnc 300]] It only keeps what a shop gives it. '
            '[[slnc 500]] Because Redis is its own program, every shop '
            'sees the same entry. [[slnc 300]] And one delete removes it '
            'for all of them.'
        ),
    ),
    dict(
        key='08-expiry', kind='console', title='Real Expiry',
        body="""FOUR. Real expiry.
  SKU-0 is cached for 2 seconds.
  another system changes the price
  to 2000. a customer sees 1000.

  nobody deletes it.
  Redis removes the key itself
  when the time is up.
  a customer then sees 2000.""",
        narration=(
            'Fourth demo: expiry. [[slnc 400]] Each entry in Redis can '
            'carry a time limit. [[slnc 300]] The time an entry has left '
            'is called its time to live, or T T L. [[slnc 300]] When the '
            'time is up, Redis removes the entry by itself. [[slnc 600]] '
            'In the demo, one price is cached for two seconds. [[slnc '
            '300]] Another system changes that price in the database to '
            'twenty pounds, and does not tell the cache. [[slnc 300]] So '
            'a customer still sees ten pounds. [[slnc 500]] Nobody '
            'deletes the key. [[slnc 300]] The demo only keeps asking '
            'Redis whether the key is still there. [[slnc 300]] When the '
            'two seconds are up, Redis removes it on its own. [[slnc '
            '300]] And the next customer sees twenty pounds.'
        ),
    ),
    dict(
        key='09-plain-write', kind='console', title='A Plain Write',
        body="""  a price-sync job writes SKU-0 again
  with a plain SET.
  seconds to live: -1, which means never.

  the price changes to 2100.
  2 seconds later a customer still
  sees 2000. the entry will never expire.""",
        narration=(
            'Now the surprise, and the headline of this video. [[slnc '
            '400]] The command that writes a key in Redis is called SET. '
            '[[slnc 300]] A SET can carry a time limit, or leave it out. '
            '[[slnc 600]] A price-sync job writes the same price back '
            'into Redis, with a plain SET, and no time limit. [[slnc '
            '300]] Redis treats that as a brand new value. [[slnc 300]] '
            'And it throws the old time limit away. [[slnc 500]] Asked '
            'how long the entry has left, Redis now says minus one. '
            '[[slnc 300]] That means never. [[slnc 600]] Then the price '
            'in the database changes to twenty-one pounds. [[slnc 300]] '
            'Two seconds later, customers still see twenty pounds. [[slnc '
            '300]] And they will keep seeing it, until somebody deletes '
            'the key by hand.'
        ),
    ),
    dict(
        key='10-one-argument', kind='code', title='One Argument',
        body="""// expires: Redis removes it itself
redis.set(key, "2000",
    SetParams.setParams().px(2000));

// never expires, and wipes the old expiry
redis.set(key, "2000");""",
        narration=(
            'The difference between those two writes is one argument. '
            '[[slnc 400]] The first write passes a time limit of two '
            'seconds. [[slnc 300]] So Redis removes the entry by itself, '
            'when the time runs out. [[slnc 300]] The second write passes '
            'nothing. [[slnc 300]] So the entry lives forever. [[slnc '
            '600]] In the plain Java version, every write set the expiry '
            'automatically. [[slnc 300]] In Redis, every writer has to '
            'remember it. [[slnc 300]] The product page, the price-sync '
            'job, the admin screen, and the warm-up script. [[slnc 500]] '
            'Forget one argument, and the promise that a price is only '
            'wrong for a short time is gone.'
        ),
    ),
    dict(
        key='11-stampede', kind='console', title='A Real Stampede',
        body="""FIVE. A real stampede.
  50 requests together, 2 shop instances,
  just after SKU-0 expired.
  a database read takes 500 milliseconds.

  every request misses.
  database reads: more than 40.
  sharing inside each instance: 2 reads.
  a lock kept in Redis: 1 read.
  it expires by itself after 5 seconds.""",
        narration=(
            'Fifth demo: a stampede. [[slnc 400]] Fifty requests arrive '
            'at the same moment, split across two shop programs. [[slnc '
            '300]] All for the same product, just after its entry has '
            'gone. [[slnc 300]] And a database read takes half a second. '
            '[[slnc 600]] Every request asks Redis, finds nothing, and '
            'goes to the database. [[slnc 300]] More than forty database '
            'reads, for one price. [[slnc 300]] The exact number depends '
            "on the computer's scheduling, so the demo does not count it "
            'exactly. [[slnc 600]] The plain Java fix lets requests '
            'inside one program share a single read. [[slnc 300]] With '
            'two programs, that gives two reads, one each. [[slnc 300]] '
            "Because neither program can see the other's waiting "
            'requests. [[slnc 600]] The fix that works across programs is '
            'a lock, kept in Redis. [[slnc 300]] A request writes a lock '
            'key, but only if nobody has written it already. [[slnc 300]] '
            'So exactly one request wins. [[slnc 300]] The winner reads '
            'the database. [[slnc 300]] Everybody else waits for the '
            'price to appear in Redis. [[slnc 300]] One database read. '
            '[[slnc 500]] The lock has its own five-second time limit. '
            '[[slnc 300]] So a shop that crashes while holding it cannot '
            'block the others forever.'
        ),
    ),
    dict(
        key='12-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  Redis is emptied, as a restart
  with nothing saved leaves it.
  the first 10 views: 10 database reads.

  out of the box: maxmemory 0,
  no limit, and policy noeviction.

  SKU-0 held as the string 1000.
  1 container for 2 shop processes.""",
        narration=(
            'Sixth demo: the bill. [[slnc 400]] Redis is emptied, just as '
            'a restart with nothing saved would leave it. [[slnc 300]] '
            'The first ten views cost ten database reads again. [[slnc '
            '300]] The database takes the whole load, until the cache '
            'fills up. [[slnc 600]] Next, size. [[slnc 300]] Out of the '
            'box, Redis has no memory limit. [[slnc 300]] And its rule '
            'for making room is to never throw anything away. [[slnc '
            '300]] So a cache has to be given a size, and told what to '
            'throw away when it is full. [[slnc 600]] Also, the price now '
            'crosses the network as text. [[slnc 300]] And Redis is one '
            'more system to run, secure, and watch.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['Got right: the whole shape.', 'Ask first, fill on a miss,', 'delete on a write, expire, warm up.', '',
              'Left out: a second process.', 'Its own map would cost 10 reads.', '',
              'Left out: a real clock.', 'Left out: a stampede nobody arranged.', '',
              'Headline: a plain SET erases', 'the expiry. TTL -1, stale for ever.'],
        narration=(
            'So what did the plain Java version get right? [[slnc 400]] '
            'The whole shape. [[slnc 300]] Ask the cache first. [[slnc '
            '300]] On a miss, read the database, and fill the cache. '
            '[[slnc 300]] Delete the cached copy after a write. [[slnc '
            '300]] Expire entries. [[slnc 300]] And warm up again after a '
            'restart. [[slnc 300]] All of that holds on Redis, with the '
            'same numbers. [[slnc 600]] But it left out three things. '
            '[[slnc 400]] A second program. [[slnc 300]] Its cache lived '
            'inside one program, so a second shop would have warmed up '
            'its own. [[slnc 400]] A real clock. [[slnc 300]] Nothing '
            'expired unless the demo said so. [[slnc 400]] And a real '
            'stampede. [[slnc 300]] It had to hold every read back, to '
            'make one happen. [[slnc 600]] And the headline. [[slnc 300]] '
            'In Redis, a plain write erases the expiry, and an old price '
            'lasts forever.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Use Redis on the side when several', 'processes need the same answers.', '',
              'An expiry on every write.', 'A delete after every change.', '',
              'A shared lock on a popular refill,', 'with an expiry of its own.', '',
              'A size limit before real traffic.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Put Redis to the side '
            'when several programs need the same cached answers. [[slnc '
            '500]] Then settle four things, because Redis will not assume '
            'any of them. [[slnc 500]] One. [[slnc 200]] Put an expiry on '
            'every write, or the entry lives forever. [[slnc 400]] Two. '
            '[[slnc 200]] Delete the entry after every change to the '
            'database. [[slnc 400]] Three. [[slnc 200]] Guard the refill '
            'of a popular entry with a lock that every shop can see. '
            '[[slnc 300]] And give that lock an expiry of its own. [[slnc '
            '400]] Four. [[slnc 200]] Give Redis a size limit, and a rule '
            'for what to throw away, before real traffic arrives.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Real: Redis 8.10.2 in a container', 'the demo starts and stops.', 'Jedis 8.0.1, Testcontainers 2.0.5.', '',
              'Real: a second Java process.', 'Real: expiry on Redis\'s own clock.', '',
              'Too much: one shop process.', 'A map in memory is faster.', '',
              'Too much: data that must be exact.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] Redis is '
            'version eight point ten point two, in a container the demo '
            'starts and stops by itself. [[slnc 300]] The Java client is '
            'called Jedis. [[slnc 300]] The container is run by a library '
            'called Testcontainers. [[slnc 300]] The second shop really '
            'is a separate Java program. [[slnc 300]] And every expiry '
            "runs on Redis's own clock. [[slnc 300]] Only the database is "
            'kept simple, so the cache stays the lesson. [[slnc 600]] So, '
            'when is this too much? [[slnc 300]] If the shop runs as one '
            'program, a cache in its own memory is faster, and costs '
            'nothing to run. [[slnc 300]] And if a price must always be '
            'exact, a cache that can be out of date is a bug, not a '
            'trade-off.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Cache-Aside, with Redis. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] The shop fills '
            'the cache, every shop sees what it filled, and an entry only '
            'expires if every write remembers to say so. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Change the plain write so '
            'it keeps the old expiry. [[slnc 300]] Guess what Redis will '
            'report as the time to live, and then run it. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
