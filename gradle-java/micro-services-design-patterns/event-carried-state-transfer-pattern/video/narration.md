# Event-Carried State Transfer Pattern — Video Narration Script

## 1. Event-Carried State Transfer

Hello, and welcome. This video explains the Event-Carried State Transfer pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When data changes, put the new data in the event itself. Then each service that cares keeps its own copy. And never has to call the owner back. Think of moving house. You could send friends a card saying, I have moved, ring me for the address. Or you send a card with the new address on it. Each friend writes it in their own address book, and can post you a letter even when you are not answering the phone. In this video, the domain is an online shop. A customer service owns the addresses, and a shipping service prints delivery labels. By the end, you will hear why thin events tie services together. How carrying the address sets shipping free. Why the copy is briefly out of date. And how version numbers handle events arriving out of order.

## 2. The Scenario

Here is the scenario. The shipping service prints delivery labels. The customer service owns the customers' addresses. Its event only said, a customer changed. So shipping had to ask for the address, every time.

## 3. Act One — A thin event, and a call back

First demo: a thin event, and a call back. The customer service's event only says, a customer changed. So the shipping service asks for the address, every time it prints a label. A hundred labels mean a hundred calls. Now the customer service goes down. Not a single label can be printed.

## 4. Act Two — The event carries the address

Second demo: the event carries the address. Now the event says, customer one's address is now this. The shipping service writes it into its own copy. It keeps ten addresses. A hundred labels need no calls at all. And with the customer service down, all hundred labels are still printed.

## 5. Act Three — The copy lags behind

Third demo: the copy lags behind. A customer moves, from Leeds to York. The event is still on its way. A label printed now, still goes to Leeds. Once the event arrives, labels go to York. The copy is always a little behind the owner. This is called eventual consistency.

## 6. Act Four — Events out of order

Fourth demo: events can arrive in the wrong order. A customer moves to Hull, then to Bristol. But the Bristol event arrives first. A copy that just takes the last event it received, ends up with Hull. The older address. So each event carries a version number. The copy ignores anything older than what it has. And it keeps Bristol.

## 7. Act Five — The bill

Fifth demo: the bill. Every service that cares keeps its own copy. Shipping, invoicing and marketing, each hold every customer's address. The events are bigger. The copies are briefly out of date. And personal data now lives in many places. Each must protect it, and delete it when asked.

## 8. The Pattern

Let's name the pattern. The event carries the new data, not just the news that something changed. Each listening service keeps its own copy, of just the data it needs. And it never calls the owner back.

## 9. Who Does What

Here is who does what. The customer service owns the addresses, and publishes each change. The address changed event carries the customer, the new address, and a version number. The shipping service keeps its own copy, and prints labels from it. The call-back version of shipping is the old way.

## 10. Where You Have Seen It

You have probably met this pattern already. Kafka topics that carry whole records, not just identifiers. Change data capture tools, which publish every changed database row. And the read side of CQRS, built from events.

## 11. When To Use It

So, when should you use it? When many services read the same data often. And must keep working when its owner is down. Include a version in every event. Accept that copies are briefly out of date. And copy only the fields each service needs.

## 12. Thanks for Watching

That's the Event-Carried State Transfer pattern. If you remember one sentence, make it this one. Send the new data, not just the news. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a customer deleted event, and remove the copy when it arrives. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
