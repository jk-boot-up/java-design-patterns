# Externalised Configuration Pattern — UML Sequence Diagrams

Five sequences. The first is the pattern in one picture; the next four are the four
things that only become possible — or only become dangerous — once the value lives
outside the program.

## 1. One Quote, With The Value Read From Outside

The read happens inside the quote, which is the whole pattern.

![Externalised Configuration pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Customer
    participant Checkout as ConfiguredCheckout
    participant Reader as GuardedSettings
    participant Setting as MoneySetting
    participant Server as ConfigServer

    Customer->>Checkout: quote(ORD-7102, goods £48.00)
    Checkout->>Reader: money(delivery.freeOver)
    Reader->>Server: lookup("delivery.freeOver")
    Server-->>Reader: "35"
    Reader->>Setting: read("35")
    Note over Setting: money? yes. between £5 and £200? yes.
    Setting-->>Reader: £35.00
    Note over Reader: remember £35.00 as the last good value
    Reader-->>Checkout: £35.00, from "the config server"
    Note over Checkout: £48.00 is at least £35.00
    Checkout-->>Customer: delivery FREE, threshold £35.00
```

</details>

Read step 2 and notice where it is. The lookup happens *inside* `quote`, not in the
constructor. That single placement decision is what makes a configuration change take
effect on the next order rather than on the next restart, and it is the detail people
get wrong when they tidy this code up.

Steps 5 to 7 are the replacement for the compiler. The text `"35"` is turned into
money and checked against a declared range before it gets any further into the
program, so nothing downstream of the reader ever has to wonder whether the threshold
is sane.

Step 8 carries an origin string back with the amount. That is what lets the quote —
and the support agent reading it three weeks later — say not just what the threshold
was but where it came from.

## 2. The Change That Lands In Four Seconds

The point of the whole exercise, and the reason anybody accepts the bill.

![Externalised Configuration Pattern — The Change That Lands In Four Seconds](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Marketing
    participant Server as ConfigServer
    participant Log as ChangeLog
    participant Checkout as ConfiguredCheckout
    participant Reader as TrustingSettings

    Note over Checkout: quoting on £50.00, the compiled-in default
    Marketing->>Server: set("delivery.freeOver", "35", "marketing")
    Server->>Server: clock advances 4 seconds
    Server->>Log: record(Fri 16:30:04, was "(not set)", now "35", by marketing)
    Note over Server: no rebuild, no redeploy, no restart
    Checkout->>Reader: money(delivery.freeOver)
    Reader->>Server: lookup("delivery.freeOver")
    Server-->>Reader: "35"
    Reader-->>Checkout: £35.00
    Note over Checkout: ORD-7102 (£48.00) now ships free
```

</details>

Compare the elapsed time with the release pipeline the pattern replaced: 135 minutes
of work, spread from Friday afternoon to Monday at 10:45. The promotion was for the
weekend.

Note step 4. The change is recorded as it happens, and it is recorded with the value
it displaced. That is not bookkeeping for its own sake — it is what makes sequence 5
possible.

## 3. The Source Is Unreachable, And The Shop Keeps Selling

The failure mode of this pattern, and the reason every setting declares a default.

![Externalised Configuration Pattern — The Source Is Unreachable, And The Shop Keeps Selling](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Customer
    participant Checkout as ConfiguredCheckout
    participant Reader as TrustingSettings
    participant Server as ConfigServer

    Note over Server: the network link to it drops
    Customer->>Checkout: quote(ORD-7102, goods £48.00)
    Checkout->>Reader: money(delivery.freeOver)
    Reader->>Server: lookup("delivery.freeOver")
    Server--xReader: ConfigSourceUnavailableException
    Note over Reader: fall back to the default compiled into the code
    Reader-->>Checkout: £50.00, from "the default ... could not be reached"
    Checkout-->>Customer: delivery £4.99
```

</details>

The shop starts, and keeps trading, which is the point of step 6. A shop that refuses
to serve customers because a configuration server is down is a worse shop than one
with a hard-coded threshold.

Now read what it cost. The promotion is off. The threshold is back to fifty pounds,
no exception reaches a customer, no alert fires, and the only trace anywhere is the
origin string in step 7. Surviving an outage quietly is not the same as surviving it
correctly, and this is exactly why the provenance is worth carrying.

## 4. The Bill: A Well-Formed Number Nobody Checked

Two sequences side by side. Same server, same value, different reader.

![Externalised Configuration Pattern — The Bill: A Well-Formed Number Nobody Checked](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Ops
    participant Server as ConfigServer
    participant Trusting as TrustingSettings
    participant Guarded as GuardedSettings
    participant Setting as MoneySetting

    Ops->>Server: set("delivery.freeOver", "-1", "ops")
    Note over Server: stored happily. Storing text is all a config server does.

    rect rgb(250, 235, 235)
    Trusting->>Server: lookup("delivery.freeOver")
    Server-->>Trusting: "-1"
    Note over Trusting: parses fine. -1 is a number.
    Trusting-->>Ops: £-1.00 — every basket in the shop ships free
    end

    rect rgb(235, 245, 235)
    Guarded->>Server: lookup("delivery.freeOver")
    Server-->>Guarded: "-1"
    Guarded->>Setting: read("-1")
    Setting--xGuarded: InvalidSettingException: expected between £5.00 and £200.00
    Note over Guarded: record the rejection, keep the last good value
    Guarded-->>Ops: £35.00, from "the last value that passed validation"
    end
```

</details>

The top half is the pattern working exactly as designed with a value somebody typed
wrongly. There is no exception, no log line, and no alert — the program was told the
threshold is minus one pound and is faithfully applying it. The first symptom is the
margin.

The bottom half is the same read with one guard in place. Notice what it falls back
to: **not** the compiled-in fifty pounds, but the last value that passed validation.
Reverting a good promotion because of an unrelated typo would be its own kind of
wrong.

Notice also that it records the rejection. A guard that silently swallows bad input
is half a guard: the typo is still there and the promotion still is not running, and
nobody is looking.

## 5. The Rollback That Is A Lookup, Not A Memory

The guard with no equivalent in the source-code world.

![Externalised Configuration Pattern — The Rollback That Is A Lookup, Not A Memory](images/uml-diagram-5.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant OnCall as On-call engineer
    participant Server as ConfigServer
    participant Log as ChangeLog

    Note over OnCall: Sat 11:40 — the margin report looks wrong
    OnCall->>Server: rollback("delivery.freeOver", "on-call")
    Server->>Log: valueBefore("delivery.freeOver")
    Log-->>Server: "35"
    Note over Log: from change #5, whose "was" field is "35"
    Server->>Server: set("delivery.freeOver", "35"), clock advances 4 seconds
    Server->>Log: record(Sat 11:40:08, was "-1", now "35", by on-call (rollback))
    Server-->>OnCall: back in force, 4 seconds after the decision
    Note over OnCall: the same correction via the release pipeline: live Mon 10 Mar 11:15
```

</details>

Step 4 is the one to look at. Nobody had to remember that the threshold used to be
thirty-five pounds, at speed, on a Saturday, while the shop gave delivery away. The
log had it, because every change records the value it displaced.

And step 7 is the honest comparison. A bad release takes a release to undo. A bad
value takes four seconds. That is what makes externalised configuration genuinely
safer rather than merely faster — and it only holds if you built the audit trail,
which is why the trail is part of the pattern and not an optional extra.
