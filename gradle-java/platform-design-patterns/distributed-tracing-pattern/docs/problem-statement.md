# The Problem — Nine Hundred Milliseconds, And Nobody Knows Where They Went

## One page, four services

A customer opens the product page for item A-2231. Behind that single click the
shop asks the catalog for the product, pricing for the price, inventory for the
stock figure, and recommendations for the "customers also bought" strip, and then
renders the page.

```
Act 1 — a product page takes nine hundred milliseconds

  A customer opens the page for product A-2231. It takes 900ms.
  Four services contributed to it: catalog, pricing, inventory
  and recommendations. Nobody can say which one is at fault.
```

Nine hundred milliseconds is not an outage. Nothing has failed. No alert has
fired. It is simply slower than it should be, and somebody has been asked to find
out why.

Start by being fair to the shop. Every one of those four services is healthy.
Every one of them is logging. There is a log aggregator, and it works. The
dashboards are green. This is not a story about a team that neglected its
observability — it is a story about a team that did everything the usual advice
says and still cannot answer the question.

## What the logs give you

Each service writes a timestamped line when it starts a piece of work and another
when it finishes. The aggregator merges the four streams by time and shows you the
result. Here it is, and this is the part to read slowly:

```
  14:32:07.000  gateway          GET /product/A-2231
  14:32:07.000  catalog          lookup started
  14:32:07.040  gateway          GET /product/A-2231
  14:32:07.040  catalog          lookup started
  14:32:07.120  catalog          lookup complete
  14:32:07.120  pricing          quote started
  14:32:07.160  catalog          lookup complete
  14:32:07.160  pricing          quote started
  14:32:07.300  pricing          quote complete
  14:32:07.300  inventory        stock check started
  14:32:07.340  pricing          quote complete
  14:32:07.340  inventory        stock check started
```

There are two "quote started" lines and two "quote complete" lines. Try to work
out how long pricing took.

You cannot. Not because the data is missing, and not because the timestamps are
wrong — every timestamp on that page is correct to the millisecond. You cannot do
it because **two customers are on the site at once**, and nothing on any line says
which customer it belongs to. Subtracting the first "quote complete" from the
first "quote started" is a guess. It might be right. It might be pairing Ada's
start with Ben's finish, in which case the answer is off by forty milliseconds and
looks entirely plausible.

Now imagine four hundred customers instead of two.

## More logging does not fix this

This is the point at which most teams add more logging, and it is worth being
clear about why that fails. The thing missing from those lines is not *detail*.
You could add the product id, the response size, the JVM thread name, the pod
name, and you would still be unable to pair a start with its finish, because none
of those values is unique to one customer's request and shared across all the
services that served it.

What is missing is exactly one thing: **an identifier that is the same on every
line of one request and different on everybody else's.** That is the whole idea.
Everything else in this pattern follows from it.

## The identifier, and the shape

Give the front door a trace id and pass it down to everything it calls, and the
merged log becomes readable again. But the pattern goes one step further, and the
extra step is the one that turns a readable log into an answer.

Alongside the trace id, each unit of work records a **span**: what the work was,
when it started, how long it took, and — the important field — **which span caused
it**. That last field is the one people leave out when they build this themselves,
and it is the difference between a pile of timings and a shape.

```
  catalog          span-2     parent span-1      120ms
  pricing          span-3     parent span-1      180ms
  inventory        span-4     parent span-1       90ms
  ranking-model    span-6     parent span-5      340ms
  recommendations  span-5     parent span-1      400ms
  render           span-7     parent span-1      110ms
  product-page     span-1     parent (none)      900ms
```

Read the parent column. Catalog, pricing, inventory, recommendations and render
all hang off `span-1`, which is the page itself. The ranking model hangs off
`span-5`, which is recommendations. That column is the shape of the request, and
once you have it the drawing draws itself:

```
  trace trace-4f2a   total 900ms
  product-page            |============================================|   900ms   0ms of it its own
    catalog               |=====                                       |   120ms
    pricing               |     ========                               |   180ms
    inventory             |              ====                          |    90ms
    recommendations       |                   ===================      |   400ms   60ms of it its own
      ranking-model       |                   ================         |   340ms
    render                |                                      ===== |   110ms
```

