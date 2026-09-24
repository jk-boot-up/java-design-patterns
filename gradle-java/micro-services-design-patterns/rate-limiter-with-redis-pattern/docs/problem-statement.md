# Problem Statement

## The scenario

The shop's product search is open to the world. Customers use it, and so do price-comparison robots, one of which, client-42, sends searches as fast as it can. The rule is 10 searches per client, filled back up once an hour. The search service does not run as one copy: it runs as three copies behind a load balancer, which deals incoming searches to them in turn, and on a busy day the shop scales out to six. The rule has to mean 10 however many copies are running.

## The naive version

Each copy of the search service keeps its own bucket for each client, in its own memory, exactly as a single server would.

```
  3 servers, each with its own bucket: 30 allowed, not 10.
  scaled out to 6 servers, the same 90: 60 allowed. every server added loosens the limit by another 10.
```

## What the twin project already did

The plain-Java Rate Limiter project in this course built the token bucket: a bucket of tokens per client, one token per search, a refusal when it is empty, a refill on a timer, and a refusal that says when to come back. It is a complete teaching of the idea and nothing here replaces it. Its last act found this same leak: three servers with a bucket each let three times the limit through.

What it could not do was fix the leak, because inside one Java program there is nowhere for a bucket to live that separate servers can all reach. It also had one clock, moved by hand, and ran one search at a time, so it could never show two servers reading the same last token, or two servers disagreeing about the time.

## What this project must deliver

The same shop and the same rule, with each client's bucket moved into a real Redis server that the demo starts in a container and stops at the end, and with Bucket4j doing the bucket arithmetic on each server. Three servers and then six sharing one bucket and letting exactly 10 through. A restarted server that finds the bucket still empty. Ninety searches released at the same instant on ninety threads, and still exactly 10 allowed. Two servers spending the same last token when the count is read and written in two steps, and the conditional write that stops it. A server whose clock runs an hour fast refilling the bucket for everyone. And an honest bill: a key per client, what happens when Redis is stopped, and a network trip on every search.

Every figure printed is Redis's own, and two runs back to back print the same thing.
