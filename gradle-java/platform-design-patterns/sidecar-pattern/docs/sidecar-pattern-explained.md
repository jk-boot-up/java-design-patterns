# The Sidecar Pattern

**Take the work that every service has to do but no service is about — retrying, giving
up, presenting a certificate, counting what happened — out of the services entirely, and
run it in a second process standing beside each one. Then accept that you now have twice
as many processes, that every call goes through one extra hop, and that you have added a
new thing which can be down to every call you were trying to make more reliable.**

---

## The idea, before any code

Think about a busy restaurant kitchen where every chef also has to answer the phone.

A chef is halfway through a sauce when the phone rings. It is a delivery driver who cannot
find the back entrance. The chef wipes their hands, takes the call, gives directions,
comes back to the sauce. Every chef in that kitchen has learned to give directions to the
back entrance, and every one of them gives slightly different directions, because they
each worked it out themselves on a busy night.

Then the council changes the one-way system, and the directions everybody has been giving
are wrong. The head chef tells the pastry chef, the grill chef and the sous chef. Nobody
tells the chef who works the overnight prep shift, because they were asleep. For the next
three weeks, most drivers get there and some do not, and the ones who do not are always on
the overnight shift, and nobody connects the two facts.

The sidecar answer is not to write down the directions and pin them up — that is a shared
library, and it helps, but everybody still has to read the new copy. The sidecar answer is
to **hire somebody to sit by the phone**. The chefs stop answering it. There is one person
who knows the directions, and when the one-way system changes you tell that one person.

The chefs got worse at something. They can no longer give directions at all — if the
phone person is off sick, the phone simply rings out, because the skill left the kitchen
on purpose. That is not an accident of the arrangement. That is the arrangement.

Now, the shop.

---

## The four services and the sixteen copies

The online store charges cards in four places: **checkout**, while a customer watches a
spinner; **refunds**, when the coffee maker comes back; **subscription billing**, at two
in the morning against thousands of saved cards; and **marketplace payouts**, paying the
independent sellers every Friday.

Four teams, four repositories, four release days. One payment provider behind all four.

And each of the four had to answer the same four questions, because the provider is across
the internet and the internet is not reliable:

| Question | Why every service has to answer it |
| --- | --- |
| How many times do we retry? | The provider wobbles: it declines everything for a fraction of a second, then is fine |
| When do we give up? | A customer will not wait forever; something has to abandon the attempt |
| Which TLS profile do we present? | The provider accepts one particular version and set of ciphers |
| What do we count, and what are the counters called? | Somebody will ask how often payments fail |

Four questions, four services, **sixteen answers** — and not one of the sixteen is about
checkout, refunds, subscriptions or payouts. They are facts about a network and a
supplier's contract. They would be identical if the shop sold bicycles.

That is the test that tells you a concern is cross-cutting: **describe the decision out
loud, and if your description never mentions what the service does, the decision does not
belong in the service.**

---

## What went wrong

In March the provider writes to every merchant: retrying ten milliseconds after a failure
does not help, it only spends capacity the provider then has to ration. From now on, at
most three attempts per payment, with a proper wait between them.

An engineer opens checkout and changes two lines. Then refunds. Then payouts. Three pull
requests, three reviews, three releases, one afternoon.

```
    checkout                     3    200ms    2000ms  TLS1.3
    refunds                      3    200ms    2000ms  TLS1.3
    marketplace-payouts          3    200ms    2000ms  TLS1.3
    subscription-billing         6     10ms    2000ms  TLS1.3
```

The fourth row is the project. Look at how the code says it:

```java
public final class CheckoutService implements TakesPayments {
    private int maxAttempts = 6;
    private long firstBackoffMillis = 10;

    public void applyPolicyReview() {
        maxAttempts = 3;
        firstBackoffMillis = 200;
    }
```

and, next door:

```java
public final class SubscriptionBillingService implements TakesPayments {
    private final int maxAttempts = 6;
    private final long firstBackoffMillis = 10;

    // there is no applyPolicyReview() here
```

