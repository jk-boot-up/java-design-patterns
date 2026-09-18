# Hexagonal Architecture Pattern — Video Narration Script

## 1. Hexagonal Architecture

Hello, and welcome. This video explains Hexagonal Architecture in Java -- also called Ports and Adapters -- and it is written and presented by Jayasekhar Konduru. Let's start with the plain definition. The core of an application defines ports -- interfaces, in its own words, for whatever it needs from the outside world. Adapters, on the outside, either implement those ports or call in through them. Every dependency between the core and the world outside it points inward, into the core, never out of it. This is the second project in a series building the same online shop five different ways, and it picks up exactly where the previous one, Layered Architecture, left off -- that project ended by admitting one honest cost: its use case still had to name its storage class to compile. This video inverts exactly that, and then proves the inversion twice: once by swapping the storage underneath the core, and once by driving the same core from somewhere completely different. By the end you will know the actual test to apply when you are unsure whether something is a port or an adapter -- which is simply, who is allowed to name whom.

## 2. The Scenario

Same order as every project in this category, placed the same way: check stock, take payment, store the order, notify the customer. Ada Okafor's three hundred and eighty-two pounds fifty. What changes in this video is not the feature. It is what the core is allowed to know about how those four things actually happen. The core needs a catalogue, a payment gateway, somewhere to store an order, and a way to notify a customer -- four needs, stated as four interfaces, all four written by the core itself.

## 3. The Naive Version

Here is where this project starts, and it is not a strawman -- it is the previous project's use case, honestly reproduced. This class's fields are typed as concrete adapters: an in-memory order store, an in-memory payment gateway, an in-memory catalogue. Not interfaces the core declared -- the actual classes that do the storing and the charging. It works. It places the order correctly. And two things follow from those field types that would not follow from an interface. You cannot unit-test this class without constructing all three adapters. And the moment any one of those three classes is replaced, this file must be opened and edited -- not because its logic changed, but because a type it named no longer exists.

## 4. Ports, Declared By The Core

So here is the fix, and it is one move, stated precisely. Four interfaces -- a place to store orders, a way to take payment, a catalogue, a way to notify -- all four declared inside the core itself, in a package called core dot port. Not in the adapter package. Inside the core. An adapter, on the outside, either implements one of these interfaces -- that is a driven adapter, one the core calls -- or it holds a reference to the core's use case and calls into it -- that is a driving adapter, one that calls the core. And here is the rule that makes this precise rather than a vibe. The core never names an adapter. Not a driven one it is calling, and not a driving one that might be calling it. If you are ever unsure whether something is a port or an adapter, ask exactly one question: who names whom?

## 5. One Move From The Project Before It

I want to be precise about how small this move actually is, because it is easy to make hexagonal architecture sound like a bigger idea than it is. In the layered architecture project, the storage interface lived in the bottom layer, called infrastructure, and the use case above it reached down to name it. That is allowed, under layering's own rule -- each layer may depend on the one beneath it. Here, the exact same interface -- three methods, save, find, describe -- lives inside the core instead. And the adapter that used to define it now reaches up to implement it. Read that again, because it is the whole trick. The interface did not change. Only which package it lives in changed -- and with it, which direction the import points. That is the entire distance between the project before this one and this one.

## 6. The Core, Driven By HTTP

So let's watch the real core run. A simulated HTTP request arrives at an adapter, which calls one method on the core's use case. The core checks stock through the catalogue port, charges through the payment port, saves through the storage port, notifies through the notifier port -- and every single one of those four names is a name the core chose for itself. Open the core's use case class and count its imports. Two: the domain, and the port package. Not one adapter. It genuinely does not know that HTTP, or any particular way of storing an order, exists.

## 7. The Half Most Treatments Skip

Most explanations of this pattern stop here, having shown you that storage can be swapped, and call it done. This video insists on the other half. Hexagonal architecture is usually taught as being entirely about databases -- swap the driven side, storage, and the core does not change. That is real, and it is half the claim. The half almost everyone skips is the driving side -- who is allowed to call in. If the core can genuinely be called from anywhere, that has to be demonstrated by actually calling it from somewhere new, not merely asserted. So this project does both, in the same act. It swaps the storage underneath the core, and it drives the very same core from a caller that shares no code at all with the first one.

## 8. The Same Core, Driven By A CLI Instead

Here is the proof. A simulated command line -- one string, parsed by hand -- calls the identical use case class the HTTP adapter called two acts ago. Same order. Same total. And critically: the use case class was not touched to make this possible. Its constructor takes the same four ports either way. This is the sentence I want you to take from this scene. A core that can only be shown accepting one kind of caller has not actually proven it is decoupled from callers -- it has proven it works with the one caller somebody happened to write first.

## 9. The Rule, Written Where A Build Can Read It

One sentence covers all of this. No class in the core package may depend on any class in the adapter package. Notice that one rule catches both mistakes at once -- the core naming a driven adapter it is calling, and the core accidentally calling back into a driving adapter that called it. Either direction breaks the same rule, and this one test covers both. It runs in gradlew test alongside everything else, and a second test widens the same rule to the naive package on purpose, to prove it is capable of failing.

## 10. Watching It Go Red

Here is what the build prints. Architecture violation. And then the part that matters: it names the naive use case class, and it names the adapter it reached for. The difference between a whiteboard promise and this message is the difference the whole category is built to teach. One of them is forgotten within a month. The other one fails a build, by name, in under a second.

## 11. The Forced Change, Both Halves At Once

So here is the bill, both halves counted together, because this project's whole claim is that both are free at once. Storage changes from a map to an append-only log. Separately, the calling side changes from a simulated HTTP request to a simulated command line. Counted from the real files on disk: two files added, one file modified -- the composition root, four lines total. And fourteen classes make up the entire core. Every one of them: never opened, for either change. Two simultaneous swaps, on opposite sides of the same hexagon, and the number of core classes that had to be touched for either one is zero.

## 12. The Bill

Every project in this category has to pay a bill honestly, and here is this one's. Interfaces for things with exactly one implementation. Notifier has one adapter in this whole project. Writing an interface for a class you will never swap is ceremony, and this project has some of it, in the name of demonstrating the shape clearly. And mapping. Every driving adapter spends real code translating its own shape -- a JSON body, a command line string -- into what the core actually wants, and translating the answer back. That cost is paid once per adapter, and it is genuinely there.

## 13. When This Is Too Much

So the honest question this project must not dodge. For an application that will only ever have one database and one way of being called, is any of this worth building? Often, no. Four interfaces, each with exactly one implementation that will never be swapped, is indirection with nothing behind it but the diagram. It is worth it the moment a core genuinely needs more than one caller, or more than one store, or needs to be tested without any of its real infrastructure existing yet. The question worth asking honestly before reaching for this: is either swap ever actually going to happen, or am I building the seam for a change that is never coming?

## 14. Thanks for Watching

That's hexagonal architecture. If you take one sentence away, take this one: hexagonal architecture is not about databases. It is about who is allowed to name whom. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, try this. Write a third driving adapter -- a console menu, a scheduled job, anything -- and confirm that PlaceOrderService dot java needs zero lines changed to accept it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching, and I'll see you in the next one.
