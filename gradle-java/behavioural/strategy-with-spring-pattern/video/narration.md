# Strategy with Spring Pattern — Video Narration Script

## 1. Strategy with Spring

Hello, and welcome. This video explains the Strategy pattern with Spring Boot, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Strategy video. That one priced the same delivery under four interchangeable rules, chose one by configuration name, and refused an unknown name. This one shows the same idea inside Spring Boot. The plain definition, in short: in Spring, the strategies are beans of one interface, and the container collects them into a map for you. By the end you will see the four rules found by the container, chosen by configuration, and extended by a fifth, then see the failures that come with it: an ambiguous injection, and a wrong name.

## 2. The Partner Project

This video assumes the Strategy video. If you have not seen it, start there. It prices delivery under four interchangeable rules, chooses one by a configured name, and refuses an unknown name. This one uses the same example. It does not teach the pattern again. It shows what Spring Boot does with it.

## 3. Before The First Line

Before the first line of code, what Spring Boot is. Spring is a framework whose core is a container that creates your objects. It can gather every bean of one interface into a map, keyed by name. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. Spring Finds The Strategies

First, the container finds the strategies. The checkout asks for a map of shipping rules, and receives four. The keys are the bean names, and we chose them, in the component annotations.

## 5. The Same Shipments, Every Rule

Second, the same three shipments under every rule. Flat charges four ninety nine for all. Weight banded ranges from two ninety nine to eight ninety nine. Free over threshold makes the heavy one free. An unknown name at run time is refused, and the message lists the names that exist.

## 6. Configuration Chooses

Third, configuration chooses. Set the property to distance, and the heavy shipment costs four ninety nine. Set it to teleport, and the application does not start. That is the right place to find a typo: at startup, not at a customer's checkout.

## 7. Four Beans, One Interface

Fourth, the failure. A class asks for one shipping rule, not the map. The container finds four, and will not choose. The application does not start. The message is clear. But adding a second bean of an interface can break a class that worked yesterday.

## 8. A Fifth Rule

Fifth, adding a rule. A fifth rule joins the map, and the checkout class is not touched. The demo registers it by hand, to keep the default at four. A scanned class would be found the same way.

## 9. A Default When Nobody Chooses

Last, a default. Mark the flat rule primary, and the class that asked for a single rule now starts. It gets the flat rule. The map still holds all four. Primary answers, which one when nobody says. The map answers, which ones exist.

## 10. The Verdict

My verdict, plainly. Inject the map. Name the beans explicitly. Check the configured name at startup. And mark one primary where a single default is needed.

## 11. How To Recognise It

How do you recognise this in code you did not write? A map of string to an interface, in a constructor. Or a primary or qualifier annotation next to an interface.

## 12. Where You Have Met This

You have met this in payment providers, message handlers and export formats, chosen by name.

## 13. What Was Used

For the record. Spring Boot four point one point one. No web server, no database, and no web starter.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: Spring's container and its injection. Nothing depends on timing.

## 15. When This Is Too Much

So when is it too much? Two rules that never change need no container. A plain conditional is easier to read.

## 16. Thanks for Watching

That's Strategy with Spring. If you take one sentence away, take this one: Spring keeps the table of strategies, and the names in it are yours to choose and to check. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, rename a bean, and see which configuration breaks. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
