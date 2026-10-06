# Feature Toggle with flagd Pattern — Video Narration Script

## 1. Feature Toggle with flagd

Hello, and welcome. This video explains the Feature Toggle pattern in Java, using two tools: flagd and OpenFeature. This video is presented by Jayasekhar Konduru. First, a simple definition. A feature toggle puts a new feature into the released code, behind a switch that is read while the program runs. So turning it on or off is a change of setting, not a new release. With flagd, each switch, called a flag, is an entry in a file. A small background program watches that file. And the shop asks it whether a flag is on, for a given customer. In our online store, the feature is gift wrap. By the end, you will hear a real flag program serve a flag that is off. The file edited, and the change noticed by itself. A rollout to some customers. A kill switch. The checkout falling back when the flag program stops. And the bill.

## 2. The Partner Project

This video builds on the plain Java Feature Toggle video. If you have not seen it, start there. That video puts gift wrap behind a table of switches. It shows the feature shipped switched off, a rollout, a kill switch, and a safe default. This video uses the same example. It does not teach the pattern again. It shows what flagd and OpenFeature do with it.

## 3. Before The First Line

Before any code, what are these two tools? OpenFeature is a standard way for code to ask whether a feature is on. flagd is a small background program that answers that question. It reads its flags from a file. It notices when the file changes. And it needs no restart. You need Docker running to try it. Without Docker, the demo says so, and stops. And a promise. Skipping this video loses none of the pattern. The plain Java video teaches all of it.

## 4. Deploying Is Releasing

First demo: releasing by redeploying. Gift wrap goes live by releasing new code. That is one release. It has a bug, so taking it away needs another release. That is two. And each release also ships every other change that is waiting.

## 5. Deploy Dark, Switch Later

Second demo: ship it switched off, and turn it on later. Gift wrap is in the released code, and flagd has it switched off. A fifty-pound order costs fifty pounds. Then the flags file is edited. And flagd notices by itself. No release, and no restart. The same order now costs fifty-three pounds, with gift wrap.

## 6. Switch On For Some

Third demo: switch it on for some customers. A ten percent rollout. flagd decides who is in by scrambling each customer's number in a fixed way. Out of a hundred customers, about ten get it. Then, only two named testers. Out of a hundred customers, just those two get it.

## 7. The Kill Switch

Fourth demo: the kill switch. Gift wrap has a bug. With twenty percent switched on, about a fifth of a hundred orders fail. One edit to the file turns it off. Out of the next hundred orders, none fail. No release.

## 8. When flagd Cannot Be Reached

Fifth demo: when flagd cannot be reached. With flagd running, a fifty-pound order costs fifty-three. With flagd stopped, it costs fifty. The order still works. Every feature simply falls back to off.

## 9. The Bill

Finally, the bill. A shop with five flags has thirty-two possible combinations. And the tests usually run just one. flagd is one more program to run and keep up. And every flag check is a network call. This demo made hundreds of them. And a flag that is settled, but still in the file, is a branch in the code nobody needs. flagd will not remove it for you.

## 10. The Verdict

So, here is the verdict. Keep flags in a file or service, served by a program like flagd. And change them there, not in the code. Percentage rollouts by a fixed scramble are repeatable, so the same customers stay in. Decide what happens when flagd is down: off is the safe answer. And remove flags once they are settled.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for a flags file listing each flag's options, its default, and its targeting rules. Look for an OpenFeature client that asks for a flag's value. Or a fractional rule, used for a percentage rollout.

## 12. Where You Have Met This

Where have you met this before? In companies that use OpenFeature with services like LaunchDarkly, Flagsmith, Unleash, or their own flag service.

## 13. What Was Used

For the record, here is what was used. The latest flagd release, built on the tenth of September, twenty twenty-six. And Docker, version twenty-four or later.

## 14. What Is Real Here

A quick, honest note about this demo. Everything is real: a real flagd in a container, a real file it watches, and real web requests. The rollout uses flagd's own fixed scramble. So the same customers are picked on every run.

## 15. When This Is Too Much

So, when is this too much? For a handful of switches that change with each release, a setting in the release itself is enough. A flag program adds a process to run, and a network call to every check.

## 16. Thanks for Watching

That's Feature Toggle, with flagd. If you remember one sentence, make it this one. A real flag program turns a file edit into a release, and the price is one more process to run, and a network call for every check. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a second flag, for express shipping. And turn it on for the two named testers. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
