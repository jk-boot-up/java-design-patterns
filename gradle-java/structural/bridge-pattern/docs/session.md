# Session Guide — Bridge Pattern

A 60-minute guided session for teaching or self-studying the Bridge pattern
using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/bridge-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises. If you are teaching a group that has *not* watched it, run the
> session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Bridge pattern solves.
2. Explain why `Notification` holds a `MessageChannel` field instead of
   subclassing per channel.
3. Identify the four roles — abstraction, refined abstraction, implementor,
   concrete implementor — in real code.
4. Predict how many new classes a new notification type or a new channel
   costs, with and without Bridge.
5. Distinguish Bridge from Adapter.

## Timetable

| Time | Segment | Mode |
| --- | --- | --- |
| 0:00–0:05 | Setup check | Hands-on |
| 0:05–0:15 | The problem | Discussion |
| 0:15–0:25 | The pattern | Explanation |
| 0:25–0:40 | Code walkthrough | Live coding |
| 0:40–0:50 | Exercises | Hands-on |
| 0:50–0:58 | Pitfalls & comparisons | Discussion |
| 0:58–1:00 | Wrap-up | — |

## 0:00–0:05 — Setup Check

Everyone runs:

```bash
java -version
./gradlew run
```

Anyone whose build fails pairs up with a neighbour. Do not debug installs
during the session — that is what the prerequisites doc is for.

## 0:05–0:15 — The Problem

**Do not show `Notification`/`MessageChannel` yet.** Start with the pain.

Put `NaiveOrderConfirmationEmail` and `NaiveOrderConfirmationSms` from
[`problem-statement.md`](problem-statement.md) side by side and ask:

> *"These two classes both send an order confirmation. What's duplicated
> between them, and what's genuinely different?"*

Land on: the *content* (subject, body) is duplicated; the *delivery
mechanics* are genuinely different — but both facts are welded into every
single class.

**Key question to land:** *"If I add a `Push` channel, how many new
classes do I write? If I add a `PasswordReset` notification type, how many
new classes?"* Two, then two more (and then a third channel needs three
more on top of that) — the N×M explosion.

## 0:15–0:25 — The Pattern

Introduce the TV remote / television analogy from
[`bridge-pattern-explained.md`](bridge-pattern-explained.md). Ask the
group: *"If a remote's 'volume up' button is pressed, does the remote need
to know whether it's talking to a Sony or a Samsung TV?"* Land on: no — the
remote only knows it's talking to *something* that understands "volume
up," exactly as `Notification` only knows it's talking to *something* that
understands `deliver(...)`.

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the four roles. Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and trace a single
`send()` call fanning out to exactly one `deliver()` call.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to
talk over the animation yourself, or switch it on to let it explain each
step in its own voice.

**The one point that must land:**

> If a `Notification` subclass ever needs an `if` statement checking which
> channel it's talking to, the pattern has not been applied — the whole
> point is that content and delivery vary on two axes that never touch.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The implementor — `MessageChannel.java`**
Point out this interface declares the one thing every channel must be able
to do: `deliver(recipient, subject, body)`. Ask: *"Why doesn't this
interface know anything about order confirmations or password resets?"*

**2. The abstraction — `Notification.java`**
This is the heart of the session. Point at the `channel` field and ask:
*"Is this inheritance or composition?"* Composition — and that one field
is the entire bridge. Point at `send()` being `final`: subclasses can never
override how delivery is triggered, only what gets delivered.

**3. A refined abstraction — `OrderConfirmationNotification.java`**
Ask: *"Which channel does this class work with?"* Trick question — it
doesn't know, and doesn't care. Prove it by running the same notification
through `EmailChannel`, `SmsChannel`, and `PushChannel` live.

**4. A concrete implementor — `SmsChannel.java`**
Point at `MAX_LENGTH` and the truncation logic. Ask: *"How many places in
this codebase know about the 140-character SMS limit?"* Exactly one.

