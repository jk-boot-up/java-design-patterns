# Service Locator with Consul Pattern — Video Narration Script

## 1. Service Locator with Consul

Hello, and welcome. This video explains the Service Locator pattern with Consul, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Service Locator video. That one argued against the pattern, but said it is still right when what is available is a fact you only learn at run time. Service discovery is exactly that, over a network. The plain definition, in short: ask a middleman for what you need, by name. By the end you will see a real service registry answer, instances come and go without the caller's code changing, the old costs return, one new cost appear, and the alternative: be given an address, and never ask.

## 2. The Partner Project

This video assumes the Service Locator video. If you have not seen it, start there. It argued against the pattern, with evidence, and it also said where the pattern is still right: where what is available is a run-time fact. This one uses the same checkout, with its collaborators now on the other side of a network. It does not teach the pattern again.

## 3. Before The First Line

Before the first line, three new things. Consul is a service registry. Services register themselves, with a name, an address, and a health check. Callers ask for the healthy ones. It runs here as a plain local process. Nginx is a web server and proxy, and Docker runs it in a container. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it, including the standard library's own form.

## 4. The Locator Asks Consul

Here is the setup. Two payment gateway instances and one notifier, each a real H T T P server, each registered with Consul with a health check. Nothing is simulated. The locator asks Consul for the healthy payment gateways. Two. Four orders are placed, and they are shared: two to each. The checkout never knew an address. It asked for payment gateway, by name.

## 5. The Genuine Advance

Now the genuine advance. Gateway one's health check is marked as failing. Consul reports one healthy gateway. Four more orders: gateway one served none, gateway two served all four. Gateway one recovers, and it is used again. The checkout's code did not change. A registry with fixed entries could never do this, and it is the reason this pattern earns its place.

## 6. The Old Costs Return

Now the old costs, over a network. The service names are strings. A typo, payment gatway, compiles fine, and fails at run time: no healthy instance. And worse, the notifier's registration is lost. Nothing in the checkout says it needs one. On a real order, the checkout asks for the gateway, and the payment goes through. Then it asks for the notifier, and there is none. The failure arrived in production, after the money moved. It is the same bill as the hand-built locator.

## 7. A New Cost: A Stale Cache

A new cost, from the network. Asking Consul on every call is slow, so it is tempting to remember the answer. A caching locator asks Consul once. Then gateway one dies, and Consul is told. The cache is not. The locator keeps handing out the dead address, and the call fails with a connection exception. Consul was asked once, in total. Faster, and wrong. The uncached locator recovers at once. And after a refresh, the cache heals too. But when to refresh is now your problem.

## 8. The Alternative: Be Given

The alternative, and the point of the whole category: stop asking. Nginx, in a Docker container, is given the healthy instances once, from Consul. The caller is given one address, nginx's, and asks nothing. Four of four requests succeed, shared across two instances. Now stop one instance. Four of four more still succeed, all served by the survivor, because nginx retried the next one. The class never knew, because it never looked anything up. This is dependency injection's idea, at the level of a network address.

## 9. The Verdict

My verdict, plainly. Service discovery is the strongest case for a locator, because where instances are is a genuine run-time fact. Even so, prefer to be given an address, by the platform, a proxy, or D N S, than to have every class ask.

## 10. How To Recognise It

How do you recognise this in code you did not write? Discovery client, get instances, in Spring Cloud. A Consul, Eureka, or ZooKeeper client, used inside business classes. A service name as a string, turned into a U R L at call time. And a load balanced client, where the lookup is hidden behind an annotation.

## 11. Where You Have Met This

You have met this in Spring Cloud's discovery client, in Netflix Eureka, and in Consul itself. And Kubernetes' built-in D N S is the given form: the platform hands your code an address, and it never asks.

## 12. What Is Real Here

The same honest admission as everywhere in this course, and for once nothing is simulated. A real Consul agent, real H T T P servers, and a real nginx in a real container. The demo instances only listen for the length of the run.

## 13. When This Is Too Much

So when is it too much? For a fixed set of services with fixed addresses, configuration is simpler, and needs no registry at all.

## 14. Thanks for Watching

That's the Service Locator with Consul. If you take one sentence away, take this one: discovery is a legitimate locator, and being given an address is better still. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, give the caching locator a time to live, and notice the decision you just made. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
