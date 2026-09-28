# Prototype Pattern Pattern — Video Narration Script

## 1. Prototype Pattern

Hello, and welcome. This video explains the Prototype pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Prototype pattern makes a new object by copying one that already exists, instead of building it from nothing. You keep one fully set-up example to hand. When you need another, you ask it for a copy of itself. Then you change only the parts that differ. Think of a photocopier. You start from a finished page, and get an independent copy instantly. In this video, we copy product listings in an online marketplace. Along the way, we look closely at Java's built-in copy method, called clone. And why the book Effective Java warns you away from it.

## 2. The Job

Here is the job. A seller lists wireless earbuds, in black. Getting that one listing right is real work. Choosing a category. Writing a description that meets the rules. Choosing a shipping profile. And setting a return window and a warranty. Now the seller wants the same earbuds in white. And then in blue. The category, description, shipping, returns, and warranty are all unchanged. Only the product code, the title, and the colour are different.

## 3. The Repeated Eleven-Argument Call

So you write it out twice, using the constructor. Each call has eleven arguments. And only two or three of them differ between black and white. Everything else is copied, word for word, between the calls. The description, category, brand, price, shipping, returns, and warranty. Add a blue version, and it is pasted a third time. Fix a typo in the description, and every copy needs the same fix.

## 4. The Cloneable Trap

Java already has a way to copy objects, so why not use it? You implement the Cloneable interface, and override the clone method. The book Effective Java spends a whole chapter explaining why this disappoints almost everyone. The clone method is protected, so you must make it public yourself. It declares an error that can never actually happen. And worst of all, it copies fields shallowly. So if you add a picture to the copy's image list, the original's list changes too. Silently. Because they were always the same list.

## 5. Why That Hurts

So neither approach works. Typing every version out by hand means the shared details get retyped again and again. And eventually, one of them drifts. Using Cloneable swaps that problem for a worse one. A method you must expose yourself, an error that means nothing, and a shallow copy that silently links two objects. Notice that the product listing itself is fine. The problem is how you duplicate one.

## 6. The Prototype Pattern

The fix is a pattern from the famous Gang of Four book. Specify the kinds of objects to create using an example instance, and create new objects by copying that example. In plain words: keep one fully assembled example around. And make new ones by copying it, and changing only what is different.

## 7. A Photocopier, Not a Blueprint

Think about the difference between a blueprint and a photocopier. A blueprint tells you how to build something from raw materials, every single time. That is what a constructor is. A photocopier is different. It starts from a finished page, and hands you an independent copy, instantly. You can scribble all over your copy, and the original on the glass does not change. That is a prototype. Not instructions, but a finished example you copy from.

## 8. The Shape of It

So here is the shape of it. The product listing class implements a small interface called Prototype. It has just one method, called copy. Call copy on an existing listing, and you get back a second, fully independent listing, with the same details. Alongside it sits a listing registry. It is a named shelf of templates. Ask it for a template by name, and it hands back a fresh copy.

## 9. One Method, No Baggage

Here is the whole Prototype interface: one method, called copy. Compare it with Cloneable. Nothing protected to expose. No error to catch that can never happen. And no automatic copying at all. Because only the real class knows which of its fields need a true copy, and which can simply be shared.

## 10. copy() Reuses the Constructor

Now look at the copy method itself. There is no special copying logic inside it. It simply calls the constructor again, passing in its own details. That works because the constructor already creates a brand new image list, and a brand new attribute map, every time it runs. It does that to protect any caller who hands it a list. So copy gets that protection for free. One piece of protective code, doing two jobs.

## 11. Deep Copy vs. Shared Reference

But not every field gets a fresh copy. The shipping profile is passed straight through. The original and the copy share the very same shipping profile object. That is only safe because the shipping profile can never change. It is a record, with no setters. This is the real design work in this pattern. Not calling the constructor again. But deciding, field by field, what needs a fresh copy, and what is safe to share.

## 12. Cloning and Tweaking

Here is what copying and adjusting looks like. Copy the black master listing. Set the new product code. Set the new title, wireless earbuds, white. Change the colour to white. And replace the pictures. Five short steps, instead of an eleven-argument call, repeating eight values that never changed. And the master listing is completely untouched. The white listing has its own independent colour details, and its own list of pictures.

## 13. The Registry

The Gang of Four book also describes a registry of templates, sometimes called a prototype manager. It is useful when the set of templates is decided while the program runs. Its create method looks up a template by name. If there is none, it refuses, and names the missing key. Otherwise, it returns a copy of the template. Notice it never builds a listing from scratch. It only ever copies. Ask for the same name twice, and you get two separate, independent listings.

## 14. Running It

Let's run the demo. First, a master listing, and a white version copied and adjusted from it. The master's own pictures are unchanged after the copy. And the shipping profile really is the same shared object in both. Then the registry hands back two independent listings, from one name. And finally, a request for a name that was never registered. It is refused with a clear message, before any listing is copied.

## 15. Where It Stops

Now the honest part. Every pattern has limits. First, deciding what to copy takes care. Every changeable field a class adds is one more thing its author must remember to copy properly. Miss one, and copies silently share a list. Exactly the bug this pattern exists to prevent. Second, copying is not checking. A copy reproduces the original's state, whether it was valid or not. Third, a registry swaps a class name the compiler can check, for a text key that is only checked at run time. Use a registry only when the templates really are decided elsewhere.

## 16. How It Relates to the Others

So how does Prototype relate to the other creational patterns? A static factory answers: give me one that does this. A builder answers: which pieces, in what order, for one object. An abstract factory answers: which whole matching set. And Prototype answers a question none of the others do. I already have one, so how do I get another that is almost the same? And they work together. A template stored in a registry might well have been built with a builder in the first place.

## 17. One Sentence to Keep

If you keep one sentence from this video, keep this one. When you already have one fully assembled object, and need another that is almost the same, copy it instead of rebuilding it. And decide, field by field, what copy should mean. A fresh copy for anything that can change. A shared reference for anything that cannot. The project has full notes, an animated walkthrough, and a teaching plan. Try adding a new changeable field to the product listing. And notice that the copy method needs no changes at all.

## 18. Thanks for Watching

That's the Prototype pattern. The full source code, written notes, and diagrams are all in the repository. If there is a pattern you would like to see covered, suggest it in the comments. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
