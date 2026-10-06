# Rate Limiter with Redis Pattern — Video Narration Script

## 1. Rate Limiter with Redis

Hello, and welcome. This video explains the Rate Limiter pattern in Java, using a real Redis server, and a library called Bucket four J. This video is presented by Jayasekhar Konduru. First, a simple definition. A rate limiter gives each caller a bucket of tokens. Every request spends one token. When the bucket is empty, the request is refused. And the bucket is filled up again on a timer. In our online store, there is a product search. A price-comparison robot sends searches as fast as it can. So the shop allows each client ten searches, filled back up once an hour. The search runs as several copies, on several servers. So ten has to mean ten, however many copies are running. By the end, you will hear the limit leak when each server keeps its own bucket. Hold when the bucket moves into Redis. Survive ninety searches at the same instant. And be broken by one server whose clock runs an hour fast.

## 2. The Scenario

Here is the scenario. The shop's product search is open to the world. Customers use it, and so does a price-comparison robot, called client forty-two. The rule is ten searches per client, filled back up once an hour. The hour is deliberate. The demo only runs for a few seconds, so no token comes back during it. And every count is exact. The search service runs as three copies, on three servers. In front of them sits a load balancer, which deals each search to the next server in turn. On a busy day, the shop runs six copies. The plain Java version kept each bucket inside one program. This time, the bucket has to work across separate programs.

## 3. A Bucket In Each Server

First demo: a bucket in each server. Each of the three servers keeps its own bucket for each client, in its own memory. Client forty-two sends ninety searches. The load balancer deals them out, thirty to each server. Each server sees a fresh client, with a full bucket. So each lets ten through. Thirty searches are allowed, not ten. Now the shop grows to six servers, and the same ninety searches arrive. Sixty are allowed. Every server the shop adds loosens the limit by another ten. The limit gets weaker just when the shop is busiest.

## 4. The Tools' Words

Before the next demo, some words, in plain language. Think of a shared whiteboard that anyone in the office can read, wipe, and write on. Redis is that whiteboard. It is a separate program that keeps small values in memory. And many programs can read and change them over the network. A heading on the whiteboard is called a key. Here, there is one key per client. And a countdown, after which a key deletes itself, is called its time to live. Bucket four J is the Java library that runs the token bucket. It fetches a client's bucket from Redis, and writes it back. When it writes, it only writes if nobody has changed the bucket since it read it. If someone has, it reads again, and tries again. That is called compare and swap. And to work out how many tokens have come back, it uses the clock of the server it runs on.

## 5. One Bucket In Redis

Second demo: one bucket, in Redis. Now no server keeps a bucket at all. On every search, each server asks Redis for the client's bucket. Client forty-two sends ninety searches through three servers. Ten are allowed, and eighty are refused. The shop grows to six servers. And a second robot, client seventy-seven, sends ninety. Still only ten are allowed. Redis holds two keys: one bucket per client, not one per server. Then server one is restarted, and comes back with empty memory. Client forty-two's next search is refused. And the refusal says: come back in sixty minutes. The bucket was never inside the server. So restarting the server does not refill it. In the plain Java version, a restart gave every client a full bucket.

## 6. Where The Bucket Lives

Here is where everything lives, in words. Client forty-two sends a search. The load balancer hands it to the next server. That server runs Bucket four J, which does three things. It reads the client's bucket from Redis. It does the sums on the server: how many tokens have come back, and is there one to spend? And it writes the new bucket back to Redis, only if nobody changed it in between. So Redis keeps the bucket, and the servers do the sums. Remember that, because the fifth demo turns on it.

## 7. All At The Same Moment

Third demo: everything at the same moment. Sending searches one after another is the easy case. So now, ninety searches, thirty on each of three servers, each on its own thread. They are held at a gate, and released at the same instant. Exactly ten are allowed, and eighty refused. No server holds a lock. No server waits its turn. Each one only writes its answer back if the bucket has not changed since it read it. The ones that lose that race just read again, and try again. The order in which they reach Redis changes on every run. The count that comes out does not.

## 8. Why Not Just A Number?

