# The Decorator Pattern Pattern — Video Narration Script

## 1. The Decorator Pattern

Hello, and welcome. This video explains the Decorator pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Decorator pattern adds behaviour to an object by wrapping it in another object with the same shape. Each wrapper does its own small job, and then passes the call along. So features can be combined while the program runs, in any order, without a class for every combination. Think of dressing for the weather, one layer at a time. In our online store, checkout pricing has optional extras, like gift wrapping and insurance. By the end, you will know how to make any combination of optional features work together, with one small class per feature.

## 2. The Scenario

Here is the scenario. A product has a base price. But customers can add optional extras. Gift wrapping, shipping insurance, and express handling. Any combination should be possible. Gift wrap alone, insurance alone, all three together, or none.

## 3. One Class Per Combination

The obvious first move is a class for each combination. Two optional features already need three classes. One for gift wrap, one for insurance, and one for both. Add a third feature, express handling, and you need four more classes to cover every combination.

## 4. The Naive Approach — One Class Per Combination

Here is the naive approach. One class handles a gift-wrapped, insured product. It adds a fixed gift-wrap fee. Then it works out an insurance charge on top. And here is the problem. The gift-wrap fee, and the insurance calculation, are both copied from the single-feature classes. Copied and pasted, not shared.

## 5. Why That Hurts

That does real damage as the system grows. The number of classes explodes. Four optional features would need fifteen classes, just to cover every mix. And every fee calculation is copied into every class that needs it. Fix a pricing bug, like changing the insurance rate, and you must find every copy. None of this is a bug. Each naive class gives the correct price. The waste is in the structure.

## 6. The Decorator Pattern

The Decorator pattern fixes exactly this. The classic book on design patterns, by the authors known as the Gang of Four, describes it like this. Attach extra responsibilities to an object while the program runs. A flexible alternative to creating subclasses. In plain words: wrap it, do not subclass it.

## 7. Remember It With Dressing for Weather

Here is how to remember it. Think about dressing for the weather. Put a jumper over your shirt. Then a raincoat over the jumper. Each layer adds its own effect: first warmth, then keeping dry. The shirt does not need to know the raincoat exists. And the raincoat does not care what is underneath. You can wear any mix of layers, in any order. Without owning a separate garment for every combination.

## 8. The Four Roles

Every decorator has four roles. The component: the shared interface that plain and decorated products both follow. Here, it is called priced item. The concrete component: a plain product, with no extras. The abstract decorator: it follows the same interface, and holds another priced item inside it. And the concrete decorators: gift wrap, insurance, and express handling. Each adds exactly one charge. Here is the most important idea in this video. Every decorator has exactly the same shape as the thing it wraps. So decorators can be nested as deep as you like. And the caller never needs to know how many layers there are.

## 9. The Component — The Shared Shape

Here is the component, the priced item interface. It is shared by plain products and decorated ones. It has just two questions: what is your cost, and what is your description? And here is the concrete component: a plain product. A name and a price, with no extras at all.

## 10. A Concrete Decorator — Delegate, Then Add

Here is one concrete decorator: insurance. It holds a wrapped priced item inside it. When asked for its cost, it first asks the wrapped item for its cost. Then it adds a two percent insurance charge on top. It has no idea whether the wrapped item is a plain product, or another decorator.

## 11. Stacking Order Changes the Result

Here is a detail worth pausing on. Insurance charges a percentage of whatever it wraps. So the order of wrapping changes the total. Gift wrap first, then insure: eighty-five dollars sixteen. Because the insurance also covers the gift-wrap fee. Insure first, then gift wrap: eighty-five dollars nine. Because the fixed fee is added after the insurance is worked out. Both are fair prices, for two different policies. The Decorator pattern makes that choice clear and visible. Instead of burying it inside one combination class.

## 12. Running It

Let's run the project. Wireless headphones cost seventy-nine dollars ninety-nine. With gift wrap, eighty-three forty-nine. Then insured, eighty-five sixteen. Then with express handling, ninety-five fifteen. Swap the gift-wrap and insurance order, and the total becomes eighty-five dollars nine. Exactly the difference we just described. And the naive combination class gives the same number as the matching stack of decorators. It is not wrong. It is just one more class than the pattern needs.

## 13. Wrap Up

So, to recap. Use a decorator when optional, combinable features would otherwise need a class for every combination. Keep every decorator's shape identical to the thing it wraps. The moment a decorator adds a new method, callers can no longer treat it like the plain item. And one comparison worth knowing. A decorator keeps the same shape, so wrapped and unwrapped items can be swapped. The Adapter pattern deliberately changes the shape, to fit two things that disagree.

## 14. Thanks for Watching

That's the Decorator pattern. If you remember one sentence, make it this one. Wrap an object in layers with the same shape, one feature per layer, instead of writing a class for every combination. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a fourth extra, like a gift message. And notice you only need one new class. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
