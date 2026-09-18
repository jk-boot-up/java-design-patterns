# The Externalised Configuration Pattern, Explained

## In One Sentence

**Values that change on a business calendar are read from outside the program at
runtime, with a default in the code so the program still starts when the source is
unreachable — and with validation, an audit trail and a fast rollback taking over
the job the compiler and the code reviewer used to do for free.**

That sentence is deliberately long, because the short version — "put the number in
a config file" — is where most of the trouble starts. The second half is the
pattern too.

## Everyday Analogy: The Price Board Outside the Greengrocer

A greengrocer has a chalkboard on the pavement with today's prices on it. When
tomatoes come in cheap, someone walks outside, wipes a number off, and writes a new
one. It takes ten seconds. Nobody consults anybody.

Now imagine the prices were painted on the shopfront instead. Same information,
same shop, same customers. Changing tomatoes from two pounds to one fifty now needs
a sign-writer, a quote, a booking, and a day when it is not raining. The price is
still correct — it is just fixed, in the literal sense.

Painted prices are not a mistake in every case. The shop's *name* is painted on,
and rightly so: it should be hard to change, and if it changes overnight without
anybody noticing, something has gone badly wrong. The skill is telling the shop
name apart from the price of tomatoes.

Then notice the two things the chalkboard costs, because they are the honest part
of the analogy. First, anyone with a hand and some chalk can write anything on it.
If they write "tomatoes 0.15" by slipping a decimal point, the shop sells tomatoes
at fifteen pence all morning and nothing squeaks — the board is not wrong, it is
just not what anybody meant. A painted sign would have gone past a sign-writer who
would have said "are you sure?". Second, the board has no memory. By Thursday
nobody can tell you what tomatoes cost on Tuesday, because wiping the old number
off is how you write the new one.

So the greengrocer who is serious about the chalkboard keeps a notebook by the till
with every price change in it, and has a rule that nothing goes on the board
outside a sensible range. That notebook and that rule are the second half of this
pattern, and the greengrocer worked them out the hard way, which is also how most
teams get there.

## The Problem, In The Shop

Free delivery when you spend over fifty pounds. The number is a constant in the
checkout code, which is the right place for it right up until marketing asks for
thirty-five pounds for one weekend, starting nine o'clock on Saturday morning, and
asks on Friday afternoon.

The demo prints the cost of granting that request:

```
  edit the constant         15 min   done Fri 07 Mar 16:45
  code review               45 min   done Mon 10 Mar 09:30
  build and test            25 min   done Mon 10 Mar 09:55
  release approval          30 min   done Mon 10 Mar 10:25
  deploy and watch          20 min   done Mon 10 Mar 10:45
  total work: 2 hours 15 minutes
  live at:    Mon 10 Mar 10:45
  the promotion was for the weekend. It is late by 2 days 1 hour 45 minutes.
```

Two hours and a quarter of actual work, spread across two and a bit days, because
the release window closes at five on Friday and reopens on Monday. The weekend
promotion goes live after the weekend.

See [`problem-statement.md`](problem-statement.md) for why none of those five steps
is unreasonable, and why the constant is a well-written line of code rather than a
mistake.

## The Pattern

Three moves, and the third one is the one that gets skipped.

**Move one: the value comes from outside, and is read per use.** The constant
becomes a lookup against a `ConfigSource`, and — this is the detail that matters —
the lookup happens inside the method that needs it, on every quote. Reading it once
in the constructor would look tidier and would buy you almost nothing, because the
value would then be fixed for the life of the object: you would have traded a
rebuild for a restart, and a restart of a live shop on Saturday morning is not much
of a trade.

**Move two: the code keeps a default.** Every setting declares a fallback that is
compiled in. If the source has no value, or cannot be reached at all, the program
uses the fallback and keeps trading. A shop that refuses to start because a config
server is down is a worse shop than one with a hard-coded threshold.

