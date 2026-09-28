# Onion Architecture Pattern — Video Narration Script

## 1. Onion Architecture

Hello, and welcome. This video explains the Onion Architecture pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Onion Architecture arranges code in rings, like the layers of an onion. The business rules sit at the centre. And every ring may depend only on rings further in, never on rings further out. Think of a tree. The trunk does not depend on the leaves. The leaves depend on the trunk. You can lose every leaf in autumn, and the tree is still the same tree. In our online store, the order class saves itself to a database. So you cannot change the storage without editing the order. In this video, we arrange the code in rings, and write the rule as a check. We will swap the storage without touching the centre, test the rules with no storage at all, and then look at the cost.

## 2. The Scenario

Here is the scenario. An order is placed, priced, and saved. The pricing rule gives ten percent off any order of one hundred pounds or more. And the storage may change over time. First memory, then a file, then a database. So here is the question. What should sit at the centre?

## 3. The Core Reaches Outward

First, the old way: the core reaches outward. The order class saves itself, by writing a database command. So to change the storage, you must edit the order class. And the order class sits right at the centre of the program.

## 4. The Pattern

Now, the pattern. Arrange the code in rings, with the business rules at the centre. Storage and screens go on the outside. And one rule. A class may refer to its own ring, or to a ring further in. Never to a ring further out.

## 5. Rings, And One Rule

Second demo: the rings, and the one rule. Ring zero, at the centre, holds the order, its lines, and the idea of a repository, a place to keep orders. Ring one holds the pricing rules. Ring two holds the use cases, like placing an order. Ring three, on the outside, holds storage and screens. The onion has eight classes. How many break the rule? None.

## 6. Checking The Rule

Third demo: checking the rule. A checker is pointed at the old, naive order class. It reports a problem. The naive order, in ring zero, refers to the database, in ring three. The checker reads every field, constructor and method of each class. So the rule is tested, not just hoped for.

## 7. Swap The Outside

Fourth demo: swap the outside. First, orders are stored in memory. The total is one hundred and eight pounds. Then, orders are stored as a line of text instead. The total is the same, one hundred and eight pounds. The text line holds the order I D, two mugs at sixty pounds, and a discount of twelve pounds. And the use case, the rules, and the order were not touched at all.

## 8. The Inside, On Its Own

Fifth demo: the inside, all on its own. A small order costs nine pounds fifty, with no discount. A big order of one hundred and twenty pounds gets ten percent off, and costs one hundred and eight pounds. No storage, no screen, and no framework was needed to check these rules. And when the same order goes through the outer rings, it gives exactly the same total.

## 9. The Bill

Finally, the cost. Saving one order, and reading it back, needed two conversions. Each time data crosses a ring, it may be copied into a different shape. To place one order, we used four classes in three rings, plus the repository idea. For a small program, that is a lot of ceremony. And one more thing. The repository idea lives at the centre. So the centre knows that storage exists, even though it does not know how it works.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for packages named domain, application, and infrastructure. Look for an interface in the domain package, implemented in the infrastructure package. Look for business classes with no framework annotations, and a use case that is handed its repository. And look for an ArchUnit test that fails when domain code imports infrastructure.

## 11. The Verdict

So, here is the verdict. Put the business rules at the centre, and let everything else depend on them. Let the centre own the ideas it needs, such as a repository. And let the outside provide them. Check the rule with a test, not a diagram. And do not use it for a program too small to have an outside worth swapping.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For a small tool with one fixed kind of storage, and only a few rules, rings are heavier than the problem. They pay off when the rules are rich, and the outside keeps changing.

## 14. Thanks for Watching

That's Onion Architecture. If you remember one sentence, make it this one. Onion Architecture puts the rules at the centre, and points every dependency inward, and the price is the copying and the extra classes the rings need. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a third kind of storage, which keeps orders in a sorted list. Then check that the checker still finds no violations. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
