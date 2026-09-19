# Scatter-Gather, Explained

## The pattern in one sentence

Scatter-gather sends one request to many parties at the same time, then gathers their answers, up to a deadline, and combines them into one.

## The six acts

### Ask Them One After Another

Four suppliers answer in eighty, a hundred and twenty, two hundred and nine hundred milliseconds. Asked in turn, the page waits thirteen hundred.

```
  four suppliers answer in [80, 120, 200, 900] milliseconds. asked in turn, the page waits 1300.
```

### Ask Them All At Once

Asked together, the same four make the page wait for the slowest: nine hundred milliseconds.

```
  the same four, asked together: the page waits for the slowest, 900 milliseconds.
```

### Do Not Wait For The Slowest

All four suppliers are being asked at the same moment. With a deadline of five hundred milliseconds, three quotes are gathered and Delta, too slow, is left out. The best of three is shown, and the page waits five hundred, not nine hundred.

```
  four suppliers held at once, all being asked together: 4 at the same moment.
  a deadline of 500 ms. quotes gathered: [Quote[supplier=Acme, pence=1250], Quote[supplier=Beta, pence=1190], Quote[supplier=Cargo, pence=1340]].
  missing: [Delta (too slow)]. best price shown: Beta at 1190.
  with the deadline, the page waits 500 ms, not 900.
```

### Say What Was Left Out

The page shows the best of two of three suppliers. The one that did not answer, Delta, would have been cheaper, at nine ninety. A partial answer is honest only if it says it is partial.

```
  the page shows: best of 2 of 3 suppliers, 1190 from Beta.
  the one that did not answer, Delta, would have been 990. a partial answer is honest only if it says it is partial.
```

### A Supplier That Fails

Beta is down. The page gets the other two quotes, and names Beta as missing, with the reason. One failure did not fail the page.

```
  Beta is down. quotes: [Quote[supplier=Acme, pence=1250], Quote[supplier=Cargo, pence=1340]]. missing: [Beta (Beta is down)].
  one failure did not fail the page.
```

### The Bill

One page view becomes four supplier calls, so a thousand views make four thousand. And if each supplier is quick ninety nine times in a hundred, asking four and waiting for all means only ninety six pages in a hundred are quick, and ten suppliers, ninety.

```
  one page view is now 4 supplier calls. 1000 page views: 4000 calls, to suppliers who see only the traffic, not the pages.
  if each supplier is quick 99 times in 100, asking 1 and waiting for all means 99.0 in 100 pages are quick.
  if each supplier is quick 99 times in 100, asking 4 and waiting for all means 96.1 in 100 pages are quick.
  if each supplier is quick 99 times in 100, asking 10 and waiting for all means 90.4 in 100 pages are quick.
  the more you ask, the more often the slowest one sets the pace. a deadline is what stops it.
```

## The verdict

Use scatter-gather when several independent sources can answer the same question, and the best or a combination of the answers is what you want. Always give it a deadline, treat a failure like a late answer, and say when an answer is partial. Watch the fan-out: every request now costs as many calls as there are sources.

## How to recognise this in code you did not write

- `CompletableFuture.allOf` or `invokeAll` with a timeout.
- A price comparison, flight search, or federated search.
- A method that returns results and a list of sources that did not respond.
- Elasticsearch's search across shards, which scatters and gathers.

## Where you have already met this

Price comparison and travel sites, search engines across shards, and any API that fans out to several backends.

## When this is too much

With one source, or when you need every answer without exception, scatter-gather has nothing to gather. With a very large fan-out, the deadline decides more than the data.