**Move three: the guards move out with the value.** The number used to be protected
by the compiler, the type system, a reviewer, and version control. None of those
follows it out of the source file. You replace them explicitly: a **typed setting**
with a **declared range**, an **audit trail** of every change, and a **rollback**
that is as fast as the change.

Do moves one and two and you have the pattern as it is usually described. Do all
three and you have the pattern as it survives contact with a Saturday.

## Participants

| Role | In this project | Job |
| --- | --- | --- |
| Client | `ConfiguredCheckout` | Asks for the value it needs, every time it needs it |
| Setting declaration | `MoneySetting` | Names the key, the default, and the acceptable range |
| Settings reader | `SettingsReader` | The seam between the program and the outside world |
| Naive reader | `TrustingSettings` | Externalises the value and validates nothing |
| Careful reader | `GuardedSettings` | Validates, keeps the last good value, records rejections |
| Configuration source | `ConfigSource` / `ConfigServer` | Stores text, and can be unreachable |
| Audit trail | `ChangeLog`, `ConfigChange` | Who changed what, when, and from what |
| The alternative | `HardCodedCheckout` | The correct, unchangeable version |
| The cost of the alternative | `ReleasePipeline` | What a release actually takes, in hours |

## Code Walkthrough

### The setting, declared

```java
public static final MoneySetting FREE_DELIVERY_OVER = new MoneySetting(
        "delivery.freeOver", Money.pounds(50), Money.pounds(5), Money.pounds(200));
```

Four facts. The key it is stored under, so a log line can name it. The default
compiled into the program, so the shop starts. And a lowest and a highest value,
which is the interesting part: below five pounds free delivery is being given away
on a packet of crisps, and above two hundred nobody ever qualifies and the
promotion is broken in the other direction. Both ends are business judgements
rather than technical limits, which is exactly why they have to be written
somewhere a program can enforce them.

This record is the replacement for the compiler. Read it that way and the shape
makes sense.

### The read, per quote

```java
@Override
public DeliveryQuote quote(Basket basket) {
    SettingValue threshold = settings.money(FREE_DELIVERY_OVER);
    Money cost = basket.goodsTotal().isAtLeast(threshold.amount())
            ? Money.zero()
            : standardDelivery;
    return new DeliveryQuote(basket, cost, threshold.amount(), threshold.origin());
}
```

Compare that with `HardCodedCheckout.quote`. The arithmetic is identical; the only
change is where the number comes from. And notice `threshold.origin()` travelling
into the quote. Once a value can come from a server, from a cached last-good copy,
or from a compiled-in default, "the threshold is thirty-five" stops being a
complete answer to anything, and the shop wants the provenance on the screen rather
than in somebody's head.

### The naive reader, and what it buys

```java
Money value = Money.parse(raw.get())
        .orElseThrow(() -> new InvalidSettingException(...));
return new SettingValue(value, source.name());
```

`TrustingSettings` does the good half of the pattern. It reads per call, so a
change is live on the next order. It falls back to the default when the key is
missing or the source is unreachable, so the shop survives an outage. Those two
behaviours are genuinely why anyone does this, and the demo shows them working:

```
  #1  Fri 07 Mar 16:30:04  delivery.freeOver  (not set) -> 35        by marketing
  the very next quote, 4 seconds later:
    ORD-7101  goods £62.00  delivery FREE
    ORD-7102  goods £48.00  delivery FREE
    ORD-7103  goods £31.50  delivery £4.99
  ORD-7102 now ships free. No rebuild, no redeploy, no restart.
```

Four seconds, against two days and change.

### The outage, and the quiet cost of surviving it

```
Act 4 - the config server stops answering
    ORD-7102  goods £48.00  delivery £4.99
  threshold in force: £50.00
  came from: the default compiled into the code, because the config server could not be reached
  the shop starts and keeps selling, because the code carries its own default.
  note what it quietly lost, though: the promotion. Back to £50.00 with no error and no alarm.
```

