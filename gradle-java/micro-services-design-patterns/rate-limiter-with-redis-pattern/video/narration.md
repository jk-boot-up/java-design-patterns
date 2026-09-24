# Rate Limiter with Redis Pattern — Video Narration Script

## 1. Rate Limiter with Redis

Hello, and welcome. This video explains the Rate Limiter pattern in Java, using a real Redis server and a library called Bucket4j. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. A rate limiter gives each caller a bucket of tokens. Every request spends one token. When the bucket is empty, the request is refused, and the bucket is filled up again on a timer. Now the same thing in our online store. The shop has a product search. A price-comparison robot sends searches as fast as it can, and the shop allows each client ten searches, filled back up once an hour. The search runs as several copies on several servers, so the ten has to mean ten, however many copies are running. By the end you will have seen the limit leak when each server keeps its own bucket, hold when the bucket moves into Redis, survive ninety searches at the same instant, and be broken by one server whose clock runs an hour fast.

## 2. The Scenario

Here is the scenario. The shop's product search is open to the world. Customers use it, and so does a price-comparison robot, which we will call client forty-two. The rule is ten searches per client, filled back up once an hour. The hour is deliberate. The demo runs for a few seconds, so no token comes back while it runs, and every count is exact on every machine. The search service runs as three copies, on three servers, behind a load balancer. A load balancer is the part that deals each incoming search to the next server in turn. On a busy day the shop runs six copies. The hand-built twin of this project kept each bucket inside one Java program. This time the bucket has to work across separate programs.

## 3. A Bucket In Each Server

Act one. Each of the three servers keeps its own bucket for each client, in its own memory, exactly as a single server would. Client forty-two sends ninety searches, and the load balancer deals them out, thirty to each server. Each server sees a fresh client with a full bucket, and lets ten through. So thirty searches are allowed, not ten. Now the shop scales out to six servers, and the same ninety searches arrive. Sixty are allowed. Every server the shop adds loosens the limit by another ten. The limit gets weaker at exactly the moment the shop is busiest.

## 4. The Tools' Words

Before the next act, the tools' words, each in plain language first. Think of a shared whiteboard, which anyone in the office can read, rub out and write on. Redis is that whiteboard: a separate program that keeps small values in memory, and lets many programs read and change them over the network. A heading on the whiteboard, the name a value is kept under, is what Redis calls a key. Here there is one key per client. A countdown after which a key deletes itself is its time to live. Bucket4j is the Java library that does the token bucket. The part of it that fetches a client's bucket from Redis and writes it back is called the proxy manager. When it writes, it writes only if nobody has changed the bucket since it read it, and if somebody has, it reads again and tries again. Bucket4j calls that compare-and-swap. And the clock it uses to work out how many tokens have come back is the clock of the server it runs on. It calls that the client clock.

## 5. One Bucket In Redis

Act two. Now no server keeps a bucket at all. Each has its own connection to one Redis, and on every search it asks Redis for the client's bucket. Client forty-two sends ninety searches through three servers. Ten are allowed, and eighty refused. The shop scales out to six servers, and a second robot, client seventy-seven, sends ninety. Still ten. Redis is holding two keys: one bucket per client, not one per server. Then server one is restarted, and comes back with empty memory. Client forty-two's next search is refused, and the refusal says to come back in sixty minutes. The bucket was never in the server, so restarting the server does not refill it. In the hand-built twin, a restart handed every client a full bucket.

## 6. Where The Bucket Lives

Here is where everything lives, in words. Client forty-two sends a search. The load balancer hands it to the next server. That server runs Bucket4j, and Bucket4j does three things. It reads the client's bucket from Redis. It does the sum on the server: how many tokens have come back since the last visit, and is there one to spend. And it writes the new bucket back to Redis, only if nobody changed it in between. So Redis keeps the bucket, and the servers do the sums. Hold on to that sentence, because the fifth act turns on it.

## 7. All At The Same Moment

Act three. Sending searches one after another is the easy case. So now ninety searches, thirty on each of three servers, each on its own thread, are held at a gate and released at the same instant. Exactly ten are allowed, and eighty refused. No server holds a lock, and no server waits its turn. Each one writes its answer back only if the bucket has not changed since it read it. The ones that lose that race simply read again and try again. The order the threads reach Redis is different on every run. The count that comes out is not.

## 8. Why Not Just A Number?

