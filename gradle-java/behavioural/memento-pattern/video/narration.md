# Memento Pattern — Video Narration Script

## 1. Memento

Hello, and welcome. This video explains the Memento pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. A memento is a sealed copy of an object's state, taken by that object, handed to somebody else to hold, and handed back later when you want to go back. It is how every undo button you have ever pressed works. That's the idea in a sentence. The rest of the video does it properly, by building a real working Java project: the shopping basket of an online shop, with an undo button on it. By the end you'll know why one equals sign is the difference between undo working and undo emptying the basket, how to let something save your state without ever being able to see it, and the one honest cost of this pattern.

## 2. The Scenario

So, imagine an online shop. This is a shopper's basket. Three products, and a voucher code that takes five pounds off the whole thing. Sixty five pounds. The basket's state is exactly two things: the lines in it, and the voucher. Remember that, because it matters in a minute. And the ticket says, add an undo button. Shoppers keep removing the wrong line and then have to go and find the product again, so one step back would save them a lot of irritation. That is the whole feature. It sounds like an afternoon's work, and this is one of those cases where the obvious afternoon's work is subtly wrong.

## 3. Look Closely at One Line

Before any code, look closely at one line. Saved lines equals lines. That does not copy anything. It writes down where the list is, not what is in it, so the saved list and the live list are the same list under two names. And then undo clears the live list, which is also the saved list, and copies the now-empty saved list back over it. Sit with that for a second, because it is the reason this pattern exists. The shopper presses undo and their basket is gone. Nothing throws. Nothing gets logged. Nobody wrote a bug — somebody wrote an equals sign.

## 4. The Naive Approach — Undo Without a Snapshot

Here's the whole thing. Read those two methods side by side and they look like opposites. They are not. The first bug we've just seen. The second one is quieter still. Look at what save doesn't mention. The voucher. It is part of the basket's state, and it is not in the save at all. And I want to be precise about the lesson, because it isn't that somebody was careless. Nobody decided not to save the voucher. It simply wasn't on anyone's mind on the day undo was written. There is no line of code you could review to find that out, because the bug is the absence of a line.

## 5. Why That Hurts

Let's be precise, because it's four separate costs. One. The bugs are silent, and they're shaped like omissions. An empty basket, and a voucher that doesn't come back. You cannot review a line that was never written. Two. Every new field is a fresh chance to forget. Add a delivery date next month and undo goes quietly half right again, and it will keep doing that once per field, forever, because nothing connects the basket's state to what undo saves. Three. The obvious fix is worse than the bug. Make the fields public so the undo code can reach in and copy them. That works, and it means anything at all can now edit a basket. You've bought one feature with the basket's encapsulation, permanently. And four. Undo by doing the opposite sounds tidy until you try it. Removing a line undoes an add — but what undoes a remove? You'd have to know which line, and where it was in the list, and what the voucher was doing at the time. Which is to say: you'd have to have saved it.

## 6. The Memento Pattern

Here's the definition from the Gang of Four book. Without violating encapsulation, capture and externalize an object's internal state, so that the object can be restored to this state later. Two halves, and the first one is the one people skip. Capturing state is easy — anybody can copy some fields. Capturing it without violating encapsulation, so that the thing holding the copy still cannot see inside the object, is the part that takes a pattern. In this project the object is a basket, the copy is a basket snapshot, and the thing holding the copies is an undo stack that manages to do its entire job without knowing that a basket contains anything at all.

## 7. An Analogy

Here's the analogy to hold on to, and with this one, if you take nothing else away, take this. You're about to rearrange a room. Before you start, you take a photograph, put it in an envelope, seal it, and hand the envelope to a friend. Your friend can hold it. They can keep several of them, in order, and hand you back whichever one you ask for. What they cannot do is open it. And they don't need to, because putting the room back is your job, not theirs. They only have to remember which envelope is which — which is exactly why you write on the outside, before I moved the sofa. That's the whole pattern. The basket is you, the snapshot is the sealed envelope, the undo stack is the friend, and the label on the outside is the one thing the friend is allowed to read.

## 8. The Roles

