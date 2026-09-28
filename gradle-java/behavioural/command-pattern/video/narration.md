# The Command Pattern Pattern — Video Narration Script

## 1. The Command Pattern

Hello, and welcome. This video explains the Command pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Command pattern turns an action into an object. Instead of just calling a method, you create an object that holds what to do, and everything needed to do it. Then the action can be stored, passed around, logged, replayed, and even asked to undo itself. This is the pattern behind every undo button you have ever pressed. In this video, we build a shopping cart for an online store, and the edits a customer makes to it. By the end, you will know why undo cannot be built from plain method calls. Where undo bugs really come from. And what the pattern costs.

## 2. The Scenario

Here is the scenario. A customer edits their shopping cart. They add an item, remove one, change a quantity, and try a discount code. Then, like every customer, they change their mind, and press undo. Each of those edits has some history attached. The cart may already have held some of that item. A removed line had a particular position in the list. And a new coupon may have replaced an older one. So here is the key idea. Undo is not the opposite of what the customer asked for. It is putting back whatever was there before they asked.

## 3. The Obvious First Move

The obvious first approach is simple. Change the cart, and write a note of what you changed. For example: add two headphones, and push a note that says, add, headphones, two. To undo, pop the note, see what kind of edit it was, and reverse it. To be fair, this is good code. About fifteen lines, easy to read. And for a cart that only ever gains brand new items, it is completely correct. The note is honest, too. It records exactly what the customer asked for. And that turns out to be the problem.

## 4. The Naive Approach — The Note Records the Request

Here is the day it goes wrong. A customer already has three headphones in their cart. And a ten percent discount code, applied last week. They add two more headphones, so the cart now holds five. Then they apply a better discount code, which replaces the old one. Then they change their mind about both, and press undo twice. Let's follow the notes. The first undo finds the coupon note, and clears the coupon. So the ten percent code, which they never touched, is gone. The second undo finds the add note, and removes the headphones line. So all five headphones disappear, including the three from last week. Nothing crashed, and nothing warned anyone. The notes were not wrong. They just never recorded what undo really needed: how the cart looked before.

## 5. Why That Hurts

So why does this hurt? Undo reverses the request, not the change the request caused. The information undo needed, the three headphones and the old coupon, was never saved. Every new kind of edit adds another field to the note, another case to the undo code, and another round of testing for the old cases. But the worst part is that this bug is silent. Nothing crashes. The customer is simply charged the wrong amount.

## 6. The Command Pattern

Here is the pattern's definition, from the famous Gang of Four book. Encapsulate a request as an object, so that you can queue it, log it, and support undo. In plain words: make the action an object. Then it can be kept, listed, logged, and reversed. Why does that matter? A method call is an event. It happens, it returns, and then it is gone. You cannot put it in a list, ask it what it did, or run it backwards. Undo needs all of those things. So the first step is simple. Instead of calling the method, create an object that represents the call.

## 7. Everyday Analogy: The Order Slip

Here is an everyday example: a restaurant order slip. A waiter does not carry your spoken words to the kitchen. They write a slip. Think about what that slip can do. It can wait in a stack with the others. It can be read back to you. It can be handed to a different chef. It can be found an hour later, when you question the bill. And it can be torn up, if you change your mind. In the pattern, the slip is the command. The kitchen, which knows how to cook but has never met you, is called the receiver. And the waiter, who carries any slip without cooking anything, is called the invoker.

## 8. The Roles

So here are the roles in our project. The command interface is called Cart Command. It has three methods: describe, execute, and undo. The invoker is called Cart History. It keeps two stacks of commands, one for done and one for undone. It only ever runs a command, or reverses one. The receiver is the Cart itself. Then there are four concrete commands: add item, remove item, change quantity, and apply coupon. Each one saves exactly the information it needs to undo itself. The old quantity. The removed line and its position. Or the old coupon. And notice that neither side knows the other. The cart has never heard of a command. And the history has never heard of a coupon.

