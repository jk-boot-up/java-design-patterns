# Session Guide — Externalised Configuration Pattern

A 60-minute guided session. The unusual shape of this one is that the pattern itself
takes ten minutes to teach and the rest of the hour is spent on what it costs. Resist
the urge to rebalance that; the costs are the part the room will actually meet in
production.

## Learning Objectives

By the end of the session a participant can:

1. Explain why a well-written constant can still be the wrong place for a value.
2. Tell a business-policy value apart from a behaviour value, and justify the call.
3. Name the three moves of the pattern, including the third one most write-ups omit.
4. Describe the two distinct ways a bad configured value fails, and why the quiet one
   is worse.
5. Name the four guards that must be rebuilt outside the program, and say which
   original guard each one replaces.
6. Explain why a rejected value falls back to the last good value rather than to the
   compiled-in default.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup, and the line of code that is not wrong |
| 0:05–0:15 | The problem: Friday at half past four |
| 0:15–0:25 | The pattern: three moves |
| 0:25–0:38 | Code walkthrough |
| 0:38–0:50 | Exercises |
| 0:50–0:58 | The bill, and the feature-flag question |
| 0:58–1:00 | Wrap-up |

## 0:00–0:05 — Setup, And The Line That Is Not Wrong

Everyone runs:

```bash
cd platform-design-patterns/externalised-configuration-pattern
./gradlew -q run
```

Then put this on the screen and ask the room to criticise it:

```java
private static final Money FREE_DELIVERY_OVER = Money.pounds(50);
```

Let them try. Someone will reach for "magic number" and then notice it is named.
Someone may suggest it should be configurable, which is the answer but not yet the
reasoning. Land the point explicitly: **there is nothing wrong with this line.** It
is a named constant, in one place, correctly typed, and a reviewer would approve it.

That matters for the rest of the hour. This pattern does not fix bad code. It fixes a
value that is in a place with the wrong change speed.

## 0:05–0:15 — The Problem: Friday At Half Past Four

Read act 2 of the output together, one line at a time.

```
  edit the constant         15 min   done Fri 07 Mar 16:45
  code review               45 min   done Mon 10 Mar 09:30
```

Stop there. Ask what happened between those two lines. The window closed at five and
did not reopen until Monday.

```
  total work: 2 hours 15 minutes
  live at:    Mon 10 Mar 10:45
  the promotion was for the weekend. It is late by 2 days 1 hour 45 minutes.
```

**Discussion question, five minutes:** which step in that list would you remove?

The useful outcome is that nobody can remove one. Code review is how a typo does not
reach a million customers. The build is how you avoid shipping something that does
not compile. Approval is how a regulated business shows releases are controlled. The
weekday window exists because the people who would notice a bad release are at their
desks on weekdays.

Close with the distinction that carries the whole session: **some values are decisions
about behaviour, and some are decisions about business policy.** Behaviour belongs
behind the pipeline and you should be glad it is hard to change. Policy changes on a
marketing calendar, and putting it behind the pipeline does not make it safer — it
makes it late.

## 0:15–0:25 — The Pattern: Three Moves

**Move one: the value comes from outside, and is read per use.** Show act 3. Four
seconds, and ORD-7102 flips to free delivery on the next quote.

Then labour the placement, because this is where tidy-minded developers go wrong.
Ask: why not read it once in the constructor and keep it in a field? Let them answer.
The answer is that you would have traded a rebuild for a restart, and a restart of a
live shop on Saturday morning is not much of a trade.

**Move two: the code keeps a default.** Show act 4 — the server goes away and the shop
keeps selling. Then read the last line of that act out loud:

```
  note what it quietly lost, though: the promotion. Back to £50.00 with no error and no alarm.
```

Ask the room how anybody would find out. The answer is only the origin string.

**Move three: the guards move out with the value.** Ask what protected the constant.
Push until you get all four: the compiler, the type system, the reviewer, version
control. Then point out that none of them follows the value out of the source file,
and that the rest of the session is about replacing them deliberately.

## 0:25–0:38 — Code Walkthrough

Four files, in this order.

**`HardCodedCheckout`** — thirty seconds. It is correct. Move on.

**`ConfiguredCheckout.quote`** — put it beside `HardCodedCheckout.quote` and have the
room name the difference. The arithmetic is identical; one line reads a setting. Point
at where that read sits: inside the method.

**`MoneySetting`** — the key, the fallback, the lowest, the highest. Ask the room to
justify £5 and £200 as the bounds. Below five pounds free delivery is being given away
on a packet of crisps; above two hundred nobody qualifies and the promotion is broken
the other way. The important realisation is that these are *business* judgements, which
is exactly why a program has to enforce them.

