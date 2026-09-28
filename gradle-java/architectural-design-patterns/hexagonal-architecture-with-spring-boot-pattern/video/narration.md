# Hexagonal Architecture with Spring Boot Pattern — Video Narration Script

## 1. Hexagonal Architecture with Spring Boot

Hello, and welcome. This video explains the Hexagonal Architecture pattern, in Java, using Spring Boot. This video is presented by Jayasekhar Konduru. First, a simple definition. In Hexagonal Architecture, the core of the program declares what it needs as interfaces, called ports. Adapters outside the core plug into those ports. With Spring Boot, the adapters become beans, chosen by configuration. And the core stays a plain Java class, which the framework simply hands out. Think of a games console. The console stays the same, and you choose which controller to plug in. This is the framework version of the Hexagonal Architecture video, with the same online store. We will run the same core on two storage options, through two different entry points, and with no framework at all. Then we will see what happens when the core reaches for Spring.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Hexagonal Architecture video. That one puts the order logic in a core that knows only ports. So storage and notification can change, without the core changing. If you are new to the pattern, watch that one first. Here, we keep the same example, and ask what Spring Boot does with it.

## 3. Before The First Line

Three things are new in this project. One. Spring Boot, which picks the adapters and wires them together, from configuration. Two. An in-memory database, called H2. Three. ArchUnit, a library that checks, in a test, that the core does not depend on the framework. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. The Core Is Plain Java

First demo: the core is plain Java. We ask Spring for the use case. It hands back an ordinary class from the core package. Not a special wrapped object, called a proxy. And how many core classes mention Spring, or any adapter? Zero.

## 5. Two Storage Adapters

Second demo: two ways to store orders. One setting in the configuration chooses the storage. Set it to memory, and orders are kept in a list. Set it to J D B C, and orders go into a database. Either way, the receipt is the same. The first order is number one, for three hundred pounds, and the stock falls to four. And the core did not change at all.

## 6. Two Doors Into One Room

Third demo: two doors into the same room. Door one is a console adapter. It orders one coffee machine, which works. Then it asks for ten, and is refused, because there is not enough stock. Door two is a batch adapter. It sends three order lines at once. Two are accepted, and one is refused. Neither door knows how the other works. Both call the same port.

## 7. The Core Without A Container

Fourth demo: the core with no framework at all. Ten thousand orders go through the real use case. The adapters are created by hand. There is no Spring anywhere in this test. The payment port is filled with a tiny one-line function. That is exactly what a port is for.

## 8. A Use Case That Reaches For Spring

Fifth demo: the shortcut. Someone writes a use case that uses Spring directly. It has a transaction annotation, and a database client. The architecture rule reports ten violations. All ten are in that one shortcut class. The real core has none. Spring will not stop you writing the shortcut. A rule will.

## 9. A Port With No Adapter

Last demo: a port with no adapter. We set the storage setting to a value that no adapter handles. The application refuses to start. It says there is no bean of type Order Store, naming the missing port. Wiring by hand would have caught this when the code compiled. The container only finds out at startup. That is later, but still before any customer is affected.

## 10. The Verdict

So, here is the verdict. Keep the core free of framework annotations. Wire it together in one configuration class. Choose the adapters with configuration settings. And keep a test rule that guards the core.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for a configuration class that creates the use case with the new keyword. And look for adapters marked with the at Conditional On Property annotation, so a setting decides which one is used.

## 12. Where You Have Met This

Where have you met this before? In Spring applications whose business code has no framework annotations at all.

## 13. What Was Used

For the record, here are the versions. Spring Boot four point one point one. The H2 database. And ArchUnit one point five. There is no web server.

## 14. What Is Real Here

A quick, honest note about this demo. Everything in it is real. The real Spring container, a real database, and a real architecture rule.

## 15. When This Is Too Much

So, when is this too much? For a small service with only one kind of storage, a port with a single adapter is just ceremony.

## 16. Thanks for Watching

That's Hexagonal Architecture with Spring Boot. If you remember one sentence, make it this one. Spring wires the hexagon together, but only a rule keeps the core free of Spring. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a Spring annotation to a core class. Then run the rule, and listen to what it reports. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
