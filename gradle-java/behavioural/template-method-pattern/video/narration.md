# The Template Method Pattern Pattern — Video Narration Script

## 1. The Template Method Pattern

Hello, and welcome. This video explains the Template Method pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Template Method pattern writes down an order of steps once, in a base class. That method is locked, so subclasses cannot change it. Subclasses only fill in what each step does. So the sequence is written once, and can never be rearranged. Only the steps vary. Think of a cake recipe. You choose the flavour and the tin. But you always mix, then bake, then ice. In this video, an online shop fulfils orders in three very different ways. By the end, you will know what the word final really buys you. How to choose between a required step, a default, and a hook. And the one serious price this pattern charges.

## 2. The Scenario

Here is the scenario. Every order the shop fulfils goes through the same six steps. Validate, reserve the stock, charge the customer, pack, dispatch, and notify the customer. That order is not a matter of taste. Charge before you reserve, and you may take money for goods you cannot supply. Notify before you dispatch, and you email a tracking number that does not exist yet. But what happens inside each step varies enormously. The shop fulfils from its own warehouse, from marketplace sellers, and as digital downloads. Holding stock in a warehouse, asking a seller to confirm, and creating a licence key have nothing in common. Except where they sit in that list of six.

## 3. The Obvious First Move

The obvious first approach is to write each route out in full. Three methods, one per route, each doing all six steps from start to finish. To be fair, this is good code. Each method reads top to bottom, with nothing hidden. There is no new vocabulary to learn. And on the day each was written, it was almost certainly correct. Three copies of a six-step sequence is not a crisis by itself. What happens to those copies over the next year is.

## 4. The Naive Approach — Two Lines the Wrong Way Round

Here is the day it goes wrong. Someone moved one line, in one copy. The digital route now notifies the customer before it dispatches. Let's follow it. The email quotes the licence key. But dispatch has not run yet, so there is no key. The customer receives a message that says: ready to download, key: not dispatched. A moment later, the real key is created, and it is correct. But nobody will ever tell the customer what it is. Nothing crashed, nothing failed to compile, and no test failed. The order was marked as fulfilled. The marketplace copy drifted too, in a different place. The charge moved above the seller's confirmation. So a customer can be charged forty-two pounds, and then told the seller cannot supply it.

## 5. Why That Hurts

So why does this hurt? Most people would say, duplication. That is true, but it is the weaker argument. Here is the stronger one. What is duplicated that the compiler cannot see? The order of the steps. It exists only as a habit, typed out by hand in three places. Nothing in the code knows it is a sequence. So it drifts, one line at a time, in whichever copy someone last edited in a hurry. And when the shop adds a seventh step, like a fraud check, someone must find all three copies. And insert the step in the same place in each. A copy that misses it is not an error. It is just a route that silently skips the check.

## 6. The Template Method Pattern

Here is the pattern's definition, from the famous Gang of Four book. Define the skeleton of an algorithm in one method, and leave some steps to subclasses. Subclasses can change certain steps, without changing the algorithm's structure. In plain words: the subclass decides how each step works. It never decides when the steps run. And that last part is not a polite request. The base class enforces it. In Java, it is enforced by one keyword.

## 7. Everyday Analogy: The Recipe

Here is an everyday example: a cake recipe. Which parts can you change? The flavouring, yes. Lemon, chocolate, whatever you have. The tin, yes. The icing is optional. Plenty of good cakes have none. But mix, then bake, then ice, is not up for debate. Ice it before you bake it, and you do not get a different style of cake. You get no cake, and no icing. That is the whole pattern. The ingredients are the steps you fill in. The icing is an optional hook. And the order is fixed by the person who wrote the recipe, on purpose.

## 8. The Roles

So here are the roles. At the top is the abstract class, called Fulfilment Process. Inside it is the template method itself, called fulfil, marked final. It is the only thing in the system that knows the six steps have an order. Below it are the three routes: warehouse, marketplace, and digital. The warehouse route overrides four methods. The marketplace route overrides six. The digital route overrides seven. The most ordinary route is the shortest. That tells you the base class's defaults were well chosen. And every step writes to a shared report. So the project can prove its claim. Run all three routes, list the steps each one performed, and the three lists are identical.

