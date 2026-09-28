# Hexagonal Architecture Pattern — Video Narration Script

## 1. Hexagonal Architecture

Hello, and welcome. This video explains Hexagonal Architecture, in Java. It is also called Ports and Adapters. This video is presented by Jayasekhar Konduru. First, a simple definition. The core of the program says what it needs from the outside world, as interfaces, in its own words. Those interfaces are called ports. Outside the core, adapters plug into those ports. Some adapters do work for the core, like storing data. Others call into the core, like a web request. And every dependency points into the core, never out of it. Think of the sockets on a wall. The wall decides the shape of the socket. A lamp, a kettle, or a charger just plugs in. You can change the lamp without rewiring the house. The previous video, Layered Architecture, ended with one honest problem. Its use case still had to name its storage class. This video fixes exactly that, and proves it twice. By the end, you will have one simple test for telling a port from an adapter: who is allowed to name whom?

## 2. The Scenario

Here is the job. It is the same order as every project in this series. A customer called Ada Okafor buys an espresso machine, a coffee grinder, and two bags of coffee beans, for three hundred and eighty-two pounds fifty. The steps are the same too. Check the stock, take the payment, store the order, and notify the customer. What changes is how much the core knows about how those steps happen. The core needs four things: a catalogue, a payment gateway, somewhere to store orders, and a way to notify. Each one is an interface, and the core writes all four itself.

## 3. The Naive Version

Let's start with the naive version. It is the use case from the previous project, copied honestly. Its fields are three concrete classes. An in-memory order store. An in-memory payment gateway. And an in-memory product catalogue. Not interfaces. The real classes that do the work. Does it work? Yes, it places the order correctly. But two problems follow. One. You cannot test this class without building all three of those classes first. Two. If any of them is replaced, this file must be edited, even though its logic did not change.

## 4. Ports, Declared By The Core

Here is the fix, and it is one single move. The core declares four interfaces. Order Store, Payment Gateway, Product Catalog, and Notifier. All four live inside the core, in a package called core dot port. Not in the adapter package. Outside the core, there are two kinds of adapter. A driven adapter implements a port. The core calls it, for example, to store an order. A driving adapter calls into the core. For example, a web request that asks the core to place an order. And here is the rule. The core never names an adapter. Not one it calls, and not one that calls it. So if you are unsure whether something is a port or an adapter, ask one question. Who names whom?

## 5. One Move From The Project Before It

This move is smaller than it sounds, so let's be precise. In the layered project, the storage interface lived in the bottom layer, called infrastructure. The use case, above it, reached down to use it. Layering allows that. Here, the very same interface, with the same three methods, lives inside the core instead. And the storage class, outside, reaches in to implement it. So the interface itself did not change at all. Only the package it lives in changed. And with it, the direction the dependency points. That is the whole distance between the previous project and this one.

## 6. The Core, Driven By HTTP

Let's watch the real core run. A pretend web request arrives at an adapter. The adapter calls one method on the core. The core checks stock through the catalogue port. It takes payment through the payment port. It saves the order through the storage port. And it notifies the customer through the notifier port. The order is created, with status two hundred and one, for three hundred and eighty-two pounds fifty. Now think about the core's use case class. It imports from only two places: the domain, and the port package. Not one adapter. It truly does not know that the web, or any particular storage, exists.

## 7. The Half Most Treatments Skip

Many explanations stop here. They show that storage can be swapped, and call it done. That is only half the story. Hexagonal architecture is often taught as being all about databases. Swap the storage, and the core does not change. That is true. The other half is about who calls into the core. If the core can really be called from anywhere, we should prove it, by calling it from somewhere new. So this project does both. It swaps the storage underneath the core. And it drives the same core from a completely different caller.

## 8. The Same Core, Driven By A CLI Instead

Here is the proof. Instead of a web request, a pretend command line calls the core. It is just one line of text, read by hand. It calls exactly the same use case class that the web adapter called. The result is the same order, with the same total. And the use case class was not touched. It takes the same four ports either way. Here is the lesson. If a core has only ever been called one way, it has not proven it is independent of its callers. It has only proven it works with the first caller someone wrote.

## 9. The Rule, Written Where A Build Can Read It

All of this fits in one rule, written as a test with a library called ArchUnit. No class in the core package may depend on any class in the adapter package. That one rule catches two mistakes. The core naming an adapter it calls. And the core calling back into an adapter that called it. The test runs with every other test in the build. And a second test points the same rule at the naive version, on purpose, to prove the rule can fail.

## 10. Watching It Go Red

So what does a failure sound like? The build reports an architecture violation. It says the rule, no core class may depend on an adapter, was broken once. Then it names the naive use case class, and the in-memory order store it reached for. A promise on a whiteboard is forgotten within a month. This message fails the build, by name, in under a second.

## 11. The Forced Change, Both Halves At Once

Now, the big change, with both halves at once. On one side, storage changes from a simple map to an append-only log. On the other side, the caller changes from a web request to a command line. Let's count what changed, from the real files. Two files were added. One file was modified: the main setup code, and only four lines of it. The core is fourteen classes. Not one of them was opened, for either change. Two swaps, on opposite sides of the core, and zero core classes touched.

## 12. The Bill

Every pattern has a cost, so let's name this one honestly. First, interfaces for things that have only one implementation. The Notifier has exactly one adapter in this project. Writing an interface for a class you will never swap is ceremony. This project has some of that, to show the shape clearly. Second, translation. Every driving adapter must translate its own input, like a web body or a line of text, into what the core wants. And then translate the answer back. That is real code, for every adapter.

## 13. When This Is Too Much

So, is this worth it for an application with one database and one way in? Often, no. Four interfaces, each with one implementation that will never change, is extra complexity with nothing behind it. It becomes worth it when the core truly needs more than one caller. Or more than one store. Or must be tested before any real infrastructure exists. So ask yourself honestly. Will either swap ever really happen? Or are you building for a change that is never coming?

## 14. Thanks for Watching

That's Hexagonal Architecture. If you remember one sentence, make it this one. Hexagonal architecture is not about databases, it is about who is allowed to name whom. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Write a third driving adapter, such as a console menu or a scheduled job. Then check that the Place Order Service class needs zero lines changed to accept it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
