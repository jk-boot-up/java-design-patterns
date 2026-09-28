"""Scene definitions for the Cache-Aside teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Cache-Aside',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Cache-Aside pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A cache is a fast copy of '
            'data, kept close at hand. [[slnc 300]] With cache-aside, the '
            'application looks in the cache first. [[slnc 300]] If the '
            'answer is not there, the application reads the real source '
            'itself. [[slnc 300]] Then it puts the answer in the cache, '
            'for next time. [[slnc 600]] Think of a shop assistant who '
            'keeps the most asked-about leaflets on the counter. [[slnc '
            '300]] If a leaflet is on the counter, they hand it over. '
            '[[slnc 300]] If not, they walk to the back room, fetch one, '
            'and leave a copy on the counter. [[slnc 700]] In our online '
            'store, the thing asked for again and again is a product '
            'page. [[slnc 500]] By the end, you will hear a thousand page '
            'views cost a thousand database reads, and then only ten. '
            '[[slnc 300]] What happens when a price changes. [[slnc 300]] '
            'How an expiry limits how out of date the cache can be. '
            '[[slnc 300]] Fifty requests rushing at one missing entry. '
            '[[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Ten popular products get almost', 'every page view.', '', 'Each view reads the product from', 'the database.', '', '1000 views: how many reads?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Ten popular products get '
            'almost every page view. [[slnc 300]] Each view reads the '
            'product from the database. [[slnc 500]] So here is the '
            'question. [[slnc 300]] A thousand views means how many '
            'database reads? [[slnc 300]] And should it?'
        ),
    ),
    dict(
        key='03-none', kind='console', title='No Cache',
        body="""ONE. No cache.
  1000 views, 10 products:
  1000 database reads.""",
        narration=(
            'First, with no cache. [[slnc 400]] A thousand product page '
            'views, over ten popular products. [[slnc 300]] That is a '
            'thousand database reads. [[slnc 300]] The same ten rows, '
            'read over and over again.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Ask the cache first.', '', 'On a miss, the application reads', 'the source itself.', '', 'Then it puts the answer in the', 'cache.', '', 'The cache never talks to the', 'database.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Ask the cache first. [[slnc '
            '300]] If it is missing, that is called a miss. [[slnc 300]] '
            'On a miss, the application reads the database itself. [[slnc '
            '300]] Then it puts the answer in the cache, for next time. '
            '[[slnc 500]] The cache never talks to the database. [[slnc '
            '300]] The application does. [[slnc 300]] The cache sits to '
            'one side, and that is why it is called cache-aside.'
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
            'Second demo: with the cache. [[slnc 400]] The same thousand '
            'views now make only ten database reads. [[slnc 500]] Nine '
            'hundred and ninety views are served from the cache. [[slnc '
            '300]] Those are called hits. [[slnc 300]] And there are ten '
            'misses, one for each product. [[slnc 500]] The database is '
            'asked once per product, not once per view.'
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
            'Third demo: changing a price. [[slnc 400]] The price changes '
            'from ten pounds to fifteen pounds. [[slnc 300]] But the code '
            'that changed it forgot about the cache. [[slnc 300]] So '
            'customers still see ten pounds. [[slnc 600]] Now the price '
            'changes to sixteen pounds, and this time the cached copy is '
            'thrown away. [[slnc 300]] The next read misses, goes to the '
            'database, and sees sixteen pounds. [[slnc 500]] Throwing '
            'away a cached copy is called invalidating it. [[slnc 300]] '
            'And every write must remember to do it.'
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
            'Fourth demo: a time limit on how out of date the cache can '
            'be. [[slnc 400]] Another system changes the price to twenty '
            'pounds, without telling the cache. [[slnc 500]] Fifty-nine '
            'seconds later, customers still see ten pounds. [[slnc 300]] '
            'Sixty-one seconds later, they see twenty. [[slnc 300]] '
            'Because every entry expires after sixty seconds. [[slnc '
            '500]] An expiry does not make the cache right. [[slnc 300]] '
            'It makes sure it is only wrong for a limited time. [[slnc '
            '300]] And you choose how long.'
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
            'Fifth demo: a stampede. [[slnc 400]] Fifty requests arrive '
            'at the same moment, for one popular product. [[slnc 300]] '
            'And its cache entry has just expired. [[slnc 500]] Every '
            'request misses. [[slnc 300]] So every request reads the '
            'database. [[slnc 300]] Fifty reads, for one row. [[slnc '
            '600]] Now let the requests share a single read. [[slnc 300]] '
            'The first one goes to the database. [[slnc 300]] The other '
            'forty-nine wait for it, and use its answer. [[slnc 300]] One '
            'read, instead of fifty.'
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
            'Finally, the bill. [[slnc 400]] If the cache restarts, it '
            'starts empty. [[slnc 300]] So the first views all go to the '
            'database. [[slnc 300]] And the database takes the whole load '
            'again, until the cache fills up. [[slnc 500]] And remember, '
            'the cache is a copy, not the truth. [[slnc 300]] It is one '
            'more thing to keep correct, to size, and to explain to the '
            'next person.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Code that calls cache.get, then', 'the database, then cache.put.', '', '@Cacheable and @CacheEvict in', 'Spring.', '', 'A Redis or Memcached client beside', 'a database client.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for code that asks the cache, then the '
            'database, then puts the answer in the cache. [[slnc 300]] In '
            'Spring, look for the Cacheable and Cache Evict annotations. '
            '[[slnc 300]] Look for a Redis or Memcached client, next to a '
            'database client. [[slnc 300]] Or a comment saying: clear the '
            'cache when you change this.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use cache-aside for data that is', 'read far more than it is written,', 'where a little staleness is', 'acceptable. Invalidate on every', 'write you control, give every', 'entry an expiry, and share the', 'read when many callers miss', 'together. Do not use it for data', 'that must always be exact, and'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use cache-aside for '
            'data that is read far more often than it is written. [[slnc '
            '300]] And where being slightly out of date is acceptable. '
            '[[slnc 500]] Invalidate on every write you control. [[slnc '
            '300]] Give every entry an expiry. [[slnc 300]] And share the '
            'read when many callers miss together. [[slnc 500]] Do not '
            'use it for data that must always be exact. [[slnc 300]] And '
            'never treat the cache as the only copy.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] "
            'Nothing depends on a real clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For data that changes on every', 'read, or that is read once, a', 'cache is overhead. For data that', 'must be exact, staleness is a bug,', 'not a trade.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If the data changes '
            'on every read, or is only read once, a cache is just extra '
            'work. [[slnc 400]] And if the data must always be exact, '
            'being out of date is a bug, not a trade-off.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Cache-Aside pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Cache-aside '
            'trades exactness for speed, and you pay in out of date '
            'reads, stampedes, and a second thing to keep correct. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 300]] '
            'It runs offline, with nothing installed except a Java '
            'development kit. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Change the expiry to ten seconds. [[slnc 300]] '
            'Then see what it does to the number of database reads, and '
            'to how out of date the prices get. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
