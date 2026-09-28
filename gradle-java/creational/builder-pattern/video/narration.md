# Builder Pattern Pattern — Video Narration Script

## 1. Builder Pattern

Hello, and welcome. This video explains the Builder pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Builder pattern creates an object one piece at a time. Instead of a constructor with a long list of arguments, you call a named method for each part you want. In any order. Then one final method checks everything, and hands back the finished object. Think of ordering at a sandwich counter. You name the bread, then each filling, one at a time. And they only make it when you say, that's everything. In this video, we build a purchase order for an online store. By the end, you will know why two famous books both recommend this pattern. And how it works together with a static factory method.

## 2. The Job

Here is the job: building a purchase order. Two things are always required. An order I D and a customer I D. And at least one item, with a shipping address. On top of that, there are five independent, optional extras. Gift wrapping. A gift message. A coupon code. Priority shipping. And a free-text note. Any order might have none of those, or all of them, in any combination.

## 3. The Constructor With Nine Parameters

So you write the constructor everyone starts with. Nine parameters, one for every fact this order might need. Now imagine reading a call to it. Nine values in a row, separated by commas. Is this a priority order, or a gift order? You have to count commas, and check against the parameter list, to know. And there are two true-or-false values in there. Swap them by accident, and the compiler says nothing at all.

## 4. Telescoping Constructors

The next idea is to add shorter constructors, for the common cases. But then a gift order without priority needs one version. A gift order with a coupon needs another. Every new combination needs a brand new constructor. Or you fall back to the nine-parameter one anyway. The book Effective Java has a name for this: the telescoping constructor. And it is named as a warning, not as something to copy.

## 5. Why That Hurts

And that costs you in five ways. One. The calling code no longer says what it means. Two. Most calls are full of nulls, and false values, because most orders use few options. Three. The order of the parameters is arbitrary, and nothing enforces it. Four. Every new option widens the constructor, and touches every caller. Five. There is nowhere to put a rule like, a gift message means the order must be gift wrapped. A constructor just stores values. Notice that the purchase order itself is fine. The problem is the way in.

## 6. The Builder Pattern

The fix is a pattern from the famous Gang of Four book. Separate the construction of a complex object from its representation, so the same process can create different results. In plain words: build the object one piece at a time, in any order. And check it is complete only when you say you are done. It is also item two in the book Effective Java. Both books describe the same code, from two angles.

## 7. A Made-to-Order Sandwich Counter

Here is an analogy: a made-to-order sandwich counter. You do not shout your whole order through the hatch at once. You name the bread. Then a filling. Then another. Then any extras you want. You never list all the toppings you do not want. And they do not start making it until you say, that's everything. If you say that with no fillings at all, they can refuse. That is exactly the shape of a builder. Build it up piece by piece, and check it only at the end.

## 8. The Shape of It

So here is the shape of it. There is exactly one way in. A static method called builder, on the purchase order class, which takes the two required I Ds. It hands back a Builder object. Every method on the Builder returns that same Builder. So the calls can be chained, one after another, in a single statement. Only the final build method does two things. It checks the order is complete. And it creates the finished, unchangeable purchase order. The purchase order's own constructor is private. The Builder is the only way to create one.

## 9. Required Facts, Optional Pieces

Here is how the code handles required and optional parts. The two facts that are always required, the order I D and the customer I D, are the Builder's only constructor arguments. And you reach that constructor through the static builder method. Every optional piece starts with a sensible default. It has no constructor argument at all. So there is nothing to skip past, because there was never a position for it.

## 10. One Method, One Piece

Every Builder method follows the same shape. Set one piece, then return the Builder itself. Returning the same Builder is what lets the next call chain straight on. So creating an order reads like a sentence. Builder, add a mug, add a book, set the shipping address, mark it priority, and build. Compare that with the nine-parameter constructor. Now every piece announces itself by name, in whatever order you wrote it.

## 11. A Rule That Lives in One Place

Here is something a plain set of setters could never give you. Setting a gift message also marks the order as gift wrapped. Because a gift message on an unwrapped box makes no sense. And that rule lives in exactly one place. Not repeated at every call. Not left to a comment that says, remember to wrap it. It is enforced once, inside the one method that can enforce it.

## 12. Checked Only When You Say You're Done

And this is the moment the order is checked for completeness. Not when an item is added, and not when the address is set. Only in build. If there are no items, build refuses, saying a purchase order needs at least one item. If there is no address, it refuses, saying a purchase order needs a shipping address. Why can't an earlier method check this? Because adding an item cannot know whether you are about to add more, or whether you are finished. Only build marks the moment you say you are done.

## 13. The Product Stops Watching the Builder

One more detail, easy to miss, and important. When build creates the order, it takes a copy of the Builder's list of items. A snapshot, not the same list. So imagine keeping the same Builder, adding another item, and building a second order. The first order has one item. The second has two. The first order did not silently gain the new item. Once build returns, the order no longer depends on the Builder at all.

## 14. The Director, the Java Way

The Gang of Four book describes one more role, called the Director. Its job is to know fixed recipes for common orders. In everyday Java, a director is usually just a static method. Here, a class called Purchase Order Presets has a method called express order. It sets the address, marks it priority, adds a same-day shipping note, and adds the items. Notice that the preset only ever uses the Builder's public methods. So the purchase order's private details can change tomorrow, and not one preset needs to change.

## 15. Running It

Let's run the demo. First, one order built by hand, with a gift message and a coupon. It is gift wrapped automatically, because it has a message. Then three presets: a gift order, a standard order, and an express order. Each one does exactly what its name says. Then the reused Builder. The first order has one item, and the second has two. Neither affects the other. And finally, two orders are rejected on purpose. One with no items, and one with no address. Both are caught before any purchase order is ever created.

## 16. Where It Stops

Now the honest part. Every pattern has limits. First, a builder is an extra object. For every order you build, a Builder exists briefly too. For an order placed a few times a second, that costs nothing. For something created millions of times in a tight loop, it is worth thinking about. Second, it is more code to write, for a type with few choices to make. That is why this project's line items and addresses are plain records, with ordinary constructors. Two or three required values, and no options. A builder there would be ceremony for no reason.

## 17. How It Relates to the Others

So how does the Builder relate to the other creational patterns? A static factory method answers: give me one that does this. A simple factory answers: which one? using a helper with a switch. An abstract factory answers: which whole matching set? And a builder answers a different question. Not which object, but which pieces, for one object, built up gradually. And they are not rivals. The builder method on the purchase order is itself a static factory method. It just returns something that collects more information, before building anything.

## 18. One Sentence to Keep

If you keep one sentence from this video, keep this one. A constructor makes you decide the whole object in one call. A builder lets you decide it one piece at a time, and checks it is complete only when you say you are done. The project has full notes, an animated walkthrough, and a teaching plan. Try adding an option of your own to the purchase order. That is the best way to make it stick.

## 19. Thanks for Watching

That's the Builder pattern. The full source code, written notes, and diagrams are all in the repository. If there is a pattern you would like to see covered, suggest it in the comments. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
