# Strategy Pattern — Video Narration Script

## 1. The Strategy Pattern

Hello, and welcome. This video explains the Strategy pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. The strategy pattern turns each branch of a decision into a class of its own, behind one shared interface. The code that needs the work done holds a strategy and calls it, without knowing or caring which one it is holding — so a new branch is a new class rather than a new case in a switch. That's the idea in a sentence, and it is how you get rid of the big switch statement where every branch does a completely different calculation. The rest of the video does it properly, by building a real working Java project: delivery pricing at an online checkout, with four different shipping rules. By the end you'll know how to add a fifth rule without editing a single line of code that already works.

## 2. The Scenario

So, imagine delivery pricing for an online store. At checkout, the shop has to quote a delivery charge — and the rule it charges by is a business decision that keeps changing. A flat rate, the same on everything. Weight bands: under a kilo, under five, under twenty, and over that. Distance: a base fee plus so much per hundred miles. And a campaign rule — free delivery on orders over fifty pounds. All four are live at some point. Marketing turns the free delivery campaign on for a fortnight and off again. None of them is the rule.

## 3. The Obvious First Move

The obvious first move is an enum for the shipping method and a switch inside the checkout code. One case per rule. And I want to be fair to it: this works. Every price it produces is correct. This is what a competent developer writes first, and for two rules that never change it is the right answer. So what we're about to look at isn't a bug report. It's a design complaint.

## 4. The Naive Approach — Four Rules, One Method

So here's the naive approach. Four unrelated pricing policies, interleaved in one method. The weight bands, the per-hundred-miles rounding, the campaign threshold — none of them have anything to do with each other, and you can't read any one of them without scrolling past the other three. But look hard at that default branch at the bottom. It's there because the compiler demands the method return something, and it does the only safe-looking thing. It charges nothing. Add a fifth constant to that enum — locker collection, say — forget this method exists, and the shop starts shipping for free. No compile error. No exception. Just a quietly wrong number on the receipt.

## 5. Why That Hurts

And that does real damage as the system grows. Four unrelated policies share one method. Adding a fifth rule means opening the one method that four working rules already depend on. There's no way to ask what the weight-banded rule charges for six and a half kilos without constructing a whole shipment and going through checkout — so the arithmetic isn't separately testable. The default branch quietly ships for free. And a test, or a regional module, or a partner integration can't introduce a pricing rule of its own without being added to the enum first.

## 6. The Strategy Pattern

The strategy pattern fixes exactly this. In Gang of Four terms, strategy defines a family of algorithms, encapsulates each one, and makes them interchangeable — so the algorithm can vary independently from the clients that use it. In plain language? Pass in the behaviour. Don't branch on a flag.

## 7. Remember It With Getting Across Town

Here's how to remember it forever. Think about getting across town. You want to get from the office to the station. You can walk, take a bus, cycle, or get a taxi. You don't change — same person, same starting point, same destination. What changes is the method, and each method has its own rules: a bus has a timetable, a taxi has a meter, a bike needs somewhere to lock up. And here's the bit that matters. You decide which one once, in the morning, based on the weather and how late you are. You do not re-decide bus or bike at every street corner. Pick the approach once, then just use it. That's strategy.

## 8. The Three Roles

Every strategy setup has three roles. The strategy itself — here, ShippingCostRule — the one interface describing the job to be done. The concrete strategies: flat rate, weight banded, distance based, free over threshold. One algorithm each, knowing nothing about checkout. And the context, CheckoutService, which holds one rule and calls it. Here's the single most important idea in this whole video. CheckoutService cannot behave differently depending on which rule it's holding, because there is no message it can send to find out which one that is. The day you need an instance-of check in there, the pattern hasn't been applied — it's just been decorated.

## 9. The Strategy — One Small Interface

This is the strategy, ShippingCostRule. Two methods. costFor does the work; name is there so the receipt can say which policy priced it — without that, the client would need a lookup table of display names, and that table is the switch we just deleted growing back somewhere new. And notice what costFor takes: a whole Shipment. Destination, weight, distance, subtotal. The flat rate rule reads none of those fields, and that's fine — it's deliberate. If costFor took just a weight, the distance rule could not exist, and adding it would change the interface and therefore every single implementation. Passing the whole shipment is what makes a new rule cost exactly one class.

## 10. A Concrete Strategy — It Knows Only Its Own Arithmetic

And this is a concrete strategy, WeightBandedRule. The band table is data, not code, so a pricing change is a change to a list rather than to the algorithm. But the thing worth noticing is what's absent. There's no mention of distance, no campaign threshold, no flat fee, and no checkout. This class knows its own arithmetic and nothing else — which means it gets its own test, and that test never has to construct an order or go anywhere near a checkout service.

## 11. The Context — Search It for the Word 'Weight'

And this is the context, CheckoutService. Search this class for the words flat, or weight, or distance, and you find nothing. It holds a rule and it calls it. There's no if, no instance-of, no enum. And that's the test of whether strategy has actually been applied: moving a switch out of this class into a helper would just relocate the decision. Taking the behaviour as a constructor argument removes it. Now — somebody always asks at this point, quite rightly: where did the branch actually go? Something still has to turn a config value into an object. It goes into a small registry at the edge of the system. And the difference isn't that it disappeared, it's what it does and how often. The naive switch ran inside the pricing logic, on every single quote, tangling the decision up with the arithmetic. The registry runs once, when the shop is configured, and answers a completely different question: which rule is in force today. In a real store that's a database row or a feature flag — the mapping is data, and the pricing code never sees it.

## 12. The Test That Actually Proves It

Here's a subtlety worth pausing on, because it changes how you test this. A test that says a six and a half kilo parcel costs twelve pounds passes against the naive design too. It tells you the arithmetic is right, but it proves nothing at all about whether the pattern was applied. This one does. It defines a pricing rule entirely inside the test — nothing in the production source knows this rule exists — hands it to CheckoutService, and it just works. If somebody quietly put the switch back tomorrow, this is the test that would go red.

## 13. Running It

When we run the project, the same Cardiff parcel gets priced by every rule in turn. Under weight bands the delivery is twelve pounds. Under the campaign rule the order is over fifty pounds, so delivery is free and the total drops to sixty four. Same client object. Same method call. Not one line of CheckoutService changed between those two quotes. And at the bottom, the thing the naive version couldn't do: an unrecognised rule name is refused outright, rather than falling into a default branch and shipping for free.

## 14. Wrap Up

So, to recap. Use strategy when a switch branches on a type or a mode field and each branch does real, unrelated work. Keep the strategies stateless, so one instance can be shared by every concurrent order. And never let the context ask what it's holding — the moment you write instance-of, the branch is back and the pattern is decoration. One honest word of warning: four classes instead of one method is a real cost. For two rules that will never change, the switch is genuinely the better answer. Strategy pays for itself when the family is open-ended — and delivery pricing really is, because marketing owns it. And if you remember one sentence from today, make it this one. Strategy and State have exactly the same shape — an interface, several implementations, a context holding one. The difference is who chooses, and how often. Strategy's choice comes from outside and stays put. A state object swaps itself for another as events arrive.

## 15. Thanks for Watching

And that's the strategy pattern. If you got something out of this, do give it a thumbs up, and subscribe. It genuinely helps the channel, and it's what makes more of these possible. And if there's a pattern you'd like me to cover next, drop it in the comments. I read every one. All the source code, the written notes and an interactive animation are in the repository. Thanks for watching, and I'll see you in the next one.
