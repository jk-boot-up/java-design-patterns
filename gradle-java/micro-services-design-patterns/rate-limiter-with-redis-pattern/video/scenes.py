"""Scene definitions for the Rate Limiter with Redis teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of Redis's and Bucket4j's
words in plain language before using the tool's name for it, and never points
at a picture the listener cannot see. Every figure is the output of
`./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Rate Limiter with Redis',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Rate Limiter pattern in Java, using a real Redis server, and '
            'a library called Bucket four J. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A rate limiter gives each '
            'caller a bucket of tokens. [[slnc 300]] Every request spends '
            'one token. [[slnc 300]] When the bucket is empty, the '
            'request is refused. [[slnc 300]] And the bucket is filled up '
            'again on a timer. [[slnc 700]] In our online store, there is '
            'a product search. [[slnc 300]] A price-comparison robot '
            'sends searches as fast as it can. [[slnc 300]] So the shop '
            'allows each client ten searches, filled back up once an '
            'hour. [[slnc 300]] The search runs as several copies, on '
            'several servers. [[slnc 300]] So ten has to mean ten, '
            'however many copies are running. [[slnc 500]] By the end, '
            'you will hear the limit leak when each server keeps its own '
            'bucket. [[slnc 300]] Hold when the bucket moves into Redis. '
            '[[slnc 300]] Survive ninety searches at the same instant. '
            '[[slnc 300]] And be broken by one server whose clock runs an '
            'hour fast.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Product search, open to the world.', 'client-42 is a price-comparison robot.', '',
              'The rule: 10 searches per client,', 'filled back up once an hour.', '',
              'The search runs as 3 copies behind', 'a load balancer, and 6 on a busy day.', '',
              'The hand-built twin kept each bucket', 'inside one program.'],
        narration=(
            "Here is the scenario. [[slnc 400]] The shop's product search "
            'is open to the world. [[slnc 300]] Customers use it, and so '
            'does a price-comparison robot, called client forty-two. '
            '[[slnc 600]] The rule is ten searches per client, filled '
            'back up once an hour. [[slnc 300]] The hour is deliberate. '
            '[[slnc 300]] The demo only runs for a few seconds, so no '
            'token comes back during it. [[slnc 300]] And every count is '
            'exact. [[slnc 600]] The search service runs as three copies, '
            'on three servers. [[slnc 300]] In front of them sits a load '
            'balancer, which deals each search to the next server in '
            'turn. [[slnc 300]] On a busy day, the shop runs six copies. '
            '[[slnc 600]] The plain Java version kept each bucket inside '
            'one program. [[slnc 300]] This time, the bucket has to work '
            'across separate programs.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='A Bucket In Each Server',
        body="""ONE. A bucket in each server.
  client-42 sends 90 searches,
  dealt in turn across the servers.

  3 servers, each with its own bucket:
  30 allowed, not 10.

  scaled out to 6 servers, the same 90:
  60 allowed.""",
        narration=(
            'First demo: a bucket in each server. [[slnc 400]] Each of '
            'the three servers keeps its own bucket for each client, in '
            'its own memory. [[slnc 500]] Client forty-two sends ninety '
            'searches. [[slnc 300]] The load balancer deals them out, '
            'thirty to each server. [[slnc 500]] Each server sees a fresh '
            'client, with a full bucket. [[slnc 300]] So each lets ten '
            'through. [[slnc 300]] Thirty searches are allowed, not ten. '
            '[[slnc 600]] Now the shop grows to six servers, and the same '
            'ninety searches arrive. [[slnc 300]] Sixty are allowed. '
            '[[slnc 500]] Every server the shop adds loosens the limit by '
            'another ten. [[slnc 300]] The limit gets weaker just when '
            'the shop is busiest.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="The Tools' Words",
        body=['Redis: a shared whiteboard, over the network.', 'Key: a heading on it. One per client.',
              'Time to live: a countdown to deletion.', '',
              'Bucket4j: the token bucket, in Java.', 'Proxy manager: fetches a bucket from',
              'Redis and writes it back.', '',
              'Compare-and-swap: write only if nothing', 'changed since you read it.',
              'Client clock: the server\'s own clock.'],
        narration=(
            'Before the next demo, some words, in plain language. [[slnc '
            '500]] Think of a shared whiteboard that anyone in the office '
            'can read, wipe, and write on. [[slnc 300]] Redis is that '
            'whiteboard. [[slnc 300]] It is a separate program that keeps '
            'small values in memory. [[slnc 300]] And many programs can '
            'read and change them over the network. [[slnc 500]] A '
            'heading on the whiteboard is called a key. [[slnc 300]] '
            'Here, there is one key per client. [[slnc 300]] And a '
            'countdown, after which a key deletes itself, is called its '
            'time to live. [[slnc 600]] Bucket four J is the Java library '
            'that runs the token bucket. [[slnc 300]] It fetches a '
            "client's bucket from Redis, and writes it back. [[slnc 500]] "
            'When it writes, it only writes if nobody has changed the '
            'bucket since it read it. [[slnc 300]] If someone has, it '
            'reads again, and tries again. [[slnc 300]] That is called '
            'compare and swap. [[slnc 500]] And to work out how many '
            'tokens have come back, it uses the clock of the server it '
            'runs on.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='One Bucket In Redis',
        body="""TWO. One bucket in Redis.
  3 servers, one Redis. client-42 sends 90:
  10 allowed, 80 refused.

  scaled out to 6 servers,
  client-77 sends 90: 10 allowed.
  Redis holds 2 keys: one bucket per client.

  server-1 is restarted with empty memory.
  client-42's next search: refused.
  retry after 60 minutes.""",
        narration=(
            'Second demo: one bucket, in Redis. [[slnc 400]] Now no '
            'server keeps a bucket at all. [[slnc 300]] On every search, '
            "each server asks Redis for the client's bucket. [[slnc 600]] "
            'Client forty-two sends ninety searches through three '
            'servers. [[slnc 300]] Ten are allowed, and eighty are '
            'refused. [[slnc 500]] The shop grows to six servers. [[slnc '
            '300]] And a second robot, client seventy-seven, sends '
            'ninety. [[slnc 300]] Still only ten are allowed. [[slnc '
            '300]] Redis holds two keys: one bucket per client, not one '
            'per server. [[slnc 600]] Then server one is restarted, and '
            'comes back with empty memory. [[slnc 300]] Client '
            "forty-two's next search is refused. [[slnc 300]] And the "
            'refusal says: come back in sixty minutes. [[slnc 500]] The '
            'bucket was never inside the server. [[slnc 300]] So '
            'restarting the server does not refill it. [[slnc 300]] In '
            'the plain Java version, a restart gave every client a full '
            'bucket.'
        ),
    ),
    dict(
        key='06-diagram', kind='diagram', title='Where The Bucket Lives',
        body=None,
        narration=(
            'Here is where everything lives, in words. [[slnc 400]] '
            'Client forty-two sends a search. [[slnc 300]] The load '
            'balancer hands it to the next server. [[slnc 300]] That '
            'server runs Bucket four J, which does three things. [[slnc '
            "500]] It reads the client's bucket from Redis. [[slnc 300]] "
            'It does the sums on the server: how many tokens have come '
            'back, and is there one to spend? [[slnc 300]] And it writes '
            'the new bucket back to Redis, only if nobody changed it in '
            'between. [[slnc 600]] So Redis keeps the bucket, and the '
            'servers do the sums. [[slnc 300]] Remember that, because the '
            'fifth demo turns on it.'
        ),
    ),
    dict(
        key='07-three', kind='console', title='All At The Same Moment',
        body="""THREE. All at the same moment.
  3 servers, 30 searches each.
  all 90 released at the same instant,
  on 90 threads:

  10 allowed, 80 refused.

  no server holds a lock. each writes back
  only if the bucket has not changed,
  and reads again if it has.""",
        narration=(
            'Third demo: everything at the same moment. [[slnc 400]] '
            'Sending searches one after another is the easy case. [[slnc '
            '300]] So now, ninety searches, thirty on each of three '
            'servers, each on its own thread. [[slnc 300]] They are held '
            'at a gate, and released at the same instant. [[slnc 600]] '
            'Exactly ten are allowed, and eighty refused. [[slnc 600]] No '
            'server holds a lock. [[slnc 300]] No server waits its turn. '
            '[[slnc 300]] Each one only writes its answer back if the '
            'bucket has not changed since it read it. [[slnc 300]] The '
            'ones that lose that race just read again, and try again. '
            '[[slnc 500]] The order in which they reach Redis changes on '
            'every run. [[slnc 300]] The count that comes out does not.'
        ),
    ),
    dict(
        key='08-four', kind='console', title='Why Not Just A Number?',
        body="""FOUR. Why not just a number in Redis?
  one token left.
  server-1 reads 1. server-2 reads 1.
  both write back 0 and serve:
  2 searches from 1 token. Redis now says 0.

  again, writing only if still what was read:
  server-2's write is turned down.
  it reads again, finds 0, and refuses.
  1 search from 1 token, 1 refused, 1 retry.""",
        narration=(
            'Fourth demo: why go to all that trouble? [[slnc 400]] The '
            'first thing most people write is a plain number in Redis. '
            '[[slnc 300]] Read it, check it, and write it back, one '
            "lower. [[slnc 600]] The demo arranges two servers' steps by "
            'hand, so this happens on every run. [[slnc 300]] One token '
            'is left. [[slnc 300]] Server one reads one. [[slnc 300]] '
            'Server two reads one. [[slnc 300]] Both write back zero, and '
            'both serve a search. [[slnc 300]] Two searches, from one '
            'token. [[slnc 500]] And afterwards, Redis says zero, so '
            'nothing looks wrong. [[slnc 300]] That is what makes it '
            'dangerous. [[slnc 600]] Now the same again, but each write '
            'only lands if the number is still what was read. [[slnc '
            "300]] Server one's write lands. [[slnc 300]] Server two's is "
            'turned down. [[slnc 300]] It reads again, finds zero, and '
            'refuses. [[slnc 300]] One search, from one token. [[slnc '
            '500]] That careful way is what Bucket four J does on every '
            'search.'
        ),
    ),
    dict(
        key='09-code', kind='code', title='The Whole Pattern, In One Builder',
        body="""buckets = Bucket4jLettuce
    .casBasedBuilder(connection)
    .clientClock(clockThatIsAheadBy(clockAhead))
    .expirationAfterWrite(
        basedOnTimeForRefillingBucketUpToMax(
            Duration.ZERO))
    .build();

