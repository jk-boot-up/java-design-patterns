# Circuit Breaker — UML Sequence Diagrams

Six sequences over the same outage. Recommendations has stopped answering, and every
call to it takes the full three-second timeout before giving up.

Throughout: the threshold is **three consecutive failures**, the reset wait is
**5000ms**, and one failed call costs **3000ms**. Every number below comes out of
`./gradlew run`.

## The State Machine

![Circuit breaker state diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
stateDiagram-v2
    [*] --> CLOSED

    CLOSED --> CLOSED : call succeeds<br/>count reset to 0
    CLOSED --> CLOSED : call fails<br/>count 1, then 2
    CLOSED --> OPEN : 3rd failure in a row<br/>trip, note the time

    OPEN --> OPEN : call arrives before 5000ms<br/>REFUSED, no call made, 0ms
    OPEN --> HALF_OPEN : call arrives after 5000ms<br/>let exactly one through

    HALF_OPEN --> CLOSED : the probe worked<br/>calls resume, count 0
    HALF_OPEN --> OPEN : the probe failed too<br/>another full 5000ms

    note right of CLOSED
        Healthy. Current flows.
    end note
    note right of OPEN
        Tripped. Costs nothing.
    end note
```

</details>

Three states, four transitions worth remembering, and one word that matters:
**consecutive**. A success in the closed state does not merely fail to increment the
count, it resets it to zero. A service that answers three times and fails once is not
down.

## Act One: Retry, Applied To An Outage

```mermaid
sequenceDiagram
    autonumber
    participant S as Shopper
    participant P as RetryingProductPage
    participant R as Recommendations

    S->>P: page(SKU-1001)
    P->>R: suggestionsFor — attempt 1
    R--xP: TIMEOUT after 3000ms
    P->>R: suggestionsFor — attempt 2
    R--xP: TIMEOUT after 3000ms
    P->>R: suggestionsFor — attempt 3
    R--xP: TIMEOUT after 3000ms
    P-->>S: page with 0 suggestions, after 9000ms

    Note over P,R: 9 seconds waited, 3 calls aimed at a service already down
```

The page the shopper eventually receives is identical to the page they would have got
at zero seconds. Every one of those nine seconds bought nothing, and a service on its
knees received three times the traffic for the privilege.

Ten shoppers make that ninety seconds and thirty calls. A test asserts both numbers.

## Act Two: Six Pages, With A Breaker

```mermaid
sequenceDiagram
    autonumber
    participant P as ProductPageService
    participant B as CircuitBreaker
    participant R as Recommendations

    P->>B: call(suggestionsFor)
    B->>R: attempt
    R--xB: TIMEOUT 3000ms
    Note over B: FAILED — failure 1 of 3

    P->>B: call(suggestionsFor)
    B->>R: attempt
    R--xB: TIMEOUT 3000ms
    Note over B: FAILED — failure 2 of 3

    P->>B: call(suggestionsFor)
    B->>R: attempt
    R--xB: TIMEOUT 3000ms
    Note over B: OPENED — not calling for 5000ms

    P->>B: call(suggestionsFor)
    B--xP: REFUSED — no call made, 0ms
    P->>P: serve the page without suggestions

    Note over P,B: 6 pages, 3 calls made, 3 refused, total 9000ms
```

Read the clock rather than the arrows. The first three pages cost three seconds each;
the last three cost nothing at all, because no call left the building.

That is the trade this pattern makes, stated honestly: it does not protect the people
who discover the outage. It protects everybody after them.

## Act Three: It Lets Itself Back In

```mermaid
sequenceDiagram
    autonumber
    participant P as ProductPageService
    participant B as CircuitBreaker
    participant C as SimulatedClock
    participant R as Recommendations

    Note over B: OPEN since 9000ms

    P->>B: call — at 9000ms
    B->>C: how long since I tripped?
    C-->>B: 0ms — less than 5000
    B--xP: REFUSED, instantly

    P->>B: call — at 14000ms
    B->>C: how long since I tripped?
    C-->>B: 5000ms — the wait is over
    Note over B: HALF-OPEN — letting ONE call through
    B->>R: the probe
    R-->>B: OK [SKU-2001, SKU-2002] in 20ms
    Note over B: CLOSED — the probe worked, calls resume
    B-->>P: 2 suggestions

    Note over P,R: nobody deployed anything to make that happen
```

There is no scheduler here and no background thread. The breaker compares the clock
against the moment it tripped, on whatever call happens to arrive next — which is why
recovery costs nothing at all when there is no traffic.

And note how cheap the probe is. **One** call. Had Recommendations still been down,
that single shopper would have waited three seconds, the breaker would have reopened
for another full five, and everybody else would have carried on being served
instantly.

## Act Four: Checkout, Where There Is No Fallback

```mermaid
sequenceDiagram
    autonumber
    participant S as Shopper
    participant C as CheckoutService
    participant B as CircuitBreaker
    participant Pay as Payments

    S->>C: pay(ORD-9001, £449.99)
    C->>B: call(charge)
    B->>Pay: attempt
    Pay--xB: TIMEOUT 3000ms
    B--xC: ServiceUnavailableException
    C-->>S: "We cannot take payment. Your basket is saved." — after 3000ms

    Note over B: after 3 failures, OPENED

    S->>C: pay(ORD-9004, £449.99)
    C->>B: call(charge)
    B--xC: REFUSED — no call made
    C-->>S: the same honest message — at once, card untouched

    Note over S,Pay: 5 shoppers told honestly, 0 cards charged
```

There is nothing a shop can substitute for taking the money, so the breaker buys no
fallback here. What it buys instead is **a fast, honest "no" rather than a spinner** —
and, less visibly but more importantly, it stops a thousand shoppers each holding a
thread open for three seconds while they discover the same outage.

Compare the two messages. Both say the same thing. One arrives after three seconds,
the other in a hundredth of a second. That difference is the entire value of the
pattern on a dependency that has no fallback.

## Act Five: The Fallback That Lies

```mermaid
sequenceDiagram
    autonumber
    participant S as Shopper
    participant C as PretendItWorkedCheckout
    participant B as CircuitBreaker
    participant Pay as Payments
    participant W as the warehouse

    S->>C: pay(ORD-9101, £449.99)
    C->>B: call(charge)
    B->>Pay: attempt
    Pay--xB: TIMEOUT 3000ms
    B--xC: ServiceUnavailableException
    Note over C: catch (RuntimeException anything)
    C-->>S: "thank you for your order" — receipt chg-assumed-ok

    C->>W: ship one espresso machine
    Note over Pay: cards actually charged: 0

    Note over S,W: nothing threw, no alert fired, every dashboard is green
```

This class is wired identically to the honest one. The difference is a single `catch`
block that returns a made-up receipt instead of throwing.

The distinction to take away is not "fallbacks are bad" — the product page's fallback
is excellent. It is this: **an empty list of suggestions is true.** The shop really
does have no suggestions to show. **A receipt for money that never moved is not
true.** A fallback that hides a real failure is worse than the error it replaced,
because the error would have been noticed in seconds, and this will be noticed at the
end of the month.

## Notes

- All five acts use the *same* `CircuitBreaker` class with the same threshold and the
  same reset wait. Nothing about the breaker changes between them. What changes is
  the caller's `catch` block, which is the only place the pattern leaves a decision.
- `CircuitBreaker` runs a `Supplier<T>` and has never heard of product pages, money
  or shopping. That is what lets one class serve all four callers, and it is also why
  it cannot possibly warn you that act five is lying.
- Every millisecond here comes from `SimulatedClock`, which moves only when a service
  or the breaker moves it. The five-second reset wait costs no real time, so the whole
  suite of 26 tests finishes in about a second and every number is exact rather than
  approximately reproducible.
- `CallLog` keeps the timeline — who called whom, when, and what happened — which is
  what makes the timestamps in act two readable as an argument rather than as noise.
