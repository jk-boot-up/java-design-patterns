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
            'Hello, and welcome. This video explains the Cache-Aside '
            'pattern in Java, using a real cache server called Redis. '
            '[[slnc 250]] It is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] Here is the plain definition, in '
            'general words. Cache-aside means you ask a fast copy first. '
            'When the copy has nothing, you fetch the real answer '
            'yourself, and you leave a copy behind for the next person. '
            '[[slnc 350]] Now the same thing in our online store. Every '
            'product page needs a price, and the prices live in the '
            'database. So the shop asks the cache for the price first. '
            'If the cache has nothing, the shop reads the database, and '
            'writes the price into the cache on its way back. '
            '[[slnc 300]] By the end you will have seen a second shop '
            'find the cache already warm, a price removed by the cache '
            'on its own clock, one ordinary write that makes a stale '
            'price last for ever, and fifty requests stampede the '
            'database with nothing arranging it.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Every product page needs a price.', 'Prices live in the database.', '',
              'Ten products get most of the views.', 'Their prices rarely change.', '',
              'The shop runs as more than one', 'process, on a busy day.', '',
              'This time the cache is its own', 'program, shared by every shop.'],
        narration=(
            'Here is the scenario. Every product page needs a price, and '
            'the prices live in the database, which is the source of '
            'truth. Ten products get most of the views, and their prices '
            'rarely change. On a busy day the shop runs as more than one '
            'process, and every one of them reads the same database. '
            '[[slnc 300]] The hand-built twin of this project already put '
            'a cache on the side, but that cache was a map inside the '
            'shop\'s own program, with a clock the demo moved by hand. '
            'This time the cache is a program of its own, shared by every '
            'shop, with a clock nobody in the shop controls. That changes '
            'three things.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='No Cache',
        body="""ONE. No cache.
  1000 product page views
  over 10 popular products:

  1000 database reads.""",
        narration=(
            'First, the version without a cache. Every product page reads '
            'the database. A thousand page views over ten popular '
            'products cost a thousand database reads. [[slnc 250]] Only '
            'ten different rows were ever read. The database answered '
            'the same ten questions a hundred times each.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="Redis's Words",
        body=['Redis is a separate program that', 'keeps small data in memory.', '',
              'A key is the name of a note.', 'Its value is what the note says.', '',
              'key:   product:SKU-0', 'value: 1000   (a price in pence)', '',
              'Every shop reads the same notes.'],
        narration=(
            'Redis brings a few words with it, and each one is simpler '
            'than it sounds. Think of a whiteboard by the door of a busy '
            'restaurant kitchen. The recipes live in a thick book in the '
            'office, and walking there is slow. So a cook writes the '
            'answer on the board, and the next cook reads the board '
            'instead of walking. [[slnc 250]] Redis is the whiteboard: '
            'a separate program that keeps small pieces of data in '
            'memory and answers over the network. [[slnc 250]] Each note '
            'has a name, which Redis calls a key, and what the note says, '
            'which Redis calls its value. Here the key is product, colon, '
            'S K U dash zero, and the value is one thousand, a price in '
            'pence, written as text. [[slnc 250]] And every cook in the '
            'kitchen reads the same board.'
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
            'Second, the pattern. The demo starts a Redis server in a '
            'container, a small sealed box the demo switches on and off '
            'itself. The shop asks Redis for the price first. When Redis '
            'has nothing, that is a miss, and the shop reads the database '
            'and writes the price into Redis, to be thrown away after '
            'sixty seconds. [[slnc 250]] The same thousand views now cost '
            'ten database reads. Ten misses, one for each product, and '
            'then nine hundred and ninety hits. Redis holds ten keys.'
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
            'Third, something the twin could never show. The first shop '
            'has viewed all ten products. Then a second shop starts, as a '
            'separate Java program with its own memory. [[slnc 250]] '
            'Given a cache in its own memory, the way the twin had it, '
            'its first ten views cost ten database reads. The first '
            'shop\'s work is no use to it. Given the same Redis, its '
            'first ten views cost no database reads at all: ten hits. '
            '[[slnc 250]] Then Redis\'s own command-line program, a third '
            'program, asks for the key for S K U zero, and is told one '
            'thousand. Finally the first shop changes that price to '
            'sixteen hundred, and deletes the key, once. No copy is left '
            'for any process, so every shop reads the new price next time.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='Where The Price Lives',
        body=None,
        narration=(
            'Here is the whole arrangement, in words. There are two shop '
            'programs, one Redis, and one database. [[slnc 250]] Each '
            'shop asks Redis first. On a miss, the shop itself reads the '
            'database, and then writes the price into Redis. Redis never '
            'reads the database. It only keeps what a shop gave it. '
            '[[slnc 250]] Because Redis is its own program, every shop '
            'sees the same entry, and one delete removes it for all of '
            'them. [[slnc 300]] The rule to remember is this: Redis '
            'never reads the database; each shop does.'
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
            'Fourth, expiry. Each entry in Redis can carry a time limit. '
            'The time an entry has left is called its time to live, and '
            'Redis shortens that to T T L. When the time is up, Redis '
            'removes the entry by itself. [[slnc 250]] In the demo, the '
            'price of S K U zero is cached for two seconds. Another '
            'system changes the price in the database to two thousand, '
            'and does not tell the cache. So a customer still sees one '
            'thousand. [[slnc 250]] Nobody deletes the key. The demo '
            'only asks Redis, again and again, whether the key is still '
            'there. When the two seconds are up, Redis removes it on its '
            'own clock, and the next customer sees two thousand.'
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
            'Now the surprise, and the headline of this video. The '
            'command that writes a key in Redis is called SET. A SET can '
            'carry a time limit, or it can leave it out. [[slnc 250]] A '
            'price-sync job writes the price of S K U zero back into '
            'Redis, with a plain SET, and no time limit. Redis treats '
            'that as a brand new value, and throws the old time limit '
            'away. Asked how long the entry has left, Redis now says '
            'minus one, which means never. [[slnc 250]] The database '
            'changes the price to twenty-one hundred. Two seconds later, '
            'as long as the first entry lived, a customer still sees two '
            'thousand. And they will keep seeing it, until somebody '
            'deletes the key by hand.'
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
            'The first write passes a time limit of two thousand '
            'milliseconds, and Redis removes the entry by itself when it '
            'runs out. The second write passes nothing, and the entry '
            'lives for ever. [[slnc 250]] In the twin, every write set '
            'the expiry, because the cache did it for you. In Redis, '
            'every writer has to remember: the page that reads a price, '
            'the price-sync job, the admin screen, the warm-up script. '
            'One forgotten argument, and the promise that a price is '
            'wrong only for a short time is gone.'
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
            'Fifth, a stampede. Fifty requests arrive at the same moment, '
            'split across two shop instances, for S K U zero, just after '
            'its entry has gone. A database read takes half a second. '
            '[[slnc 250]] Every request asks Redis, finds nothing, and '
            'goes to the database. More than forty database reads, for '
            'one price. The exact number is up to the computer\'s thread '
            'scheduler, so the demo describes it rather than counting it. '
            '[[slnc 250]] The twin\'s fix lets the requests inside one '
            'program share one read. With two instances, that gives two '
            'reads, one per instance, because neither can see the '
            'other\'s waiting requests. [[slnc 250]] The fix that works '
            'across programs is a lock kept in Redis. A request writes a '
            'lock key, but only if nobody has written it already. Redis '
            'calls that SET with N X, and exactly one request wins. The '
            'winner reads the database. Everybody else waits for the '
            'price to appear in Redis. One database read. [[slnc 250]] '
            'The lock has its own five-second time limit, so a shop that '
            'dies holding it cannot block the others for ever.'
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
            'Sixth, the bill. Redis is emptied, the way a restart with '
            'nothing saved would leave it, and the first ten views cost '
            'ten database reads again. The database takes the whole load '
            'until the cache warms up. [[slnc 250]] Redis has a setting '
            'for its size limit, called max memory, and out of the box '
            'it is zero, which means no limit. Its rule for making room, '
            'called the eviction policy, is no eviction, which means it '
            'never throws anything away. A cache has to be given a size, '
            'and told what to discard. [[slnc 250]] The price now '
            'crosses the network as text: Redis holds S K U zero as the '
            'string one thousand. And Redis is one more system to run, '
            'secure and watch: one container, for two shop processes.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['Got right: the whole shape.', 'Ask first, fill on a miss,', 'delete on a write, expire, warm up.', '',
              'Left out: a second process.', 'Its own map would cost 10 reads.', '',
              'Left out: a real clock.', 'Left out: a stampede nobody arranged.', '',
              'Headline: a plain SET erases', 'the expiry. TTL -1, stale for ever.'],
        narration=(
            'So what did the hand-built twin get right? The whole shape. '
            'Ask the cache first. On a miss, read the database and fill '
            'the cache. Delete the cached copy after a write. Expire '
            'entries. Warm up again after a restart. All of that holds on '
            'Redis, with the same figures. [[slnc 300]] What it left out '
            'was three things. A second process: its cache was a map '
            'inside one program, so a second shop would have spent ten '
            'reads warming its own. A real clock: nothing expired unless '
            'the demo said so. And a real stampede: the twin had to hold '
            'every database read back to make one happen. [[slnc 300]] '
            'And the headline: in the twin the expiry came with every '
            'write. In Redis, a plain write erases it, and a stale price '
            'lasts for ever.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Use Redis on the side when several', 'processes need the same answers.', '',
              'An expiry on every write.', 'A delete after every change.', '',
              'A shared lock on a popular refill,', 'with an expiry of its own.', '',
              'A size limit before real traffic.'],
        narration=(
            'The verdict. Put Redis on the side when several processes '
            'need the same cached answers. [[slnc 250]] Then say four '
            'things out loud, because Redis will not assume any of them. '
            'Put an expiry on every write, or the entry lives for ever. '
            'Delete the entry after every change to the database, so '
            'every shop reads again. Guard the refill of a popular entry '
            'with a lock every shop can see, and give that lock an expiry '
            'of its own. [[slnc 250]] And give Redis a size limit, and a '
            'rule for what to throw away, before it meets real traffic.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Real: Redis 8.10.2 in a container', 'the demo starts and stops.', 'Jedis 8.0.1, Testcontainers 2.0.5.', '',
              'Real: a second Java process.', 'Real: expiry on Redis\'s own clock.', '',
              'Too much: one shop process.', 'A map in memory is faster.', '',
              'Too much: data that must be exact.'],
        narration=(
            'What in this project is real? Redis version eight point ten '
            'point two, in a container the demo starts and stops itself. '
            'The Java client is Jedis, and the container is run by a '
            'library called Testcontainers. The second shop is a '
            'genuinely separate Java program, and every expiry runs on '
            'Redis\'s own clock. The database is the one thing kept '
            'simple, so that the cache stays the lesson. [[slnc 300]] '
            'And when is this too much? If the shop runs as one process, '
            'a map in its own memory is faster and costs nothing to run. '
            'And if a price must always be exact, a cache that can be '
            'stale is a bug, not a trade.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Cache-Aside with Redis. [[slnc 250]] If you take one "
            'sentence away, take this one: the shop fills the cache, '
            'every shop sees what it filled, and an entry expires only '
            'if every write remembers to say so. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository. [[slnc 300]] If you '
            'try one exercise, change the plain write so it keeps the '
            'old expiry, guess what Redis will report as the time to '
            'live, and then run it. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