**`TrustingSettings` beside `GuardedSettings`** — read them side by side. They differ in
one `try` block. Make sure the room sees that `GuardedSettings` falls back to
`lastGood`, not to `setting.fallback()`, and ask why before telling them.

## 0:38–0:50 — Exercises

### Exercise 1 — Break the range on purpose (everyone)

In `ConfiguredCheckout`, change the setting's lowest bound from `Money.pounds(5)` to
`Money.pounds(-1000)`. Run the demo.

Act 7 now accepts `-1` and the shop gives delivery away with validation switched on.
The point: the type was never the guard. The range is.

### Exercise 2 — Move the read into the constructor (everyone)

Change `ConfiguredCheckout` to read the threshold once when it is constructed. Run
`./gradlew test`.

`ConfiguredCheckoutTest.theThresholdIsReadEveryTime` fails, and it is the only one
that does. Discuss what real-world change that refactor has just made necessary: a
restart.

### Exercise 3 — Fall back to the default instead (discussion, then code)

In `GuardedSettings.fallBack`, delete the `lastGood` lookup so a rejected value always
falls back to `setting.fallback()`. Run the demo.

Act 7 now reverts to £50 when somebody types `-1`, silently cancelling a promotion
that was set deliberately an hour earlier. Ask the room which is worse, and make them
argue it.

### Exercise 4 — Stretch

Write a `LayeredConfigSource` that consults an environment-variable source first and
the config server second. The interesting part is not the loop — it is deciding what
`name()` should return, because the origin string is now doing real work.

## 0:50–0:58 — The Bill, And The Feature-Flag Question

Walk acts 5 and 6, and insist on the difference between them.

`-1` is **quiet**. Every basket ships free, no exception, no log line, no alert, and
the first symptom is the margin report. `fifty` is **loud**. Nothing can be quoted at
all and you find out in seconds.

Ask which is worse. The room usually says the outage. Push back: the outage is
detected immediately by anything that watches error rates, and rolls back in four
seconds. The quiet one runs all weekend.

Then open `TheBillTest` and point out that `minusOneGivesEverythingAway` **passes**.
It is not a bug report. It is a description of the pattern working exactly as designed
with a value somebody typed wrongly.

Close on the boundary question, which is the one they will actually have to answer at
work: **what should never be externalised?** Anything you can break the shop with by
typing into a text box. The order of the steps in a workflow, the structure of a
total, the algorithm. If someone raises feature flags, take it — externalised
configuration holds parameters that live forever; feature flags hold switches that
select code paths and are supposed to be deleted. Flags that are never removed turn a
codebase into a maze of dead paths, and that is the failure mode of that pattern, not
this one.

## 0:58–1:00 — Wrap-Up

One sentence: **take the number out of the code, and take the compiler, the reviewer
and the history out with it.**

Then the table:

| What you lost | What replaces it |
| --- | --- |
| The compiler refusing "fifty" | A typed setting that parses and rejects |
| A reviewer querying `-1` | A declared range the value must fall inside |
| Version control's history | An audit trail of who changed what, and when |
| A revert and a redeploy | A rollback as fast as the change |

Homework: find one constant in your own codebase that changes on a marketing calendar
rather than an engineering one, and write down the range it should be allowed to take.
The range is usually the hard part, and it is usually a conversation with somebody who
is not an engineer.

## Facilitator Notes

**The most common wrong turn** is a participant concluding that configuration should
be avoided because it is dangerous. Correct it early: the pipeline is not safer for
this value, it is slower, and the demo shows the promotion missing its weekend. The
lesson is to externalise deliberately with the guards rebuilt, not to externalise
nothing.

**The second most common** is agreeing enthusiastically that everything should be
configurable. Exercise 3 and the closing boundary question are aimed at this.

**If the room is senior**, spend longer on the audit trail. Experienced people have
usually been asked "what was this value at 9am on Saturday" and have not been able to
answer.

**If the room is junior**, spend longer on act 2 and less on act 7. The realisation
that a correct one-line change can still be useless is the one that sticks.

**Timing risk:** the code walkthrough over-runs if you read `Money` or
`ReleasePipeline` in detail. Neither is the pattern. `ReleasePipeline` is a price tag
and `Money` is plumbing; show their output, not their internals.

## Materials Checklist

- [ ] JDK 21 installed, `./gradlew test` green before the session
- [ ] `./gradlew -q run` output on screen, scrollable
- [ ] `docs/images/class-diagram.png` on screen for the walkthrough
- [ ] `docs/animation.html` open in a browser as a fallback for the acts
- [ ] `HardCodedCheckout.quote` and `ConfiguredCheckout.quote` side by side
- [ ] `TrustingSettings` and `GuardedSettings` side by side