buckets.getProxy(
        SearchLimit.keyFor(clientId),
        SearchLimit::configuration)
    .tryConsume(1);""",
        narration=(
            'In the code, the whole pattern is one chain of settings on '
            "each server. [[slnc 500]] It is built on the server's own "
            'connection to Redis. [[slnc 300]] It uses compare and swap: '
            'the careful write from the fourth demo. [[slnc 500]] It is '
            'given the clock this server will use for its sums. [[slnc '
            '300]] And it is told to put a countdown on each key. [[slnc '
            '300]] So Redis deletes a bucket by itself, once that bucket '
            'would be full again. [[slnc 600]] Then, on every search, the '
            "server asks for this client's bucket, with the rule of ten "
            'an hour. [[slnc 300]] And it tries to spend one token. '
            '[[slnc 300]] The answer is yes, or no.'
        ),
    ),
    dict(
        key='10-five', kind='console', title='Whose Clock?',
        body="""FIVE. Whose clock?
  server-1 and server-2 have correct clocks.
  client-42 spends 10 searches through them.
  the next: refused.

  server-3's clock runs one hour fast.
  client-42 sends 20 through it:
  10 allowed.

  Redis keeps the bucket. the sums are done
  on each server, with that server's clock.""",
        narration=(
            'Fifth demo, and this is the headline of the project. [[slnc '
            '400]] Two servers, with correct clocks, spend client '
            "forty-two's ten searches. [[slnc 300]] The next search is "
            'refused. [[slnc 300]] The bucket is empty. [[slnc 600]] Now '
            'a third server joins. [[slnc 300]] And its clock runs one '
            'hour fast. [[slnc 500]] Client forty-two sends twenty '
            'searches through it. [[slnc 300]] Ten are allowed. [[slnc '
            '600]] The fast server read the empty bucket. [[slnc 300]] By '
            'its own clock, an hour had passed since the bucket was last '
            'filled. [[slnc 300]] So it refilled the bucket, spent a '
            'token, and wrote the result to Redis. [[slnc 300]] Redis '
            'stored it, because Redis never looks at a clock. [[slnc '
            '600]] Redis keeps the bucket. [[slnc 300]] But each server '
            'does the sums, with its own clock. [[slnc 300]] A limit '
            'shared by every server is only as good as the worst clock '
            'among them.'
        ),
    ),
    dict(
        key='11-clocks', kind='bullets', title='The Clocks Must Agree',
        body=['The hand-built twin had one clock.', 'Time could not disagree with itself.', '',
              'Here every server brings its own.', 'A clock that runs fast refills early,',
              'for every server at once.', '',
              '✓ Keep the servers\' clocks in step.', '✓ Watch for drift like any other fault.'],
        narration=(
            'Why could the plain Java version never show this? [[slnc '
            '400]] It had one clock, moved by hand in the demo. [[slnc '
            '300]] So time could never disagree with itself. [[slnc 600]] '
            'Here, every server brings its own clock. [[slnc 300]] A '
            'server whose clock runs fast thinks the refill time has come '
            'early. [[slnc 300]] And because the bucket is shared, it '
            'refills early for every server at once. [[slnc 600]] So the '
            "rule is simple. [[slnc 300]] Keep the servers' clocks in "
            'step. [[slnc 300]] And treat a clock that drifts like any '
            'other fault.'
        ),
    ),
    dict(
        key='12-six', kind='console', title='The Bill',
        body="""SIX. The bill.
  1000 different clients search once each:
  Redis holds 1000 keys, each set to
  delete itself in 60 minutes.

  Redis is stopped. 5 searches:
  5 errors from the limiter, and no answer.
  the shop must choose.

  this demo needed 1 container for 6 servers.""",
        narration=(
            'Sixth demo: the bill. [[slnc 400]] A thousand different '
            'clients search once each. [[slnc 300]] And Redis holds a '
            'thousand keys. [[slnc 500]] Each key deletes itself after '
            'sixty minutes, when its bucket would be full again. [[slnc '
            '300]] Because a full bucket and no bucket mean the same '
            'thing. [[slnc 300]] So the keys do not pile up forever. '
            '[[slnc 600]] Then Redis is stopped. [[slnc 300]] Five '
            'searches reach the limiter, and get five errors. [[slnc '
            '300]] Not a yes, and not a no. [[slnc 500]] Let them '
            'through, and there is no limit at all. [[slnc 300]] Refuse '
            'them, and five real customers see an error. [[slnc 300]] '
            'Bucket four J cannot choose for you. [[slnc 300]] The shop '
            'must. [[slnc 600]] And every search, allowed or not, now '
            'waits for a trip across the network to Redis.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['✓ It got the bucket right: tokens, refill,', '   a bucket per client, when to come back.',
              '✓ It found the leak: 3 servers, 30 allowed.', '',
              '✗ Nowhere outside the servers to keep it.', '✗ One search at a time: no lost update.',
              '✗ One clock: time could not disagree.', '✗ A bucket cannot go down.'],
        narration=(
            'So what did the plain Java version get right? [[slnc 400]] '
            'All of the bucket. [[slnc 300]] Tokens, one per search. '
            '[[slnc 200]] A refusal when empty. [[slnc 200]] A refill on '
            'a timer. [[slnc 200]] A bucket per client. [[slnc 200]] And '
            'a refusal that says when to come back. [[slnc 300]] It even '
            'found the leak: three servers with a bucket each let thirty '
            'through. [[slnc 600]] What it left out was everything that '
            'happens when the bucket lives somewhere else. [[slnc 500]] '
            'Inside one program, there was nowhere outside the servers to '
            'keep it. [[slnc 300]] It ran one search at a time, so two '
            'servers could never read the same last token. [[slnc 300]] '
            'It had one clock, so time could never disagree. [[slnc 300]] '
            'And a bucket kept in memory can never be unreachable.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Many servers? Keep the bucket outside', 'all of them, where they can all reach it.', '',
              '1. Make the check and the write one step.', '2. Keep the servers\' clocks in step.',
              '3. Decide what an error from the store', '   means: let through, or refuse.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] When a service runs as '
            'more than one copy, keep the bucket outside all of them. '
            '[[slnc 300]] In a store they can all reach. [[slnc 600]] '
            'Then settle three things, because the store will not. [[slnc '
            '500]] One. [[slnc 200]] The check and the write must be one '
            "step. [[slnc 300]] Bucket four J's compare and swap does "
            'that. [[slnc 300]] A plain number does not. [[slnc 400]] '
            "Two. [[slnc 200]] The servers' clocks must agree, because "
            'they, not Redis, do the refill sums. [[slnc 400]] Three. '
            '[[slnc 200]] Someone must decide what the limiter answers '
            'when the store cannot be reached.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Redis 8.10.2, Bucket4j 8.20.0,', 'Lettuce 7.7.0, Testcontainers 2.0.5,',
              'in a container the demo starts and stops.', '',
              'Too much on one server: an in-memory', 'bucket is exact, free, and never down.',
              'Roughly right is enough? A bucket per', 'server with the limit divided up.', '',
              'Redis is a system to run and watch.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The store '
            'is Redis, version eight point ten point two, the newest '
            'release. [[slnc 300]] It runs in a container that the demo '
            'starts and stops by itself. [[slnc 300]] Bucket four J is '
            'version eight point twenty. [[slnc 300]] You just need '
            'Docker switched on first. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 600]] So, "
            'when is this too much? [[slnc 300]] On one server, a bucket '
            'in memory is exact, free, and can never go down. [[slnc '
            '300]] If the limit only needs to be roughly right, give each '
            'server a share of the limit, with no network trip. [[slnc '
            '500]] Redis is one more system to run and watch. [[slnc '
            '300]] It earns its place when there are many servers, and '
            'the limit must be one number however many there are.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Rate Limiter, with Redis. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Redis '
            'keeps the bucket, but the servers do the sums, so the write '
            'must be careful, and the clocks must agree. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            "one exercise to try. [[slnc 300]] Make the fast server's "
            'clock run an hour slow instead. [[slnc 300]] Guess how many '
            'searches it allows, and then run it. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
