# Aggregate Pattern — Video Narration Script

## 1. Aggregate

Hello, and welcome. This video explains the Aggregate pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An aggregate is a small group of objects that is treated as one unit. It has one main object, called the root, which is the only way in. So the rules that cover the whole group cannot be broken from outside. Think of a bank teller's window. You cannot reach into the vault yourself. Every deposit and withdrawal goes through the teller, who checks the rules. In our online store, the group is an order, and its lines. In this video, an order breaks all its own rules, when anyone can reach inside it. Then one root guards them all. We will hear why it refers to other groups only by I D, how it is saved as a whole, and how drawing it too big goes wrong.

## 2. The Scenario

Here is the scenario. In our online store, an order has lines. And some rules cover all the lines together. A line holds between one and ten of an item. Each item appears on only one line. The total may not go over one thousand pounds. And once an order is placed, it cannot change. So here is the question. Who enforces these rules?

## 3. A Loose Order

First, a loose order. It is just a list, with public fields. A line of minus three mugs goes in. The same machine goes on two separate lines. The total reaches nearly six thousand pounds, far over the limit. And a line is added after the order was placed. All of it is accepted. Every rule exists only in the head of whoever wrote the calling code.

## 4. The Pattern

Now, the pattern. There is one root: the Order. Its lines cannot be reached, or even created, except through it. Every rule that covers the lines lives in the root. So there is exactly one place to look. And other aggregates, such as the customer, are referred to by I D only.

## 5. The Root Guards The Rules

Second demo: the same actions, through the root. Zero mugs is refused. Eleven mugs is refused. Six mugs is fine. But five more of the same mug would make eleven, so that is refused too. A total over one thousand pounds is refused. A change after placing the order is refused. And an empty order cannot be placed. Six rules, each enforced, all in one class.

## 6. There Is Only One Door

Third demo: there is only one door. From outside, the list of lines is read-only. Trying to clear it throws an error. And an order line has no public constructor. So no line can exist that the order has not checked.

## 7. Other Aggregates By Id

Fourth demo: other aggregates, by I D. Three orders that each hold the whole customer object load the customer three times. Three orders that only hold a customer I D load it no times at all. The customer is a separate aggregate, with its own rules, and its own saves. An order should know who the customer is, not carry the customer around.

## 8. Saved Whole, Or Not At All

Fifth demo: saved whole, or not at all. Two clerks read the same order, and each adds a line. Clerk A saves, and it is accepted. Clerk B saves, and it is refused, because the order changed since B read it. The order is read whole, changed whole, and saved whole. So an order with only half of one clerk's change can never exist.

## 9. An Aggregate Drawn Too Big

Finally, the cost of drawing it too big. Suppose the aggregate is the customer, together with all their orders. Two clerks change two different orders. The second save is refused, because both changed the same customer aggregate. That is a false conflict. With one aggregate per order, both saves go through. The boundary is a choice. And drawing it too wide costs you real conflicts.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a class with private collections, and methods that add to them. Look for a read-only view being returned, instead of the list itself. Look for a repository that saves the whole order, and never a single line. And look for other aggregates held by I D.

## 11. The Verdict

So, here is the verdict. Draw the aggregate around what must stay consistent together, and no wider. Make one class the root, and the only way in. Keep the rules inside it. Refer to other aggregates by I D. And save and load the whole thing, together.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. The storage is in memory, and the version check is a real check. The two clerks load one after the other, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For a simple record with no rules across its parts, a single class is enough. An aggregate earns its place when rules cover several objects together.

## 14. Thanks for Watching

That's the Aggregate pattern. If you remember one sentence, make it this one. An aggregate is where a rule lives, and where a save begins and ends. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a rule that an order can hold at most five different items. Then notice which class had to change. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