## 9. The Template Method — Seven Lines and One Keyword

Here is the whole pattern, in one method. Seven calls, in order, in the fulfil method. Every route in the system runs exactly this method. The key word is final. A route may decide how any step behaves. It cannot decide when the steps run. That is not a rule someone must remember in code review. Breaking it is a compile error. Each step is also a deliberate kind of gap. Validate is private, so nobody can replace it. Three steps are abstract, so every route must fill them in. Two steps have defaults, so a route that wants the usual behaviour writes nothing. And the last step does nothing at all, on purpose. We will come back to that one.

## 10. Three Kinds of Hole

So, there are three kinds of gap, and choosing between them is most of the work. Abstract means: you must fill this in. Use it when no default could be right for everyone. Reserving stock in a warehouse and asking a seller to confirm have nothing in common to share. A default means: you may replace this. Packing is usually the same, box it and label it. So the warehouse route says nothing about packing, and gets the right behaviour for free. And then hooks, which come in two kinds. One kind is a question, such as: does this route need a shipping address? The digital route answers no, without weakening the address check for anyone else. The other kind is a place to join in. A step called after fulfilment does nothing by default, but runs every time. So the marketplace route can record its commission there, without the base class ever knowing marketplaces exist. But be careful with hooks. Each one is a permission you give away for the life of the class.

## 11. Why the Order Being Fixed Is Worth Something

Now here is the payoff. In the digital route, dispatch creates the licence key, and writes it on the report. Then notify reads the key from the report, and puts it in the email. These are the same two actions as in the naive version. Here they are correct, and not because the author was careful. Notify can rely on dispatch having already run. Because fulfil is final. So no route, today or next year, can ever swap those two steps. That is what the keyword buys. A step can safely depend on an earlier step's work, forever.

## 12. The Test That Proves It

Here is the test that proves the claim. It uses a recording route. Each of its steps does nothing, except write down its own name. Run it, and you can check the order of the steps directly. Could you write this test for the naive version? Only for the three routes that exist today. It could say nothing about a fourth route added next year, and that is exactly where drift comes from. Here, the guarantee is built into the structure. The test simply confirms it. There are forty-six tests in total. Some of them deliberately confirm the naive version's two bugs, so you can hear exactly what goes wrong.

## 13. Running It

Let's run the demo. First, the hand-written version. An email about a licence key is sent before the key even exists. Second, the same three routes, running through the template. The demo lists the steps each route performed. Three completely different implementations, and three identical lists. Not because the routes agreed. None of them knows what the others do. Because only the fulfil method decides the order. Finally, a fourth route is added: click and collect. One new class. No change to the base class, or to any existing route. And it gets the same six steps, in the same order, for free.

## 14. What to Remember

So, what should you remember? One final method owns the order, and subclasses fill in the steps. Abstract means must fill in. A default means may replace. A hook means may join in. A step can rely on an earlier step, because the order cannot change. And a new route is one new class, with nothing that works reopened. Now the honest cost. Each route uses up its one chance to extend a class. Every route extends this base class, and can never extend anything else. That is why composing objects is usually the better modern default. Also, the sequence is shared by everyone. Add a seventh step, and every route changes at once, including ones you cannot see. Finally, two related patterns. Factory Method is this same idea, narrowed to a single gap that creates an object. And Strategy uses composition instead of inheritance. It costs nothing, but it guarantees nothing about order. You have met Template Method already, in Java's Abstract List, in servlets, in JUnit's before-each methods, and in every Spring class with Template in its name.

## 15. Thanks for Watching

That's the Template Method pattern. If you remember one sentence, make it this one. Let one final method own the order of the steps, and let subclasses fill in only the steps themselves. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a fraud check between validate and reserve. Add it first to the template, and then to the three hand-written copies. And count how many edits each one takes. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
