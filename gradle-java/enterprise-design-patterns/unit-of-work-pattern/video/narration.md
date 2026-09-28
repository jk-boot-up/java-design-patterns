# Unit of Work Pattern — Video Narration Script

## 1. Unit of Work

Hello, and welcome. This video explains the Unit of Work pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A unit of work keeps a list of everything that changed. What is new, what was changed, and what was removed. Then it writes it all together at the end, in one step, or not at all. Think of an online shopping basket. You add and remove items freely. Nothing is charged until you press pay, and then it all happens at once. In our online store, the question is: what happens when placing an order writes seven things, and the seventh fails? By the end, you will know what half an order looks like. What a transaction fixes, and what it still costs. And how a unit of work does better.

## 2. The Scenario

Here is the scenario. Placing an order writes one order row, three order line rows, and three stock updates. Seven writes in total. And the third stock update, for the monitor, fails. So here is the question. What is left behind in the database?

## 3. Each Object Saves Itself

First, the naive way: each object saves itself as it changes. The order is written. Then the keyboard's stock, and its line. Then the mouse's stock, and its line. Then the monitor's stock update is rejected. What is left? One order, with only two of its three lines. Keyboard stock down by two, mouse stock down by one, and the monitor untouched. Nothing knows it is broken. And nothing can undo it, because the writes have already happened.

## 4. Wrap It In A Transaction

The second approach is the one experienced developers reach for: wrap it all in a transaction. And it mostly works. The failure rolls everything back. No orders, no lines, and all three stock levels back to ten. The cost is time. The transaction, and its locks, stay open for the whole calculation. Including a slow check made for every line. Here, that is twenty-two ticks of time. And other customers wait on those locks.

## 5. The Pattern

Now, the pattern. It keeps a list. As the objects change, each change is registered: new, changed, or removed. Nothing touches the database yet. The slow checks happen now, with no locks held. Only at the end, called commit, does it write everything, in one short transaction.

## 6. Nothing Until Commit

Third demo: nothing is written until commit. After changing every object, there have been zero database operations. Seven changes are registered, and waiting. Then commit writes them. The order first, then its lines, then the stock updates. The database was locked for seven ticks, not twenty-two. Because the slow work was already done.

## 7. All Of It, Or None

Fourth demo: all of it, or none. The same failure again. The monitor's stock update is rejected, during commit. The transaction rolls back. And the database is exactly as it was before. No orders, no lines, and all stock levels at ten. All of the order, or none of it. The customer never saw half an order.

## 8. Cost One: Order Of Writes

Now the costs. The first: the order of writes matters. Written in the order they were registered, the lines came before their order. And the database refused, because a line pointed at an order that did not exist yet. So the unit of work must know that parents come before children. And it must sort its changes before writing them.

## 9. Cost Two: Knowing What Changed

The second cost: knowing what changed. There are two ways. Check every field of every object, which is slow. Or be told, which puts the burden on the calling code. This project is told. The caller says, register dirty, meaning, this object changed. Forget to say it, and the change is never written.

## 10. Cost Three: Memory Disagrees

Fifth demo: the third cost, memory and the database disagree. Until commit, memory says the keyboard has eight in stock. The database still says ten. The whole list of changes lives in memory. So a huge bulk update is a memory problem too. And anything reading the database in the meantime sees the old picture.

## 11. The Toy Database

A word about the database in these demos. It is a toy. Rows, an operation counter, and a write that can be told to fail, on demand. For this project, it also learned to begin and roll back a transaction. And to check that a line's order really exists. Every count in this video came from its counter.

## 12. Where You Have Met This

You have met this pattern before. In Spring, the at Transactional annotation starts a unit of work. The persistence context tracks what changed. And writes it all when the transaction ends, in an order it works out for you. Writing out those changes is called a flush. If a write ever happened at a moment you did not expect, that was the unit of work choosing when to commit.

## 13. What Is Real Here

A quick, honest note about this demo. The pattern is real. The database is a stand-in, with no real locks, and no other users. The ticks are a model of how long locks are held, not a real measurement. What is real is the shape. Slow work outside the transaction, and writes inside a short one.

## 14. When This Is Too Much

So, when is this too much? A single write does not need a unit of work. It would just be ceremony. It earns its place when one business action must write several rows together. And when half of them would be worse than none.

## 15. Thanks for Watching

That's the Unit of Work pattern. If you remember one sentence, make it this one. Do the slow work first, then write everything once, or not at all. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add removal to the unit of work. And use it to cancel an order. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
