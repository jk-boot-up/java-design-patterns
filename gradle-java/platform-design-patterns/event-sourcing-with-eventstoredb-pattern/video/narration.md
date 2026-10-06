# Event Sourcing with EventStoreDB Pattern — Video Narration Script

## 1. Event Sourcing with EventStoreDB

Hello, and welcome. This video explains the Event Sourcing pattern in Java, using a real database built for events. It was called EventStoreDB, and has recently been renamed KurrentDB. This video is presented by Jayasekhar Konduru. First, a simple definition. Event sourcing means you never overwrite what you know. You write down each thing that happened, in order, and never change it. When you need the current state, you add the list up. Think of a bank statement: a list of payments, with the total worked out from them. In our online store, the loyalty scheme keeps every award, every spend, and every expiry. And it adds them up to get the balance. By the end, you will hear two checkouts spend the same points at the same moment. A real database refuse the second one. A retry the database recognises. A screen that catches up by reading the history. And what deleting a customer really removes.

## 2. The Scenario

Here is the scenario. The shop gives one loyalty point for every pound spent. Customers can spend points on later orders. And unused points expire. No balance is stored anywhere. Every award, spend, and expiry is written down. And the balance is added up from them whenever someone asks. The plain Java version kept those events in a simple list, inside one program, with one writer. Here, the events live in a real database. And two places can write to it at once: the website, and the phone app. That is where the trouble starts.

## 3. KurrentDB's Words

This database brings a few words with it. First, the name. It was called EventStoreDB for many years. Its makers renamed it KurrentDB. Same database, new name. Think of a paper ledger with numbered lines, one ledger per customer. You may only write on the next empty line. And you never rub anything out. One ledger, one list of events for one customer, is called a stream. Each line has a number, starting at zero, called its revision. Writing on the next line is called an append. There is no way to change a line. The only other thing you can do is throw the whole ledger away.

## 4. A Real Log, Read Back

First demo: a real log, read back. The demo starts KurrentDB in a container, a small sealed box it switches on and off by itself. It appends four things that happened to one customer in March. KurrentDB numbers them, revision zero to three. Then a second connection reads the stream from the start, and adds it up. Sixty points earned: balance sixty. Twenty-five spent: balance thirty-five. A hundred and twenty earned: balance a hundred and fifty-five. Fifteen expired: balance a hundred and forty. Nothing stores a hundred and forty. It was added up just now, from four events. And the Java library has no way to change an event.

## 5. Two Checkouts, No Check

Second demo: two checkouts at once, with no check. A customer has a hundred and forty points. They pay for two orders at the same moment: one on the website, one in the phone app. Paying with points has two steps. First, look: read the stream, and add it up. Then decide: if there are enough points, append a spend. Both checkouts look, and both see a hundred and forty points, at revision three. Both decide a hundred is less than a hundred and forty. Both append a spend of a hundred points, with no check. Both appends are accepted. The balance is now minus sixty. The customer spent two hundred points, but only had a hundred and forty.

## 6. The Expected Revision

Third demo: the same race, with a check. Another customer, with a hundred and forty points. This time, each checkout adds one condition to its append. Only write this if the stream is still at the revision I looked at. That is called the expected revision. Both look, and see revision three. Both append, expecting revision three. One append is accepted, at revision four. The other is refused. The database says: you expected revision three, but the stream is now at four. The refused checkout looks again. It sees forty points. A hundred is more than forty, so it tells the customer no. The balance is forty. Nothing was locked. The database just compared one number.

## 7. One Number Decides

Here is the whole setup, in words. Two checkouts, one stream, one database. Each checkout reads the stream, adds it up, and remembers the revision it saw. Then it appends, and passes that revision along. The database compares it with the stream's real last revision. If they match, the event is written, and the stream moves on by one. If they do not, someone else wrote in between, and the append is refused. The rule to remember: whoever writes first moves the number. Everyone who looked before that has to look again.

## 8. One Argument

The difference between those two races is one setting. The first append says: any. Write this, whatever state the stream is in. The second says: only if the stream is still at revision three. And here is the part to remember. In the Java library, any is the default. An append that says nothing about revisions is always accepted. The check is real, but it is off, until you turn it on.

## 9. A Retry It Recognises

Fourth demo: a retry. The shop awards a customer forty-five points for an order. The reply gets lost on the network. So the shop does not know if the award was written, and sends it again. Every event carries a random label chosen by the writer, called the event I D. Sent again with a new event I D, the award is simply written twice. Two awards for one order, and a balance of ninety. That is the double-award bug, happening for real. For another customer, the retry reuses the same event I D, and the same expected revision. The database gives the same answer as the first time, and writes nothing. One award, and a balance of forty-five. The retry is recognised, not refused. So the shop never has to guess.

## 10. A Screen That Catches Up

Fifth demo: a screen that catches up. The support team has a screen showing every customer's balance. It starts last, after everything so far. And it asks the database for every loyalty stream, from the very first event. That is called a catch-up subscription. The database sends the eighteen events already stored. Then it says: you have caught up. The screen shows every customer's balance, including the minus sixty and the ninety. Then a new order awards the first customer twenty points. Nobody tells the screen. Moments later, it shows a hundred and sixty. A copy built like this is called a projection, or a read model. Starting late lost nothing.

## 11. The Bill: Deleting A Stream

Sixth demo: the bill. A customer asks to be forgotten. So the shop deletes that customer's stream. Reading the stream now gives: stream not found. But KurrentDB also keeps one log of everything, every stream together, in the order written. Reading that whole log still finds two of the deleted customer's events. They stay on disk until a later clean-up, called a scavenge. The support screen still shows that customer's ninety points. The delete reached the stream, not the copies built from it. And when a later order reuses the same stream name, it starts at revision two, not zero. The numbering carries on from where the deleted events stopped.

## 12. What Else It Costs

So what else does this cost? Deleting a stream hides it. It does not erase it. Real erasure needs the clean-up to run. And every copy built from the stream must be told to forget too. The revision check is off by default. So every piece of code that writes must remember to turn it on. This demo ran the database with security switched off. No network encryption, and no passwords. A real production server must never run like that. And it is one more database to run, back up, and watch.

## 13. What The Simulation Left Out

So what did the plain Java version get right? The whole idea. Events are only ever added. The balance is added up, never stored. A hundred and forty points, from the same four events. All of that holds here. What it left out was everything that needs two programs. Its list had one writer, so two checkouts could never race. It had no lost replies, no screen starting late, and its delete really removed things. And the headline. Two checkouts spending the same points at once. With no check, both are accepted, and the balance goes to minus sixty. With the expected revision, the second one is refused.

## 14. The Verdict

So, here is the verdict. Give each thing that must stay consistent its own stream. Here, one customer's points. Look, decide, and then append with the revision you looked at. If the append is refused, do not just send it again. Look again, and decide again, because the answer may now be no. And choose each event's I D once, when you first decide. Reuse it on every retry. So a lost reply can never become a second award.

## 15. What Is Real, And When Not

A quick, honest note about this demo. The database is KurrentDB, version twenty-six point one point two, the newest release. It runs in a container that the demo starts and stops by itself. You just need Docker switched on first. The two checkouts are two real connections, really racing. And the support screen is a real subscription. So, when is this too much? If only one program ever writes, and nobody will ever ask how a number got there, a row holding the number is simpler. And much cheaper to run.

## 16. Thanks for Watching

That's Event Sourcing, with EventStoreDB, now called KurrentDB. If you remember one sentence, make it this one. Append with the revision you looked at, because without it, the database accepts whatever arrives. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Give the first race the expected revision. Guess which result will change, and then run it. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
