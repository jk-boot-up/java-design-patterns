# Problem Statement

## The Scenario

An online shop has an order history page. A customer opens it to see what they have
bought: one line per item, with the product's name, the quantity and what it cost.

The page is assembled the obvious way, and the obvious way is not wrong:

- Ask the **Orders** service what this customer bought. That comes back as order
  lines — a product code, a quantity, a price — and no product names, because Orders
  does not have the names.
- Ask the **Catalog** service what those product codes are called, once, for all of
  them at a time.
- Stitch the two answers together and render the page.

That is the API Composition pattern, done properly, and this project's
`ComposingOrderHistory` does exactly that. It batches the catalog call. It does not
loop. Nobody would object to it in review.

## What Goes Wrong

Nothing crashes. That is what makes this one hard to see.

Run act one and watch three views of the same page:

```
Act 1 - composing the page on every view
     80ms ->   110ms  Orders    OK   ...
    110ms ->   170ms  Catalog   OK   ...
    170ms ->   200ms  Orders    OK   ...
    200ms ->   260ms  Catalog   OK   ...
    260ms ->   290ms  Orders    OK   ...
    290ms ->   350ms  Catalog   OK   ...
  3 views cost 270ms and 6 service calls
  every view rebuilt a page identical to the last one
```

Ninety milliseconds and two service calls, per view. Three views, and every one of
them rebuilt a page identical to the last one.

Now scale that the way a real shop scales. An order is placed **once**. The page
showing it is opened by the customer, then again from the confirmation email, then
by a support agent, then by the customer's phone, then again next week. The
underlying facts changed once. The shop paid to discover them a thousand times.

And there is a second cost, less obvious and more dangerous. Every one of those
views is a live dependency on two other services. If Catalog is slow, the order
history page is slow. If Catalog is down, a page about **orders the customer has
already paid for** cannot be shown at all.

## Why That Hurts

The page is correct. The code is correct. Every test passes. There is no incident,
no alert, and no stack trace — and so nothing ever forces the question.

What you have instead is a shop that gets steadily more expensive as it gets more
popular, and a page whose availability is the product of the availability of every
service it touches.

## The Tempting Fix, And Why It Is The Whole Point

Everybody reaches for the same thing: **put a cache in front of it.**

This project takes that seriously enough to build it. `CachedOrderHistory` is a real
cache, with a real expiry, and it works — `itCachesThePage` proves the second view
is free.

Then read the other four tests in `CachedOrderHistoryTest`, because they are the
argument of this entire project:

- **`itServesAPageItKnowsNothingAbout`** — the cache holds rows it never understood.
  It stored bytes. It cannot reason about them.
- **`aRenameCannotInvalidateIt`** — Catalog renames a product. The cache has no idea.
  It was not told, and there is no mechanism by which it could be told.
- **`itIsCorrectedByATimerAndNothingElse`** — the only thing that will ever fix it is
  the clock running out. Not a fact about the world. A timer.
- **`thereIsNoFreeSetting`** — and so you are left tuning an expiry. Short, and you
  have paid for a cache that misses. Long, and you are confidently showing people
  things that stopped being true.

A cache is a copy that cannot know when it is wrong.

## The Question This Project Answers

What if the copy were kept up to date by the same events that changed the truth?

Not a timer. Not a guess. The actual facts — an order was placed, a product was
renamed, stock changed — arriving as they happen, updating the page as they go.

## The Second Half, Which Is Harder

If you stop there, you have sold the pattern and hidden the bill. There are two
things you must be told before you use this, and this project demonstrates both
rather than mentioning them.

**The page can be out of date, and there is a moment where that is genuinely
alarming.** Act three holds the events in flight and shows a customer whose order is
placed, paid for, and final — looking at an order history page with nothing on it.
That window is real. It closes by itself, but it is real, and you have to decide
whether the page you are building can live inside it.

**The read model must never be used to make a decision.** Act five puts the last
kettle in the shop window: the read model says one is available, the ledger says
zero, and a second shopper tries to buy it. What saves the shop is that the sale was
decided on the write side, by the ledger, which refuses. Show a read model's stock
number. Never sell against it.

## The Goal

By the end of this project you should be able to:

1. Explain why composing a page on every view is correct and still wrong at scale,
   and why nothing will ever alert you to it.
2. Say precisely what a read model has that a cache does not — not speed, but the
   ability to be told it is wrong.
3. State where the work went, rather than claiming it disappeared: to write time,
   paid once per order instead of once per view.
4. Describe the staleness window honestly, including the part where a paid order is
   not yet on the customer's page.
5. Say the rule out loud: the write side is where a decision is made, and a read
   model is throwaway — rebuildable from the events at any time.
