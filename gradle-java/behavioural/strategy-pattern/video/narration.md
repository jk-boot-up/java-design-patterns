# The Strategy Pattern Pattern — Video Narration Script

## 1. The Strategy Pattern

Hello, and welcome. This video explains the Strategy pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Strategy pattern turns each branch of a decision into its own class, behind one shared interface. The code that needs the work done holds a strategy, and calls it. It does not know, or care, which strategy it holds. So a new option is a new class, not a new case in a switch statement. Think of getting across town. You can walk, take the bus, or call a taxi. You choose once, and then just go. In this video, we price delivery at an online checkout, using four different shipping rules. By the end, you will know how to add a fifth rule without editing a single line of code that already works.

## 2. The Scenario

Here is the scenario. At checkout, an online shop must quote a delivery charge. And the rule it uses keeps changing, because it is a business decision. There are four rules. A flat rate, the same on everything. Weight bands: under one kilo, under five, under twenty, and above. Distance: a base fee, plus a charge per hundred miles. And a campaign rule: free delivery on orders over fifty pounds. Marketing switches the campaign on for two weeks, and off again. No single rule is permanent.

## 3. The Obvious First Move

The obvious first approach is simple. A list of shipping methods, and a switch statement inside the checkout code, with one case per rule. To be fair, this works. Every price it produces is correct. For two rules that never change, it is the right answer. So what follows is not a bug report. It is a design complaint.

## 4. The Naive Approach — Four Rules, One Method

Here is the naive version. Four unrelated pricing rules, mixed together in one method. Weight bands, distance rounding, and the campaign threshold have nothing to do with each other. Yet you cannot read one without reading past the other three. Now think about the default branch at the bottom of the switch. It exists because the method must return something. And it does the only safe-looking thing: it charges nothing. Add a fifth shipping method, such as locker collection, and forget this switch. The shop starts delivering for free. No compile error, no crash, just a quietly wrong number on the receipt.

## 5. Why That Hurts

And the damage grows with the system. Four unrelated rules share one method. A fifth rule means editing the method that four working rules depend on. To test one rule, like the price for six and a half kilos, you must build a whole shipment, and go through checkout. The default branch quietly delivers for free. And no test, regional module, or partner can add a rule of its own, without changing the central list first.

## 6. The Strategy Pattern

The Strategy pattern fixes exactly this. Here is its definition, from the famous Gang of Four book. Define a family of algorithms, put each one in its own class, and make them interchangeable. In plain words: pass in the behaviour. Do not branch on a flag.

## 7. Remember It With Getting Across Town

Here is an easy way to remember it: getting across town. You want to get from the office to the station. You could walk, take a bus, cycle, or get a taxi. You do not change. Same person, same start, same destination. What changes is the method, and each method has its own rules. A bus has a timetable, a taxi has a meter, and a bike needs somewhere to lock up. And here is the key point. You decide once, in the morning, based on the weather and how late you are. You do not decide again at every street corner. Choose the approach once, then just use it. That is Strategy.

## 8. The Three Roles

Every Strategy design has three roles. The strategy is the interface for the job. Here, it is called Shipping Cost Rule. The concrete strategies are the four rules: flat rate, weight banded, distance based, and free over a threshold. Each one is one algorithm, and knows nothing about checkout. And the context is the Checkout Service. It holds one rule, and calls it. Here is the most important idea in the video. The checkout cannot behave differently depending on which rule it holds. It has no way to find out which rule that is. If you ever need to check the rule's type inside the checkout, the pattern has not really been applied.

## 9. The Strategy — One Small Interface

The strategy interface has just two methods. Cost For works out the delivery price. And name gives the rule's display name, so the receipt can say which rule priced it. Without name, you would need a separate table of display names, and that table is the old switch, growing back. Notice what Cost For receives: the whole shipment. Destination, weight, distance, and order total. The flat rate rule uses none of those, and that is fine. If Cost For only received a weight, the distance rule could not exist. Passing the whole shipment means a new rule costs exactly one new class.

## 10. A Concrete Strategy — It Knows Only Its Own Arithmetic

Now one real strategy: the weight banded rule. Its price bands are data, a simple list, not code. So changing a price means editing a list, not the algorithm. It goes through the bands from lightest to heaviest, and returns the first price that fits. And notice what is missing. No distance, no campaign threshold, no flat fee, and no checkout. This class knows its own arithmetic, and nothing else. So it can be tested on its own, without ever creating an order.

## 11. The Context — Search It for the Word 'Weight'

Now the context, the Checkout Service. Search it for the words flat, weight, or distance. You find nothing. It holds a rule, and calls it. No if statements. No type checks. No list of methods. Moving the switch into a helper would only relocate the decision. Receiving the rule as a constructor argument removes it. People often ask: where did the decision go? Something still has to turn a setting into a rule object. It moves into a small registry, at the edge of the system. The naive switch ran inside the pricing logic, on every quote. The registry runs once, when the shop is configured. It only answers one question: which rule is in force today? In a real shop, that answer is a database row, or a feature flag.

## 12. The Test That Actually Proves It

Here is a subtle point about testing. A test saying a six and a half kilo parcel costs twelve pounds would pass for the naive design too. It proves the arithmetic, but nothing about the pattern. This test does. It creates a brand new pricing rule, entirely inside the test file. Nothing in the main code knows it exists. It hands the rule to the Checkout Service, and it simply works. If someone ever put the switch back, this is the test that would fail.

## 13. Running It

Let's run the demo. The same parcel, going to Cardiff, is priced by every rule in turn. With weight bands, delivery costs twelve pounds. With the campaign rule, the order is over fifty pounds, so delivery is free, and the total drops to sixty-four pounds. The same checkout object. The same method call. Not one line of the checkout changed between those two quotes. And finally, something the naive version could not do. An unknown rule name is refused outright. It does not fall into a default branch, and deliver for free.

## 14. Wrap Up

So, to recap. Use Strategy when a switch branches on a type or mode, and each branch does real, unrelated work. Keep strategies stateless, so one instance can be shared by every order at once. And never let the context ask what it is holding. The moment it checks the type, the branch is back. One honest warning. Four classes instead of one method is a real cost. For two rules that never change, the switch is the better answer. Strategy pays off when the family of rules keeps growing, as delivery pricing does. And one sentence to remember. Strategy and State have exactly the same shape. The difference is who chooses, and how often. A strategy is chosen from outside, and stays put. A state swaps itself for another, as events happen.

## 15. Thanks for Watching

That's the Strategy pattern. If you remember one sentence, make it this one. Pass in the behaviour, instead of branching on a flag. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. If there is a pattern you would like to see covered, suggest it in the comments. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
