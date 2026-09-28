# Strategy with Spring Pattern — Video Narration Script

## 1. Strategy with Spring

Hello, and welcome. This video explains the Strategy pattern, in Java, using Spring Boot. This video is presented by Jayasekhar Konduru. First, a simple definition. The Strategy pattern puts each option of a decision in its own class, behind one shared interface. In Spring, the strategies are beans of one interface. And the container collects them into a map for you, keyed by name. Think of a phone's contact list. You pick a name, and the phone knows the number. This is the framework version of the Strategy video, with the same delivery pricing. We will let Spring find the four pricing rules, choose one by configuration, and add a fifth. Then we will see the failures that come with it: an ambiguous injection, and a wrong name.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Strategy video. That one prices delivery under four interchangeable rules. It chooses one by a configured name, and refuses an unknown name. If you are new to the pattern, watch that one first. Here, we keep the same example, and ask what Spring Boot does with it.

## 3. Before The First Line

One thing is new in this project: Spring Boot. At its heart, Spring is a container that creates your objects. It can gather every bean of one interface into a map, keyed by each bean's name. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. Spring Finds The Strategies

First demo: Spring finds the strategies. The checkout asks for a map of shipping rules. It receives four: distance, flat, free over threshold, and weight banded. The keys are the bean names. And we chose those names ourselves, in each class's component annotation.

## 5. The Same Shipments, Every Rule

Second demo: three shipments, priced under every rule. The flat rule charges four pounds ninety-nine for all of them. Weight banded ranges from two ninety-nine to eight ninety-nine. Free over threshold makes the heavy, expensive one free. And an unknown rule name, like teleport, is refused. The error message lists the names that do exist.

## 6. Configuration Chooses

Third demo: configuration chooses the rule. Set the shipping rule setting to distance, and the heavy shipment costs four ninety-nine. Set it to teleport, and the application refuses to start. That is the right moment to find a typo. At startup, not at a customer's checkout.

## 7. Four Beans, One Interface

Fourth demo: a failure. One class asks for a single shipping rule, instead of the map. Spring finds four candidates, and refuses to guess. The application does not start. The message says it expected a single bean, but found four. The message is clear. But notice the risk. Adding a second bean of an interface can break a class that worked perfectly yesterday.

## 8. A Fifth Rule

Fifth demo: adding a fifth rule, called express. It joins the map, and costs nine pounds ninety-nine. The checkout class was not touched at all. In this demo, it is registered by hand, so the default stays at four. A normal scanned class would be found in exactly the same way.

## 9. A Default When Nobody Chooses

Last demo: a default, for when nobody chooses. Mark the flat rule as primary. Now the class that asked for a single rule starts up, and receives the flat rule. And the map still holds all four. Primary answers the question: which one, when nobody says? The map answers: which ones exist?

## 10. The Verdict

So, here is the verdict. Inject the map of strategies. Name each bean explicitly. Check the configured name when the application starts. And mark one bean as primary, where a single default is needed.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for a constructor that receives a map, from names to an interface. Or the at Primary, or at Qualifier annotations, next to an interface.

## 12. Where You Have Met This

Where have you met this before? In payment providers, message handlers, and export formats, chosen by name.

## 13. What Was Used

For the record, here are the versions. Spring Boot four point one point one. No web server, no database, and no web library.

## 14. What Is Real Here

A quick, honest note about this demo. Spring's container and its injection are real. And nothing depends on timing.

## 15. When This Is Too Much

So, when is this too much? Two rules that never change do not need a container. A plain if statement is easier to read.

## 16. Thanks for Watching

That's Strategy with Spring. If you remember one sentence, make it this one. Spring keeps the table of strategies for you, and the names in it are yours to choose, and to check. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Rename one of the beans. Then find out which configuration breaks. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