**5. The trap — `NaiveOrderConfirmationSms.java` /
`NaiveShippingUpdateSms.java`**
Put the truncation block from both naive classes side by side. Ask:
*"These are identical. What happens when the SMS provider changes the
limit to 160 characters?"* Two edits instead of one — and that gap grows
with every notification type added.

**6. The client — `NotificationDemo.java`**
Run `./gradlew run` live. Point at the section demonstrating truncation
with a long shipping-status message, and show the `…` in the SMS output
but not the email output for the exact same notification instance's
content.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a channel (everyone)

Add a `WhatsAppChannel` (pick any made-up formatting rule, e.g. prefix
every message with `"[WA] "`). Confirm every existing `Notification`
subclass works with it immediately, with zero changes to
`Notification`/`OrderConfirmationNotification`/etc.

> **The payoff:** a whole new delivery mechanism cost exactly one class.
> Say this out loud when someone finishes.

### Exercise 2 — Add a notification type (everyone)

Add a `BackInStockNotification` refined abstraction. Confirm it works with
`EmailChannel`, `SmsChannel`, and `PushChannel` immediately, with zero
changes to any channel class.

### Exercise 3 — Break the bridge on purpose (discussion)

Add an `if (channel instanceof SmsChannel)` check inside a
`Notification` subclass's `body()` method that shortens the body when
talking to SMS. Discuss: *"What did we just throw away?"* The whole point
of the abstraction staying ignorant of the implementor — now content and
delivery are coupled again, exactly like the naive trap.

### Exercise 4 — Stretch (for fast finishers)

Give `Notification` a package-private setter so its `channel` can be
swapped after construction (rather than only at construction time via the
constructor). Discuss: does this still satisfy Bridge? (Yes — the pattern
only requires the connection to be composition, not that it be
immutable.)

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- Bridge only pays off with two genuinely independent axes of variation —
  don't introduce it for a single channel or a single notification type.
- The abstraction must never need to know implementor-specific facts (like
  SMS's 140-character limit) to do its job.
- A `final` implementor field is a deliberate simplicity choice here, not
  a requirement of the pattern.

Then the comparison table. The line worth memorising:

> **Adapter reconciles two interfaces that already exist and disagree.
> Bridge designs two hierarchies from the start so they never have to
> agree on more than one seam.**

Close with real-world sightings: JDBC drivers, logging facades (SLF4J),
cross-platform UI toolkits, device drivers.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one place in your own codebase where "what" and "how" are welded
> into one class per combination — a report generator with one class per
> (report type, output format) pair is a common one — and sketch what the
> Bridge split would look like.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "Isn't this the same as Adapter?" | No — Adapter reconciles an interface you didn't design after the fact; Bridge designs two hierarchies together, up front, so they never disagree in the first place |
| "Why not just pass a lambda instead of a `MessageChannel` interface?" | You could for a single method — but `MessageChannel` also carries `channelName()`, and a named interface documents the implementor role clearly for a teaching example |
| "This feels like overkill for three channels and three notification types" | Fair, at this size. The payoff scales with how many types exist on *each* axis — with two channels and two types it's a wash; with five and five it's the difference between 10 and 25 classes |
| "Shouldn't `SmsChannel` know about `OrderConfirmationNotification` to format it specially?" | No — that would break the whole separation. If a channel needs type-specific formatting, that belongs in the notification's `body()`, decided independently of which channel eventually receives it |

**If you are running short on time:** cut Exercise 4 and shorten the
pitfalls discussion. Never cut Exercise 3 — hitting the "what did we throw
away" moment is where the value of keeping the abstraction ignorant of the
implementor actually lands.

**If you have extra time:** have participants implement a `deliver()` for
a hypothetical `SlackChannel` that formats the message as Markdown, and
discuss whether that requires any change to `Notification` or its
subclasses (it should not).

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/bridge-pattern-explained.mp4`) — useful
      as a recap for anyone who joins late, or to send round afterwards
- [ ] The printed notification output from `./gradlew run` ready to put on
      the board
- [ ] IDE font size raised for screen sharing
