# Onion Architecture Pattern — Video Narration Script

## 1. Onion Architecture

Hello, and welcome. This video explains the Onion Architecture pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: onion architecture arranges code in rings, with the business rules at the centre. Every ring may depend only on rings further in, never outward. This is another project in the architecture category, whose subject is how a whole application is arranged, and who may depend on whom. In our online store, the order class saves itself with a database statement, and so it cannot change without touching the database. By the end you will see an order that reaches out to a database, see the rings and the one rule, see a checker catch a class that breaks the rule, see the storage swapped without touching the inside, see the rules checked with no storage at all, and see the bill, which is conversions and ceremony.

## 2. The Scenario

Here is the scenario. An order is placed, priced and saved. The pricing rule gives ten percent off orders of one hundred pounds or more. Storage may change, from memory, to a file, to a database. The question: what sits at the centre?

## 3. The Core Reaches Outward

First, the core reaches outward. The order saved itself with a SQL statement. To change the storage, the order class, at the centre, must be edited.

## 4. The Pattern

The pattern. Rings, with the business rules at the centre. Storage and screens outside. One rule: a class may refer to its own ring, or to a ring further in. Never outward.

## 5. Rings, And One Rule

Second, rings, and one rule. Ring zero is the order, the order line, and the idea of a repository. Ring one is the pricing rules. Ring two is the use cases. Ring three is storage and screens. The rule: a class may refer to its own ring, or to a ring further in, never outward. Among the eight classes of the onion, violations: none.

## 6. Checking The Rule

Third, checking the rule. The checker is pointed at the naive order. It reports: the naive order, in ring zero, refers to the SQL database, in ring three. The checker reads the fields, constructors and methods of each class, so the rule is tested, not just hoped for.

## 7. Swap The Outside

Fourth, swap the outside. Stored in memory, the total is ten thousand eight hundred. Stored as a text record, the same. The record is the order id, the mug, two at sixty pounds, and a discount of twelve hundred. The use case, the rules and the order were not touched.

## 8. The Inside, On Its Own

Fifth, the inside, on its own. A small order is nine fifty. A big order is ten thousand eight hundred, ten percent off twelve thousand. No storage, no screen, and no framework was used to check the rules. Through the outside, the same order gives the same total.

## 9. The Bill

Last, the bill. One order saved and read back through the outer ring costs two conversions. Every trip across a ring may copy the order into another shape. To place one order there are four classes in three rings, plus the repository idea. For a small program, that is a lot of ceremony. And the repository idea lives in the centre, so the centre knows that storage exists, though not how.

## 10. How To Recognise It

How do you recognise this in code you did not write? Packages named domain, application and infrastructure. An interface in the domain package, implemented in the infrastructure package. Entities with no framework annotations, and a use-case class that receives its repository. An ArchUnit test that fails when domain code imports infrastructure.

## 11. The Verdict

Here is my verdict, plainly. Put the business rules at the centre, and let everything else depend on them. Let the centre own the ideas it needs, such as a repository, and let the outside supply them. Check the rule with a test, not a diagram. Do not use it for a program too small to have an outside worth swapping.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For a small tool with one fixed storage and few rules, rings are heavier than the problem. They pay off when rules are rich and the outside changes.

## 14. Thanks for Watching

That's Onion Architecture. If you take one sentence away, take this one: onion architecture puts the rules at the centre and points every dependency inward, and the price is the copying and the classes that the rings need. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a third storage that keeps orders in a sorted list, and confirm the checker still finds no violations. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
