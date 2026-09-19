# Dependency Injection Pattern — Video Narration Script

## 1. Dependency Injection

Hello, and welcome. This video explains Dependency Injection in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a class says what it needs, in its constructor, and is given it. It never goes looking. This is the last project in the foundational category, and it closes an argument the last two videos began. Registry put things in a known place. Service Locator made a middleman that could find them. Dependency Injection stops the class asking at all. All three used the same three collaborators in our online store, a discount policy, a payment gateway and a notifier. By the end you will have seen it done in plain Java first, in nine lines, and you will have seen a small container written from scratch, so that a container is something you have watched being built, not something you take on trust.

## 2. The Argument So Far

A quick recap of the argument. The registry: a well-known place to put things. It left dependencies invisible, and state shared between tests. The service locator: a middleman that finds or creates them. The compiler still said nothing while a dependency was missing. The problem in both is one word: ask. The class asks, so nobody outside it knows what it needs.

## 3. The Signature Is The List

Here is the answer. The checkout service declares what it needs, in its constructor. Discount policy. Payment gateway. Notifier. That is the signature, and the signature is the dependency list. It is complete. It is checked by the compiler. Try to build a checkout service with no arguments, and it does not compile. There is no way to forget a collaborator. It never looks anything up, so nothing is hidden. And it is valid the moment it exists.

## 4. Wired By Hand

Now the wiring, by hand, before any framework. Something has to build the objects, and hand them to each other. Here it is: nine lines of plain Java, in one place. Build the policy, the gateway and the notifier. Build the checkout service with those three. Build the printer and the auditor. Build the storefront with all of them. It runs. Charged nine thousand pence. Three messages sent. That is what a container does for you. A container is an optimisation of something you can write yourself.

## 5. Three Forms

There are three forms. Constructor injection, which you have seen. Setter injection: for things that are genuinely optional. Here the notifier has a setter and a do-nothing default, and the order works without one. And field injection, where the fields are private, and something reaches in from outside. This one compiles with no arguments, and is invalid. Placing an order throws a null pointer exception. It only works once something reaches in with reflection. It cannot be built validly in a test without a framework. My recommendation: constructor injection. Mandatory, visible, and valid on creation.

## 6. A Container, Written Here

Now a container, written here, so it is not magic. Eighty-six lines. It reads each constructor's parameter types. For each one, it finds or builds a matching object. Then it calls the constructor. It builds the same graph as the hand wiring, and the same order is charged, nine thousand pence. That is what Spring, Guice and Dagger do, plus scanning, lifetimes, and a great deal of polish.

## 7. The Bill: It Fails At Start-Up

Now the bill. A container that cannot build the graph fails, and it fails when it starts. A bean missing: no bean for its parameter of type notifier. A circular dependency: chicken needs egg, and egg needs chicken. That is better than the service locator, which failed on the first real order, after the money moved. But it is still not at compile time. And a warning: a class whose constructor takes seven things has a design problem that no injection style fixes. The long constructor is telling you the class does too much.

## 8. Also On The Bill

Two more costs. First, by hand, the wiring grows with the application. Nine lines is fine. Nine hundred is not. That is what a container is for. And it costs you some magic, because now something else builds your objects. Second, constructors grow long. When they do, do not blame the injection. Listen to what it is telling you.

## 9. The Progression

Here is the whole argument, in three moves. The registry put things in a known place. The service locator made a middleman that could find them. Dependency injection stopped the class asking at all. Each one solved the problem the one before it left. And the last one is the only one where the class tells you, in its signature, what it needs.

## 10. The Verdict

My verdict, plainly. Use constructor injection. Wire by hand until the wiring hurts. Then use a container. And remember: dependency injection is not Spring. You have just done it, in plain Java.

## 11. How To Recognise It

How do you recognise this in code you did not write? A constructor whose parameters are interfaces, in a class that never calls new on its collaborators. In Spring, the component or service annotation, with the collaborators as constructor parameters. In Guice and Dagger, the inject annotation. And a main method, or a config class, that builds everything in order. This project does not run Spring. The point is that you no longer need it to understand it.

## 12. What Is Real Here

The same honest admission as everywhere in this course. It is all plain Java, including the container. The container is teaching size: no scanning, no scopes, no polish. But the failures it shows, a missing bean and a circular dependency, are the real ones.

## 13. When This Is Too Much

So when is it too much? Never, for the idea. A container is too much for a small application that fits in a main method.

## 14. Thanks for Watching

That's Dependency Injection. If you take one sentence away, take this one: stop asking, and be given, because a signature that lists what a class needs is worth more than any framework. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, make two beans depend on each other, and read the message the container gives you. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
