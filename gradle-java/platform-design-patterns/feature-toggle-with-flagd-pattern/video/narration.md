# Feature Toggle with flagd Pattern — Video Narration Script

## 1. Feature Toggle with flagd

Hello, and welcome. This video explains the Feature Toggle pattern with flagd and OpenFeature, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Feature Toggle video. That one put gift wrap behind a table of switches read at run time. It showed the feature deployed dark, switched on for some customers, turned off by a kill switch, and safe when the table cannot be read. This one shows the same idea inside flagd and OpenFeature. The plain definition, in short: with flagd, a flag is an entry in a file that a daemon watches. The application asks the daemon whether a flag is on for a customer. By the end you will see a real flag daemon serve a flag that is off, see the file edited and the daemon notice by itself, see a rollout to a share of customers and to named testers, see a kill switch, see the checkout fall back when the daemon is stopped, and see the bill.

## 2. The Partner Project

This video assumes the Feature Toggle video. If you have not seen it, start there. It puts gift wrap behind a table of switches, and shows a dark deploy, a rollout, a kill switch, and a safe default. This one uses the same example. It does not teach the pattern again. It shows what flagd and OpenFeature does with it.

## 3. Before The First Line

Before the first line of code, what flagd and OpenFeature is. Open Feature is a standard way to ask whether a feature is on. Flagd is a small daemon that answers that question. It reads its flags from a file, notices when the file changes, and needs no restart. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. Deploying Is Releasing

First, deploying is releasing. Gift wrap goes live by deploying it: one deploy. It has a bug, so taking it away is another: two deploys. Each deploy ships every other change waiting in the branch too.

## 5. Deploy Dark, Switch Later

Second, deploy dark, switch later. Gift wrap is in the deployed code, and flagd has it off. An order of five thousand costs five thousand. The flags file is edited, and flagd notices by itself: no deploy, no restart. The same order costs fifty three hundred.

## 6. Switch On For Some

Third, switch on for some. A ten percent rollout, decided by flagd's own hash of the customer. Of a hundred customers, about a tenth got it. Then only two named testers: of a hundred customers, two got it.

## 7. The Kill Switch

Fourth, the kill switch. Gift wrap has a bug. With twenty percent on, about a fifth of a hundred orders failed. One edit to the file turned it off. Of a hundred orders, none failed. No deploy.

## 8. When flagd Cannot Be Reached

Fifth, when flagd cannot be reached. Flagd is up, and an order of five thousand costs fifty three hundred. Flagd is stopped, and it costs five thousand. The order still works, and every feature falls back to off.

## 9. The Bill

Last, the bill. A shop with five flags would have thirty two possible combinations. The tests usually run one. Flagd is another process to run and keep up, and every flag check is a network call: this demo made hundreds. And a flag that is settled and still in the file is an if that nobody needs. Flagd does not remove it for you.

## 10. The Verdict

My verdict, plainly. Keep flags in a file or service that a daemon serves, and change them there, not in code. Rollouts by hash are repeatable, so the same customers stay in. Decide what happens when the daemon is down: off is the safe answer. And remove settled flags.

## 11. How To Recognise It

How do you recognise this in code you did not write? A flags.json with variants, defaultVariant and targeting. An OpenFeature client, client.getBooleanValue(...). A fractional rule for a percentage rollout.

## 12. Where You Have Met This

You have met this in companies that use openfeature with launchdarkly, flagsmith, unleash or their own service.

## 13. What Was Used

For the record. flagd, latest, built September tenth, twenty twenty six. Docker, 24 or later.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: a real flagd in a container, a real file it watches, and real HTTP calls. The rollout is by flagd's own hash, so the same customers are picked on every run.

## 15. When This Is Too Much

So when is it too much? For a handful of switches that change with each release, a setting in the deployment is enough. A daemon adds a process and a network call to every check.

## 16. Thanks for Watching

That's Feature Toggle with flagd. If you take one sentence away, take this one: a real flag daemon turns a file edit into a release, and the price is a process to run and a call for every check. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, add a second flag for express shipping, and turn it on for the named testers. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
