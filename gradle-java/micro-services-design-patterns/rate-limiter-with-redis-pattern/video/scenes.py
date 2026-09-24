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
            'Hello, and welcome. This video explains the Rate Limiter '
            'pattern in Java, using a real Redis server and a library '
            'called Bucket4j. [[slnc 250]] It is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] Here is the plain '
            'definition, in general words. A rate limiter gives each '
            'caller a bucket of tokens. Every request spends one token. '
            'When the bucket is empty, the request is refused, and the '
            'bucket is filled up again on a timer. [[slnc 350]] Now the '
            'same thing in our online store. The shop has a product search. '
            'A price-comparison robot sends searches as fast as it can, and '
            'the shop allows each client ten searches, filled back up once '
            'an hour. The search runs as several copies on several '
            'servers, so the ten has to mean ten, however many copies are '
            'running. [[slnc 300]] By the end you will have seen the limit '
            'leak when each server keeps its own bucket, hold when the '
            'bucket moves into Redis, survive ninety searches at the same '
            'instant, and be broken by one server whose clock runs an hour '
            'fast.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Product search, open to the world.', 'client-42 is a price-comparison robot.', '',
              'The rule: 10 searches per client,', 'filled back up once an hour.', '',
              'The search runs as 3 copies behind', 'a load balancer, and 6 on a busy day.', '',
              'The hand-built twin kept each bucket', 'inside one program.'],
        narration=(
            'Here is the scenario. The shop\'s product search is open to '
            'the world. Customers use it, and so does a price-comparison '
            'robot, which we will call client forty-two. [[slnc 250]] The '
            'rule is ten searches per client, filled back up once an hour. '
            'The hour is deliberate. The demo runs for a few seconds, so no '
            'token comes back while it runs, and every count is exact on '
            'every machine. [[slnc 300]] The search service runs as three '
            'copies, on three servers, behind a load balancer. A load '
            'balancer is the part that deals each incoming search to the '
            'next server in turn. On a busy day the shop runs six copies. '
            '[[slnc 250]] The hand-built twin of this project kept each '
            'bucket inside one Java program. This time the bucket has to '
            'work across separate programs.'
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
            'Act one. Each of the three servers keeps its own bucket for '
            'each client, in its own memory, exactly as a single server '
            'would. Client forty-two sends ninety searches, and the load '
            'balancer deals them out, thirty to each server. [[slnc 250]] '
            'Each server sees a fresh client with a full bucket, and lets '
            'ten through. So thirty searches are allowed, not ten. '
            '[[slnc 300]] Now the shop scales out to six servers, and the '
            'same ninety searches arrive. Sixty are allowed. Every server '
            'the shop adds loosens the limit by another ten. The limit '
            'gets weaker at exactly the moment the shop is busiest.'
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
            'Before the next act, the tools\' words, each in plain language '
            'first. [[slnc 250]] Think of a shared whiteboard, which anyone '
            'in the office can read, rub out and write on. Redis is that '
            'whiteboard: a separate program that keeps small values in '
            'memory, and lets many programs read and change them over the '
            'network. A heading on the whiteboard, the name a value is '
            'kept under, is what Redis calls a key. Here there is one key '
            'per client. A countdown after which a key deletes itself is '
            'its time to live. [[slnc 300]] Bucket4j is the Java library '
            'that does the token bucket. The part of it that fetches a '
            'client\'s bucket from Redis and writes it back is called the '
            'proxy manager. [[slnc 250]] When it writes, it writes only if '
            'nobody has changed the bucket since it read it, and if '
            'somebody has, it reads again and tries again. Bucket4j calls '
            'that compare-and-swap. [[slnc 250]] And the clock it uses to '
            'work out how many tokens have come back is the clock of the '
            'server it runs on. It calls that the client clock.'
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
            'Act two. Now no server keeps a bucket at all. Each has its own '
            'connection to one Redis, and on every search it asks Redis for '
            'the client\'s bucket. [[slnc 250]] Client forty-two sends '
            'ninety searches through three servers. Ten are allowed, and '
            'eighty refused. [[slnc 250]] The shop scales out to six '
            'servers, and a second robot, client seventy-seven, sends '
            'ninety. Still ten. Redis is holding two keys: one bucket per '
            'client, not one per server. [[slnc 300]] Then server one is '
            'restarted, and comes back with empty memory. Client '
            'forty-two\'s next search is refused, and the refusal says to '
            'come back in sixty minutes. The bucket was never in the '
            'server, so restarting the server does not refill it. In the '
            'hand-built twin, a restart handed every client a full bucket.'
        ),
    ),
    dict(
        key='06-diagram', kind='diagram', title='Where The Bucket Lives',
        body=None,
        narration=(
            'Here is where everything lives, in words. Client forty-two '
            'sends a search. The load balancer hands it to the next server. '
            'That server runs Bucket4j, and Bucket4j does three things. '
            'It reads the client\'s bucket from Redis. It does the sum on '
            'the server: how many tokens have come back since the last '
            'visit, and is there one to spend. And it writes the new bucket '
            'back to Redis, only if nobody changed it in between. '
            '[[slnc 300]] So Redis keeps the bucket, and the servers do the '
            'sums. Hold on to that sentence, because the fifth act turns on '
            'it.'
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
            'Act three. Sending searches one after another is the easy '
            'case. So now ninety searches, thirty on each of three servers, '
            'each on its own thread, are held at a gate and released at '
            'the same instant. [[slnc 250]] Exactly ten are allowed, and '
            'eighty refused. [[slnc 250]] No server holds a lock, and no '
            'server waits its turn. Each one writes its answer back only if '
            'the bucket has not changed since it read it. The ones that '
            'lose that race simply read again and try again. The order the '
            'threads reach Redis is different on every run. The count that '
            'comes out is not.'
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
            'Act four asks why Bucket4j goes to that trouble. The first '
            'thing most people write is a plain number in Redis: read it, '
            'check it, write it back one lower. [[slnc 250]] The demo puts '
            'two servers\' steps in a fixed order by hand, so this happens '
            'on every run, not only on a busy day. One token is left. '
            'Server one reads one. Server two reads one. Both write back '
            'zero, and both serve a search. Two searches, from one token. '
            '[[slnc 250]] And afterwards Redis says zero, so nothing looks '
            'wrong. That is what makes it dangerous. [[slnc 300]] Now the '
            'same again, but each write lands only if the number is still '
            'what was read. Server one\'s write lands. Server two\'s is '
            'turned down. It reads again, finds zero, and refuses. One '
            'search from one token. That second way is what Bucket4j does '
            'on every search.'
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
            'In the code, the whole pattern is one builder chain on each '
            'server. It is built on the server\'s own connection to Redis. '
            'The name of the method says compare-and-swap, the careful '
            'write from act four. [[slnc 250]] The builder is given the '
            'clock this server will use for its sums. It is told to set a '
            'countdown on each key, so Redis deletes a bucket by itself '
            'once the bucket would be full again. [[slnc 250]] Then, on '
            'every search, the server asks for the bucket under the key '
            'for this client, with the rule of ten an hour, and tries to '
            'spend one token. The answer is yes or no.'
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
            'Act five is the headline of this project. Two servers with '
            'correct clocks spend client forty-two\'s ten searches, and the '
            'next one is refused. The bucket is empty. [[slnc 300]] Now a '
            'third server joins, and its clock runs one hour fast. Client '
            'forty-two sends twenty searches through it. Ten are allowed. '
            '[[slnc 250]] The fast server read the empty bucket. By its own '
            'clock, an hour had passed since the bucket was last filled. '
            'So it filled the bucket, spent a token, and wrote the answer '
            'to Redis. Redis stored it, because Redis never looks at a '
            'clock. [[slnc 300]] Redis keeps the bucket. The sums are done '
            'on each server, with that server\'s clock. A limit shared by '
            'every server is only as good as the worst clock among them.'
        ),
    ),
    dict(
        key='11-clocks', kind='bullets', title='The Clocks Must Agree',
        body=['The hand-built twin had one clock.', 'Time could not disagree with itself.', '',
              'Here every server brings its own.', 'A clock that runs fast refills early,',
              'for every server at once.', '',
              '✓ Keep the servers\' clocks in step.', '✓ Watch for drift like any other fault.'],
        narration=(
            'Why could the hand-built twin never show this? It had one '
            'clock, a test clock the demo moved by hand, so time could '
            'never disagree with itself. [[slnc 250]] Here, every server '
            'brings its own clock. A server whose clock runs fast decides '
            'the refill time has come early, and because the bucket is '
            'shared, it refills early for every server at once. '
            '[[slnc 300]] So the rule is simple. Keep the servers\' clocks '
            'in step, and treat a clock that drifts like any other fault.'
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
            'Act six is the bill. One thousand different clients search '
            'once each, and Redis holds one thousand keys. Each is set to '
            'delete itself in sixty minutes, when its bucket would be full '
            'again, because a full bucket and no bucket mean the same '
            'thing. So the keys do not pile up for ever. [[slnc 300]] Then '
            'Redis is stopped. Five searches reach the limiter, and get '
            'five errors. Not a yes, and not a no. Let them through, and '
            'there is no limit at all. Refuse them, and five real customers '
            'see an error. Bucket4j cannot choose for you. The shop must. '
            '[[slnc 300]] And every search, allowed or not, now waits for a '
            'trip across the network to Redis before it is served. One '
            'container, for six servers.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['✓ It got the bucket right: tokens, refill,', '   a bucket per client, when to come back.',
              '✓ It found the leak: 3 servers, 30 allowed.', '',
              '✗ Nowhere outside the servers to keep it.', '✗ One search at a time: no lost update.',
              '✗ One clock: time could not disagree.', '✗ A bucket cannot go down.'],
        narration=(
            'So what did the hand-built simulation get right? All of the '
            'bucket. Tokens, one per search, a refusal when it is empty, a '
            'refill on a timer, a bucket per client, and a refusal that '
            'says when to come back. And it found the leak: three servers '
            'with a bucket each let thirty through. [[slnc 300]] What it '
            'left out were the things that only happen when the bucket '
            'lives somewhere else. Inside one program, there was nowhere '
            'outside the servers to keep it. It ran one search at a time, '
            'so two servers could never read the same last token. It had '
            'one clock, so time could never disagree. And a bucket that is '
            'a field in memory can never be unreachable.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Many servers? Keep the bucket outside', 'all of them, where they can all reach it.', '',
              '1. Make the check and the write one step.', '2. Keep the servers\' clocks in step.',
              '3. Decide what an error from the store', '   means: let through, or refuse.'],
        narration=(
            'The verdict. When a service runs as more than one copy, keep '
            'the bucket outside all of them, in a store they can all reach. '
            'Then say three things out loud, because the store will not. '
            '[[slnc 250]] One. The check and the write must be one step. '
            'Bucket4j\'s compare-and-swap does that for you, and a plain '
            'number does not. [[slnc 200]] Two. The servers\' clocks must '
            'agree, because they, not Redis, do the refill sums. '
            '[[slnc 200]] Three. Somebody must decide what the limiter '
            'answers when the store cannot be reached.'
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
            'What is real here? The store is Redis, version eight point '
            'ten point two, the newest release, running in a container '
            'that the demo starts at the beginning and stops at the end, on '
            'a random free port. Bucket4j is version eight point twenty, '
            'and it talks to Redis through a client library called Lettuce. '
            'Nothing is installed and nothing is left running. The one '
            'thing you need is a container runtime, such as Docker Desktop, '
            'switched on before you start. Every number in this video comes '
            'from the program\'s own output, and two runs one after the '
            'other print the same thing. [[slnc 300]] So when is this too '
            'much? On one server, a bucket in memory, like the twin\'s, is '
            'exact, free, and cannot go down. If a limit only needs to be '
            'roughly right, a bucket per server with the limit divided '
            'between them costs no network trip. [[slnc 250]] Redis is one '
            'more system to run and watch. It earns that when there are '
            'many servers, and the limit has to be one number however many '
            'there are.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Rate Limiter with Redis. [[slnc 250]] If you take one "
            'sentence away, take this one: Redis keeps the bucket, but the '
            'servers do the sums, so the write must be careful and the '
            'clocks must agree. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, make the '
            'fast server\'s clock run an hour slow instead, guess how many '
            'searches it allows, and then run it. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