For anyone listening rather than looking: each line is one unit of work, indented
under whatever called it, with a bar showing when it ran and how long it lasted,
all against the same timeline. The page's bar fills the full width, because the
page is the whole request. Catalog's bar is short and sits at the left. Render's
is short and sits at the right. The long one in the middle is recommendations, and
nested inside it, filling almost all of it, is the ranking model.

## The number that names the culprit

The drawing is persuasive, but the arithmetic underneath it is what actually
answers the question, and it turns on one idea: **self time**.

The page span lasted the full nine hundred milliseconds. On total time it is the
biggest thing in the trace and it always will be, which makes total time useless
for finding anybody. Subtract the time each span spent *waiting on its children*
and what is left is the time that piece of work is genuinely responsible for:

```
    ranking-model     340ms   37% of the page
    pricing           180ms   20% of the page
    catalog           120ms   13% of the page
    render            110ms   12% of the page
    inventory          90ms   10% of the page
    recommendations    60ms    6% of the page
```

The ranking model is thirty-seven per cent of what the customer waited for.
Recommendations as a whole — the model plus its own work — is four hundred
milliseconds, forty-four per cent of the page.

Notice that the page span, which lasted the longest of anything in the trace, does
not appear in that list at all, because its self time is zero. It did no work. It
waited. That is the distinction that lets a trace name a culprit where a stopwatch
cannot.

## The bill — and this is the part people skip

Every write-up of this pattern stops at the waterfall. Here is what it costs, and
all three items are real failures that happen in real systems, none of which
announces itself.

**One service is not instrumented.** Recommendations is well-behaved in every
respect but one: it never opens a span of its own. It still receives the trace
context and still passes it on, so nothing errors and nothing warns.

```
  trace trace-7c19   total 900ms
  product-page            |============================================|   900ms   60ms of it its own
    catalog               |=====                                       |   120ms
    pricing               |     ========                               |   180ms
    inventory             |              ====                          |    90ms
    ranking-model         |                   ================         |   340ms
    render                |                                      ===== |   110ms
```

The four hundred milliseconds did not vanish — it had to land somewhere, and it
landed on the parent. The page now appears to spend sixty milliseconds doing its
own work, work it never did. The ranking model appears to hang directly off the
page, which is a call that does not exist. The service actually responsible is not
on the diagram at all.

This is worse than a gap, because a gap you would notice. What you get instead is
a complete, plausible, wrong picture, and somebody spends an afternoon reading the
page renderer.

**The work moves to another thread.** Real tracing libraries keep the current
context in a thread-local so that your method signatures stay clean. That is a
genuine kindness right up to the moment the work moves to a thread pool, a
`CompletableFuture`, or a scheduled job — because a thread-local belongs to a
thread, and the new thread's copy is empty.

```
  trace trace-async-broken   total 400ms   2 separate roots — this trace is broken
  product-page            |============================================|   400ms
  recommendations         |============================================|   400ms
```

Two roots in one trace. Four hundred milliseconds of work that belongs to nobody.
And the code that broke it is line-for-line indistinguishable from the code that
worked.

**You kept one trace in a hundred.** A shop serving a thousand requests a second,
six spans each, is asking a backend to store half a billion spans a day. Nobody
pays for that, so you sample.

```
  kept       10,000
  discarded  990,000

  A customer complains about request number 862,144.
  Was it kept?  no — it is gone, and it is not recoverable
```

Sampling is decided per trace, at the front door, *before* anybody could know the
request was going to matter. So the one request somebody complains about has a
ninety-nine per cent chance of having been thrown away, and it was thrown away for
exactly the same reason as every other request: nothing about it stood out yet.

## What the shop actually needs

| What logs could not do | What the trace gives you |
| --- | --- |
| Pair a start line with its finish | **A trace id** shared across one request and no other |
| Say which call caused which | **A parent span id** on every span |
| Name a culprit | **Self time** — duration less the time spent waiting |
| Show where the time sat in the request | **A waterfall**, drawn from the parent links |

And the three things it costs, each of which has to be engineered rather than
assumed:

| The failure | What it takes to avoid it |
| --- | --- |
| A service that opens no span | Instrument **every** hop, or accept a wrong answer |
| Work handed to another thread | Pass the context as a **value**, never rely on a thread-local |
| The one trace you needed was discarded | **Tail sampling** — decide to keep once you know it was slow |

That is the whole of this project: one identifier, one parent link, and an honest
account of the three ways it stops working.
