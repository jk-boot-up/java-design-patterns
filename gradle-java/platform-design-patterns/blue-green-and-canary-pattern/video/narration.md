# Blue-Green and Canary Pattern — Video Narration Script

## 1. Blue-Green and Canary

Hello, and welcome. This video explains the Blue-Green and Canary pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: blue green runs the old and the new release side by side, and switches traffic at once. A canary sends a small share of traffic to the new release first, and grows it only while it stays healthy. This is another project in the platform category, whose subject is how software is shipped, run and operated. In our online store, a new release of the checkout must go live without customers noticing, and without taking the risk all at once. By the end you will see a release that fails requests while it is replaced, see a switch with none failing, see a quick way back, see a canary meet only a few failures, see a gate halt a bad release and promote a good one, and see the bill, which is double capacity and a shared database.

## 2. The Scenario

Here is the scenario. A new release of the checkout is ready. One order in ten is a big one, and the new release has a bug with big orders that nobody has found yet. The question: how do we go live?

## 3. Replace It Where It Stands

First, replace it where it stands. Stop version one, install version two, start version two. Ten requests arrive while it is down. Of a hundred requests, ten failed.

## 4. The Pattern

The pattern. Run the new release beside the old one. Blue green: switch all the traffic at once, and back at once. Canary: send a small share first, and grow it while it stays healthy.

## 5. Blue And Green

Second, blue and green. Version two is started beside version one, and tried with a test order. It is fine. Version one served fifty requests meanwhile. The switch is one setting. After it, version two serves the next fifty. Of a hundred requests, none failed.

## 6. Going Back

Third, going back. Version two has a bug with big orders. Fifty requests on version two, five failed. One setting sends traffic back to version one, which was never stopped. The next fifty requests, none failed.

## 7. A Canary

Fourth, a canary. Five percent of traffic goes to the buggy version two. Of two hundred requests, version two got ten, and failed two. Had all two hundred gone to version two, twenty would have failed. A few customers found the bug, not everyone.

## 8. Promote In Steps, With A Gate

Fifth, promote in steps, with a gate. Steps of five, twenty five, fifty and a hundred percent, with a gate at five percent failures. The buggy version two is halted after one step, with twenty percent failing, and traffic goes back to version one. The good version two goes through all four steps, and ends at a hundred percent.

## 9. The Bill

Last, the bill. Two full copies run during the switch: capacity twenty instead of ten. And version two wrote five orders in a new format before we went back. Version one can read none of them. Both releases share one database, so a release that changes the data cannot be switched back safely.

## 10. How To Recognise It

How do you recognise this in code you did not write? Two deployments or target groups behind a load balancer. Traffic weights of 5, 25 and 100 percent. Argo Rollouts, Flagger, AWS CodeDeploy, Kubernetes with an Istio route. A rollout that pauses on an error-rate check.

## 11. The Verdict

Here is my verdict, plainly. Release beside the old version, never on top of it. Switch by a setting, so that going back is a setting. Use a canary for risky changes, with a gate on failures. Keep data changes compatible in both directions, and pay for the extra capacity for the time it takes.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For an internal tool where a short outage is fine, a plain restart is enough. These methods pay off where downtime or a bad release is costly.

## 14. Thanks for Watching

That's Blue-Green and Canary. If you take one sentence away, take this one: blue green and canary let a release go live beside the old one and go back with one setting, and the price is double capacity and a shared database that both releases must understand. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, change the gate to two percent, and see whether the buggy release is halted sooner. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
