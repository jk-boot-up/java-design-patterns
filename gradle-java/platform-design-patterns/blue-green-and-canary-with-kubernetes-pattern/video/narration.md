# Blue-Green and Canary with Kubernetes Pattern — Video Narration Script

## 1. Blue-Green and Canary with Kubernetes

Hello, and welcome. This video explains the Blue-Green and Canary patterns in Java, using Kubernetes. This video is presented by Jayasekhar Konduru. First, a simple definition. Blue-green runs the old and new releases side by side, and switches all the traffic at once. A canary sends a small share of traffic to the new release first, and grows it while it stays healthy. On Kubernetes, blue-green is one change to which copies a service points at. And a canary is a change to how many copies of each release are running. In our online store, a new checkout release must go live safely. By the end, you will hear a real cluster fail every request while a release is replaced. A real switch, and a real switch back. A canary spread by the cluster itself. A gate that stops a bad release. And the bill.

## 2. The Partner Project

This video builds on the plain Java Blue-Green and Canary video. If you have not seen it, start there. That video runs two releases behind a simple routing rule. And it shows a switch, a switch back, a canary, and a gate. This video uses the same example. It does not teach the pattern again. It shows what Kubernetes does with it.

## 3. Before The First Line

Before any code, what is Kubernetes? Kubernetes runs containers in small groups, called pods. And it keeps as many pods running as you ask for. A service gives those pods one address. It picks which pods to send traffic to by their labels. A tool called kind runs a whole Kubernetes cluster inside Docker, on your own machine. You need Docker running, with kind and the kube control tool installed. Without them, the demo says so, and stops. And a promise. Skipping this video loses none of the pattern. The plain Java video teaches all of it.

## 4. Replace It Where It Stands

First demo: replace it where it stands. Version one is stopped, to make room for version two. Twenty requests arrive while nothing is running. And all twenty fail. This is a real cluster, and it really refuses them.

## 5. Blue And Green

Second demo: blue and green. Version two runs beside version one. Only a separate test port can reach it. Twenty requests before the switch are all answered by version one. The switch is one change to the service. Twenty requests after it are all answered by version two. And none failed.

## 6. Going Back

Third demo: going back. Version two has a bug with big orders. Twenty big orders go to version two, and all twenty fail. One change points the service back at version one. Its pods never stopped. Twenty big orders: none fail.

## 7. A Canary

Fourth demo: a canary. Nine pods of version one, and one pod of version two, behind one service. Three hundred big orders are sent. A few dozen fail: a small share, just as a canary should be. The cluster itself decides how to spread the requests. So the exact count changes from run to run. If all three hundred had gone to version two, every one would have failed.

## 8. Promote In Steps, With A Gate

Fifth demo: promote in steps, with a gate. The steps are one, five, and ten pods of version two. The gate says: stop if more than five requests in a hundred fail. The buggy release is stopped. And every pod is version one again. One lesson: a first step with only a few requests can miss a bug. The next step, with more traffic, is what catches it.

## 9. The Bill

Finally, the bill. During a blue-green switch, both releases are fully running. Four pods, where one release needs only two. Both releases share one database. So a release that changes the shape of the data cannot be switched back safely. And a whole cluster is a lot to run, just for a checkout.

## 10. The Verdict

So, here is the verdict. Release beside the old version. On Kubernetes, switch by changing where the service points, and go back the same way. Use pod counts for a canary, with a gate on failures, and enough traffic at each step. Use a rollout tool to automate it. And keep data changes readable by both releases.

## 11. How To Recognise It

How can you spot this in a system someone else built? Look for a service that picks its pods by a version label. Look for two deployments of one app, with different version labels. Or look for rollout tools like Argo Rollouts or Flagger.

## 12. Where You Have Met This

Where have you met this before? On Kubernetes platforms, and the release tools built for them.

## 13. What Was Used

For the record, here is what was used. Kubernetes, run through kind, version zero point thirty-three. The nginx web server, as the stand-in service. And Docker, version twenty-four or later.

## 14. What Is Real Here

A quick, honest note about this demo. Everything is real: a real cluster, real pods, and a real service. The canary's spread is chosen by the cluster. So its counts change from run to run.

## 15. When This Is Too Much

So, when is this too much? For an internal tool where a short outage is fine, a plain restart is enough. And a cluster is a lot to run for one service.

## 16. Thanks for Watching

That's Blue-Green and Canary, with Kubernetes. If you remember one sentence, make it this one. On Kubernetes, a release is a label choice and some pod counts, and the cluster does the rest. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Change the gate to two failures in a hundred. Then run the fifth demo again. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