The test that pins this down does not assert that the billing service is wrong. It asserts
that **there is no method on it that could make it right**:

```java
assertTrue(!methods.contains("applyPolicyReview"),
        "the point of this project is that nobody wrote this method here");
```

That is a much stronger statement, and it is the real shape of the problem. Three services
were updated because somebody opened three files. The fourth stayed as it was because
nothing in the shop's code, build or test suite knows that a fourth file exists.

Nothing throws. Nothing is logged. **All four services' tests still pass**, including
billing's, because billing tests its own copy and its own copy is internally consistent.
No test written inside any of the four repositories could have caught this. A test can
only check the code it can see.

---

## The night, in numbers

Three weeks later, at two in the morning, the provider wobbles for three hundred
milliseconds.

The contract allows the shop twelve attempts across the whole merchant account during an
event like that: three per payment, four services taking payments. The thirteenth is not
declined — it is **refused**, and so is every one after it, for the entire account.

Subscription billing is already running, because it is always running at two in the
morning.

```
    subscription-billing  £12.99   6x, 310ms    pay_SUB-90118
    checkout              £47.99   3x, 600ms    pay_ORD-4417
    refunds               £22.50   3x, 600ms    pay_REF-3820
    marketplace-payouts   £186.40  —            NOT PAID
      429 refused — the account's 12-attempt allowance is spent

    subscription-billing  6 attempts
    checkout              3 attempts
    refunds               3 attempts
    marketplace-payouts   1 attempt
    total                 13 of 12 allowed, 1 refused
```

Subscription billing spent half the shop's allowance before checkout had finished its
first payment — **and subscription billing succeeded.** It got its money. Its dashboard is
green. As far as the billing team will ever know, that night went perfectly.

Marketplace payouts made one attempt, was refused, and the sellers were not paid. Every
line of the payouts service is correct. It was updated in March. It did exactly what the
provider asked. It arrived fourth.

**The code that misbehaved and the code that suffered are in different repositories, owned
by different people, in different rooms.** That sentence is why this pattern exists.

---

## The pattern

Stop asking the service to know how to talk to the provider. Run a second process beside
it — its own container, on the same machine, sharing the same network address — and point
the service at `localhost`. The second process is the one that goes out to the internet.

Retrying, giving up, presenting the certificate and counting what happened all happen out
there, where the service cannot see them and does not have to.

The service that carried twenty lines of retry code now carries one:

```java
public final class ServiceBehindASidecar implements TakesPayments {

    private final String name;
    private final Sidecar sidecar;

    @Override
    public Receipt pay(Payment payment) {
        return sidecar.send(payment);
    }
}
```

One class replaced four. That is not a trick of the demo; it is the measurement. The four
services differed from one another **only** in the cross-cutting code each of them
carried. Take that out and what is left is a name and a request. The business logic that
made checkout different from refunds never lived in the part we removed — which is the
proof that the part we removed was never theirs.

And the policy is now one object rather than four literals:

```java
public record SidecarConfig(int maxAttempts,
                            long firstBackoffMillis,
                            long deadlineMillis,
                            String tlsProfile) {

    public static SidecarConfig agreedWithTheProvider() {
        return new SidecarConfig(3, 200, 2_000, "TLS1.3");
    }
}
```

In this project that is a Java record, because everything here runs in one JVM. In the
deployed version it is a small configuration file that the proxy beside each service reads
at start-up. Either way the property that matters is a counting property: **there is one
of it.**

The same night, run again:

```
    subscription-billing  £12.99   3x, 603ms    pay_SUB-90118
    checkout              £47.99   3x, 603ms    pay_ORD-4417
    refunds               £22.50   3x, 603ms    pay_REF-3820
    marketplace-payouts   £186.40  3x, 603ms    pay_PAY-7741

    total                 12 of 12 allowed, 0 refused
```

Four payments, twelve attempts, nobody refused, the sellers paid. The policy was not
applied four times and missed once. It was stated once.

---