The shop stays up, which is the point of the default. But read the last line. The
promotion is off, and nothing anywhere says so. This is a real failure mode of this
pattern and it is why the origin string is worth carrying: the only way anybody
finds out is if something is looking at where the value came from.

### And now the bill

The demo spends three of its nine acts here, because this is the part write-ups
leave out and the part teams discover on a Saturday.

**A well-formed, catastrophic number.** Somebody types `-1`:

```
  #2  Sat 08 Mar 09:12:04  delivery.freeOver  35       -> -1        by marketing
    ORD-7101  goods £62.00  delivery FREE
    ORD-7102  goods £48.00  delivery FREE
    ORD-7103  goods £31.50  delivery FREE
  every basket in the shop now ships free, including the £31.50 one.
  -1 is a perfectly well-formed number, so nothing complains. There is no exception and no log line.
```

Every basket is worth more than minus one pound, so every basket ships free. No
exception, no log line, no alert. The program was told the threshold is minus one
pound and is faithfully applying it. The first symptom is the margin.

**Text that is not a number.** Eight minutes later, `fifty`:

```
    ORD-7101  checkout failed: setting 'delivery.freeOver' has value "fifty" — expected an amount of money such as "35" or "4.99"
  not one basket can be quoted. The shop is down, and it was taken down by a text box.
```

A full outage, with nothing deployed. In one sense this is the better failure,
because you find out immediately.

### Paying the bill: validate at the boundary

`GuardedSettings` reads the same key from the same source, and behaves identically
whenever the value is sensible. Four rules cover the cases where it is not.

**Validate at the boundary.** Every value goes through `MoneySetting.read`, which
insists the text is money and that the money is in range. Nothing that fails gets
further into the program, so no downstream code has to wonder.

**Keep the last good value.** When a bad value arrives, carry on with the last one
that passed — not the compiled-in default. This matters more than it sounds.
Reverting to fifty pounds because somebody fat-fingered an unrelated edit would
silently cancel a perfectly good promotion, which is its own kind of wrong.

**Fall back to the default only as a last resort.** If there has never been a good
value — the shop has just started and the first thing it read was rubbish — there
is nothing to keep, so the default keeps the shop selling.

**Say so, loudly.** Every rejection is recorded. A guard that silently swallows bad
input is half a guard: the typo is still there and the promotion still is not
running. In a real shop this is an error-level log and an alert.

```
  delivery.freeOver: money, £5.00 to £200.00, default £50.00
  REJECTED  setting 'delivery.freeOver' has value "fifty" — expected an amount of money such as "35" or "4.99"
  REJECTED  setting 'delivery.freeOver' has value "-1" — expected between £5.00 and £200.00
  both bad values were stopped at the edge, and the shop kept the last value that passed.
```

### Paying the bill: the audit trail

```
  #1  Fri 07 Mar 16:30:04  delivery.freeOver  (not set) -> 35        by marketing
  #2  Sat 08 Mar 09:12:04  delivery.freeOver  35       -> -1        by marketing
  #3  Sat 08 Mar 09:20:04  delivery.freeOver  -1       -> fifty     by marketing
  #4  Sat 08 Mar 10:05:04  delivery.freeOver  fifty    -> 35        by marketing
  #5  Sat 08 Mar 11:40:04  delivery.freeOver  35       -> -1        by ops
  5 changes to one setting in under a day, and not one of them is in the git history.
```

Five facts per line, and the one people leave out is `was`. Without it a rollback
is a feat of memory performed at speed while the shop gives delivery away. With it,
a rollback is a lookup.

The log is append-only on purpose. An audit trail you can tidy up afterwards
answers nothing, because the one occasion you most need it is the one occasion
somebody has a motive to tidy it.

And note the question the log is for. Nobody will ever ask you what the threshold
is *now* — you can read that off the server. They will ask what it was at nine
o'clock on Saturday.

### Paying the bill: a rollback as fast as the change

