# Feature Toggle Pattern — Video Narration Script

## 1. Feature Toggle

Hello, and welcome. This video explains the Feature Toggle pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a feature toggle puts a new feature in the deployed code, behind a switch that is read while the program runs. Turning it on or off is then a change of a setting, and not a new release. This is another project in the platform category, whose subject is how software is shipped, run and operated. In our online store, gift wrap is ready, but we want to turn it on for a few customers first, and off again at once if it goes wrong. By the end you will see a feature that can only be released by deploying, see a feature deployed dark and switched on later, see it switched on for some customers, see a kill switch stop failures, see the safe answer when the switch table is down, and see the bill, which is combinations and old switches.

## 2. The Scenario

Here is the scenario. Gift wrap adds three pounds to an order. It has been coded, and it has a bug that nobody has found yet. We would like to try it on a few customers first. The question: how do we switch it on?

## 3. Deploying Is Releasing

First, deploying is releasing. Gift wrap goes live by deploying it: one deploy. It has a bug, so taking it away is another: two deploys. Each deploy ships every other change waiting in the branch too. The wish to switch one thing carries everything else with it.

## 4. The Pattern

The pattern. Ship the feature switched off. A table of switches is read while the program runs. Turning the feature on, for some customers or all, or off again, is a change of setting.

## 5. Deploy Dark, Switch Later

Second, deploy dark, switch later. Gift wrap is in the deployed code, switched off. An order of five thousand costs five thousand. The switch is turned on in the table, with no deploy. The same order costs fifty three hundred.

## 6. Switch On For Some

Third, switch on for some. A ten percent rollout: of a hundred customers, ten got it. Then only two named testers: of a hundred customers, two got it.

## 7. The Kill Switch

Fourth, the kill switch. Gift wrap has a bug. With twenty percent on, of a hundred orders, twenty failed. One change in the table turned it off. Of a hundred orders, none failed. No deploy.

## 8. When The Table Cannot Be Read

Fifth, when the table cannot be read. The table is up, and an order of five thousand costs fifty three hundred. The table is down, and it costs five thousand. The order still works, and every feature falls back to off.

## 9. The Bill

Last, the bill. Five toggles make thirty two possible combinations. The tests usually run one. And on day two hundred, three toggles have been settled for over ninety days, and are still in the code: express shipping, gift wrap, and new search. Every one is an if that nobody needs.

## 10. How To Recognise It

How do you recognise this in code you did not write? if (flags.isEnabled("name", user)) in application code. LaunchDarkly, Unleash, Flagsmith, Togglz, or a homemade table. A percentage rollout by user id. A toggle named after a ticket, still in the code a year later.

## 11. The Verdict

Here is my verdict, plainly. Ship features switched off, and turn them on for a few, then more. Keep a kill switch for anything risky. Choose the safe answer for when the table cannot be read. And remove every toggle once it has settled, because each one costs a combination.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For a change that is small and safe, a plain release is simpler. A toggle is a branch in your code that must later be removed.

## 14. Thanks for Watching

That's Feature Toggle. If you take one sentence away, take this one: a feature toggle turns release into a setting and gives you a kill switch, and the price is combinations to test and old toggles to remove. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a rule that switches gift wrap on for customers whose number is even, and check it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
