# Blue-Green and Canary with Kubernetes Pattern — Video Narration Script

## 1. Blue-Green and Canary with Kubernetes

Hello, and welcome. This video explains the Blue-Green and Canary pattern with Kubernetes, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Blue-Green and Canary video. That one ran two releases of the checkout behind a router that was a rule on the request number. It showed an in place upgrade failing requests, a switch and a switch back, a canary, and a gate that halts a bad release. This one shows the same idea inside Kubernetes. The plain definition, in short: on Kubernetes, blue green is a change to a service's selector, between two deployments. A canary is a change to the replica counts of two deployments behind one service. By the end you will see a real cluster fail every request while a release is replaced, see a real switch and a real switch back, see a canary spread by the cluster itself, see a gate halt a bad release, and see the bill: pods for two releases at once.

## 2. The Partner Project

This video assumes the Blue-Green and Canary video. If you have not seen it, start there. It runs two releases behind a router that is a rule on the request number, and shows a switch, a switch back, a canary and a gate. This one uses the same example. It does not teach the pattern again. It shows what Kubernetes does with it.

## 3. Before The First Line

Before the first line of code, what Kubernetes is. Kubernetes is a system that runs containers in groups called pods, and keeps as many as you ask for. A service gives them one address, and picks them by label. Kind runs a whole cluster inside Docker on your own machine. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. Replace It Where It Stands

First, replace it where it stands. Version one is stopped to make room for version two. Twenty requests arrive while nothing is running, and all twenty fail. This is a real cluster, and it really refuses.

## 5. Blue And Green

Second, blue and green. Version two runs beside version one, and only a test port reaches it. Twenty requests before the switch are all answered by version one. The switch is one patch to the service. Twenty after are all answered by version two, and none failed.

## 6. Going Back

Third, going back. Version two has a bug with big orders. Twenty big orders on version two: all twenty fail. One patch sends the service back to version one, whose pods never stopped. Twenty big orders: none fail.

## 7. A Canary

Fourth, a canary. Nine pods of version one and one of version two, behind one service. Three hundred big orders: a few dozen failed, a small share, as a canary should be. The spread is chosen by the cluster's own rules, so the exact count changes from run to run. Had all three hundred gone to version two, all would have failed.

## 8. Promote In Steps, With A Gate

Fifth, promote in steps, with a gate. Steps of one, five and ten pods of version two, with a gate at five failures in a hundred. The buggy release is halted, and every pod is version one again. A first step with few requests can miss a bug, and the next step, with more traffic, catches it.

## 9. The Bill

Last, the bill. During a blue-green switch both releases are fully running: four pods, where one release needs two. Both share one database, so a release that changes the data cannot be switched back safely. And a cluster is a lot to run for a checkout.

## 10. The Verdict

My verdict, plainly. Release beside the old version. On Kubernetes, switch with a selector and go back with the same. Use replica counts for a canary, with a gate on failures and enough traffic per step. Automate it with a rollout tool, and keep data changes compatible in both directions.

## 11. How To Recognise It

How do you recognise this in code you did not write? A Service whose selector includes a version label. Two Deployments of one app, with different version labels. Argo Rollouts or Flagger objects.

## 12. Where You Have Met This

You have met this in kubernetes platforms and their release tools.

## 13. What Was Used

For the record. Kubernetes, via kind 0.33. nginx, alpine. Docker, 24 or later.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: a real cluster, real pods, and a real service. The canary's spread is the cluster's own, so its counts change from run to run.

## 15. When This Is Too Much

So when is it too much? For an internal tool where a short outage is fine, a plain restart is enough, and a cluster is a lot to run for one service.

## 16. Thanks for Watching

That's Blue-Green and Canary with Kubernetes. If you take one sentence away, take this one: on Kubernetes a release is a selector and some replica counts, and the cluster does the rest. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, change the gate to two failures in a hundred, and rerun act five. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
