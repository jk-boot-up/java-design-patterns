# Message Filter Pattern — Video Narration Script

## 1. Message Filter

Hello, and welcome. This video explains the Message Filter pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A message filter sits between a channel of messages and one receiver. It checks each message against a rule, and passes on only the ones that match. The sender and the receiver never know it is there. Think of the spam filter on your email. The world sends you everything. The filter decides what reaches your inbox. And a good one keeps the rest in a spam folder, just in case. In this video, the domain is an online shop. Every order is published on an orders channel. A gift-wrap service and a loyalty service each care about only some of them. By the end, you will hear what happens when everyone gets everything. How filters fix it. How to chain them. And where dropped messages go.

## 2. The Scenario

Here is the scenario. Every order the shop takes is published on one orders channel. The gift-wrap service only cares about gift orders. The loyalty service only cares about registered customers who spend over fifty pounds. But the channel gives every service every order.

## 3. Act One — Everything to everyone

First demo: every service is handed every order. Ten orders are published. The gift-wrap service receives all ten. It opens each one, and checks: is this a gift? Two are: orders two and four. Eight deliveries it had to open, and ignore. And every other service repeats its own checks.

## 4. Act Two — A filter

Second demo: a message filter, in front of the gift-wrap service. The filter has one rule: gift orders only. The gift-wrap service now receives exactly two orders. The filter dropped the other eight. Checkout still sends every order. It does not know the filter exists.

## 5. Act Three — Chained filters

Third demo: filters can be chained. The loyalty service wants registered customers only. And only orders over fifty pounds. Two filters, one after the other. The first drops three guest orders. The second drops four small orders. The loyalty service receives orders one, four, and six.

## 6. Act Four — A changed rule

Fourth demo: the rule changes, and nothing else does. The bonus threshold rises to sixty pounds. Only the filter's rule changes. The loyalty service now receives orders one and four. Checkout and the loyalty service were not changed.

## 7. Act Five — The bill

Fifth demo: the bill. A dropped message is gone. Fifteen messages were dropped by the filters in this demo. None was kept anywhere. If a rule is wrong, real orders vanish, with no error. So count the drops, or send them somewhere to be checked, like a spam folder.

## 8. The Pattern

Let's name the pattern. Between the channel and a receiver, put a filter with one rule. If a message matches, pass it on. If not, drop it, and count it. Filters can be chained, to combine rules. And the sender and receiver stay exactly as they were.

## 9. Who Does What

Here is who does what. The channel delivers every order to every subscriber. A message filter is itself a subscriber. It holds a rule, the next step to pass matches to, and a count of what it dropped. The gift-wrap and loyalty services are the receivers. And an order event is the message.

## 10. Where You Have Seen It

You have probably met this pattern already. Apache Camel and Spring Integration both have a filter step. Cloud messaging services let each subscription have a filter. Kafka Streams has one too. And every email rule, and every spam filter, is a message filter.

## 11. When To Use It

So, when should you use it? When receivers on a shared channel want only some of the messages. Keep each rule small, and chain them. And always count, or keep, what you drop. When many receivers want very different subsets, a content-based router may be clearer.

## 12. Thanks for Watching

That's the Message Filter pattern. If you remember one sentence, make it this one. Let a filter decide what reaches each receiver, and never lose track of what it drops. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Send dropped messages to a discard channel, and print them. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
