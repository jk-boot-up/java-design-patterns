# Message Filter with Apache Camel Pattern — Video Narration Script

## 1. Message Filter with Apache Camel

Hello, and welcome. This video explains the Message Filter pattern, built with Apache Camel, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A message filter sits in front of a receiver. It lets through only the messages that receiver wants, and drops the rest. Apache Camel is an open-source library for moving messages, and it has a filter step built in. Think of a company post room. Each department gives it a rule, such as, only letters marked gift wrap. The post room applies the rules. And a good one keeps a tray of letters nobody wanted. In this video, the domain is an online shop, whose checkout announces every order to its services. By the end, you will hear how a filter step works in Camel. How to change a rule while everything runs. And why a discard channel matters.

## 2. The Scenario

Here is the scenario. Checkout announces ten orders. The gift-wrap service only wants gift orders. The loyalty service only wants registered customers, spending over fifty pounds. Without filters, each service was handed all ten.

## 3. Act One — Every service gets every order

First demo: every service is handed every order. Checkout sends each order to one place. Camel copies it to every service. The gift-wrap service is handed all ten orders. It must open each one, to see if it is a gift.

## 4. Act Two — A filter in front

Second demo: a filter in front of the gift-wrap service. The rule is one short expression. Is this order a gift? Only two orders get through. O R D two, and O R D four. Eight are dropped. Checkout was not changed. It does not know the filter exists.

## 5. Act Three — Two conditions

Third demo: a rule with two conditions. The customer must be registered. And the order must be over fifty pounds. The loyalty service receives three orders. O R D one, four, and six.

## 6. Act Four — Change the rule while running

Fourth demo: change the rule while everything keeps running. The threshold is read from the settings, as each order passes. It is raised to sixty pounds. Now only O R D one and four get through. No route was changed. Nothing was restarted.

## 7. Act Five — The bill, and a discard channel

Fifth demo: the bill. A filter drops messages. And a wrong rule drops them silently. So rejected orders are sent to a discard channel instead. Eight orders are kept there, and can be counted. The costs. Rules written in text, only checked when they run. And more than ten library files, instead of none.

## 8. The Pattern, in Camel

Let's name the pattern, in Camel's words. A filter step, with a rule, in front of each receiver. The rule is written in Camel's Simple language. And rejected messages go to a discard channel, where they can be counted.

## 9. Who Does What

Here is who does what. Shop routes holds every route, and every rule. Rules holds the threshold, which can change while the routes run. Order event is the message. And received records what each service was given.

## 10. Where You Have Seen It

You have probably met this already. Camel's filter step, and Spring Integration's filter. Message selectors in Java messaging. And the rules in your email, that sort or discard incoming mail.

## 11. When To Use It

So, when should you use Camel for this? When many services subscribe to the same messages, and the rules change. Keep each rule short. And add a discard channel, so nothing is lost without a trace.

## 12. Thanks for Watching

That's the Message Filter, with Apache Camel. If you remember one sentence, make it this one. Put a rule in front of each receiver, and keep what it rejects. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a discard channel to the gift-wrap filter too. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
