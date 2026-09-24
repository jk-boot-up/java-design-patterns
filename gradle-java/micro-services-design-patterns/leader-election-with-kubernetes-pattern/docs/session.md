# Session Guide — Leader Election with Kubernetes Pattern

A 60-minute session built around one question: once the lease lives in a real API server, who decides that it has run out, and what can a leader that froze still do?

## Learning Objectives

1. Say, in plain words, what a cluster, a node, the API server, a Lease, its holder, its renewal time and a resource version are.
2. Show the API server refusing a write made from an old version with 409 Conflict, and say why that is the only rule it enforces about a lease.
3. Compare a leader shut down cleanly with a leader killed outright, and say why only one of them leaves a whole lease with no leader.
4. Use the lease's own holder and renewal time to prove that a frozen leader sent a report after it had lost the lease.
5. Explain a fencing token, where it comes from here, and why the receiver, not Kubernetes, has to check it.
6. Say what Fabric8's elector does after it loses the lease, and what a real deployment does about that.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The staff-room notice board, and the plain-Java project recapped in two minutes |
| 0:08–0:18 | Acts one and two: no election, then a lease, and the 409 |
| 0:18–0:28 | Act three: stopped cleanly, and killed outright |
| 0:28–0:42 | Act four: the frozen leader, and the lease's own record as proof |
| 0:42–0:50 | Acts five and six: fencing, and the bill |
| 0:50–0:55 | The verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, and check that `kind version` works.

```bash
cd micro-services-design-patterns/leader-election-with-kubernetes-pattern
./gradlew -q run
```

Act one: how many reports reached the manager? Act two: what are the three fields the demo reads from the lease, and what would a copy with the second, refused write have to do next? Act three: why did one handover take a couple of seconds and the other about a whole lease? Act four: A checked it was the leader, and it was. What made the report wrong anyway, and which two fields of the lease prove it? Act five: where does the token come from, and who checks it? Act six: A was alive for two whole leases and nobody led. Why?

Then open `src/main/java/com/jk/explore/leaderelectionk8s/Candidate.java` and read `report` aloud. The check and the send are two lines apart. Everything in act four happens between them.

## Discussion

Ask the room which jobs in a real store need one leader: the nightly sales report, the job that releases unpaid orders' stock, the one that sends the weekly newsletter. Which of them would be harmless if run twice? Those need no election.

Then ask what should receive the token in each case. An inbox is easy. A payment provider may not accept one. If the receiver cannot check a token, what else could the leader do?

## Exercises

1. Change the lease in `Candidate` to 2 seconds and the renew deadline to 3, run it, and read the error Fabric8 gives before anything starts.
2. Remove `withReleaseOnCancel(true)`, run act three, and predict how the first handover's description changes.
3. In `stoppedLeading`, call `System.exit(1)`, and say what would restart the copy in a real deployment.
4. Make the inbox read the lease's current count of holder changes from the API server instead of remembering the highest token it has seen, and say what that costs and what it gains.
5. Suppose B's clock runs ten seconds fast. Using the rule every copy follows — the last renewal time plus the lease length, compared with its own clock — say what B does while A is perfectly healthy.

Close with the verdict: let the elector renew, fence every write the leader makes, and let a copy that loses the lease exit and be restarted.
