# Hexagonal Architecture with Spring Boot Pattern — Video Narration Script

## 1. Hexagonal Architecture with Spring Boot

Hello, and welcome. This video explains the Hexagonal Architecture pattern with Spring Boot, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Hexagonal Architecture video. That one put the order use case in a core that knows only ports, with adapters outside it, so storage and notification could change without the core changing. This one shows the same idea inside Spring Boot. The plain definition, in short: in Spring Boot, the adapters are beans chosen by configuration, and the core stays a plain class that the container is handed. By the end you will see the same core run on two storage adapters chosen by a property, through two driving adapters, and with no container at all, then see what happens when the core reaches for Spring.

## 2. The Partner Project

This video assumes the Hexagonal Architecture video. If you have not seen it, start there. It puts the order use case in a core that knows only ports, with adapters outside it, so storage and notification can change without the core changing. This one uses the same example. It does not teach the pattern again. It shows what Spring Boot does with it.

## 3. Before The First Line

Before the first line of code, what Spring Boot is. Spring Boot picks and wires the adapters from configuration. ArchUnit is a library that checks, in a test, that the core does not depend on the framework. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. The Core Is Plain Java

First, the core is plain Java. The container hands out the use case as an ordinary class from the core package. It is not a proxy. And no class in the core mentions Spring, or any adapter.

## 5. Two Storage Adapters

Second, one property chooses the storage. With memory, the order is kept in a list. With jdbc, it goes to a database. The receipt is the same, and the stock falls to four in both. The core did not change.

## 6. Two Doors Into One Room

Third, two doors into the same room. A console adapter places an order for a machine, and is refused for ten. A batch adapter places three lines, and one is refused. Neither knows how the other works. Both call the same port.

## 7. The Core Without A Container

Fourth, the core without a container. Ten thousand orders go through the real use case, with adapters made by hand. No Spring at all. The payment port is a one line lambda. That is what a port is for.

## 8. A Use Case That Reaches For Spring

Fifth, the shortcut. A use case with a transaction annotation and a database client breaks the inside rule ten times. All ten are in that class. The real core breaks it never. Spring will not stop you writing the shortcut. A rule will.

## 9. A Port With No Adapter

Last, a port with no adapter. Set the property to a value nobody handles, and the application does not start. It names the missing port. Hand wiring would have failed at compile time. The container finds out at startup, which is later, but still before any customer.

## 10. The Verdict

My verdict, plainly. Keep the core free of annotations. Wire it in one configuration class. Choose adapters by configuration. And keep a rule that guards the inside.

## 11. How To Recognise It

How do you recognise this in code you did not write? A configuration class that calls new on a use case. And conditional on property annotations on adapters.

## 12. Where You Have Met This

You have met this in Spring applications whose business code has no annotations.

## 13. What Was Used

For the record. Spring Boot four point one point one, H2, and ArchUnit one point five. No web server.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: the real container, a real database and a real rule.

## 15. When This Is Too Much

So when is it too much? For a small service with one storage, a port with one adapter is ceremony.

## 16. Thanks for Watching

That's Hexagonal Architecture with Spring Boot. If you take one sentence away, take this one: Spring wires the hexagon, and only a rule keeps the core free of Spring. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, add an annotation to the core, and run the rule. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