```
  #6  Sat 08 Mar 11:40:08  delivery.freeOver  -1       -> 35        by on-call (rollback)
  back in force at 4 seconds past the decision, and nobody had to remember the old value: the log had it.
  the same correction through the release pipeline would be live Mon 10 Mar 11:15.
```

This is the guard with no equivalent in the source-code world, and the one that
genuinely makes externalised configuration *safer* rather than merely faster. A bad
release takes a release to undo. A bad value takes four seconds.

## What this simulation does not show

Being explicit about the edges, because the code deliberately stops short of
several real things.

**No network.** `ConfigServer` is a map in the same JVM. A real config server is a
process you call over HTTP, which adds latency to every read and makes caching
unavoidable — see the note on caching below. Nothing here models that, because
modelling it would teach you about HTTP clients rather than about configuration.

**No caching or refresh interval.** This project reads the source on every quote.
A real implementation caches the value and refreshes it on a timer, or is pushed a
notification when it changes. That is an optimisation, and it introduces its own
subtlety: a cache means there is a window in which two instances of the shop are
quoting different thresholds.

**No multiple layered sources.** Real systems stack sources with a precedence order
— environment variables over a mounted file over a config server over the
compiled-in default — so that an operator can override one value on one instance.
The idea is a short step from `ConfigSource`; the project sticks to one source to
keep the lesson about the guards rather than the plumbing.

**No secrets.** Passwords, API keys and certificates are configuration in the
technical sense and a completely different problem in practice, because the audit
trail must not contain the value and the source must be encrypted. Treating a
database password the way this project treats a delivery threshold would be a
serious mistake.

**No consistency across instances.** When the shop runs on six machines, a change
does not reach all six at the same instant. For a delivery threshold that is
harmless. For a value two instances must agree on — a shard count, a feature flag
that changes a data format — it is not, and that is a distributed-systems problem
this pattern does not solve.

## Why The Tests Are The Proof

Fifty-four tests, and two of them are worth singling out because of what they
assert.

`TheBillTest.minusOneGivesEverythingAway` **passes**. It asserts that every basket
in the shop ships free when the threshold is minus one pound, and that nothing
throws. It is not describing a bug; it is describing the pattern working exactly as
designed with a value somebody typed wrongly. A test suite that only contained the
happy path would let you believe this could not happen.

`ConfiguredCheckoutTest.theThresholdIsReadEveryTime` changes the configured value
three times and quotes between each change. It is there to catch the tempting
refactor — reading the value once in the constructor — which would pass every other
test in the suite and quietly destroy the point of the pattern.

`ReleasePipelineTest` pins the naive cost: 135 minutes of work, live Monday at
10:45, late by two days one hour forty-five. Those figures are spoken out loud in
the video, so they are asserted here rather than trusted.

`DemoRunsTest` runs the demo twice and requires identical output, and checks every
number the narration quotes against what the program actually prints.

## What You Gain

- **A business decision moves at business speed.** Four seconds instead of two
  days, without weakening the pipeline that protects everything else.
- **The pipeline gets its dignity back.** Code review is for code again, instead of
  being a rubber stamp on somebody's marketing calendar.
- **The same build runs everywhere.** One artefact, configured differently for
  staging and production, rather than a build per environment.
- **The shop survives its configuration source.** A default in the code means a
  config outage is a degradation, not an outage.
- **Rollback becomes cheap enough to actually use.** Which changes behaviour:
  people try things when undoing them is four seconds.
- **The provenance of every value is answerable.** "Where did this threshold come
  from" has an answer on the screen.

## What To Watch Out For

**Externalising things that should not be externalised.** Not every constant is a
business policy. The order of the steps in a fulfilment workflow, the structure of
a total, the algorithm — those belong in the source, behind the review. If you can
break the shop by typing into a text box, you have externalised too much. The test
is simple: does this value change on a marketing calendar or an engineering one?

**Forgetting the range.** A type alone does not save you. `-1` is money, and it is
catastrophic. Every numeric setting wants a floor and a ceiling, and picking them
is a conversation with whoever owns the number, not a guess.

