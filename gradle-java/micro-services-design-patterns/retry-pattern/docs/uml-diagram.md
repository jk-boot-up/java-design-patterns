# Retry with Backoff — UML Sequence Diagrams

Five sequences over the same checkout, the same £449.99, and the same gateway.
What changes is only which way the network fails — and in the last one, where a
single line of code sits.

Throughout: one attempt at the gateway costs 50 milliseconds whether it works or
not, and the policy is three attempts with a 100ms wait that doubles, plus up to
20% jitter.

## One Attempt That Recovers, Step By Step

![Retry with backoff sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as Shopper
    participant C as CheckoutService
    participant R as Retrier
    participant P as RetryPolicy
    participant G as PaymentGateway

    S->>C: pay(ORD-5001, £449.99)
    C->>C: PaymentRequest.forOrder(...)
    Note over C: the key is built ONCE, here, outside the retry

    C->>R: call(payment for ORD-5001, action)
    R->>P: delayBeforeAttempt(1)
    P-->>R: 0ms — the first attempt never waits
    R->>G: charge(request)
    G-->>R: GatewayTimeoutException
    Note over R: a timeout is retryable

    R->>P: delayBeforeAttempt(2)
    P-->>R: 103ms — 100 base plus jitter
    R->>R: wait
    R->>G: charge(request) — same key
    G-->>R: Receipt chg-1
    R-->>C: chg-1
    C-->>S: paid, 203ms after asking
```

</details>

The shopper waited 203 milliseconds instead of 50, and got a completed order
instead of an error page. That trade is the whole reason the pattern exists.

## Act One: A Timeout That Recovers

![Act One: A Timeout That Recovers](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant R as Retrier
    participant G as PaymentGateway

    R->>G: attempt 1
    G-->>R: TIMEOUT — request never arrived
    Note over G: nothing was charged
    R->>R: wait 103ms
    R->>G: attempt 2 — same key
    G-->>R: CHARGED chg-1 £449.99

    Note over R,G: card charged 1 time — £449.99
```

</details>

The simple case, and the one everybody has in mind when they write a retry. The
request never reached the gateway, so no money moved, so trying again is plainly
safe.

Note the wait: 103 milliseconds, not 100. Those three extra milliseconds are the
jitter, and with one caller they look like noise. They are not — see act five.

## Act Two: A Declined Card

![Act Two: A Declined Card](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant R as Retrier
    participant G as PaymentGateway

    R->>G: attempt 1
    G-->>R: CardDeclinedException — the bank said no
    Note over R: not retryable — rethrow immediately
    R--xR: no wait, no attempt 2, no attempt 3

    Note over R,G: the gateway was asked 1 time — answered in 50ms
```

</details>

A refused card is refused for a reason, and the reason is still true a hundred
milliseconds later. The naive loop asks three times and takes three delays to
arrive at the same "no".

Telling this diagram apart from the one above it is half of what the pattern is,
and in the code it is one line: `failure instanceof GatewayTimeoutException`.

## Act Three: The Reply That Got Lost

![Act Three: The Reply That Got Lost](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant R as Retrier
    participant G as PaymentGateway
    participant B as the bank

    R->>G: attempt 1 — key-ORD-5001
    G->>B: take £449.99
    B-->>G: done, chg-1
    G--xR: reply lost on the way home
    Note over R: the caller sees a plain timeout — identical to act one

    R->>R: wait 103ms
    R->>G: attempt 2 — key-ORD-5001, the same key
    G->>G: I have seen this key before
    G-->>R: REPLAYED chg-1 — the charge I already made

    Note over R,G: card charged 1 time — £449.99
```

</details>

This is the realistic failure and the dangerous one, and the note in the middle is
the sentence to take away: **from the caller's side this is identical to act one.**
There is no flag to check and no clever code that can tell "the request was lost"
from "the receipt was lost". That is a property of networks, not a gap in this
project.

So the careful caller stops trying to tell them apart. It carries the same key,
and the gateway — which checks its key map *before* it charges — recognises the
repeat and hands back the charge it already made.

## Act Four: The Same Failure, With A Plain Loop

![Act Four: The Same Failure, With A Plain Loop](images/uml-diagram-5.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant N as NaiveCheckoutService
    participant G as PaymentGateway
    participant B as the bank

    N->>N: build request — key-ORD-5001-attempt-1
    N->>G: attempt 1
    G->>B: take £449.99
    B-->>G: done, chg-1
    G--xN: reply lost
    Note over N: retrying immediately, no wait

    N->>N: build request — key-ORD-5001-attempt-2
    Note over N: a NEW key. This is the bug, and this is the whole of it.
    N->>G: attempt 2
    G->>G: I have never seen this key
    G->>B: take £449.99 again
    B-->>G: done, chg-2
    G-->>N: CHARGED chg-2

    Note over N,G: card charged 2 times — £899.98
```

</details>

Read the diagram for what is *not* in it. No exception escapes. No error is logged.
The checkout returns a valid receipt and the order looks perfect. The only evidence
that anything went wrong is on a bank statement, and it surfaces as a phone call
two days later.

The gateway did nothing wrong either. It was handed a key it had never seen, which
by definition means a new job. Every double charge in this project is the caller's
doing.

## Act Five: Why Jitter Exists

![Act Five: Why Jitter Exists](images/uml-diagram-6.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as Caller A
    participant B as Caller B
    participant G as PaymentGateway

    A->>G: attempt 1
    B->>G: attempt 1
    G--xA: TIMEOUT — the gateway is struggling
    G--xB: TIMEOUT

    Note over A,B: without jitter both wait exactly 100ms
    Note over A,B: with jitter A waits 103ms and B waits 117ms

    A->>G: attempt 2 at 103ms
    B->>G: attempt 2 at 117ms
    Note over G: two requests spread out, not one wave
```

</details>

With two callers this is a curiosity. With a thousand callers who all failed at the
same instant it is the difference between a trickle and a stampede that repeats
itself on a timer.

A struggling service is usually struggling because of load. A retry policy without
jitter reliably re-applies that load in synchronised waves, which is the opposite
of what backoff was trying to achieve.

## Notes

- Acts one to four are the *same* gateway object with different faults scripted
  onto it. Nothing about the gateway changes between them, and the gateway is
  correct throughout.
- `Retrier` never sees a `PaymentRequest`. It runs a `Supplier<T>` and has no idea
  what it is retrying — which is what makes it reusable, and also why it cannot
  possibly warn you that the thing it is retrying is unsafe to repeat.
- Every millisecond in these diagrams comes out of `SimulatedClock`, which moves
  only when the retrier or the gateway moves it. The backoff costs no real time, so
  the whole test suite finishes in about a second and every number is exact rather
  than approximately reproducible.
- The jitter values (103ms, 117ms) come from a seeded `Random`, so they are the
  same on every run and on every machine. In production the seed comes from the
  machine, and it should.