## What actually changed — all three rows

```
                                            before     after
  copies of a cross-cutting decision            16         4
  places to edit for one policy change           4         1
  processes to run and patch                     4         8
```

Read all three rows or none of them.

The first two are why you would do this. The third is why it is not free. Four proxies are
four more things that want memory, a version number, a restart when they are patched, a
place in somebody's on-call rota and a line in a runbook. **Anybody who tells you this
pattern simplifies your deployment has not counted.**

The first row is the one that scales, and it scales in a particular way worth naming.
Add a fifth service that takes payments and the copies go from sixteen to twenty the old
way. Beside the services it is still four:

```java
public static int copiesInsideTheServices(int services) {
    return services * CROSS_CUTTING_CONCERNS;
}

public static int copiesBesideTheServices() {
    return CROSS_CUTTING_CONCERNS;
}
```

**The second method takes no argument, and the missing argument is the whole answer.** The
number of places a decision is written down has stopped depending on the number of
services, because the services are no longer where the decision is written down.

---

## The line: what may move out, and what must not

Retry counts, deadlines, certificates and counters are facts about the network. They move.

Whether a refund is allowed after ninety days is a fact about the shop. It must not.

The test is the same one from the top of this document: **say the decision out loud. If
your sentence has to name what the service does, the decision stays in the service.** "Try
three times, two hundred milliseconds apart" names nothing. "Refuse refunds after ninety
days" names refunds.

This matters more than it sounds, because proxy configuration is a wonderful hiding place.
It is written in a format most of the team cannot read, it lives in a repository most of
the team does not check out, and it is applied by restarting something rather than by
deploying something. A business rule that ends up there is a business rule that no
developer will ever think to look for — and the next person who goes looking for "where do
we decide about refunds?" will search the refunds service, find nothing, and conclude the
rule does not exist.

The sidecar's own configuration object is asserted to be innocent of the shop:

```java
String written = SidecarConfig.agreedWithTheProvider().line();
assertFalse(written.contains("checkout"));
assertFalse(written.contains("refund"));
assertFalse(written.contains("payout"));
```

---

## The bill, part one: a second thing that can be down

A healthy gateway, a healthy service, a £47.99 coffee maker. Then the proxy beside
checkout fails to start after a patch. The gateway is fine. The service is fine. The
network is fine.

```
    connection refused to localhost — no sidecar beside checkout

  attempts that reached the gateway: 0
```

Zero. The request never left the machine — and the service has no retry code left to fall
back on, because we deleted it on purpose when we moved the concern out.

**You added a dependency to every single call, in order to make those calls more
reliable.**

That trade is usually worth taking. A proxy on the same machine, with no business logic in
it, that does one narrow job, fails far less often than the internet does. It has no
database, no deploys tied to feature work, and no code path that only runs on a Tuesday.
But it is a trade, and it has a shape you should recognise before you take it: on the
night it goes wrong, it goes wrong for **every** call the service makes, rather than for
one of them. The failure is not smaller, it is rarer and wider.

That shape is why real sidecars are boring on purpose. Everything you are tempted to add
to one — a cache, a little bit of routing logic, a header that is *almost* a business rule
— is a new way for the whole service to stop working at once.

---

## The bill, part two: the hop

```
    retry code inside the service      3 attempts, 600ms
    retry code in a proxy next door    3 attempts, 603ms
```

Three milliseconds. One per attempt, for crossing to a neighbouring process and coming
back. It is small, it is real, and it is paid on every call for as long as the service
exists.

Three milliseconds on a payment that already takes six hundred is nothing. Three
milliseconds on an internal call that takes two is a fifty per cent increase, and if every
service in a large system talks through a proxy then every hop between them is paid twice
— once on the way out of one and once on the way into the next. That is the arithmetic
that decides whether a service mesh is a good idea in your system or a very expensive one,
and it is arithmetic, not taste.

---

## The admission: in one program, this is Decorator