Act four asks why Bucket4j goes to that trouble. The first thing most people write is a plain number in Redis: read it, check it, write it back one lower. The demo puts two servers' steps in a fixed order by hand, so this happens on every run, not only on a busy day. One token is left. Server one reads one. Server two reads one. Both write back zero, and both serve a search. Two searches, from one token. And afterwards Redis says zero, so nothing looks wrong. That is what makes it dangerous. Now the same again, but each write lands only if the number is still what was read. Server one's write lands. Server two's is turned down. It reads again, finds zero, and refuses. One search from one token. That second way is what Bucket4j does on every search.

## 9. The Whole Pattern, In One Builder

In the code, the whole pattern is one builder chain on each server. It is built on the server's own connection to Redis. The name of the method says compare-and-swap, the careful write from act four. The builder is given the clock this server will use for its sums. It is told to set a countdown on each key, so Redis deletes a bucket by itself once the bucket would be full again. Then, on every search, the server asks for the bucket under the key for this client, with the rule of ten an hour, and tries to spend one token. The answer is yes or no.

## 10. Whose Clock?

Act five is the headline of this project. Two servers with correct clocks spend client forty-two's ten searches, and the next one is refused. The bucket is empty. Now a third server joins, and its clock runs one hour fast. Client forty-two sends twenty searches through it. Ten are allowed. The fast server read the empty bucket. By its own clock, an hour had passed since the bucket was last filled. So it filled the bucket, spent a token, and wrote the answer to Redis. Redis stored it, because Redis never looks at a clock. Redis keeps the bucket. The sums are done on each server, with that server's clock. A limit shared by every server is only as good as the worst clock among them.

## 11. The Clocks Must Agree

Why could the hand-built twin never show this? It had one clock, a test clock the demo moved by hand, so time could never disagree with itself. Here, every server brings its own clock. A server whose clock runs fast decides the refill time has come early, and because the bucket is shared, it refills early for every server at once. So the rule is simple. Keep the servers' clocks in step, and treat a clock that drifts like any other fault.

## 12. The Bill

Act six is the bill. One thousand different clients search once each, and Redis holds one thousand keys. Each is set to delete itself in sixty minutes, when its bucket would be full again, because a full bucket and no bucket mean the same thing. So the keys do not pile up for ever. Then Redis is stopped. Five searches reach the limiter, and get five errors. Not a yes, and not a no. Let them through, and there is no limit at all. Refuse them, and five real customers see an error. Bucket4j cannot choose for you. The shop must. And every search, allowed or not, now waits for a trip across the network to Redis before it is served. One container, for six servers.

## 13. What The Simulation Left Out

So what did the hand-built simulation get right? All of the bucket. Tokens, one per search, a refusal when it is empty, a refill on a timer, a bucket per client, and a refusal that says when to come back. And it found the leak: three servers with a bucket each let thirty through. What it left out were the things that only happen when the bucket lives somewhere else. Inside one program, there was nowhere outside the servers to keep it. It ran one search at a time, so two servers could never read the same last token. It had one clock, so time could never disagree. And a bucket that is a field in memory can never be unreachable.

## 14. The Verdict

The verdict. When a service runs as more than one copy, keep the bucket outside all of them, in a store they can all reach. Then say three things out loud, because the store will not. One. The check and the write must be one step. Bucket4j's compare-and-swap does that for you, and a plain number does not. Two. The servers' clocks must agree, because they, not Redis, do the refill sums. Three. Somebody must decide what the limiter answers when the store cannot be reached.

## 15. What Is Real, And When Not

What is real here? The store is Redis, version eight point ten point two, the newest release, running in a container that the demo starts at the beginning and stops at the end, on a random free port. Bucket4j is version eight point twenty, and it talks to Redis through a client library called Lettuce. Nothing is installed and nothing is left running. The one thing you need is a container runtime, such as Docker Desktop, switched on before you start. Every number in this video comes from the program's own output, and two runs one after the other print the same thing. So when is this too much? On one server, a bucket in memory, like the twin's, is exact, free, and cannot go down. If a limit only needs to be roughly right, a bucket per server with the limit divided between them costs no network trip. Redis is one more system to run and watch. It earns that when there are many servers, and the limit has to be one number however many there are.

## 16. Thanks for Watching

That's Rate Limiter with Redis. If you take one sentence away, take this one: Redis keeps the bucket, but the servers do the sums, so the write must be careful and the clocks must agree. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, make the fast server's clock run an hour slow instead, guess how many searches it allows, and then run it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
