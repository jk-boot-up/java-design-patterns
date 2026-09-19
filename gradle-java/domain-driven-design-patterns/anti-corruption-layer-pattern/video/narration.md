# Anti-Corruption Layer Pattern — Video Narration Script

## 1. Anti-Corruption Layer

Hello, and welcome. This video explains the Anti-Corruption Layer pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: an anti-corruption layer is a translator that sits between your own model and another system's model, so that the other system's ideas, names and codes never leak into yours. This is the fifth project in the domain-driven design category, whose subject is writing code that says what the business says. In our online store, the thing we have to talk to is an old inventory system that nobody is allowed to change. By the end you will see the old system's codes spread through four features, see one layer translate them once, see bad data stopped at the door, and see the cost of the layer, which is the bill.

## 2. The Scenario

Here is the scenario. The online store gets its stock levels from an old inventory system. It sends every value as a string. It uses one letter codes. It cannot be changed, and its owners add new codes now and then without telling anyone. The question: how should the shop use it?

## 3. Their Model, Everywhere

First, their model, everywhere. The old system sends strings. A quantity of zero zero one two. A flag of Y. A status of A. Four features in the shop read that record directly, so four places have each learnt what those codes mean. It works, today.

## 4. The Pattern

The pattern. A layer between the shop and the old system. It is the only class that knows the old codes. It translates them into the shop's own model. And it refuses anything it cannot translate, so bad data stops at the door.

## 5. Their Model, Translated Once

Second, translated once. Each old record becomes a stock level, with a real number and a meaning. The blue mug: twelve, in stock. The old mug: none, discontinued. The tea: two hundred and forty, in stock. No code has crossed the layer.

## 6. Bad Data Stops At The Door

Third, bad data. The old system sends a quantity of twelve X. The shortcut fails deep inside a report, with a number format exception, and no mention of which item. The layer refuses it at the door, and says: legacy data for the blue mug, quantity twelve X is not a number.

## 7. The Other Side Changes

Fourth, the other side changes. The old system starts sending H, for a product on hold, and tells nobody. The four features each guess. The page says in stock. The basket lets a customer buy it. With the layer, there is one decision, in one place: on hold, and it cannot be bought.

## 8. What The Layer Costs

Fifth, the cost. The old row has seven fields, and the shop uses four. The layer drops three: the last count date, the warehouse and the unit. The day a feature needs one of them, the layer has to be extended, and the shop's model with it. That is the price of keeping the model clean.

## 9. What The Layer Protects

Last, what the layer protects. The shop has four availability words of its own: in stock, out of stock, discontinued, and on hold. The old system's words stay behind the layer. Replace the old system, and you write one new adapter. Nothing else changes.

## 10. How To Recognise It

How do you recognise this in code you did not write? An interface in your domain and an adapter class that implements it against another system. Mapping code between two sets of types with different names for the same idea. A package for the other system's types that nothing but one class imports. Names like LegacyXAdapter, Translator or Facade around an old service.

## 11. The Verdict

Here is my verdict, plainly. Use an anti-corruption layer when your model must stay clean against a system you do not control: legacy, third-party, or a very different one. Put every translation in one adapter, refuse what cannot be translated, and list what you drop. Do not build one for a system whose model already matches yours.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? When the other system's model already matches yours, or when it is small and stable, a direct call is simpler. The layer earns its place against a model that is foreign, large or changing.

## 14. Thanks for Watching

That's Anti-Corruption Layer. If you take one sentence away, take this one: an anti-corruption layer keeps someone else's ideas out of yours, at the price of a translator you must maintain. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a new status to the old system, and decide what the layer should make of it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
