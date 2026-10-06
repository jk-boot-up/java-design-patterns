# Blue-Green and Canary Pattern — Video Narration Script

## 1. Blue-Green and Canary

Hello, and welcome. This video explains the Blue-Green and Canary patterns, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Blue-green runs the old release and the new release side by side. Then it switches all the traffic across at once. A canary sends only a small share of traffic to the new release first. And it grows that share only while the new release stays healthy. The name comes from coal mines, where a canary warned miners of danger before it reached everyone. In our online store, a new release of checkout must go live without customers noticing, and without taking all the risk at once. By the end, you will hear a release that fails requests while it is replaced. A switch where none fail. A quick way back. A canary that meets only a few failures. A gate that stops a bad release. And the bill.

## 2. The Scenario

Here is the scenario. A new release of checkout is ready. One order in ten is a big one. And the new release has a bug with big orders, that nobody has found yet. So here is the question. How do we go live?

## 3. Replace It Where It Stands

First demo: replace it where it stands. Stop version one. Install version two. Start version two. Ten requests arrive while it is down. So, out of a hundred requests, ten failed.

## 4. The Pattern

Now, the pattern. Run the new release beside the old one. With blue-green, switch all the traffic at once. And switch it back at once, if needed. With a canary, send a small share first. And grow it while the new release stays healthy.

## 5. Blue And Green

Second demo: blue and green. Version two is started beside version one. It is tried with a test order, and it works. Meanwhile, version one serves fifty real requests. The switch is one setting. After it, version two serves the next fifty. Out of a hundred requests, none failed.

## 6. Going Back

Third demo: going back. Version two has the bug with big orders. Of fifty requests on version two, five failed. One setting sends traffic back to version one. Version one was never stopped, so it is ready at once. The next fifty requests: none failed.

## 7. A Canary

Fourth demo: a canary. Five percent of traffic goes to the buggy version two. Out of two hundred requests, version two got ten. And two of them failed. If all two hundred had gone to version two, twenty would have failed. A few customers met the bug, not everyone.

## 8. Promote In Steps, With A Gate

Fifth demo: promote in steps, with a gate. The steps are five, twenty-five, fifty, and a hundred percent. The gate says: stop if more than five percent of requests fail. The buggy version two is stopped after the first step, with twenty percent failing. And traffic goes back to version one. A good version two passes all four steps, and ends up with all the traffic.

## 9. The Bill

Finally, the bill. During the switch, two full copies are running. So you pay for twice the capacity. And there is a harder cost. Before we went back, version two saved five orders in a new format. Version one cannot read any of them. Both releases share one database. So a release that changes the shape of the data cannot be switched back safely.

## 10. How To Recognise It

How can you spot this pattern in a system someone else built? Look for two copies of a service, behind one load balancer. Look for traffic weights, like five, twenty-five, and a hundred percent. Look for tools like Argo Rollouts, Flagger, or Amazon CodeDeploy. Or a rollout that pauses to check the error rate.

## 11. The Verdict

So, here is the verdict. Release beside the old version, never on top of it. Switch with a setting, so going back is also just a setting. Use a canary for risky changes, with a gate on failures. Keep data changes readable by both the old and new releases. And accept paying for extra capacity while the switch happens.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Nothing depends on a real clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For an internal tool where a short outage is fine, a plain restart is enough. These methods pay off where downtime, or a bad release, is costly.

## 14. Thanks for Watching

That's Blue-Green and Canary. If you remember one sentence, make it this one. Release beside the old version, and go back with one setting, but pay for double capacity, and keep the shared data readable by both. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Change the gate to two percent. Then see whether the buggy release is stopped sooner. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
