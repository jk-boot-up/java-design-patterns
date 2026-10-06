# Event Sourcing Pattern — Video Narration Script

## 1. Event Sourcing

Hello, and welcome. This video explains the Event Sourcing pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Event sourcing stores the things that happened, in order, and never changes them. The current state is worked out by adding those things up, whenever someone asks. The total is not something you keep. It is something you calculate. Think of a bank statement. The bank does not just send you a number. It sends a list of payments, with a running total down the side. In our online store, we look at the loyalty points scheme. A customer rings up and asks why their balance is a hundred and forty. By the end, you will know why a stored total can never explain itself. How a bug found three weeks late is investigated with a question nobody planned. And the four things this pattern costs, because most systems should not use it.

## 2. The Scenario

Here is the scenario. The shop runs a very simple loyalty scheme. You earn one point for every pound you spend. You can spend points on a later order. And points you have not used within twelve months expire. The shop stores it the usual way. A table, with one row per customer, holding one number. One customer has a hundred and forty points. And that number is correct. This is not a broken system. Then one afternoon, the customer rings up with a reasonable question. Why is it a hundred and forty?

## 3. The Naive Approach — Keep the Total

Here is the method that adds points to a customer. It is one line long. It receives four things: the customer, the number of points, which order earned them, and the date. Then it adds the points to the customer's total, and stops. So four facts arrive. Only one is used. The order number and the date reach the code, and are simply dropped. Nobody wrote a bug. This is just what storing only the current state does. It keeps the answer, and throws away the working. And every interesting question is about the working.

## 4. What the Row Can Say

First demo: a support agent tries to answer the customer. The balance is a hundred and forty. And the whole explanation is: the row says a hundred and forty. How it got there was never written down. Four things happened to this customer in March. Each was added to a number, and then forgotten. The usual fix is an audit log: a second table, recording what happened. That helps. But an audit log is a second copy of the truth. And copies drift apart. When they disagree, you cannot tell which one is wrong.

## 5. Three Weeks Later, a Bug

Second demo: a worse story. A new release has a bug. For three weeks, every order awards its points twice. Then someone spots it, and the fix is one line. The hard part is this. Which customers were affected, and by how much? Three customers have balances of a hundred, twenty-five, and sixty. Which of those is wrong? You cannot tell. A doubled forty-five-pound order, plus an earlier ten-pound order, gives a hundred. One honest hundred-pound order also gives a hundred. They look exactly the same. The bug did not just cause damage. Every time it ran, it also erased the evidence of the damage.

## 6. The Pattern

So here is the idea. Nobody ever told this system: the customer has a hundred and forty points. What it was told was a list of events. Sixty earned on the first. Twenty-five spent on the third. A hundred and twenty earned on the eighth. Fifteen expired on the fourteenth. The hundred and forty is just arithmetic done on those facts. And then the facts were thrown away, and only the arithmetic kept. Event sourcing does it the other way round. Keep the facts. Do the arithmetic when someone asks. Every benefit, and every cost, in this video comes from that one sentence.

## 7. Three Moves

In practice, it is three moves. One. Make each change a fact, with a name, in the past tense. Not: add sixty points. But: sixty points were awarded to this customer, on the first of March, for this order. An instruction can be refused. A fact cannot, because it already happened. Two. Add it to the end of a log, and never touch it again. The log has no update, and no delete. The past does not change, so the record of it must not change either. Three, the one that feels strange at first. The current balance is not stored anywhere. When someone asks, start at zero, go through the customer's events in order, and add each one. Ask again, and it is worked out again. That sounds wasteful, and sometimes it is. But first, let's hear what it buys.

## 8. Who Does What

Let's name the pieces. There are four. First, the event. It is just a fact, with no logic in it. There are three kinds: points awarded, points redeemed, and points expired. Each carries everything needed to understand it, including the order number and the date. Second, the event store, which is the log. You can add to it, and read it, but never change it. Third, the class that turns events into a balance. It has no stored balance at all. Every number it gives is worked out on the spot. Fourth, a snapshot store. It is a cache, and never the truth. We will come back to it, because it is where this pattern gets dangerous. Checkout, which calls all this, cannot tell which design is behind it. This is a choice about storage, not about the calling code.

## 9. The Fold — and Why It Is 140