Everything above happened inside one Java program. In one program, a proxy that a service
talks through is an object wrapping another object — and an object wrapping another object
is the **Decorator** pattern from §11 of this course.

The `Sidecar` class would not surprise anybody who has read that project. It holds a
reference to the thing it wraps, it does some work before and after, and it presents the
same operation to its caller. There is no new code here.

**What makes Sidecar a different pattern is not the code. It is where the code runs.**

| | Decorator | Sidecar |
| --- | --- | --- |
| Ships as | part of your jar | its own process or container |
| Written in | your service's language | any language |
| Changes when | your service is rebuilt and redeployed | somebody restarts the proxy |
| Failure adds | nothing new | a second process that can be down |
| Costs per call | a method call | a network hop |

Read the "changes when" row against Act 4 and the "failure adds" row against Act 6. The
same property is doing both: the thing is genuinely outside your service. That is what
buys you the one-line policy change, and it is what charges you the extra process and the
extra failure. **You cannot have one without the other**, and a project that shows you the
first without the second is selling something.

So the question is never "wrapper or no wrapper". It is:

> **Does this concern need to change without rebuilding the service? Or does it need to
> apply to a service written in a language your library does not support?**

Yes to either, and it goes next door. No to both, and a shared library inside your own
process is cheaper, simpler, faster, and has one fewer thing that can be down. A team that
reaches for a sidecar when a library would do has bought the entire bill and none of the
benefit.

---

## Where you have already met this

You have run sidecars without calling them that.

A **log shipper** running beside your application, reading the files it writes and sending
them somewhere. Your application knows nothing about the log system's protocol, and the
log system can be replaced without your application being rebuilt.

A **metrics agent** that scrapes and forwards, for the same reason.

**A service mesh** — Istio, Linkerd — which is this pattern applied to *every* call between
*every* service in a system, with a control plane pushing configuration out to all the
proxies at once. That is Act 4 at the scale of a company, and Act 5's third row at the
scale of a company too: a mesh doubles your process count, and that is the honest reason
some teams try one and turn it off again.

An **nginx** or **Envoy** container in the same Kubernetes pod, terminating TLS so that the
application behind it only ever speaks plain HTTP on localhost. That is the third question
from the top of this document, moved out. The next project in this category builds exactly
that, for real.

---

## Pitfalls

**Putting business logic in the proxy.** Covered above, and it is the one that does lasting
damage, because the damage is to the next person's ability to find things.

**Forgetting the proxy is a dependency.** If a service's health check passes while its
sidecar is down, the service will be sent traffic it cannot serve. Whatever decides
"is this instance ready?" has to include the thing beside it.

**A sidecar that grows.** Each addition is individually reasonable and collectively turns
a narrow, boring, reliable process into a second application with its own bugs — one that
now takes the whole service down when it fails.

**Debugging across two logs.** A request now appears in the service's log and in the
proxy's log, with different formats and different clocks. A trace identifier that crosses
both is not optional once you have done this; see §39.

**Reaching for it when a library would do.** The most common mistake, and the most
expensive, because the costs are all real and the benefit is zero if both questions above
are "no".

---

## Related patterns

**Decorator (§11)** is the same structure inside one process. Discussed at length above.

**Proxy (§14)** is the same structure with a different intent: Proxy controls access to
something, a sidecar takes work off something. A sidecar usually *is* a proxy in the
network sense, which is why the word keeps appearing.

**API Gateway (§26)** is in front of *all* the services and handles traffic coming in. A
sidecar is beside *one* service and, in this project, handles traffic going out. The
question a gateway answers is "is this request allowed into the shop at all?"; the
question a sidecar answers is "how does anything on this network talk to that supplier?"

**Retry with Backoff (§29)** is the policy itself. This project is about *where that policy
lives*, not what it says.

**Circuit Breaker (§30)** is the natural next thing to move out here, for exactly the same
reasons, and with exactly the same warning about what must not follow it.

**Externalised Configuration (§38)** is the other half of Act 4. The sidecar is where the
behaviour runs; externalised configuration is why you can change it without a deploy.