**Falling back to the default on a bad value.** Tempting, and wrong. A typo in one
setting should not silently cancel a good value somebody set deliberately an hour
ago. Keep the last good value and shout.

**Failing silently.** The commonest mistake once validation exists. Rejecting a bad
value and saying nothing leaves the shop correct and the promotion off, with nobody
looking for the cause. A rejection is an alert.

**Putting secrets through the same path.** See above. Different problem, different
tooling.

**No audit trail.** When the value left the source code it left the version
history. If nothing replaced that, "what was the threshold on Saturday" is
unanswerable, and that question *will* be asked — usually by somebody in finance.

**Assuming the change is atomic across instances.** For a threshold, fine. For
anything two instances must agree on, not fine.

## Externalised Configuration vs. Feature Flags

These overlap enough to be worth separating, because the confusion causes real
architectural mess.

Both read a value from outside at runtime. The difference is what the value *is*.
Externalised configuration holds **parameters**: a threshold, a page size, a
timeout, a courier name. Feature flags hold **switches that select code paths**: is
the new checkout on, is this customer in the experiment.

The practical distinction is what accumulates. A parameter lives forever and has a
value. A flag is supposed to be temporary — it exists to de-risk a release and then
be deleted, along with the branch it was guarding. Flags that are never removed turn
the codebase into a maze of dead paths, which is the failure mode of that pattern
and not of this one.

If you find yourself putting an `if` on a configured value to choose between two
implementations, you are building a feature flag, and it wants a plan for its own
deletion.

## Where You Have Already Seen It

- **Spring Boot's `@Value` and `@ConfigurationProperties`** — the second with
  validation annotations, which is exactly `MoneySetting`'s job with a framework
  doing the parsing.
- **Spring Cloud Config Server with `@RefreshScope`** — the canonical Java
  implementation, and what Tier 2 of this project builds.
- **Kubernetes ConfigMaps and Secrets** — configuration as a mounted file or
  environment variables, with the secrets path deliberately separate.
- **The twelve-factor app's third factor**, "store config in the environment",
  which is where a lot of teams first meet the idea.
- **`application.properties` with a profile per environment** — the same pattern,
  read at startup rather than per use, which is why a change needs a restart.
- **AWS Parameter Store, HashiCorp Consul, etcd** — the same shape at
  infrastructure scale, usually with the audit trail built in.

## Try It Yourself

1. **Add a second setting.** Externalise the standard delivery charge alongside the
   threshold. Give it its own range. Notice how little of `ConfiguredCheckout`
   changes, and that the audit trail now has two keys in it.

2. **Break the range on purpose.** Widen `MoneySetting`'s lowest bound to minus one
   thousand pounds and run the demo. Act 7 will now accept `-1`, and the shop gives
   delivery away with validation switched on. The range is the guard, not the type.

3. **Move the read into the constructor.** Change `ConfiguredCheckout` to read the
   threshold once when it is built. Run the tests and watch
   `theThresholdIsReadEveryTime` fail. Then think about which real-world change you
   have just made necessary: a restart.

4. **Add a layered source.** Write a `LayeredConfigSource` that tries an
   environment-variable source first and the config server second. Decide what its
   `name()` should say, and notice that the origin string is now doing real work.

5. **Make the rollback safer.** `ConfigServer.rollback` goes back exactly one step.
   Make it roll back to the last value that would have passed validation, so
   rolling back twice in a row cannot land on an earlier bad value.

## See Also

- [`problem-statement.md`](problem-statement.md) — the naive version and its cost
- [`class-diagram.md`](class-diagram.md) — the structure
- [`uml-diagram.md`](uml-diagram.md) — the call flow of one quote
- [`animation.html`](animation.html) — step through the nine acts in a browser
- [`session.md`](session.md) — a 60-minute guided teaching session
- [`prerequisites.md`](prerequisites.md) — what you need to know first
