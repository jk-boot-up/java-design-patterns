# Decorator Pattern — Video Narration Script

## 1. The Decorator Pattern

Hello, and welcome. This video explains the Decorator pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. The decorator pattern adds behaviour to an object by wrapping it in another object with the same interface. Each wrapper does its own small piece of work and then passes the call along, so features can be combined at runtime, in any order, without writing a class for every combination. That's the idea in a sentence. The rest of the video does it properly, by building a real working Java project: checkout pricing in an online store, with stackable extras like gift wrapping and insurance. By the end you'll know how to make any combination of optional features work together, in any order, with one small class per feature.

## 2. The Scenario

So, imagine checkout pricing for an online store. A product has a base price, but customers can add optional extras: gift wrapping, shipment insurance, and express handling. And any combination of these should be selectable — gift wrap alone, insurance alone, all three together, or none at all.

## 3. One Class Per Combination

The obvious first move is a class for each combination you need today. Two optional features already need up to three classes — one for gift wrap, one for insurance, one for both together. Add a third feature, express handling, and covering every combination needs four more classes on top of that.

## 4. The Naive Approach — One Class Per Combination

So here's the naive approach. NaiveGiftWrappedInsuredProduct adds a flat gift-wrap fee, then computes an insurance premium on top of that. And here's the problem. Both the gift-wrap fee and the insurance premium calculation are already duplicated from the single-feature classes elsewhere in the codebase — copy-pasted, not shared.

## 5. Why That Hurts

And that does real damage as the system grows. The number of classes grows combinatorially — four optional features would need fifteen classes just to cover every subset. Every fee calculation is copy-pasted into every class that needs that feature. Fix a pricing bug, like changing the insurance rate, and you have to hunt down every copy individually. None of this is a bug — each naive class computes a correct price. The waste is structural: combinable behavior modeled as a fixed set of subclasses.

## 6. The Decorator Pattern

The decorator pattern fixes exactly this. In Gang of Four terms, decorator attaches additional responsibilities to an object dynamically, providing a flexible alternative to subclassing for extending functionality. In plain language? Wrap it, don't subclass it.

## 7. Remember It With Dressing for Weather

Here's how to remember it forever. Think about dressing for weather. A base shirt can have a sweater put on over it, and a raincoat put on over the sweater. Each layer adds its own effect — warmth, then water resistance. The shirt never needs to know a raincoat exists, and the raincoat never needs to know what's underneath it. You can wear any subset of layers, in any order, without owning a distinct garment for every combination.

## 8. The Four Roles

Every decorator setup has four roles. The component, PricedItem, the interface both plain and decorated products share. The concrete component, Product, a plain item with no extras. The abstract decorator, ProductDecorator, which implements the component and holds another component by composition. And the concrete decorators — GiftWrapDecorator, InsuranceDecorator, ExpressHandlingDecorator — each adding exactly one fee. Here's the single most important idea in this whole video. Every decorator exposes exactly the same interface as the thing it wraps, so decorators nest arbitrarily deep, and the client never has to know how many layers it's calling into.

## 9. The Component — The Shared Shape

This is the component, PricedItem. It's the shared interface both plain products and decorated products implement — just cost, and description. And this is the concrete component, Product. A plain item with a name and a price, no extras, no decorators involved at all.

## 10. A Concrete Decorator — Delegate, Then Add

And this is a concrete decorator, InsuranceDecorator. It extends ProductDecorator, which holds a wrapped PricedItem by composition. cost calls wrapped-dot-cost first, then adds a two percent premium on top of whatever comes back. It has no idea whether wrapped is a plain Product or another decorator underneath it.

## 11. Stacking Order Changes the Result

Here's the subtlety worth pausing on. Because InsuranceDecorator prices a percentage of whatever it wraps, wrapping order changes the total. Gift-wrap then insure comes to eighty five dollars and sixteen cents, because the premium includes the gift-wrap fee. Insure then gift-wrap comes to eighty five dollars and nine cents, because the flat fee is added after insurance is already computed. Both are legitimate prices for different policies — decorator makes that an explicit, visible choice, not a decision buried in one combination class.

## 12. Running It

When we run the project, each decorator stacks cleanly on top of the last, one feature at a time, up to ninety five dollars and fifteen cents with all three extras. Reverse the gift-wrap and insurance order and the total shifts to eighty five dollars and nine cents — exactly the difference we just walked through. And down at the bottom, the naive combination class produces the exact same number as the matching decorator stack — it isn't wrong, it's just one more class than the pattern ever needed.

## 13. Wrap Up

So, to recap. Use decorator when optional, combinable behavior would otherwise mean one class per combination. Keep every decorator's interface identical to the component it wraps — the moment a decorator adds a new method, callers can no longer treat it interchangeably with the plain component. And if you remember one sentence from today, make it this one. Decorator keeps the same interface in and out so wrapped and unwrapped objects stay interchangeable. Adapter deliberately changes the interface to reconcile two shapes that disagree.

## 14. Thanks for Watching

And that's the decorator pattern. If you got something out of this, do give it a thumbs up, and subscribe. It genuinely helps the channel, and it's what makes more of these possible. And if there's a pattern you'd like me to cover next, drop it in the comments. I read every one. All the source code, the written notes and an interactive animation are in the repository. Thanks for watching, and I'll see you in the next one.
