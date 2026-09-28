# Chain of Responsibility with Spring Pattern — Video Narration Script

## 1. Chain of Responsibility with Spring

Hello, and welcome. This video explains the Chain of Responsibility pattern, in Java, using Spring Boot. This video is presented by Jayasekhar Konduru. First, a simple definition. A chain passes a request along a line of objects, until one of them is willing to answer. In Spring, each link in the chain is a bean of one shared interface. And Spring hands you the whole list of links, already sorted. Think of airport security. Your bag goes through one check after another: passport, scanner, and a hand search. Any one of them can stop you. This is the framework version of the Chain of Responsibility video, with the same online checkout. We will build the same order checks from Spring beans. Then we will see what changes. The order of the checks becomes a cost, a failing check needs a policy, and a setting can remove a check.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Chain of Responsibility video. That one passes a checkout request along four checks: address, stock, fraud, and payment. It stops at the first check that answers, and reports which checks never ran. If you are new to the pattern, watch that one first. Here, we keep the same example, and ask what Spring Boot does with it.

## 3. Before The First Line

One thing is new in this project: Spring Boot. At its heart, Spring is a container that creates your objects for you. It can collect every bean of one interface into a list. And it sorts that list using an order number written on each class. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. Spring Builds The Chain

First demo: Spring builds the chain. Spring hands us the four checks, in this order. Address, stock, fraud, and payment limit. Where does that order come from? From order numbers, written on four different classes. So no single file shows you the whole chain.

## 5. Five Requests

Second demo: five customers place orders. Asha passes every check, so nobody objects, and the fallback approves her order. Erin is rejected by the address check. The other three checks never ran. Ben is stopped by the stock check. Carol is stopped by the fraud check. And Dev is referred to a person, by the payment limit check.

## 6. The Order Is The Cost

Third demo: the order of the checks is a cost. The fraud service is paid for, per call. With the cheap checks first, only three of the five orders reach the paid fraud service. Put the paid check first, and all five orders reach it. The same checks, and the same answers. But a bigger bill. And in Spring, a single order number decides it.

## 7. A Link That Throws

Fourth demo: a check that crashes. The fraud service is down, and its check throws an error. The chain catches the error, and refers Asha's order to a person. The caller receives a decision, not an error. That is a policy, and it is written once, in the code that walks the chain. Without it, one broken service would stop every checkout.

## 8. Switched Off By A Property

Fifth demo: a setting switches a check off. Set the fraud check's setting to false, and that check disappears. The chain is now three checks long. Carol, who was rejected before, is now approved. And no code changed. That is handy in a test, but dangerous in production. So print the chain's order when the application starts.

## 9. Nobody Answers

Last demo: what if nobody answers? When every check has no opinion, a fallback decides. It is a named setting. By default, it approves, so Asha goes through. Change it to refer, and Asha is sent to a person instead. Reaching the end of a chain should be a decision, not an accident.

## 10. The Verdict

So, here is the verdict. Put the cheap, decisive checks first. Decide what a crashing check should mean. Print the chain's order when the application starts. And test the whole chain, not just each check.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for a constructor that receives a list of one interface. With the at Order annotation on each implementation. And a loop that stops at the first answer.

## 12. Where You Have Met This

Where have you met this before? In servlet filters, in Spring Security's filter chain, and in validation pipelines.

## 13. What Was Used

For the record, here are the versions. Spring Boot four point one point one. No web server, no database, and no web library.

## 14. What Is Real Here

A quick, honest note about this demo. Spring's container, and its ordering, are real. The paid fraud service is only a counter. Nothing is really paid for.

## 15. When This Is Too Much

So, when is this too much? For two checks that never change, a plain if statement is clearer than a chain.

## 16. Thanks for Watching

That's Chain of Responsibility with Spring. If you remember one sentence, make it this one. Spring builds and orders the chain for you, and that order becomes a cost you have to watch. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Give two checks the same order number. Then run it, and find out what happens. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
