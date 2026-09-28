# Bulkhead with Resilience4j Pattern — Video Narration Script

## 1. Bulkhead with Resilience4j

Hello, and welcome. This video explains the Bulkhead pattern in Java, using a library called Resilience four J. This video is presented by Jayasekhar Konduru. First, a simple definition. A bulkhead gives each kind of work its own compartment. So a slow job can fill its own compartment, but cannot take the room that other work needs. The name comes from ships. Walls divide the hull into watertight rooms, so one hole floods one room, not the whole ship. In Resilience four J, a bulkhead is an annotation. It limits how many calls to one thing may run at the same time. Or it gives those calls threads of their own. In our online store, a slow nightly supplier feed must never stop checkout from selling. By the end, you will hear one shared compartment let the feed starve checkout. Then a compartment each, protecting it. And the costs: the idle room behind the wall, a way to bypass it by accident, and the two kinds of bulkhead.

## 2. The Partner Project

This video builds on the plain Java Bulkhead video. If you have not seen it, start there. That video gives the supplier feed and checkout their own pools of workers. So a slow feed cannot stop the shop selling. This video uses the same example. It does not teach the pattern again. It shows what Resilience four J does with it.

## 3. Before The First Line

Before any code, what is Resilience four J? It is a library of resilience patterns for Java. It has two kinds of bulkhead. One limits how many calls run at once. The other runs the calls on threads of their own. Here, it runs inside Spring Boot, switched on by an annotation. And a promise. Skipping this video loses none of the pattern. The plain Java video teaches all of it.

## 4. One Compartment For Everything

First, the problem. One compartment serves everything, and it has four permits. A permit is simply permission for one call to run. Four slow feed jobs take all four permits. Then checkout arrives. It is fast, and nothing is wrong with it. But it is refused. A background job has stopped the shop selling.

## 5. A Compartment Each

Second demo: a compartment each. The feed gets two permits of its own. Two slow feed jobs fill them. A third feed job is refused. Checkout has its own compartment. So it sells as normal. The hole floods one room. The ship stays up.

## 6. What A Full Compartment Does

Third demo: what a full compartment does to the callers. It refuses them at once. The waiting time is set to zero, so no caller queues up. You can add a fallback method, which is a backup answer. With a fallback, the refused job hears: feed batch skipped tonight. Without one, it gets an error.

## 7. The Cost Of The Wall

Fourth demo: what the wall costs. The feed's compartment has no permits free. Checkout's compartment has four permits free, sitting idle. And nothing can lend them to the feed. That is the price of the protection. Just like the ship, where an empty room cannot lend its space to a flooded one.

## 8. The Annotation Is A Proxy

Fifth demo: a trap. Spring adds the bulkhead by wrapping the object in a proxy. A proxy is a stand-in that sits in front of the real object, and checks each call on the way in. But if a method calls another method on the same object, the call never goes through the proxy. So here, ten feed jobs are called from inside the same object. All ten run at once, in a compartment meant for two. And the bulkhead still reports two permits free. It never saw a single call. The same rule applies to every Spring annotation that works through a proxy.

## 9. A Compartment With Its Own Threads

Last demo: the other kind of bulkhead. This one runs each call on threads of its own. Four jobs are handed to it. Two are running. One waits in a queue that holds only one. And the fourth is refused. The caller was never blocked, not even by the slow jobs. So here is the difference. The permit kind protects the caller's shared threads. The thread pool kind protects the caller itself, because the caller never waits.

## 10. The Verdict

So, here is the verdict. Give each kind of work its own compartment. And size each one from real load, not from a guess. Choose the thread pool kind when the caller must never be blocked. And never call a bulkhead method from inside the same object, because the proxy is skipped.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for a bulkhead annotation, with a name. Look for a type set to thread pool. Or look for a bulkhead full exception in a log.

## 12. Where You Have Met This

Where have you met this before? In any Spring service that calls several other services, where some of them are slow.

## 13. What Was Used

For the record, here is what was used. Spring Boot, version four point one point one. Resilience four J, version two point four point zero. There is no web server, and no web starter.

## 14. What Is Real Here

A quick, honest note about this demo. Everything is real: the real bulkheads, and real threads. The slow calls are held at a gate, until the demo opens it. So nothing depends on timing, and every run gives the same result.

## 15. When This Is Too Much

So, when is this too much? If there is only one caller and one slow service, you do not need compartments. A simple limit on how often you call it is enough. That is the job of a rate limiter.

## 16. Thanks for Watching

That's Bulkhead, with Resilience four J. If you remember one sentence, make it this one. Resilience four J gives you compartments as configuration, and the wall always costs some idle capacity. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Give the checkout compartment two permits instead of four. Then guess what the fourth demo will report, before you run it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
