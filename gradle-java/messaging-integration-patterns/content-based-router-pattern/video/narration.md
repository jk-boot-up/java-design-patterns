# Content-Based Router Pattern — Video Narration Script

## 1. Content-Based Router

Hello, and welcome. This video explains the Content-Based Router pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A content-based router looks inside each message. Then it sends the message to a different channel, depending on what it contains. So senders and receivers never need to know about each other. Think of a post office sorting room. A clerk reads each address, and drops the letter into the right bag. In our online store, orders of different kinds arrive together. And each kind needs to go somewhere different. In this video, every order lands on one channel, and the warehouse must sort them. Then a router sends each one to its own channel. We will hear why the order of rules matters, what happens to a message nothing matches, and then the cost.

## 2. The Scenario

Here is the scenario. Orders arrive together in the online store. Physical goods, gift cards, subscriptions, and some very expensive orders. Physical goods must go to the warehouse. Gift cards must go to digital delivery. And very expensive orders must go to fraud review. So here is the question. Who decides where each one goes?

## 3. One Channel For Everything

First, the naive way: one channel for everything. All six orders arrive on the warehouse's channel. Two of them are gift cards, which the warehouse cannot pack. And one is neither kind. So the warehouse needs an if statement for each kind of order. And every new kind means changing the warehouse.

## 4. The Pattern

Now, the pattern. A router reads each message. Rules say: if it looks like this, send it to that channel. The first rule that matches wins. And the senders and receivers know nothing about the rules.

## 5. A Router Looks Inside

Second demo: a router that looks inside. Order one is physical, so it goes to the warehouse. Order two is a gift card, so it goes to digital delivery. Order three is physical, but worth twelve hundred pounds, so it goes to fraud review. And the subscription, which no rule covers, goes to manual review. Every order ends up in exactly one place.

## 6. The First Rule That Matches Wins

Third demo: the first rule that matches wins. Take a gift card worth fifteen hundred pounds. With the high value rule checked first, it goes to fraud review. With the high value rule checked last, it goes to digital delivery instead. The order of the rules is part of the design. And nothing warns you when that order changes.

## 7. Nothing Matches

Fourth demo: when nothing matches. A subscription order arrives, and no rule covers it. With a fallback channel, it goes to manual review. With no fallback, it goes nowhere. It is dropped, and counted as dropped. A router with no fallback silently loses anything it does not recognise.

## 8. A New Route, And Nobody Else Changes

Fifth demo: a new route, and nobody else changes. One rule is added. Three rules become four. Now a European subscription goes to a tax check. The senders and the receivers were not touched at all. And a physical European order still goes to the warehouse, because an earlier rule matches it first.

## 9. The Bill

Finally, the cost. The sender starts calling physical orders, goods, instead of physical. The router's rule is looking for the word physical. So it misses them, and they all fall through to manual review. The router reads the content, so it depends on the content's exact format. Routing on a label in the message's envelope avoids that. But then the sender must fill that label in. And every route is one more rule to test.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a method that takes a message, and returns a channel or queue name. Look for Apache Camel's choice and when, or Spring Integration's router. Look for RabbitMQ topic exchanges, with routing keys. And a chain of if statements in the sender, choosing a queue.

## 11. The Verdict

So, here is the verdict. Use a content-based router when one stream carries messages that need different handling. And the difference is in the content. Order the rules on purpose. Always have a fallback, which keeps and reports what it cannot route. Prefer routing on a label the sender sets deliberately, over reaching into the body. And test every rule, and the order between them.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every result you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? If there is only one destination, or the sender already knows where each message goes, a router is an extra step for nothing.

## 14. Thanks for Watching

That's the Content-Based Router. If you remember one sentence, make it this one. A content-based router puts all the sorting in one place, and its price is depending on the content, and rules whose order matters. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a rule sending orders over one thousand pounds to a manual approval channel. And decide where it belongs in the order of rules. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