So here are the pieces, and there are only three. Basket is the originator. It's the only class that knows what the basket's state actually is, which is why it's the only class that writes a snapshot and the only class that reads one back. Basket snapshot is the memento. It holds a complete copy, and the interesting thing about it is the access modifiers rather than the fields — we'll come to that. And basket history is the caretaker. It stacks snapshots up and hands them back, and it is defined by what it cannot do. Notice that the history never touches the snapshot's contents. Every arrow that opens an envelope comes from the basket. That's the shape worth remembering.

## 9. The Memento — Two Interfaces, No Framework

Here's the memento, and there are two things in it. The first is list dot copy of. A copy, taken at the moment of saving, that nothing can reach afterwards. A photograph of the basket rather than a window onto it. Everything else in this pattern is arrangement; that line is the substance. The second is the access modifiers, and I'd read them before the fields. The books describe a memento as having a wide interface for the originator and a narrow one for everybody else. In Java you get that for free. Label is public, so an undo menu can display, undo: removed the laptop stand. Lines and voucher have no modifier at all, which means only classes in this package can call them — and the only class in this package that wants to is the basket. The constructor is package-private too. The only way to get a snapshot is to ask a basket for one.

## 10. The Originator and the Caretaker

And here's the other half. Six lines on the basket, and they are the only six in the project that know what a basket's state is. That's the property worth protecting. Add a gift message next month and undo keeps working the moment you've added it to these two methods — nothing outside the class needs to hear about it. Notice also that restore reads the snapshot without consuming it, so the same one could be restored twice. That's what makes redo a ten-line addition later rather than a rewrite. And then the caretaker. Read it looking for something it cannot do. It pops a snapshot, hands it to the basket, and reads the label. It never opens one, because the methods that would let it aren't visible from there. Undo works, and the undo stack does not know that a basket contains lines.

## 11. The Tests — Asserting the Structure, Not Just the Behaviour

Sixteen tests, and these two are the ones that prove the pattern. A test saying undo restores the basket is a fine test, but it doesn't say anything about the design. The first one here asserts the structure. It walks the snapshot's declared methods by reflection and fails if any public one is outside a small allowed list. Because a comment saying, the caretaker must not read a snapshot, survives exactly as long as the first person who is in a hurry. This doesn't. Add a public getter and it names the method back at you. And the second one is the interesting one, because it asserts the wrong answer. It pins the naive version's empty basket in place, with a message explaining why. Fix the naive version and its own tests go red. That's deliberate. Being broken is its entire job, and the cost of that design should be something the build says out loud rather than something a README claims.

## 12. Running It

Run it, and the two halves sit side by side. Same basket. Same mistake. Same click on undo. The top half is the version without a snapshot. The shopper removes one line, presses undo, and gets an empty basket and a zero pound total. No exception. Nothing in the log. Just a basket that is gone. The bottom half is the mementoed one. The line is back, the voucher is back, the total is back. And here's the part I'd frame. Nobody wrote any code that says, when you undo, remember the voucher as well. The voucher came back because a snapshot is complete by definition — it is the basket's state, all of it, taken by the only object that knows what that means.

## 13. What to Remember

So, what to take away. Undo is not, do the opposite. Undo is, put back the copy you took — and the object that took the copy is the only one that ever needs to see it. On the comparison, because this is the question I'd expect. Memento and command are both correct answers to how do I do undo, and they get confused constantly. Memento stores the state before the change and puts it back. Command stores the operation and runs an inverse. Memento is smaller to write and bigger to hold. Command is the other way round, and it needs every operation to have a genuine inverse — so ask yourself what the inverse of clear the basket is, given that it has to restore the order of the lines too. And prototype shares the machinery of copying but none of the intent: it copies an object so you can have another one, not so you can go back. Now the honest bill. Every snapshot is a full copy, so twenty snapshots of a big basket is twenty baskets. That's why the history caps the stack, and if your state is genuinely large, command is the better trade. And one thing to watch that catches people out. The copy here is shallow, and it's safe because basket line is a record — a thing that never changes is safe to share. Give it a setter and that stops being true, and it stops being true silently. Immutable parts make a shallow copy safe. Mutable parts make it a bug waiting to be found.

## 14. Thanks for Watching

That's the memento pattern. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository — including the exercise I'd most recommend. Make the snapshot's lines method public, run the tests, and watch the encapsulation test name the offending method back at you. It takes a minute, and it's the moment the structural promise stops being a comment. If this helped, a like genuinely does help other people find it, and subscribe if you'd like the rest of the behavioural series. Thanks for watching, and I'll see you in the next one.
