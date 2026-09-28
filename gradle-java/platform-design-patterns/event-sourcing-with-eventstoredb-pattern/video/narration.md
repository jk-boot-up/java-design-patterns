# Event Sourcing with EventStoreDB Pattern — Video Narration Script

## 1. Event Sourcing with EventStoreDB

Hello, and welcome. This video explains the Event Sourcing pattern in Java, using a real database built for events. It was called EventStoreDB, and its makers have recently renamed it KurrentDB. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. Event sourcing means you never overwrite what you know. You write down each thing that happened, in order, and you never change it. When you need the current state, you add the list up. Now the same thing in our online store. The shop runs a loyalty scheme. Instead of keeping one number for a customer's points, it keeps every award, every spend and every expiry, and works out the balance by adding them up. By the end you will have seen two checkouts spend the same points at the same moment, a real database refuse the second one, a retry the database recognises, a screen that catches up by reading the history, and what deleting a customer really removes.

## 2. The Scenario

Here is the scenario. The shop gives one loyalty point for every pound spent. Customers can spend points on later orders, and points that are not used expire. No balance is stored anywhere. Every award, every spend and every expiry is written down, and the balance is added up from them whenever somebody asks. The hand-built twin of this project kept those events in a plain list, inside one program, with one writer. Here the events live in a real database, and two places can write to it at once: the shop's website, and its phone app. That is where the trouble starts.

## 3. KurrentDB's Words

This database brings a few words with it, and each one is simple. First, the name. It was called EventStoreDB for many years. Its makers renamed the company Kurrent, and the database KurrentDB. It is the same database, and the Java library has a new name to match. Think of a paper ledger with numbered lines, one ledger per customer. You may only write on the next empty line, and you never rub anything out. One ledger, one list of events for one customer, is what KurrentDB calls a stream. Here the stream is named loyalty, dash, C 4 4 1 7. Each line in the ledger has a number, starting at zero, and KurrentDB calls that number the revision. Writing on the next line is called an append. There is no way to change a line. The only other thing you can do is throw the whole ledger away.

## 4. A Real Log, Read Back

First, a real log. The demo starts KurrentDB in a container, a small sealed box it switches on and off itself. It appends the four things that happened to customer C 4 4 1 7 in March, and KurrentDB numbers them revision zero to three. Then a second connection, as a different program would, reads the stream from the start and adds it up. Sixty points earned, balance sixty. Twenty-five spent, balance thirty-five. A hundred and twenty earned, balance a hundred and fifty-five. Fifteen expired, balance a hundred and forty. Nothing stores a hundred and forty. It was added up just now, from four events. And the Java library has no call that changes one event.

## 5. Two Checkouts, No Check

Second, the failure. Customer C 5 1 2 0 has a hundred and forty points, and is paying for two orders at the same moment: one on the website, one in the phone app. Paying with points is two steps. First look: read the stream and add it up. Then decide: if there are enough points, append a spend. Both checkouts look, and both see a hundred and forty points, at revision three. Both decide that a hundred is not more than a hundred and forty. Both append a spend of a hundred points, with no check. Both appends are accepted, at revisions four and five. The balance is now minus sixty. The customer spent two hundred points they only had a hundred and forty of, and the database was never asked to mind.

## 6. The Expected Revision

Third, the pattern's answer. The same race, for customer C 5 1 2 1, with a hundred and forty points. This time each checkout adds one sentence to its append: only write this if the stream is still at the revision I looked at. KurrentDB calls that the expected revision. Both look, and see revision three. Both append, expecting revision three. One append is accepted, at revision four. The other is refused. The refusal is called Wrong Expected Version, and it says: expected revision three, but the stream is at revision four. The refused checkout looks again, and sees forty points. A hundred is more than forty, so it tells the customer no. The balance is forty. Nothing was locked. The database compared one number.

## 7. One Number Decides

Here is the whole arrangement, in words. Two checkouts, one stream, one database. Each checkout reads the stream, adds it up, and remembers the revision of the last event it saw. Then it appends, and hands that revision back. The database checks it against the stream's real last revision. If they match, the event is written, and the stream moves on by one. If they do not match, somebody else wrote in between, and the append is refused. The rule to remember is this: whoever writes first moves the number, and everyone who looked before that has to look again.

