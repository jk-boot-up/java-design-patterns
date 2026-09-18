# The Problem: Four Copies of One Decision, and the Night Three of Them Were Updated

## A shop that charges cards in four places

The online store takes money from customers in four different parts of the system, and
they have almost nothing to do with each other.

**Checkout** takes the money while a customer is sitting there watching a spinner. If it
is slow, the customer notices. If it fails, the customer might not come back.

**Refunds** gives money back when the copper coffee maker comes back in the post. Nobody
is watching. It can take a minute and nobody minds, but it absolutely must happen.

**Subscription billing** runs at two in the morning against thousands of saved cards,
charging people for their monthly bag of coffee. It runs alone, in the dark, unattended.

**Marketplace payouts** pays the independent sellers who list their own products on the
shop. It runs every Friday, it moves large amounts, and the sellers notice immediately if
it does not happen.

Four teams. Four repositories. Four release cadences. One payment provider at the other
end of all four.

## The four decisions nobody wanted to make

None of those four teams wanted to become an expert on the payment provider's network
behaviour. But every one of them had to answer the same four questions before their
service could go live, because the provider is on the other side of the internet and the
internet is not reliable.

**How many times should a failed attempt be retried?** The provider wobbles. Every few
days it declines everything for a fraction of a second and then is perfectly fine again.
Nothing is broken and nobody needs paging — the right answer is to wait a moment and ask
again. So how many moments, and how long?

**When do you give up altogether?** A customer will not wait forever. There has to be a
point at which the whole operation is abandoned and an error is shown, however many
attempts are left.

**Which transport security profile do you present?** The provider accepts a particular
version of TLS with particular ciphers, and every service has to be configured to speak
it.

**What do you count, and what do you call the counters?** Somebody will eventually ask how
often payments fail, and the answer has to come from somewhere.

Four questions, four services, sixteen answers. And this is the important part: **not one
of those sixteen answers has anything to do with checkout, refunds, subscriptions or
payouts.** They are all facts about a network and a supplier's contract. They would be the
same if the shop sold bicycles.

Here is what the program prints:

```
    service               attempts  backoff  deadline     tls
    checkout                     6     10ms    2000ms  TLS1.3
    refunds                      6     10ms    2000ms  TLS1.3
    subscription-billing         6     10ms    2000ms  TLS1.3
    marketplace-payouts          6     10ms    2000ms  TLS1.3

  copies of a cross-cutting decision: 16
  places to edit to change one:       4
```

Four identical rows. Nobody copied anything dishonestly — two competent people reading the
same provider documentation write almost the same twenty lines. But once four versions
exist, there is no mechanism anywhere in the shop that will ever bring them back together.

## March: the provider writes to everybody

The provider sends a letter to all its merchants. Retrying ten milliseconds after a
failure does not help anybody, it says; the failure has not had time to clear, and all
you have done is spend capacity that the provider then has to ration. From now on: **at
most three attempts per payment, and wait properly between them.**

The shop's platform engineer agrees, and does the obvious thing. Opens checkout, changes
two lines, opens a pull request, gets it reviewed, ships it. Then refunds. Then
marketplace payouts. Three pull requests, three reviews, three releases, all in one
afternoon.

```
    checkout                     3    200ms    2000ms  TLS1.3
    refunds                      3    200ms    2000ms  TLS1.3
    marketplace-payouts          3    200ms    2000ms  TLS1.3
    subscription-billing         6     10ms    2000ms  TLS1.3
```

Look at the fourth row.

Subscription billing was not updated. Not through carelessness and not through anybody
being wrong. It runs overnight, so nobody was looking at it that week. It is owned by the
billing team, who were not in the meeting with the provider. It lives in its own
repository with its own build. It had no open work that sprint, so nobody opened it at
all.

There was no fourth place to look unless you already knew there was a fourth place to
look.

**Nothing throws. Nothing is logged. Every test in all four services still passes** —
including subscription billing's, because subscription billing tests its own copy of the
policy, and its own copy is internally consistent. There is no test anybody could have
written, in any of the four repositories, that would have caught this. A test can only
check the code it can see.

## The night it costs money

Three weeks later, at two in the morning, the provider has one of its wobbles. Three
hundred milliseconds of declining everything, then fine again.

The provider's contract allows the shop twelve attempts across the whole merchant account
during an event like this: three per payment, four services that take payments. The
thirteenth attempt is not declined — it is **refused**, and so is every attempt after it,
for the entire account, not just for the service that asked.

Subscription billing is already running, because it is always running at two in the
morning. It hits the wobble first.

```
    subscription-billing  £12.99   6x, 310ms    pay_SUB-90118
    checkout              £47.99   3x, 600ms    pay_ORD-4417
    refunds               £22.50   3x, 600ms    pay_REF-3820
    marketplace-payouts   £186.40  —            NOT PAID
      429 refused — the account's 12-attempt allowance is spent

  What the gateway counted, from its own end:
    subscription-billing  6 attempts
    checkout              3 attempts
    refunds               3 attempts
    marketplace-payouts   1 attempt
    total                 13 of 12 allowed, 1 refused
```

Read the first column and the last row together, because that is the whole lesson.

Subscription billing spent six of the shop's twelve attempts before checkout had finished
its first payment. **And subscription billing succeeded.** It got its money. Its
dashboards are green. Its error rate is zero. As far as the billing team will ever know,
that night went perfectly.

Marketplace payouts made one attempt, was refused outright, and did not pay the sellers.
There is nothing wrong with the marketplace payouts service. It was updated in March. It
did exactly what the provider asked. It happened to arrive fourth.

**The code that misbehaved and the code that suffered are in different repositories, owned
by different people, in different rooms.** On Monday morning somebody opens an incident
about marketplace payouts, and every line of that service is correct.

## Why the obvious fixes do not work

**"Write a shared library."** This is a real answer and often the right one, and the video
says so. But notice what it does not fix. A library is a dependency version. Updating the
policy now means publishing a new version and then getting four teams to upgrade to it —
which is the same problem with an extra step, because the fourth team still has to open
their repository. And a library only works if all four services are written in the same
language. The moment the shop's search team ships something in Go, the library cannot help
them at all.

**"Put a rule in the code review checklist."** This depends on somebody knowing that a
fourth copy exists. That knowledge is what was missing.

**"Write a test."** A test lives inside one service and can only see that service's copy.

**"Put it behind the API gateway."** The gateway is at the front door — it sees traffic
coming *into* the shop. These four services are making calls *out* of the shop, to a
supplier. A gateway never sees them.

## What has to change

The four decisions are not decisions about the shop's business. They are decisions about
how anything on this network talks to that supplier. They have ended up inside four
services because that is where the code that makes the call lives, and for no other
reason.

So the question this pattern answers is: **can the code that makes the call live somewhere
other than inside the service?** Not in a library compiled into it — somewhere genuinely
outside it, that can be changed without opening, rebuilding, retesting or redeploying any
of the four services at all.

The answer is yes, and the cost of that yes is the second half of this project.
