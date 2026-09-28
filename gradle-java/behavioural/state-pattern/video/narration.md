# The State Pattern Pattern — Video Narration Script

## 1. The State Pattern

Hello, and welcome. This video explains the State pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The State pattern gives every state of an object its own class. The object then hands each request to whichever state it is currently in. So what is allowed depends on which state class is present, not on checks someone wrote against a status field. And an action that makes no sense in a state is simply missing from it. Think of a vending machine. With no coins in it, pressing a button does nothing. With a pound fifty in it, the same button gives you a drink. In this video, an online order moves from placed, to paid, to packed, to shipped, to delivered, with cancellations and refunds along the way. By the end, you will know why a refusal should be missing code, not a remembered check. How State differs from Strategy. And when not to use it.

## 2. The Scenario

Here is the scenario. An order moves through a simple lifecycle. Placed, then paid, then packed, then shipped, then delivered. Two more states end the story: cancelled, and refunded. Once an order reaches either of those, nothing more happens to it. Six things can be asked of an order. Pay, pack, ship, deliver, cancel, and refund. And the answer to every one depends on where the order is right now. That sentence is the whole problem.

## 3. Look Closely at One Row

Before any code, let's look closely at one action: cancel. Cancelling a placed order moves no money, because none was taken. Cancelling a paid order refunds the customer. Cancelling a packed order refunds the customer and puts the stock back on the shelf, because a box has already been packed. And a shipped order cannot be cancelled at all. The goods are already on a van. So cancel is not one rule with a permission check in front of it. It is several different jobs, plus a refusal.

## 4. The Naive Approach — One Rule, Three Copies

The obvious first approach is a status field, and a check at the top of each method. To be fair, this is short, simple, and the whole lifecycle is in one file. For small machines, a status list and a table of allowed moves is often the right answer. The problem is that the rules get written once per method. And each copy is phrased however its author found natural. The cancel check was written as: anything that has not arrived yet can be cancelled. That sounds sensible. But it quietly includes shipped orders. So a parcel that is already on a van gets refunded. The refund check had a different history. Support asked for cancelled orders to be refundable too. But cancelling had already refunded the customer. So that change pays the customer a second time.

## 5. Why That Hurts

And here is what makes it truly nasty. There is a third copy of the same rules, used to decide which buttons to show on screen. That copy is correct. It says a shipped order can only be delivered. So the cancel button never appears. Nobody clicking around the app can reach the bug. Everyone believes the rule is enforced. But the server still accepts a cancel request, from a script, a retry, or a support tool. Nobody made these mistakes while looking at the whole lifecycle. They happened because the lifecycle is never written down in one place.

## 6. The State Pattern

Here is the pattern's definition, from the famous Gang of Four book. Allow an object to change its behaviour when its internal state changes. The object will appear to change its class. That last sentence does all the work. A shipped order and a placed order are the same Java object. But they accept different requests, and do different things with them. Exactly as if they were different classes. In plain words: stop writing one method that handles every state. Instead, write one class per state, that handles every method.

## 7. Everyday Analogy: The Vending Machine

Here is the picture to keep in your head: a vending machine. One machine has no coins in it. The same machine, a moment later, holds a pound fifty. Same machine, same buttons. But pressing a button does something completely different. You would not say the machine has a mode number. You would say it is waiting for money, or ready to sell. Those are named conditions. And notice this, because it separates State from Strategy. Nobody chooses the machine's condition from outside. It gets there because of what just happened. A coin went in. A drink came out.

## 8. The Roles

So here are the pieces. The Order is called the context. It holds one current state, and passes every request to it. It contains no if statements about status at all. Order State is the interface. It declares all six requests. Then there are seven real states: placed, paid, packed, shipped, delivered, cancelled, and refunded. Each one holds everything that is true at that point in the lifecycle. And here is something uncomfortable. This design looks exactly like the Strategy pattern. A context, an interface, and some implementations. We will come back to how they differ.

## 9. Every Request Refuses By Default

This is the most important decision in the project. Every request on the interface has a default body. And every default body refuses the request. So a state does not list what it forbids. It only lists what it allows, by overriding those methods. Everything else refuses by itself. Think about what that does to mistakes. In the status field version, forgetting a check opens a door. That is exactly how shipped orders became cancellable. Here, forgetting to override closes a door. The careless mistake now points the safe way. And the refusal message is built from the state's allowed actions. For example: cannot refund a shipped order, the only thing it will accept is deliver.

## 10. The Context Has No Conditionals At All

Now, what is left of the Order itself? Every public method is one line. It passes the request to the current state. The order does not know there are seven states. It does not know their sequence. And there is not one if statement about status in it. What the order does own is the history. When a request is refused, the refusal is recorded, and then passed on. So a line like, someone tried to cancel this after it shipped, is always recorded. That is exactly what you want when reading a support ticket. And from outside, nobody can simply set an order's state. It only changes as a result of asking the order to do something.

## 11. Same Verb, Genuinely Different Work

This part decides whether the pattern is worth it. If the states only differed in which requests they allowed, this would be over-engineering. But they differ in real work. Cancel, in the paid state, gives the money back. Cancel, in the packed state, gives the money back, and also puts the stock back on the shelf. In the status field version, those were branches of one method. The day someone merges them, because they look nearly the same, the stock stops going back. The shipped state also overrides cancel, but only to refuse it with a better reason. It says: this order is already with the courier. When a refusal has a reason worth telling a person, write it down.

## 12. The Test That Proves It

The tests are where the argument becomes proof. The first test passes, and what it checks is the bug. Pay, cancel, then refund, and the shop has paid the customer twice. It passes, because that is really what the naive code does. Next to it, the same steps run through the State version. The refund is refused, and the shop's ledger shows exactly one refund. And one more test is even better. It tries all seven states with all six actions, forty-two combinations. For each one, it checks that the buttons shown on screen exactly predict whether the action is accepted. The naive version can never pass that test, and the reason is its bug.

## 13. Running It

Let's run the demo. First, the status field version. The screen shows only a deliver button. But the server accepts a cancel anyway, and then a refund. The shop ends up ninety-seven pounds and forty-nine pence out of pocket, over two refunds. That is real money, lost to one copied condition. Now the same two requests through the State version. Both are refused, with reasons a person can read. And both are recorded in the history. Finally, the demo lists the buttons for every state. That list comes from the same classes that hold the behaviour. So the screen and the server can never disagree again.

## 14. What to Remember

So, what should you remember? First, State and Strategy have exactly the same class structure. You cannot tell them apart by their diagram. The difference is who is in control. A strategy is chosen by the caller, and never changes itself. For example, the checkout picks a shipping calculator, and it just does its sum. A state is entered because of what the object just did. And states hand control to each other. When the paid state packs an order, it moves the order into the packed state. Now the honest cost. Seven classes, where there used to be one list of statuses. And the full table of moves is no longer in one place. It is spread across seven files. That is a real loss. So do not use this for every status field. If each state only differs in permission, use a status list and a table of allowed moves. Use the State pattern when the actual work differs by state, as it does here.

## 15. Thanks for Watching

That's the State pattern. If you remember one sentence, make it this one. Give each state its own class, so that a forbidden action is simply code that does not exist. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a return requested state, between delivered and refunded. Add it to the State version, and then to the status field version. And count how many places you had to edit in each. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