## 8. One Argument

The difference between those two races is one argument. The first append says any: write this, whatever state the stream is in. The second says: only if the stream is still at revision three. And here is the part to remember. In the Java library, any is the default. An append that says nothing about revisions is accepted whatever happened since you looked. The check is there, it is real, and it is off until you turn it on.

## 9. A Retry It Recognises

Fourth, a retry. The shop awards customer C 5 1 2 2 forty-five points for an order. The reply gets lost on the network, so the shop does not know whether the award was written, and it sends it again. Every event carries a random label chosen by the writer, which KurrentDB calls the event id. Sent again with a new event id, the award is simply written twice. Two awards for one order, and a balance of ninety. That is the double-award bug from the hand-built twin, happening for real. For customer C 5 1 2 3, the retry reuses the same event id and the same expected revision. The database answers revision zero again, the same answer as the first time, and writes nothing. One award, a balance of forty-five. The retry is recognised, not refused, so the shop never has to guess.

## 10. A Screen That Catches Up

Fifth, a second copy that keeps itself up to date. The support team has a screen showing every customer's balance. It starts last, after everything so far, and asks the database for every loyalty stream, from the very first event. KurrentDB calls that a catch-up subscription. The database sends the eighteen events already stored, then says: you have caught up. The screen shows a hundred and forty for C 4 4 1 7, minus sixty for C 5 1 2 0, forty for C 5 1 2 1, and ninety for C 5 1 2 2. Then a new order awards C 4 4 1 7 twenty points. Nobody tells the screen. Moments later it shows a hundred and sixty. A copy built like this is called a projection, or a read model. Starting late lost nothing.

## 11. The Bill: Deleting A Stream

Sixth, the bill. Customer C 5 1 2 2 asks to be forgotten, and the shop deletes that customer's stream. Reading the stream now gives: stream not found. But KurrentDB also keeps one log of everything, every stream at once, in the order it was written. Reading that whole log still finds two events belonging to the deleted stream. They stay on the disk until a later clean-up, which KurrentDB calls a scavenge. The support screen still shows ninety points for that customer. The delete reached the stream, not the copies built from it. And when a later order writes to the same stream name, it is accepted at revision two, not zero. The numbering carries on from where the deleted events stopped.

## 12. What Else It Costs

So what else does this cost? Deleting a stream hides it; it does not erase it. Real erasure needs the clean-up to run, and every copy built from the stream, like the support screen, has to be told to forget as well. The revision check is off by default, so every piece of code that writes has to remember to turn it on. This demo ran the database with its security switched off. No encryption on the network, which the database calls T L S, and no passwords. That kept it to one container on one machine. A production server must never run like that. And it is one more database to run, back up and watch.

## 13. What The Simulation Left Out

So what did the hand-built twin get right? The whole idea. Events are only ever added. The balance is added up, never stored. A hundred and forty points, from the same four events. All of that holds on KurrentDB. What it left out was everything that needs two programs. Its list lived inside one program, with one writer, so two checkouts could never race. It had no lost replies to retry, no screen starting late, and its delete really removed things. And the headline: two checkouts spending the same points, at the same moment. With no check, both are accepted, and the balance goes to minus sixty. With the expected revision, the second one is refused.

## 14. The Verdict

The verdict. Give each thing that must stay consistent its own stream: here, one customer's points. Look, decide, and then append with the revision you looked at. When the append is refused, do not simply send it again. Look again, and decide again, because the answer may now be no. And choose each event's id once, when you first decide, and reuse it on every retry, so a lost reply can never become a second award.

## 15. What Is Real, And When Not

What in this project is real? KurrentDB version twenty-six point one point two, the newest release, in a container the demo starts and stops itself. The Java client is the KurrentDB client, version one point two point one, and the container is run by a library called Testcontainers. The two checkouts are two real connections, racing, and the support screen is a real subscription. And when is this too much? If only one program ever writes, and nobody will ever ask how a number got to be what it is, a row holding the number is simpler, and far cheaper to run.

## 16. Thanks for Watching

That's Event Sourcing with EventStoreDB, now called KurrentDB. If you take one sentence away, take this one: append with the revision you looked at, because without it, the database will accept whatever arrives. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, give the first race the expected revision, guess which line of the output changes, and then run it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
