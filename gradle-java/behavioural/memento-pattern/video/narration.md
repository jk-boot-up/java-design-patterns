# Memento Pattern — Video Narration Script

## 1. Memento

Hello, and welcome. This video explains the Memento pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A memento is a sealed copy of an object's state. The object takes the copy itself, and hands it to someone else to keep. Later, when you want to go back, the copy is handed back, and the object restores itself. Think of a save point in a video game. The game saves everything about your progress. If things go wrong, you load the save, and you are back where you were. In this video, we add an undo button to the shopping basket of an online shop. By the end, you will know why one equals sign can make undo empty the whole basket. How to let something keep your state without ever seeing inside it. And the one honest cost of this pattern.

## 2. The Scenario

Here is the scenario. A shopper's basket holds three products, and a voucher code worth five pounds off. The total is sixty-five pounds. The basket's state is exactly two things. The lines in it, and the voucher. Remember that, because it matters soon. The request is simple: add an undo button. Shoppers keep removing the wrong item, and then have to find the product again. It sounds like an afternoon's work. But the obvious afternoon's work is quietly wrong.

## 3. Look Closely at One Line

Before any code, let's look closely at one line. Saved lines equals lines. That line does not copy anything. It records where the list is, not what is in it. So the saved list and the live list are the same list, under two names. Then undo clears the live list. Which also clears the saved list, because they are the same list. Then it copies the empty saved list back. So the shopper presses undo, and their whole basket disappears. Nothing crashes, and nothing is logged. Nobody wrote a bug on purpose. Somebody wrote an equals sign.

## 4. The Naive Approach — Undo Without a Snapshot

Here is the naive version in full. One method to save, and one to undo. They look like opposites, but they are not. The first bug we just heard. The second is even quieter. Think about what the save method never mentions. The voucher. It is part of the basket's state, but it is not saved at all. Nobody decided to leave it out. It just was not on anyone's mind the day undo was written. And there is no line of code to review, because the bug is a missing line.

## 5. Why That Hurts

So what exactly is wrong? Four separate things. One. The bugs are silent, and they are missing lines. An empty basket, and a voucher that never comes back. Two. Every new field is another chance to forget. Add a delivery date next month, and undo becomes half-right again. Three. The obvious fix is worse. Make the basket's fields public, so the undo code can copy them. That works, but now anything at all can change a basket. And four. Undoing by doing the opposite sounds tidy, until you try it. Removing a line undoes an add. But what undoes a remove? You would need to know which line it was, where it sat, and what the voucher was. In other words, you would need to have saved it.

## 6. The Memento Pattern

Here is the pattern's definition, from the famous Gang of Four book. Without breaking encapsulation, capture an object's internal state and store it outside, so the object can be restored to that state later. Anyone can copy some fields. The hard part is doing it without breaking encapsulation. That means whoever holds the copy still cannot see inside it. In this project, the object is the basket. The copy is a basket snapshot. And the undo history keeps the snapshots, without ever knowing what a basket contains.

## 7. An Analogy

Here is the analogy to hold on to. You are about to rearrange a room. First, you take a photograph of it. You seal the photo in an envelope, and hand it to a friend. Your friend can keep several envelopes, in order. And hand back whichever one you ask for. But they cannot open them. They do not need to, because putting the room back is your job, not theirs. They only need to know which envelope is which. So you write a label on the outside, such as, before I moved the sofa. In our project, the basket is you. The snapshot is the sealed envelope. The undo history is your friend. And the label is the only thing your friend may read.

## 8. The Roles

So here are the pieces, and there are only three. The Basket is called the originator. It is the only class that knows what its state is. So it is the only class that creates a snapshot, and the only one that reads one back. The Basket Snapshot is the memento. It holds a complete copy of the basket's state. And the Basket History is called the caretaker. It stacks up snapshots, and hands them back. It is defined by what it cannot do: it cannot look inside a snapshot. Only the basket ever opens the envelope.

## 9. The Memento — Two Interfaces, No Framework

Now the snapshot itself, and two details matter. First, when it is created, it makes a real copy of the basket's lines. Not a reference to the live list, but a copy that nothing can change afterwards. A photograph of the basket, not a window onto it. That single step is the heart of the pattern. Second, the access rules. The label can be read by anyone, so an undo menu can show, undo: removed the laptop stand. But the lines and the voucher can only be read by classes in the same package. And the only class there that wants them is the basket. Even creating a snapshot is restricted. The only way to get one is to ask a basket for it.

## 10. The Originator and the Caretaker

Now the other half, the basket and the history. The basket has two short methods. Save creates a snapshot of its lines and voucher. Restore empties its lines, copies the snapshot's lines back, and restores the voucher. These are the only lines in the project that know what a basket's state is. Add a gift message next month, update these two methods, and undo keeps working. Nothing outside the basket needs to know. Restore does not use up the snapshot, so it could be restored twice. That makes adding redo later a small change. And the history. To undo, it takes the latest snapshot, hands it to the basket, and reads the label. It never opens the snapshot, because it simply cannot. Undo works, and the history does not even know a basket has lines.

## 11. The Tests — Asserting the Structure, Not Just the Behaviour

The project has sixteen tests. Two of them prove the pattern. The first checks the structure. It looks at every public method on the snapshot. And it fails if any method outside a small allowed list could reveal the basket's contents. A comment saying, the history must not read a snapshot, lasts until someone is in a hurry. This test does not. The second test checks a wrong answer, on purpose. It confirms that the naive basket still empties itself on undo. Being broken is that version's job, and the build says so out loud.

## 12. Running It

Let's run the demo. The same basket, the same mistake, and the same press of undo. First, the version without a snapshot. The shopper removes one item by mistake, and presses undo. The basket is now empty, and the total is zero. No error. Nothing in the log. The basket is just gone. Now the memento version. The item is back, the voucher is back, and the total is back to sixty-five pounds. Notice that nobody wrote code saying, when you undo, remember the voucher too. The voucher came back because a snapshot is complete by definition. It is the basket's whole state, taken by the only object that knows what that means.

## 13. What to Remember

So, what should you remember? Undo is not, do the opposite. Undo is, put back the copy you took. And only the object that took the copy ever needs to see inside it. People often confuse Memento with Command, because both can build undo. Memento saves the state before a change, and puts it back. Command saves the operation, and runs its reverse. Memento is simpler to write, but uses more memory. Command is the other way round, and every operation needs a true reverse. And Prototype also copies objects, but for a different reason. It copies an object to make another one, not to go back in time. Now the honest cost. Every snapshot is a full copy. Twenty snapshots of a big basket means twenty baskets in memory. That is why the history limits how many it keeps. One more warning. The copy here is shallow, and that is only safe because each basket line can never change. Give a line a setter, and the copy quietly stops being safe.

## 14. Thanks for Watching

That's the Memento pattern. If you remember one sentence, make it this one. Undo means putting back a sealed copy, taken by the only object that is allowed to open it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make the snapshot's lines method public. Run the tests, and listen as the encapsulation test names that method. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
