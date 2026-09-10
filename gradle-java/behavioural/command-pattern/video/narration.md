# Command Pattern — Video Narration Script

## 1. The Command Pattern

Hello, and welcome. This video explains the Command pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. The command pattern turns an action into an object. Instead of calling a method, you create something that holds what to do and everything it needs in order to do it — so the action can be stored, passed around, logged, replayed, and asked to undo itself afterwards. That's the idea in a sentence, and it's the pattern behind every undo button you have ever pressed. The rest of the video does it properly, by building a real working Java project: a shopping cart in an online store, and the edits a customer makes to it. By the end you'll know why undo cannot be built out of method calls, where undo bugs actually live, and what the pattern costs you.

## 2. The Scenario

So, imagine a shopping cart in an online store. The customer adds an item, removes one, changes a quantity, tries a discount code. Then they do what every customer does: they change their mind, and they look for the undo. Now look at those four edits again, because each one has a piece of history attached to it. The cart might already have had some of that item. The line you removed was in a particular position on the screen. The coupon you applied may have pushed another one off. Undo is not the opposite of what the customer asked for. It is the restoration of what was there before they asked.

## 3. The Obvious First Move

The obvious first move is to change the cart, and write a note beside it saying what you just did. Add two of H one hundred, push a note saying add, H one hundred, two. Undo pops the note, looks at what kind of edit it was, and reverses it. I want to be fair to this, because it is good code. Fifteen lines, readable at a glance, and for a cart that only ever gains brand new lines it is completely correct. The note is honest, too: an accurate record of what the customer asked for. And that is exactly the problem, although you cannot see it yet.

## 4. The Naive Approach — The Note Records the Request

So here is the naive approach, and here is the day it bites. A customer has three headphones in their cart and a ten percent code they applied last week. They add two more headphones, so the cart says five. They spot a better discount code and apply that instead. Then they change their mind about both, and press undo twice. Follow the notes. The first undo pops the coupon note and clears the coupon — so the ten percent code they never touched is gone. The second undo pops the add note and removes the line — so all five headphones disappear, including the three they chose last week. Nothing threw an exception. Nothing logged a warning. The note was never wrong; it simply never held the thing undo actually needed, which is what the cart looked like beforehand.

## 5. Why That Hurts

So why does that hurt? Undo reverses the request rather than the change it caused, and the state it needed — the three headphones, the old coupon — was never written down by anybody. A fifth kind of edit means another field on the note, another case in the switch, and a re-test of the four that already worked. But the one that matters is the last: this bug is silent. Nothing crashes. The customer is simply charged the wrong amount. Most explanations of this pattern stop at the switch getting long. That is the design complaint. The lost discount is the actual bug, and it is the reason to change anything.

## 6. The Command Pattern

The Gang of Four put it like this: encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations. In plain language: make the action an object, and it can be held, listed, logged and reversed. Here is why that is not just jargon. A method call is an event. It happens, it returns, and then it is gone. You cannot put it in a list. You cannot ask it what it did. You cannot run it again tomorrow, or against a different cart, or backwards. Undo needs every one of those. So the first move is not clever at all: stop calling the method, and make an object that is the call.

## 7. Everyday Analogy: The Order Slip

Here is the everyday version. A waiter does not carry your words to the kitchen. They write a slip. Think about what that slip can do that your spoken sentence cannot. It can be stacked with the others. Read back to you. Handed to a different chef. Found again an hour later when you query the bill. And torn up if you change your mind before it is cooked. Your spoken words could do none of that, because they only existed while you were saying them. The slip is the command. The kitchen — which knows how to cook and has never met you — is the receiver. And the waiter, who can carry any slip without being able to cook a thing on it, is the invoker.

## 8. The Roles

So here are the roles. In the middle, the command interface — Cart Command — with three methods: describe, execute and undo. On the left, the invoker, Cart History, which holds two stacks of that interface and does exactly two things with an element: runs it, or reverses it. On the right, the receiver, the Cart itself. Along the bottom, the four concrete commands, and notice what is written under each one: the field it captures. Previous quantity. The removed line and its position. Previous coupon. Those fields are the pattern doing its real work. And notice that the ignorance runs both ways. The Cart has never heard of a command. And Cart History has never heard of a coupon — it pops an object and sends it undo. What that means is the command's business, not the invoker's.