## 9. The Command — Three Methods

The whole interface is just three methods. Describe returns one line for the history log, in the customer's own terms. Execute makes the change. And undo reverses it. Which one is hard? Undo, of course. Notice one detail. Both execute and undo receive the cart as a parameter. A command does not hold on to a cart. It only holds plain values, like a product code, a quantity, or a coupon. The cart is handed in at the moment it is needed.

## 10. The One That Is Not Trivial to Reverse

This part is the reason the project exists, so let's go slowly. Take the add item command. The very first thing execute does is ask the cart: how many of this item do you already have? It saves that answer. Then it adds the new items. Now think about undo. Adding two headphones to a cart that held three leaves five. Undoing that does not mean removing the line. It means setting the quantity back to three. And we can only know that when the command runs, not when it is created. So here is the rule, and it is where undo bugs live. Save the information you need for undo inside execute, from the receiver, at the moment the command runs. Not in the constructor. At construction time, the cart may not yet look the way it will when the command runs. The other commands follow the same rule. Remove item saves the line and its position, so undo puts it back in the same place. And apply coupon saves the coupon it replaced. Usually there is none. But sometimes, it is exactly the discount the naive version threw away.

## 11. The Invoker, Which Knows Nothing

Now the invoker, Cart History. To execute, it runs the command, pushes it onto the done stack, and clears the undone stack. To undo, it pops the top command, tells it to undo, and moves it to the undone stack. Two decisions are worth noticing. First, clearing the undone stack. Once you take a new action, the old redo path is gone. Every text editor you have used behaves this way. Second, if execute fails with an error, the command is never pushed. Undoing a half-finished edit would reverse something that never fully happened. And notice what this class never mentions. No coupons, no quantities, no products. That is why a new kind of edit never needs to change this file.

## 12. The Test That Proves It

Here is the test that proves the pattern works. A simple test like, adding two items leaves two items, would also pass for the naive version. It tests the cart, not the pattern. This test is different. It creates a gift wrapping command, inside the test file itself. Nothing in the main code has ever heard of gift wrapping. Yet Cart History runs it, and undoes it, without a single change. If someone ever added special cases back into the history class, this is the test that would fail. Two more tests check the exact cases the naive version got wrong. Undoing an add restores the old quantity. And undoing a coupon restores the coupon it replaced. The project has thirty-seven tests, and those three carry the argument.

## 13. Running It

Let's run the demo, and compare. First, the naive version. After two undos, the cart is empty, and the discount code is gone. Then the same two edits, done with commands. After two undos, the cart has its three headphones, and its ten percent code, exactly as it started. The same customer, the same actions, and two different results. The difference is one saved field per command, captured at the right moment. And there is a bonus. The history can print a readable list of everything the customer did, in plain words. Nobody wrote extra code for that. It comes free, because every edit is an object that can describe itself.

## 14. What to Remember

So, what should you remember? Make each action an object, with execute, undo, and describe. Save the information undo needs inside execute, never in the constructor. Keep the invoker simple: it holds commands, and knows nothing else. And a new kind of edit is one new class, with no old file reopened. Now the honest costs. Every operation becomes a class. For four edits that never change, the naive version is a third of the code, and it works. Use Command when undo, logging, or queuing is a real need. The pattern gives undo a home, but it does not check that your undo is correct. And simple reads should not be commands, because there is nothing to undo. Finally, know its close relative, the Memento pattern. Command saves the difference, and each edit must know how to reverse itself. Memento saves a full snapshot instead, and needs no reversing, but costs a copy at every step. And you have used Command already. A task handed to a thread pool is a command without undo. And a database migration with an up step and a down step is a command with undo.

## 15. Thanks for Watching

That's the Command pattern. If you remember one sentence, make it this one. Turn each action into an object that saves what it needs to undo itself, at the moment it runs. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Move that saving step out of execute, and into the constructor. Run the tests, and exactly one will fail. Working out which one, and why, is worth more than the rest of this video. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
