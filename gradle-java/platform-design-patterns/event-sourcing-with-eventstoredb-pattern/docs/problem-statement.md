# Problem Statement

## The scenario

The shop runs a loyalty scheme. Customers earn one point per pound spent, spend points on later orders, and lose points they have not used within twelve months. No balance is stored anywhere. Every award, spend and expiry is kept as an event, in order, and the balance is worked out by adding them up. A customer can pay with points on the website or in the phone app, and both write to the same history.

## The naive version

The naive version skips the check. It reads a customer's events, adds them up, decides the customer can afford the spend, and appends the spend. If two checkouts do that at the same moment, both see the same balance and both spend it:

```
  C-5120 has 140 points. the website and the phone app both look: 140 points, at revision 3.
  both decide 100 is not more than 140, and both append a redemption with the check off.
  both appends accepted, at revisions 4 and 5. balance now: -60 points.
```

## What the twin project already did

The plain-Java Event Sourcing project in this course taught the whole idea. Events are facts in the past tense and are only ever added. The balance is added up, never stored. The same four March events explain why customer C-4417 has 140 points. It showed that a bug fix can be made in the code that reads events without editing a single event. It also covered snapshots, erasure, versioned events and the difference from CQRS. None of that is replaced here.

It had one comfort, though. Its event store was a list inside one program, with one writer, so two decisions could never overlap. Nothing could be lost on a network. No reader ever started late. And its delete really removed the events.

## What this project must deliver

The same shop, the same customers and the same March events, kept in a real KurrentDB server (the database once called EventStoreDB). The demo starts it in a container and stops it at the end. It covers:

- Four events appended and read back from the start by a second connection.
- Two real connections racing to spend the same points: once with no check, which gives -60, and once with the expected revision, which refuses the second spend with WrongExpectedVersion.
- A retry after a lost reply. With a new event id it is written twice. With the same event id the server recognises it and writes nothing.
- A support dashboard that starts last, catches up on 18 stored events and then follows new ones.
- An honest bill. A deleted stream is not found, but its events stay in the whole log until a scavenge runs and stay on the dashboard, and the stream's numbering carries on. The server ran with security off, which production must never do.

Every figure printed is the program's own, and two runs back to back print the same thing.