## 9. The Command — Three Methods

And here is the entire pattern. Three methods. Describe gives you one line for the audit trail, in the customer's terms. Execute does the edit. Undo reverses it. Ask a room which of those three is hard and everybody says undo, and everybody is right. Notice that both execute and undo take the cart as a parameter rather than holding onto one. That is deliberate. A command holds values — a S K U, a quantity, a coupon — never a live line that the cart might replace underneath it. The receiver is passed in at the moment it is needed. Everything else in this video is a consequence of these twelve lines.

## 10. The One That Is Not Trivial to Reverse

Read this one twice, because it is the reason the project exists. The first line of execute asks the cart how many of this S K U it already has, and keeps the answer. Then it makes the change. Now look at undo. Adding two to a cart that held three leaves five. Undoing that is not remove the line — it is put it back to three. Which branch applies is not known when the command is constructed. It is only known when it runs. So here is the rule, and it is the one place undo bugs live. Capture the state you will need to reverse yourself inside execute, from the receiver, at the moment you run. Not in the constructor — that is a guess about a cart you have not reached yet, and an earlier undo may have made it wrong before you get there. A field the constructor does not set is the visible sign of a command that captures at run time. The other three are the same shape. Remove captures the line and its position, because putting it back at the bottom of the screen is not undo. Apply coupon captures the coupon it replaced — null nine times out of ten, and the tenth time it is the discount the naive version threw away.

## 11. The Invoker, Which Knows Nothing

And here is the invoker, in full. Execute runs the command, pushes it onto the done stack, and clears the undone stack. Undo pops the top command, sends it undo, and moves it across. Two decisions are worth naming. First, undone dot clear: once you take a new action, the old future is unreachable — every text editor you have used behaves this way. Second, and this one is quieter: if execute throws, the push never happens, because undoing a half-applied edit would apply the reverse of something that never fully happened. Now search this class for the word coupon. Or quantity. Or S K U. They are not there. That is precisely why a fifth kind of edit does not open this file.

## 12. The Test That Proves It

This is the test that proves the claim. A test that says adding two items leaves two items passes against the naive editor as well — it tests the cart, not the pattern. This one does not. Gift wrapping is a command declared inside the test file. Nothing in the main source has ever heard of it. Cart History was compiled long before it existed, and it runs it, and undoes it, without a single change. If somebody put a switch back into the invoker tomorrow, this is the test that goes red. Beside it sit two more: undoing a merged add restores the previous quantity, and undo restores the replaced coupon — the two cases the note-and-switch version got wrong. There are thirty-seven tests here, and those three carry the argument.

## 13. Running It

Run it, and the two halves sit side by side. Section one is the naive editor: two undos, and the cart is empty and the coupon is gone. Section four is the identical pair of edits done as commands: two undos, and the cart has its three headphones and its ten percent code, exactly as it started. Same customer, same actions, two different answers — and the difference is one field per command, captured at the right moment. Then section five, which people do not expect. History dot log gives you a readable list of everything that was done, in the customer's language. You did not write that. It came free, because every edit was already an object that could describe itself.

## 14. What to Remember

So, what to remember. Make the action an object, with execute, undo and describe. Capture the state undo will need inside execute, from the receiver — never in the constructor. The invoker holds a stack of the interface and knows nothing else. And a new kind of edit is one class, with no working file reopened. Now the honest part, because a pattern video that only lists benefits is selling you something. Every operation becomes a class. For four edits that will never change, the naive version is a third of the code and it works — use it. Command pays when undo, logging or queuing is a real requirement. The inverse is yours to get right; the pattern gives you a place to put undo, it does not check that yours is correct. And reads should not be commands — nothing to undo, nothing to log. Finally, know its sibling. Command stores the difference and needs each edit to know its inverse. Memento stores the state and needs no inverses at all, at the cost of a copy per step. And you have used this already: every Runnable handed to an executor is a command without an undo, and every database migration with an up and a down is a command with one.

## 15. Thanks for Watching

That's the command pattern. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository — including the exercise I would most recommend: move that capture out of execute and into the constructor, run the suite, and watch exactly one test go red. Understanding which test, and why it is that one, is worth more than the rest of this video. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the behavioural series. Thanks for watching, and I'll see you in the next one.
