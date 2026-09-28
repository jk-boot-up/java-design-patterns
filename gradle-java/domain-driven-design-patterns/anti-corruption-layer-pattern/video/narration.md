# Anti-Corruption Layer Pattern — Video Narration Script

## 1. Anti-Corruption Layer

Hello, and welcome. This video explains the Anti-Corruption Layer pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An anti-corruption layer is a translator. It sits between your own model, and another system's model. So the other system's ideas, names, and codes never leak into yours. Think of an interpreter at a business meeting. Each side speaks its own language. The interpreter makes sure neither side has to learn the other's. In our online store, we must talk to an old inventory system that nobody is allowed to change. In this video, the old system's codes spread through four features. Then one layer translates them, once. We will hear bad data stopped at the door, and the cost of keeping the layer.

## 2. The Scenario

Here is the scenario. The online store gets its stock levels from an old inventory system. It sends every value as text. It uses one-letter codes. It cannot be changed. And its owners sometimes add new codes, without telling anyone. So here is the question. How should the shop use it?

## 3. Their Model, Everywhere

First, the naive way: their model, everywhere. The old system sends text. A quantity written as zero zero one two. A stock flag of Y. And a status code of A. Four features in the shop read that record directly. So four places have each learned what those codes mean. It works, for today.

## 4. The Pattern

Now, the pattern. Put a layer between the shop and the old system. It is the only class that knows the old codes. It translates them into the shop's own model. And it refuses anything it cannot translate. So bad data stops at the door.

## 5. Their Model, Translated Once

Second demo: translated, once. Each old record becomes a stock level, with a real number, and a clear meaning. The blue mug: twelve, in stock. The old mug: none, discontinued. The tea: two hundred and forty, in stock. Not a single old code crossed the layer.

## 6. Bad Data Stops At The Door

Third demo: bad data stops at the door. The old system sends a quantity of twelve X. Without the layer, the error happens deep inside a report. It says only that a number could not be read, and does not say which item. With the layer, the record is refused at the door. And the message says: legacy data for the blue mug, quantity twelve X is not a number.

## 7. The Other Side Changes

Fourth demo: the other side changes. The old system starts sending a new status code, H, meaning on hold. And it tells nobody. Without the layer, the four features each guess. The product page says, in stock. And the basket lets a customer buy it. With the layer, there is one decision, in one place. On hold, and it cannot be bought.

## 8. What The Layer Costs

Fifth demo: what the layer costs. Each old record has seven fields. The shop uses four. The layer drops three: the last stock count date, the warehouse, and the unit. The day a feature needs one of those, the layer must be extended. And the shop's model with it. That is the price of keeping your model clean.

## 9. What The Layer Protects

Last demo: what the layer protects. The shop has four availability words of its own. In stock, out of stock, discontinued, and on hold. The old system's codes stay behind the layer. So if the old system is ever replaced, you write one new adapter. Nothing else in the shop changes.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for an interface in your own domain, with an adapter class that implements it, by calling another system. Look for mapping code between two sets of types, with different names for the same idea. Look for a package of the other system's types, used by only one class. And look for names like legacy adapter, translator, or facade, around an old service.

## 11. The Verdict

So, here is the verdict. Use an anti-corruption layer when your model must stay clean, next to a system you do not control. An old system, a third party's system, or one with a very different model. Put every translation in one adapter. Refuse anything that cannot be translated. And write down what you drop. Do not build one for a system whose model already matches yours.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every result you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? When the other system's model already matches yours, or when it is small and never changes, a direct call is simpler. The layer earns its place against a model that is foreign, large, or changing.

## 14. Thanks for Watching

That's the Anti-Corruption Layer. If you remember one sentence, make it this one. An anti-corruption layer keeps someone else's ideas out of your model, at the price of a translator you must maintain. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a new status code to the old system. Then decide what the layer should make of it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
