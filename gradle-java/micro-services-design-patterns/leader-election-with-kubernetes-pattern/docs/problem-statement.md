# Problem Statement

## The scenario

The shop runs three copies of its reporting service, so that one can crash, or be upgraded, without the service going away. Every night exactly one report must reach the store manager: yesterday's sales. Three copies that all send it fill the manager's inbox with duplicates; no copy sending it means a morning with no numbers. The copies have to agree, among themselves and without a person deciding, which one of them sends it — and keep agreeing when that one dies, stops, or freezes.

## The naive version

Every copy sends the report.

```
  three copies of the reporting service run as 3 separate processes. none of them asks who is in charge.
  the nightly sales report is sent by every copy: [A, B, C].
  the manager receives it 3 times.
```

## What the simulation already did

The plain-Java Leader Election project in this course put a lease between the copies: one shared record saying who leads and until when. The copy that holds it sends the report; the others wait, and take over when it runs out. It showed a dead leader leaving a gap, a paused leader waking up and sending a second report, and a fencing token as the answer. It is a complete teaching of the idea, and nothing here replaces it.

It had one comfort, though. The lease record was an object inside the same Java program as the copies, with a clock that moved only when the program said so. The record itself decided when a lease had expired, "pausing" a copy was not calling it for a while, and there was only one way for a leader to go away.

## What this project must deliver

The same shop and the same report, with the lease moved into a real Kubernetes API server, in a one-node kind cluster that the demo creates and deletes. Three copies as three real Java processes, each electing through Fabric8's LeaderElector. The lease's own record, read by an outside observer, showing who holds it and how many times the holder has changed. Two writes made from one version of the lease, and the server refusing the second. A leader shut down cleanly next to a leader killed outright, and how long each leaves the shop without a leader. A leader frozen with every thread stopped after it checked that it leads, and the lease's own holder and renewal time proving it sent the report after the lease had passed to another copy. The fencing check that refuses it. And an honest bill: the loser does not rejoin by itself, the lease is judged by each copy's own clock, and a whole cluster is needed for one nightly report.

Every figure printed comes from the real cluster, and two runs back to back print the same thing.