Here is how the balance is worked out, in words. Start a running total at zero. For each of the customer's events, add its effect on the balance. Return the total. That loop is the balance. There is no other balance. Now print each step, not just the answer. First of March: earned sixty points. Balance, sixty. Third of March: spent twenty-five. Balance, thirty-five. Eighth of March: earned a hundred and twenty. Balance, a hundred and fifty-five. Fourteenth of March: fifteen points expired. Balance, a hundred and forty. A support agent can read that down the phone. It even explains the expiry, which is the question support dreads most. Nobody wrote that explanation. It is the sum, showing its working.

## 10. The Query Nobody Wrote in Advance

Third demo: the same bug, with a log behind it. The buggy release recorded two award events instead of one. And two events never look like one. Three weeks later, someone writes a brand new question. For this customer, find any order that earned points more than once. The answer: order nine thousand and one, awarded twice. That question was invented after the fact. And it could be answered, because the data was already in the log. Nobody predicted it. Nobody built a table for it. Then the repair. Count each order's award only once, and the balance is fifty-five, not a hundred. And here is the key point. No event was edited, or deleted, or added. The log is exactly the same as before. The log was never wrong. The shop really did award those points twice. What was wrong was how the log was read. So the fix lives in the reading code, and history stays history.

## 11. The Bill — Reading Gets Expensive

That is what you gain. Now the bill, and it is large. Four events is nothing. Five thousand is not. Working out one balance from the start reads all five thousand events. Every time anyone asks. The fix is a snapshot. Save the balance as it stood at event five thousand. The next read starts there, and reads one new event instead of five thousand. Same answer, far less work. But notice what a snapshot is. It is a stored balance. The very thing this pattern set out to stop keeping, brought back for speed. So in this project, each snapshot records which event it was taken at. And which version of the code calculated it. That second part matters more than it seems.

## 12. The Bill — A Snapshot Can Be Quietly Wrong

Here is how a snapshot goes wrong, silently. Suppose a snapshot is taken while the double-counting bug is still in the reading code. It records ninety points. Then the fix lands. Adding up the log correctly now gives forty-five. The log is right. The adding up is right. And the snapshot is wrong, forever, and nothing tells you. No error, no warning, no failed test. A wrong balance is just a number, and numbers do not look wrong. The cure is blunt, and correct. Throw every snapshot away, and add the log up again. You can only do that because the log kept everything. So here is the rule. The log is the truth. A snapshot is a cache you may always delete. The moment anyone treats a snapshot as the record, you are back where you started.

## 13. The Bill — Erasure, and Old Events

Two more costs, the kind you meet years later. The first is erasure. A customer has a legal right to be forgotten. And the log has no delete. The obvious idea is: just remove their events. That destroys their history forever, which the system was built to prevent. And an old snapshot still holds their balance, so their data is still there. The real answers are harder. Encrypt personal details inside each event, and destroy the key when asked. Or keep the event, but blank out who it was. Either way, it must be designed in before the first event is ever written. The second cost is versioning. The order number field was only added in twenty twenty-three. Older events do not have it, and never will. So the duplicate search finds zero duplicates in an old stream, even when two identical awards are clearly there. And it reports that calmly. Every reader you ever write carries that gap forever.

## 14. Event Sourcing Is Not CQRS

One more thing, because two patterns are often confused. C Q R S means reads and writes come from different models. This project has a small class that does exactly that, with no event log at all. Writes update a row, and reads come from a second model, shaped for the screen. That is C Q R S, without event sourcing. And the main class here does the opposite. It stores events, and answers reads by adding up those same events. One model. That is event sourcing, without C Q R S. So here are two sentences worth remembering. C Q R S changes where reads come from. Event sourcing changes what writes store. They often appear together. But you can have either one without the other.

## 15. When to Reach for It

So, when should you use this? Ask one question. Will anyone ever need to know how this number got to be what it is? A shopping basket, a settings page, a stock level? No. Nobody will audit those. Keep the number. For those, this pattern is a large bill for nothing. Money, loyalty points, orders, or anything an auditor might ask about? Yes. There, the history is not overhead. The history is the product. This pattern is often used where it should not be. That is why so much of this video is about its costs.

## 16. Thanks for Watching

That's the Event Sourcing pattern. If you remember one sentence, make it this one. Store what happened, not the total, and work the total out when asked, but remember that snapshots, erasure, and old events all have a price. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Fix the double-award bug a different way. Instead of changing how the log is read, add a new event that takes the extra points back. Then ask: which repair would you rather explain to an auditor? If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
