# Content-Based Router Pattern — Video Narration Script

## 1. Content-Based Router

Hello, and welcome. This video explains the Content-Based Router pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a content based router looks inside each message, and sends it to a different channel depending on what it contains, so senders and receivers never have to know about each other. This is the second project in the messaging and integration category, whose subject is how separate systems exchange messages safely. In our online store, orders of different kinds arrive together, and each kind needs a different place to go. By the end you will see every order arrive on one channel and the warehouse forced to sort them, see a router send each to its own channel, see that the order of the rules decides, see what happens to a message nothing matches, add a route without touching anyone else, and see the bill.

## 2. The Scenario

Here is the scenario. Orders arrive together in the online store: physical goods, gift cards, subscriptions, and some of very high value. Physical goods go to the warehouse. Gift cards go to digital delivery. Very high value orders go to fraud review. The question: who decides where each one goes?

## 3. One Channel For Everything

First, one channel for everything. All six orders arrive on the warehouse's channel. Two are gift cards, which nothing physical can be done for, and one is neither. The warehouse now has an if for each kind, and every new kind means changing the warehouse.

## 4. The Pattern

The pattern. A router reads each message. Rules say: if it looks like this, send it to that channel. The first rule that matches wins. And senders and receivers do not know about the rules.

## 5. A Router Looks Inside

Second, a router looks inside. Order one, physical, goes to the warehouse. Order two, a gift card, goes to digital delivery. Order three, physical but worth twelve hundred pounds, goes to fraud review. The subscription, which no rule covers, goes to manual review. Every order is in exactly one place.

## 6. The First Rule That Matches Wins

Third, the first rule that matches wins. A gift card worth fifteen hundred pounds. With the high value rule first, it goes to fraud review. With the high value rule last, it goes to digital delivery. The order of the rules is part of the design, and nothing warns you when it changes.

## 7. Nothing Matches

Fourth, nothing matches. A subscription order that no rule covers. With a fallback channel, it goes to manual review. With no fallback, it goes nowhere, and is dropped, and counted. A router with no fallback loses what it does not recognise, and says nothing.

## 8. A New Route, And Nobody Else Changes

Fifth, a new route, and nobody else changes. One rule is added: three rules become four. An EU subscription now goes to a VAT check. The senders and the receivers were not touched. A physical EU order still goes to the warehouse, because an earlier rule matched first.

## 9. The Bill

Last, the bill. The sender starts calling physical orders goods. The router's rule looks for physical, misses them, and they fall to manual review. The router reads the content, so it is coupled to the content's format. Routing on a header keeps that in the envelope, at the cost of the sender filling it in. And every route is one more rule to test.

## 10. How To Recognise It

How do you recognise this in code you did not write? A method that returns a channel or queue name from a message. Apache Camel's choice().when(...), Spring Integration's router. RabbitMQ topic exchanges and routing keys. An if chain that chooses a queue, in the sender.

## 11. The Verdict

Here is my verdict, plainly. Use a content-based router when one stream carries messages that need different handling, and the difference is in the content. Order the rules on purpose, always have a fallback that keeps and reports what it cannot route, and prefer routing on a header that the sender sets deliberately over reaching into the body. Test every rule and the order between them.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? If there is only one destination, or the sender already knows where each message goes, a router is a step for nothing.

## 14. Thanks for Watching

That's Content-Based Router. If you take one sentence away, take this one: a content-based router puts the sorting in one place, and its price is coupling to the content and rules whose order matters. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a rule for orders over a thousand pounds to a manual approval channel, and decide where it goes in the order. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