Fourth demo: why go to all that trouble? The first thing most people write is a plain number in Redis. Read it, check it, and write it back, one lower. The demo arranges two servers' steps by hand, so this happens on every run. One token is left. Server one reads one. Server two reads one. Both write back zero, and both serve a search. Two searches, from one token. And afterwards, Redis says zero, so nothing looks wrong. That is what makes it dangerous. Now the same again, but each write only lands if the number is still what was read. Server one's write lands. Server two's is turned down. It reads again, finds zero, and refuses. One search, from one token. That careful way is what Bucket four J does on every search.

## 9. The Whole Pattern, In One Builder

In the code, the whole pattern is one chain of settings on each server. It is built on the server's own connection to Redis. It uses compare and swap: the careful write from the fourth demo. It is given the clock this server will use for its sums. And it is told to put a countdown on each key. So Redis deletes a bucket by itself, once that bucket would be full again. Then, on every search, the server asks for this client's bucket, with the rule of ten an hour. And it tries to spend one token. The answer is yes, or no.

## 10. Whose Clock?

Fifth demo, and this is the headline of the project. Two servers, with correct clocks, spend client forty-two's ten searches. The next search is refused. The bucket is empty. Now a third server joins. And its clock runs one hour fast. Client forty-two sends twenty searches through it. Ten are allowed. The fast server read the empty bucket. By its own clock, an hour had passed since the bucket was last filled. So it refilled the bucket, spent a token, and wrote the result to Redis. Redis stored it, because Redis never looks at a clock. Redis keeps the bucket. But each server does the sums, with its own clock. A limit shared by every server is only as good as the worst clock among them.

## 11. The Clocks Must Agree

Why could the plain Java version never show this? It had one clock, moved by hand in the demo. So time could never disagree with itself. Here, every server brings its own clock. A server whose clock runs fast thinks the refill time has come early. And because the bucket is shared, it refills early for every server at once. So the rule is simple. Keep the servers' clocks in step. And treat a clock that drifts like any other fault.

## 12. The Bill

Sixth demo: the bill. A thousand different clients search once each. And Redis holds a thousand keys. Each key deletes itself after sixty minutes, when its bucket would be full again. Because a full bucket and no bucket mean the same thing. So the keys do not pile up forever. Then Redis is stopped. Five searches reach the limiter, and get five errors. Not a yes, and not a no. Let them through, and there is no limit at all. Refuse them, and five real customers see an error. Bucket four J cannot choose for you. The shop must. And every search, allowed or not, now waits for a trip across the network to Redis.

## 13. What The Simulation Left Out

So what did the plain Java version get right? All of the bucket. Tokens, one per search. A refusal when empty. A refill on a timer. A bucket per client. And a refusal that says when to come back. It even found the leak: three servers with a bucket each let thirty through. What it left out was everything that happens when the bucket lives somewhere else. Inside one program, there was nowhere outside the servers to keep it. It ran one search at a time, so two servers could never read the same last token. It had one clock, so time could never disagree. And a bucket kept in memory can never be unreachable.

## 14. The Verdict

So, here is the verdict. When a service runs as more than one copy, keep the bucket outside all of them. In a store they can all reach. Then settle three things, because the store will not. One. The check and the write must be one step. Bucket four J's compare and swap does that. A plain number does not. Two. The servers' clocks must agree, because they, not Redis, do the refill sums. Three. Someone must decide what the limiter answers when the store cannot be reached.

## 15. What Is Real, And When Not

A quick, honest note about this demo. The store is Redis, version eight point ten point two, the newest release. It runs in a container that the demo starts and stops by itself. Bucket four J is version eight point twenty. You just need Docker switched on first. Every number you heard comes from the program's own output. So, when is this too much? On one server, a bucket in memory is exact, free, and can never go down. If the limit only needs to be roughly right, give each server a share of the limit, with no network trip. Redis is one more system to run and watch. It earns its place when there are many servers, and the limit must be one number however many there are.

## 16. Thanks for Watching

That's Rate Limiter, with Redis. If you remember one sentence, make it this one. Redis keeps the bucket, but the servers do the sums, so the write must be careful, and the clocks must agree. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make the fast server's clock run an hour slow instead. Guess how many searches it allows, and then run it. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
