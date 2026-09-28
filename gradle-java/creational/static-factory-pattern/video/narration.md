# Static Factory Method Pattern — Video Narration Script

## 1. Static Factory Method

Hello, and welcome. This video explains the Static Factory Method pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A static factory method is a static method that returns an object of its own type. It is used instead of a public constructor. Because it has a name, it can say what it makes. And because it is a method, it can hand back a shared object, or a different class, instead of always building something new. If you have ever written List dot of, you have already used one. In this video, we build the discounts for an online shop's checkout. By the end, you will know exactly what this technique gives you, and exactly where it stops.

## 2. The Job

Here is the job. An online shop prices an order, and applies a discount to it. The shop needs several kinds of discount. Ten percent off. Five pounds off. Free shipping. No discount at all. And one clever one, which picks whichever of two others saves the customer more. The checkout should not care which one it is given. It should just apply it, and move on.

## 3. The First Attempt Does Not Compile

So you start where everyone starts: constructors. Ten percent off is one number. Five pounds off is also one number. So you write two constructors, each taking one decimal number. And it does not compile. Java says the constructor is already defined. Why? A constructor's name is fixed. It is always the name of the class. So the only way to tell two constructors apart is by their parameter types. And both take one decimal number. The difference, percent versus pounds, only exists in your head. There is nowhere in the code to put it.

## 4. So Everyone Writes This Instead

So what does everyone do instead? They widen the constructor until every kind of discount fits. One constructor, with three parameters: a percentage, an amount off, and a free shipping flag. And an unwritten rule: set the ones you are not using to zero. Now imagine reading four calls to it, each with three values. Which one gives five pounds off? You can work it out, but only by counting commas. And a call with all zeros? That is a discount that does nothing. But nothing in that line says so.

## 5. Why That Hurts

And that costs you in five ways. One. The call no longer says what it means. Two. Nothing stops someone passing a percentage, an amount, and free shipping, all at once. That is nonsense, and the compiler accepts it. Three. Every discount carries fields that belong to the other kinds. Four. A new kind of discount means changing the constructor, and every caller with it. Five. The new keyword always creates a new object. Even a discount of nothing is built fresh, every single time. Notice that the discount type itself is fine. The problem is the way in.

## 6. The Static Factory Method

The fix has a name. A static factory method is a static method that returns an object of its own type, used instead of a public constructor. It is item one, the very first item, in the book Effective Java. In plain words: give the constructor a name. That is the whole idea. One warning. This is not a Gang of Four pattern. And despite the word factory, it is not the Factory Method pattern. They share a word, and nothing else.

## 7. A Vending Machine

Think about a vending machine. You press a button with a label on it. You do not open the front and reach inside. The button has a name, so you always know what you asked for. The machine decides which shelf and which slot. That is its business, not yours. It might hand you one it already had waiting. And if a button means nothing, it does not have to make anything at all. That is the whole idea. You ask for an outcome, not a manufacturing step.

## 8. The Shape of It

So here is the shape of it. Your code calls a named method on the Discount interface itself. The type is its own factory. There is no separate factory class anywhere in this project. Behind the interface are five classes that do the real work. And none of them is public. So no code outside the package can even name them. That means all five could be renamed, merged, or deleted tomorrow. And not a single caller would break.

## 9. The Type Is Its Own Factory

Here is the code. Since Java eight, an interface can hold static methods. So all six ways in live on the Discount interface itself. Just listen to the names. None. Percentage. Amount off. Free shipping. Best of. And for coupon. You know what each one does without reading inside it. And percentage and amount off could never have been two constructors. Both take one number. As named methods, they sit side by side, and nobody confuses them. That is the first freedom: a name.

## 10. Freedom Two: Not to Allocate

Now the second freedom, which a constructor can never have: not creating anything. A discount of nothing holds no data. There is no reason for two of them to exist. So the class keeps one shared instance, and hides its constructor. The none method hands back that same object, every single time. The new keyword always means, make a new one. It cannot say, here is one I already had. A named method can. That is exactly why Integer dot value of exists. And why calling new Integer is deprecated.

## 11. Freedom Three: to Choose the Class

The third freedom is the deepest one: choosing the class. A static factory method does not have to return the class you expect. Ask for a percentage discount of zero. You do not get a percentage discount holding a zero. You get the shared do-nothing discount instead. Nobody outside can tell, and nobody can complain. Because the return type was only ever Discount. Notice the input check, too. A percentage below zero, or above one hundred, is refused, before anything is built.

## 12. What the Client Looks Like

And here is the payoff: the whole checkout. Search it for the new keyword applied to a discount. There is none. Search it for a branch on the kind of discount. There is none. Search it for any of the five discount class names. Not one of them appears. It takes a Discount, asks what it is worth, and subtracts it. That is all. Every decision was made inside a factory method, long before.

## 13. The Same Trick on a Value Type

The same trick works beautifully on a small value type: money. Money dot pounds of five, and Money dot pence of five. Two completely different amounts. As constructors, they could never exist side by side, because both take one number. As named methods, they say exactly what they mean. There is also a parse method, for text coming from outside. And money zero hands back one shared instance, for the same reason as the do-nothing discount.

## 14. You Already Use This Every Day

You are not really learning something new. You are learning the name of something you already use. List dot of. Integer dot value of. Optional dot empty. Local Date dot now. Every one of those is a static factory method. And here is something worth remembering. List dot of returns a different class, depending on how many items you pass it. You have never noticed, and it has never caused a problem. That is the third freedom, quietly at work. The usual names are of, from, value of, get instance, new instance, parse, and copy of. Use those, and your code reads like Java's own library.

## 15. Running It

Let's run the demo. Every coupon code from the shop goes through the for coupon method. It returns whichever discount fits. The code save ten gives ten percent off, which saves twelve pounds on a one hundred and twenty pound order. The code best deal builds a combined discount, holding two others, and picks the bigger saving. The caller could never have built that itself, because it cannot name any of the classes. Then the proofs. Percentage and amount off, which could never have been constructors. A none discount that really is shared. A zero percent discount, quietly becoming the do-nothing discount. And an unknown coupon, refused before any object was created.

## 16. Where It Stops

Now the honest part. This technique has limits. Hiding the constructor means nobody outside can extend your classes. For value types, that is usually a good thing. But sometimes, it is a real problem for someone. Static factory methods are also harder to find. There is no new keyword to search for. And the big one. A static method is fixed when the code compiles. A subclass cannot change what gets built, and neither can a configuration file. The day you need that, you have outgrown this technique. And do not use it everywhere. In this project, the order and the receipt are plain records, with ordinary constructors. They have nothing to decide.

## 17. The Rest of the Family

Which brings us to the rest of the factory family. A static factory says: give me one that does this, with no factory class at all. A simple factory asks: which one? And answers with a switch, in a helper class. A factory method asks which one, and lets a subclass answer. And an abstract factory asks: which whole matching set? One choice, many related objects. Each one exists because the one before it reaches a limit. So start with the static factory. And move up only when something really forces you to.

## 18. One Sentence to Keep

If you keep one sentence from this video, keep this one. A constructor cannot be named, and cannot refuse to create a new object. A static factory method can do both. Everything else in this video follows from those two facts. The project has full notes, an animated walkthrough, and a teaching plan. Try adding a discount of your own. That is the best way to make it stick.

## 19. Thanks for Watching

That's the Static Factory Method. The full source code, written notes, and diagrams are all in the repository. If there is a pattern you would like to see covered, suggest it in the comments. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
