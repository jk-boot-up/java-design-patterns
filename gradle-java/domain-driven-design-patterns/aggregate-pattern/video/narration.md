# Aggregate Pattern — Video Narration Script

## 1. Aggregate

Hello, and welcome. This video explains the Aggregate pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: an aggregate is a small cluster of objects that is treated as one unit. It has one root, which is the only way in, so the rules that span the cluster cannot be broken from outside. This is the second project in the domain-driven design category, whose subject is writing code that says what the business says. In our online store, the cluster is an order and its lines. By the end you will see an order break every one of its own rules when anyone can reach inside it, then see one root guard them all, why it refers to other aggregates only by id, how it is saved whole, and how drawing it too big goes wrong.

## 2. The Scenario

Here is the scenario. In the online store, an order has lines. And there are rules that span the lines. A line holds between one and ten of an item. An item appears on one line only. The total may not pass a thousand pounds. And a placed order cannot change. The question: who enforces them?

## 3. A Loose Order

First, a loose order. It is a list with public fields. A line of minus three mugs goes in. The same machine goes on two lines. The total comes to nearly six thousand pounds, far over the limit. And a line is added after the order was placed. Every rule is true only in the head of whoever wrote the caller.

## 4. The Pattern

The pattern. One root, the order. Its lines cannot be reached, or even built, except through it. Every rule that spans the lines lives in the root, so there is exactly one place to look. And it refers to other aggregates, like the customer, by id only.

## 5. The Root Guards The Rules

Second, the same operations through the root. Nought mugs is refused. Eleven mugs is refused. Six mugs are fine, but five more of the same would make eleven, and that is refused too. A total over a thousand pounds is refused. A change after placing is refused, and an empty order cannot be placed. Six rules, each enforced, all in one class.

## 6. There Is Only One Door

Third, one door. The list of lines, seen from outside, is read only. Trying to clear it throws. And an order line has no public constructor, so no line can exist that the order has not checked.

## 7. Other Aggregates By Id

Fourth, other aggregates by id. Three orders that hold the whole customer object load the customer three times. Three that hold only a customer id load none. The customer is a different aggregate, with its own rules and its own saves. An order should know who, not carry them.

## 8. Saved Whole, Or Not At All

Fifth, saved whole. Two clerks read the same order, and each add a line. Clerk A saves, and it is accepted. Clerk B saves, and is refused, because the order changed since it was read. The order is read whole, changed whole and saved whole. So an order with half of one clerk's change cannot exist.

## 9. An Aggregate Drawn Too Big

Last, the bill. Suppose the aggregate is the customer and all their orders. Two clerks change two different orders. The second save is refused, because both changed the customer. That is a false conflict. With one aggregate per order, both saves go through. The boundary is a choice, and drawing it too wide costs you real contention.

## 10. How To Recognise It

How do you recognise this in code you did not write? A class with private collections and methods that add to them. A read only view returned instead of the list itself. A repository that saves the order, and never a line. And other aggregates held by id.

## 11. The Verdict

Here is my verdict, plainly. Draw the aggregate around what must be consistent together, and no wider. Make one class the root, and the only way in. Keep the rules in it. Refer to other aggregates by id. And save and load the whole thing.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. The stores are in memory, and the version check is a real check. The two clerks are two loads, one after the other, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For a plain record with no rules across its parts, a single class is enough. An aggregate earns its place when rules span several objects.

## 14. Thanks for Watching

That's Aggregate. If you take one sentence away, take this one: an aggregate is where a rule lives, and where a save begins and ends. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a rule that an order can hold at most five different items, and see which class changes. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
