# Feature Toggle Pattern — Video Narration Script

## 1. Feature Toggle

Hello, and welcome. This video explains the Feature Toggle pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A feature toggle puts a new feature into the released code, behind a switch. The switch is read while the program runs. So turning the feature on or off is a change of setting, not a new release. Think of the light switches in a new house. The wiring is all installed. But each light only comes on when you flip its switch. In our online store, gift wrap is ready. But we want to try it on a few customers first, and turn it off at once if it goes wrong. By the end, you will hear a feature that can only be released by redeploying. The same feature shipped switched off, and turned on later. Turned on for some customers only. A kill switch that stops failures. A safe answer when the switches cannot be read. And the bill.

## 2. The Scenario

Here is the scenario. Gift wrap adds three pounds to an order. It has been built. And it has a bug that nobody has found yet. We would like to try it on a few customers first. So here is the question. How do we switch it on?

## 3. Deploying Is Releasing

First demo: deploying is releasing. Gift wrap goes live by releasing new code. That is one release. It has a bug, so taking it away needs another release. That is two. And each release also ships every other change waiting to go out. Switching one feature drags everything else along with it.

## 4. The Pattern

Now, the pattern. Ship the feature switched off. A table of switches is read while the program runs. Turning the feature on, for some customers or for everyone, is a change in that table. And so is turning it off again.

## 5. Deploy Dark, Switch Later

Second demo: ship it dark, and switch it on later. Gift wrap is in the released code, but switched off. An order of fifty pounds costs fifty pounds. Then the switch is turned on in the table. No release. The same order now costs fifty-three pounds.

## 6. Switch On For Some

Third demo: switch it on for some customers. A ten percent rollout. Out of a hundred customers, ten get gift wrap. Then, only two named testers. Out of a hundred customers, just those two get it.

## 7. The Kill Switch

Fourth demo: the kill switch. Gift wrap has its bug. With twenty percent of customers switched on, twenty orders out of a hundred fail. One change in the table turns it off. Out of the next hundred orders, none fail. And there was no release.

## 8. When The Table Cannot Be Read

Fifth demo: when the switch table cannot be read. With the table working, a fifty-pound order costs fifty-three, with gift wrap. With the table down, it costs fifty. The order still works. Every feature simply falls back to off.

## 9. The Bill

Finally, the bill. Five toggles make thirty-two possible combinations. And the tests usually run just one of them. And on day two hundred, three toggles have been fully on for more than ninety days. They are still in the code: express shipping, gift wrap, and new search. Each one is a branch in the code that nobody needs any more.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for code that asks whether a named feature is enabled, for this user. Look for services like LaunchDarkly, Unleash, or Flagsmith, or a homemade table of switches. Look for a rollout by percentage of users. Or a toggle named after an old ticket, still in the code a year later.

## 11. The Verdict

So, here is the verdict. Ship features switched off. Then turn them on for a few customers, and then more. Keep a kill switch for anything risky. Choose a safe answer for when the table cannot be read. And remove every toggle once the decision is settled. Because each one doubles the combinations to test.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Nothing depends on a real clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For a small, safe change, a normal release is simpler. A toggle is a branch in your code, and it must be removed later.

## 14. Thanks for Watching

That's the Feature Toggle pattern. If you remember one sentence, make it this one. A feature toggle turns a release into a setting, and gives you a kill switch, and the price is combinations to test, and old toggles to remove. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a rule that turns gift wrap on for customers whose number is even. And check that it works. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
