# Service Locator with Consul Pattern — Video Narration Script

## 1. Service Locator with Consul

Hello, and welcome. This video explains the Service Locator pattern, in Java, using Consul. This video is presented by Jayasekhar Konduru. First, a simple definition. A service locator is a middleman. You ask it for what you need, by name. Think of a taxi dispatcher. You ask for a taxi, and the dispatcher knows which cars are free right now. This is the framework version of the Service Locator video. That one argued against the pattern. But it said the pattern is still right when what is available is only known while the program runs. Finding services across a network is exactly that. By the end, you will hear a real service registry answer. Services come and go, without the caller's code changing. The old costs return, a new one appears, and then we hear the alternative: be given an address, and never ask.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Service Locator video. That one argued against the pattern, with evidence. And it said where the pattern is still right. Here, we use the same checkout. But its helpers now live on the other side of a network. We will not teach the pattern again.

## 3. Before The First Line

Three things are new in this project. First, Consul, a service registry. Services register themselves, with a name, an address, and a health check. Callers ask Consul for the healthy ones. Second and third, nginx, a web server that can forward requests, running inside Docker. And one promise. If you skip this video, you lose none of the pattern. This one is about the tools.

## 4. The Locator Asks Consul

First demo: the locator asks Consul. Here is the setup. Two payment gateway services, and one notifier. Each is a real web server, registered with Consul, with a health check. Nothing is simulated. The locator asks Consul for the healthy payment gateways. There are two. Four orders are placed, and shared, two to each. The checkout never knew an address. It only asked for payment gateway, by name.

## 5. The Genuine Advance

Second demo: the real advance. Gateway one's health check is marked as failing. Consul now reports one healthy gateway. Four more orders. Gateway one serves none. Gateway two serves all four. Then gateway one recovers, and it is used again. The checkout's code never changed. A registry with fixed entries could never do this. And it is why this pattern earns its place here.

## 6. The Old Costs Return

Third demo: the old costs return. Service names are just text. A typo, payment gatway, compiles fine. And fails only while running: no healthy service by that name. Worse, the notifier's registration is lost. And nothing in the checkout says it needs one. A real order arrives. The checkout asks for a gateway, and the payment goes through. Then it asks for the notifier, and there is none. The failure arrived in production, after the money moved. The same cost as the hand-built locator.

## 7. A New Cost: A Stale Cache

Fourth demo: a new cost, an out-of-date cache. Asking Consul on every call is slow. So it is tempting to remember the answer. A caching locator asks Consul just once. Then gateway one dies, and Consul is told. But the cache is not told. The locator keeps handing out the dead address. And the call fails, with a connection error. Faster, and wrong. The locator without a cache recovers at once. And after a refresh, the cache heals too. But deciding when to refresh is now your problem.

## 8. The Alternative: Be Given

Fifth demo: the alternative, be given. Nginx, in a Docker container, is given the list of healthy services, once, from Consul. The calling code is given just one address: nginx's. It asks nothing. Four out of four requests succeed, shared across the two gateways. Now stop one gateway. Four more requests, and all four still succeed. Nginx simply retried the one that was still running. The calling code never knew, because it never looked anything up. That is dependency injection's idea, applied to a network address.

## 9. The Verdict

So, here is the verdict. Finding services on a network is the strongest case for a locator. Because where the services are is only known while the program runs. Even so, prefer to be given an address. By the platform, a proxy, or D N S. Rather than making every class ask.

## 10. How To Recognise It

How can you spot this in code someone else wrote? Look for Spring Cloud's Discovery Client, and its get instances method. Look for a Consul, Eureka, or ZooKeeper client, used inside business classes. Look for a service name, written as text, turned into a web address at call time. And a load-balanced client, where the lookup hides behind an annotation.

## 11. Where You Have Met This

Where have you met this before? In Spring Cloud's discovery client. In Netflix Eureka. And in Consul itself. Kubernetes' built-in D N S is the given form. The platform hands your code an address, and your code never asks.

## 12. What Is Real Here

A quick, honest note about this demo. For once, nothing is simulated. A real Consul service, real web servers, and a real nginx, in a real container. The demo services only run for the length of the demo.

## 13. When This Is Too Much

So, when is this too much? For a fixed set of services, at fixed addresses, simple configuration is easier. And it needs no registry at all.

## 14. Thanks for Watching

That's the Service Locator, with Consul. If you remember one sentence, make it this one. Finding services is a fair use of a locator, but being given an address is better still. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Give the caching locator an expiry time. And notice the decision you just had to make. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
