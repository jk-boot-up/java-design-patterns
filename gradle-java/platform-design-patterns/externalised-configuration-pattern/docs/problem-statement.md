# The Problem — A Number You Cannot Change Without Shipping Software

## One line of code

The shop gives free delivery when you spend over fifty pounds. In the code, that
is a single line:

```java
private static final Money FREE_DELIVERY_OVER = Money.pounds(50);
```

Start by being fair to it. It is a named constant rather than a bare number. It
says what it means. It appears in exactly one place. Its type is money, so it
cannot accidentally be compared against a quantity or a postcode. Every piece of
advice about magic numbers has been followed. If you put this line in front of a
reviewer they would approve it without a comment, and they would be right to.

There is nothing wrong with this line. That is the first thing to understand
about this pattern: the problem it solves is not a code problem.

## Friday, half past four

Marketing wants the threshold dropped to thirty-five pounds for one weekend, to
push a slow category. The promotion starts at nine o'clock on Saturday morning.
They ask on Friday afternoon.

Changing the line takes fifteen minutes. Getting the changed line into the
running shop takes rather longer, and the demo walks through it step by step with
real times:

```
Act 2 - marketing wants £35.00 from Sat 08 Mar 09:00, and asks on Friday at 16:30
  edit the constant         15 min   done Fri 07 Mar 16:45
  code review               45 min   done Mon 10 Mar 09:30
  build and test            25 min   done Mon 10 Mar 09:55
  release approval          30 min   done Mon 10 Mar 10:25
  deploy and watch          20 min   done Mon 10 Mar 10:45
  total work: 2 hours 15 minutes
  live at:    Mon 10 Mar 10:45
  the promotion was for the weekend. It is late by 2 days 1 hour 45 minutes.
```

Read the second line of that table and then the third. The edit finishes at a
quarter to five on Friday. The review finishes at half past nine on **Monday**,
because the release window closes at five and does not reopen until the weekend
is over.

The promotion was for the weekend. It goes live after the weekend has finished.

## Nothing in that list is unreasonable

It is tempting to read the table as an indictment of the pipeline. It is not.

A second person reading the change is how the shop avoids shipping a typo to a
million customers. A build and a test run is how it avoids shipping something
that does not compile against the current branch. An approval step is how a
regulated business demonstrates that releases are controlled. A weekday deployment
window exists because the people who would notice a bad release and roll it back
are at their desks on weekdays.

Every one of those steps is the right thing to have in front of a change to *how
the shop works*. All of them together are absurd in front of a change from fifty
to thirty-five.

And that is the distinction this pattern asks you to make. Some of the values in
your program are **decisions about behaviour** — the algorithm, the order of the
steps, the structure of the total. Those belong in the source code, behind the
whole pipeline, and you should be glad they are hard to change. Others are
**decisions about business policy** — a threshold, a page size, a timeout, which
of three couriers is currently preferred. Those change on a marketing calendar,
not an engineering one, and putting them behind the pipeline does not make them
safer. It makes them late.

## The naive workarounds, and why they are worse

Three things teams reach for before they reach for this pattern, and all three
are worth naming because you will meet them.

**A second constant, and an `if` on the date.** Ship the weekend threshold
alongside the normal one with a date range around it. This works exactly once.
The second time marketing asks, the dates are different, and now you are back in
the pipeline to edit the dates — except the code has grown a branch and a set of
hard-coded dates that will be wrong forever.

**A system property on the command line.** Closer, and genuinely better than the
constant. But it is fixed for the life of the process, so a change means a
restart, and a restart of a running shop is not a thing you do at nine on a
Saturday morning either. You have replaced a rebuild with a restart, which on the
weekend in question is not much of a trade.

**A database table read on every checkout.** Now you are actually doing the
pattern, you have just chosen an inconvenient source for it and you probably have
not thought about what happens when the database is slow, or what happens when
somebody types the wrong thing into the table. Which brings us to the real point.

## The bill — and this is the lesson people skip

Move the threshold out of the program and a change takes four seconds instead of
two days. That is the headline, and every write-up of this pattern stops there.

Look at what else has changed, though. That number used to be guarded by three
things, none of which you had to ask for:

- **The compiler** refused to let it be the word "fifty".
- **The type system** refused to let it be anything other than money.
- **A reviewer** would have queried minus one pound out of ordinary human surprise.

The threshold is now a text box. All three guards stayed behind in the source
code. What arrives in their place is a string, at runtime, that nobody has read.

The demo shows both of the ways that goes wrong, because they go wrong very
differently.

**A well-formed, catastrophic number.** Somebody types `-1`:

```
Act 5 - the bill: somebody types -1 into the box on Saturday morning
  #2  Sat 08 Mar 09:12:04  delivery.freeOver  35       -> -1        by marketing
    ORD-7101  goods £62.00  delivery FREE
    ORD-7102  goods £48.00  delivery FREE
    ORD-7103  goods £31.50  delivery FREE
  every basket in the shop now ships free, including the £31.50 one.
  -1 is a perfectly well-formed number, so nothing complains. There is no exception and no log line.
  it reached the running shop in 4 seconds, with no compiler, no code review and no test suite in the way.
```

Every basket in the shop now qualifies for free delivery, because every basket is
worth more than minus one pound. There is no exception. There is no error log.
Nothing anywhere reports a problem, because as far as the program is concerned
nothing *is* a problem: it was told the threshold is minus one pound and it is
faithfully applying the threshold it was told. The first symptom is the margin.

**Text that is not a number at all.** Eight minutes later, somebody types the
word `fifty`:

```
Act 6 - the bill: eight minutes later, somebody types the word fifty
  #3  Sat 08 Mar 09:20:04  delivery.freeOver  -1       -> fifty     by marketing
    ORD-7101  checkout failed: setting 'delivery.freeOver' has value "fifty" — expected an amount of money such as "35" or "4.99"
    ORD-7102  checkout failed: setting 'delivery.freeOver' has value "fifty" — expected an amount of money such as "35" or "4.99"
    ORD-7103  checkout failed: setting 'delivery.freeOver' has value "fifty" — expected an amount of money such as "35" or "4.99"
  not one basket can be quoted. The shop is down, and it was taken down by a text box.
```

That one is loud, which in a sense makes it the better of the two failures — you
find out immediately. It is also a full outage. Not one customer can be quoted,
and nobody deployed anything.

Both of those reached the running shop in four seconds. Both of them came from a
text box on a Saturday morning, when nobody is reviewing anything.

## What the shop needs instead

The answer is not to put the number back in the code. The answer is to move the
three guards out with it, deliberately, as things you build rather than things you
inherit:

| What you lost | What replaces it |
| --- | --- |
| The compiler refusing "fifty" | A **typed setting** that parses and rejects |
| A reviewer querying `-1` | A **declared range** the value must fall inside |
| Version control's history | An **audit trail** of who changed what, and when |
| A revert and a redeploy | A **rollback** as fast as the change itself |

And one more that has no equivalent in the source-code world, because in the
source-code world it cannot happen: the configuration source can be **unreachable**.
A shop that will not start because a config server is down is a worse shop than
one with a hard-coded threshold, so the code has to carry its own default and keep
selling through an outage — while being honest that running on the default means
the promotion is quietly off.

That is the whole of this project: the number moves out, and the four guards move
out with it.
