"""Scene definitions for the Cache-Aside teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Cache-Aside',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Cache-Aside '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'cache-aside means the application looks in a cache first. If '
            'the answer is not there, the application reads the real '
            'source itself, and puts the answer in the cache for next '
            'time. [[slnc 350]] This is another project in the '
            'microservices category, whose subject is how many small '
            'services stay reliable when they talk to each other. In our '
            'online store, the thing that gets asked for over and over is '
            'a product page. [[slnc 300]] By the end you will see a '
            'thousand page views cost a thousand database reads, then '
            'ten, see what happens on a write, see an expiry bound how '
            'stale the cache can be, watch fifty requests stampede a cold '
            'key and one read serve them all, and see the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Ten popular products get almost', 'every page view.', '', 'Each view reads the product from', 'the database.', '', '1000 views: how many reads?'],
        narration=(
            'Here is the scenario. Ten popular products get almost every '
            'page view. Each view reads the product from the database. '
            '[[slnc 300]] The question: a thousand views is how many '
            'database reads? And should it be?'
        ),
    ),
    dict(
        key='03-none', kind='console', title='No Cache',
        body="""ONE. No cache.
  1000 views, 10 products:
  1000 database reads.""",
        narration=(
            'First, no cache. A thousand product page views, over ten '
            'popular products. That is a thousand database reads, on the '
            'same ten rows, over and over.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Ask the cache first.', '', 'On a miss, the application reads', 'the source itself.', '', 'Then it puts the answer in the', 'cache.', '', 'The cache never talks to the', 'database.'],
        narration=(
            'The pattern. Ask the cache first. On a miss, the application '
            'reads the source itself. Then it puts the answer in the '
            'cache, for next time. The cache never talks to the database. '
            'The application does, and that is why it is called aside.'
        ),
    ),
    dict(
        key='05-aside', kind='console', title='Look Aside',
        body="""TWO. Look aside.
  the same 1000 views:
  10 database reads,
  990 cache hits,
  10 misses.""",
        narration=(
            'Second, look aside. The same thousand views now make ten '
            'database reads. Nine hundred and ninety are served by the '
            'cache, and ten were misses, one for each product. The '
            'database is asked once for each product, not once for each '
            'view.'
        ),
    ),
    dict(
        key='06-write', kind='console', title='Writes',
        body="""THREE. Writes.
  price to 1500, cache
  forgotten: customers see 1000.

  price to 1600, cache entry
  thrown away: customers see
  1600.""",
        narration=(
            'Third, writes. The price changes to fifteen hundred, but the '
            'change forgot the cache. Customers still see a thousand. '
            'Change it to sixteen hundred and throw the cached copy away, '
            'and the next read goes to the database and sees sixteen '
            'hundred. Every write must remember to invalidate.'
        ),
    ),
    dict(
        key='07-ttl', kind='console', title='A Time Limit On Staleness',
        body="""FOUR. Expiry.
  another system changes the
  price to 2000.
  59 seconds: still 1000.
  61 seconds: 2000.

  wrong for a bounded time.""",
        narration=(
            'Fourth, a time limit on staleness. Another system changes '
            "the price behind the cache's back. After fifty nine seconds, "
            'customers still see a thousand. After sixty one, they see '
            'two thousand. An expiry does not make the cache right. It '
            'makes it wrong for a bounded time, and you choose how long.'
        ),
    ),
    dict(
        key='08-stampede', kind='console', title='A Stampede',
        body="""FIVE. A stampede.
  50 requests, one expired key.
  each checks the cache: 50
  database reads.

  sharing one read: 1.""",
        narration=(
            'Fifth, a stampede. Fifty requests arrive together for one '
            'popular product whose entry has just expired. Every one '
            'misses, so every one reads the database: fifty reads, for '
            'one row. [[slnc 300]] Let the requests share a single read, '
            'and there is one. The others wait for it, and use its '
            'answer.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  the cache restarts, empty:
  the first 10 views go to the
  database.

  a copy, not the truth: one
  more thing to keep right.""",
        narration=(
            'Last, the bill. If the cache restarts empty, the first views '
            'all go to the database, and it takes the whole load again '
            'until the cache warms up. And the cache is a copy, not the '
            'truth. There is now a second thing to keep right, to size, '
            'and to explain to the next person.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Code that calls cache.get, then', 'the database, then cache.put.', '', '@Cacheable and @CacheEvict in', 'Spring.', '', 'A Redis or Memcached client beside', 'a database client.'],
        narration=(
            'How do you recognise this in code you did not write? Code '
            'that calls cache.get, then the database, then cache.put. '
            '@Cacheable and @CacheEvict in Spring. A Redis or Memcached '
            "client beside a database client. A comment saying 'clear the "
            "cache when you change this'."
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use cache-aside for data that is', 'read far more than it is written,', 'where a little staleness is', 'acceptable. Invalidate on every', 'write you control, give every', 'entry an expiry, and share the', 'read when many callers miss', 'together. Do not use it for data', 'that must always be exact, and'],
        narration=(
            'Here is my verdict, plainly. Use cache-aside for data that '
            'is read far more than it is written, where a little '
            'staleness is acceptable. Invalidate on every write you '
            'control, give every entry an expiry, and share the read when '
            'many callers miss together. Do not use it for data that must '
            'always be exact, and never treat the cache as the only copy.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. Every number quoted comes from '
            "this program's own output. Nothing depends on a clock, so "
            'every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For data that changes on every', 'read, or that is read once, a', 'cache is overhead. For data that', 'must be exact, staleness is a bug,', 'not a trade.'],
        narration=(
            'So when is it too much? For data that changes on every read, '
            'or that is read once, a cache is overhead. For data that '
            'must be exact, staleness is a bug, not a trade.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Cache-Aside. [[slnc 250]] If you take one sentence "
            'away, take this one: cache-aside trades exactness for speed, '
            'and you pay in stale reads, stampedes and a second thing to '
            'keep right. [[slnc 350]] The full source, the written notes, '
            'the diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'change the expiry to ten seconds, and see what it does to '
            'the database reads and the staleness. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
