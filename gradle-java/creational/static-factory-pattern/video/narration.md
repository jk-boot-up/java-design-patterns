# Static Factory Method — Video Narration Script

The full spoken script, scene by scene. This is the human-readable copy;
the authoritative text lives in the `narration` field of each scene in
[`scenes.py`](scenes.py), next to the slide it belongs to.

**Voice:** female (macOS `Samantha`, US English), rate 165 wpm.
**Runtime:** approximately 11 and a half minutes.

The script is written to be spoken, not read: contractions, short
sentences, and `[[slnc NNN]]` pause markers in `scenes.py` that the
synthesiser turns into breathing room. The markers are stripped below
and from the subtitles.

Currency and symbols are written out in words — "five pounds", not "£5" —
because the synthesiser reads them poorly. Keep that habit if you edit the
script.

The first scene carries the author credit and the last carries the
subscribe call to action; keep both if you re-record.

---

## Scene 1 — Static Factory Method

Hello, and welcome. This video explains the Static Factory Method pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. A static factory method is a static method that returns an instance of its own class, standing in place of a public constructor. Because it has a name it can say what it makes; and because it is a method rather than a constructor, it is free to hand back a cached object, or a subtype, instead of always building something new. That's the idea in a sentence, and if you've ever written List dot of, you have already used it — you just didn't know it had a name. The rest of the video does it properly, by building a real working Java project: a small e-commerce checkout, in Java 21. By the end you'll know exactly what it buys you, and exactly where it runs out of road.

## Scene 2 — The Job

So here's the job. We've got an online shop. It prices an order, and it applies a discount to it. And the shop needs a few different kinds. Ten percent off. Five pounds off. Free shipping. Nothing at all. And one more that's a bit clever, it picks whichever of two others saves the customer more. Now the checkout, it shouldn't care which one it got handed. It should just apply the thing and move on.

## Scene 3 — The First Attempt Does Not Compile

Okay, so you start where everyone starts. Constructors. Ten percent off, that's one number. Five pounds off, also one number. So, two constructors, each taking a double. And it doesn't compile. Java tells you the constructor is already defined. Now, why? A constructor's name is fixed. It's the name of the class, you don't get to pick it. So the only thing that can tell two constructors apart is the list of parameter types. And both of these take a double. To the compiler, these are the same constructor, written out twice. The difference, percent versus pounds, that only exists in your head. There's literally nowhere in the code to put it.

## Scene 4 — So Everyone Writes This Instead

So what does everybody do instead? You widen the constructor until every kind fits through it. One constructor, three parameters, and an unwritten rule that you zero out whatever you're not using. Now look at those four call sites, and tell me which one gives five pounds off. You can work it out. But you're counting commas to do it. And that last one, all zeros? That's a discount that does nothing. Nothing in that line tells you so.

## Scene 5 — Why That Hurts

And that costs you. Five separate ways. One. The call site doesn't say what it means any more. Two. Nothing stops somebody passing a percentage, and an amount, and free shipping, all at once. Which is nonsense, and the compiler will take it quite happily. Three. Every kind of discount is carrying fields that belong to the other kinds. Four. Adding a new kind means changing the constructor, so every caller changes with it. And five. The word new always allocates. So even a discount of nothing makes you a brand new object, every single time you ask for one. But notice what isn't wrong here. The type is fine. It's the way in that's the problem.

## Scene 6 — The Static Factory Method

Right, so the fix has a name. A static factory method is just a static method that returns an instance of its own class, and you use it instead of a public constructor. It's item one in Effective Java, the very first thing in the book. In plain words? You give the constructor a name. That's it. That's the whole idea. One warning before we carry on, and this one matters. This is not a Gang of Four pattern. And despite the word factory being in there, it is not the same thing as the Factory Method pattern. They share a word. That's all they share. Don't let anybody tell you different in an interview.

## Scene 7 — A Vending Machine

Think about a vending machine. You press a button with a label on it. You don't open up the front and reach inside. The button has a name, so you always know what you asked for. The machine works out which shelf and which slot, and honestly, that's its business, not yours. It might hand you one it already had sitting there. And if you press a button that means nothing, well, it doesn't have to manufacture anything at all. And that's the whole idea, really. You're asking for an outcome. You're not asking for a manufacturing step.

## Scene 8 — The Shape of It

So here's the shape of it. Your code sits up at the top, and it calls a named method on the Discount interface itself. The type is its own factory. There's no separate factory class anywhere in this project. None. Below the line are the five classes doing the actual work. And not one of them is public. So no code outside the package can even write their names down. Which means, and this is the good bit, all five of them could be renamed tomorrow. Or merged. Or deleted. And not a single caller would break. They never knew they were there.

## Scene 9 — The Type Is Its Own Factory

And here's the code. Since Java 8, an interface can hold static methods, so all six ways in live on Discount itself. Just read the names. None. Percentage. Amount off. Free shipping. Best of. For coupon. You know what every one of those does without reading a single line inside them. And percentage and amount off? Those two could never have been constructors. One takes a number, and so does the other. As named methods, they sit right next to each other, and nobody is ever going to confuse them. That's the first freedom. And honestly, on its own, it'd already be worth doing.

## Scene 10 — Freedom Two: Not to Allocate

Now, the freedom a constructor can never have. A discount of nothing has no state. There's no reason for two of them to exist. Ever. So the class keeps one shared instance, hides its constructor away, and the none method hands you back that same object every single time. And think about what new actually means. It's defined as making something new. It has no way of saying, actually, here's one I already had. A named method does. This is exactly why Integer dot value of exists. And exactly why calling new Integer is deprecated.

## Scene 11 — Freedom Three: to Choose the Class

The third freedom, this is the deep one. A static factory method doesn't have to return the class you'd expect. Ask for a percentage discount of zero. You don't get a percentage discount holding a zero. You get the shared do nothing one instead. And nobody outside can tell. Nobody outside can complain either, because the return type was only ever Discount. You asked for an outcome, so the method is free to serve it however it likes. Have a look at the validation as well. It runs before anything gets built. A constructor can throw too, sure, but only after you've already committed to the word new.

## Scene 12 — What the Client Looks Like

And this. This is the payoff. The whole checkout. Go looking for the word new applied to a discount. There isn't one. Look for a branch on the kind of discount. There isn't one. Look for any of those five class names. Not one of them is in here. It takes a Discount, asks it what it's worth, and subtracts it. That's all it does. Every decision got made inside a factory method, long before this line ever ran.

## Scene 13 — The Same Trick on a Value Type

The same trick works beautifully on a small value type. Money dot pounds of five, and Money dot pence of five. Two completely different amounts of money. As constructors, they could never have lived side by side, because both of them take a number. As named methods, they read themselves out loud, and nobody has to guess the unit. There's a parse method as well, for text coming in from the outside world. And money zero hands back one shared instance, for exactly the same reason the no discount one does.

## Scene 14 — You Already Use This Every Day

Here's the thing, though. You're not learning something new. You're learning the name of something you already do. List of. Integer value of. Optional empty. Local date now. String value of. Every single one of those is a static factory method. And this next bit is worth hanging on to. List dot of gives you back a different class depending on how many elements you pass it. There are special implementations for zero, for one, and for two. You've never noticed. It's never once caused you a problem. That's the third freedom, working away quietly, in code you use every day. And those names along the bottom, they're the conventions the whole ecosystem follows. Of. From. Value of. Get instance. New instance. Parse. Copy of. Use those, and your code reads like the standard library.

## Scene 15 — Running It

Let's run it, and you can see the whole lot on one screen. Every coupon code coming in from the storefront goes through the for coupon method, and that returns whichever implementation fits. That best deal code builds a composite, holding two other discounts, and that's a class the caller couldn't possibly have assembled itself, because it can't name any of the three. Then look at the proof down at the bottom. Two methods that could never have been two constructors. A none that genuinely is shared. A percentage of zero, quietly turning into the do nothing discount. And an unknown coupon, turned away before a single object was created.

## Scene 16 — Where It Stops

Right. Now the honest part, because everything has a ceiling. Hiding the constructor means nobody outside can subclass your implementations. For value types, that's usually a feature rather than a bug. But every now and then, it's a real problem for somebody. Static factories are also harder to find. There's no new to search for. It's just a method, sitting there among all the others. And then the big one. A static method is resolved at compile time. It can't be overridden. So a subclass can't change what gets built, and neither can a config file. The day you need that, you've outgrown this technique. Oh, and one more thing. Don't go applying this everywhere. Order and Receipt in this project are plain records, with ordinary public constructors, because they've got nothing to decide. That contrast is completely deliberate.

## Scene 17 — The Rest of the Family

Which brings us neatly on to the rest of the family. The static factory says, give me one that does this. No factory class at all. The simple factory asks, which one? and moves that question out into a helper class with a switch in it. Factory method asks which one, and lets a subclass answer, so the decision moves into the type system. And the abstract factory asks, which whole matching set? One choice, and you get many related objects out of it. Every one of those exists because the one before it hits a ceiling. So start here. And move up only when something genuinely forces you to.

## Scene 18 — One Sentence to Keep

If you keep one sentence from all of this, keep this one. A constructor can't be named, and it can't refuse to allocate. A static factory method does both. And everything else we've talked about follows from those two things. There's a full set of notes in the project, an animated walkthrough you can step through at your own pace, and a session plan if you fancy teaching this to somebody else. Go and add a discount of your own. That's the best way to make it stick.

## Scene 19 — Thanks for Watching

And that's the static factory method. If you got something out of this, do give it a thumbs up, and subscribe. It genuinely helps the channel, and it's what makes more of these possible. And if there's a pattern you'd like me to cover next, drop it in the comments. I read every one. All the source code, the written notes and the diagrams are in the repository. Thanks for watching, and I'll see you in the next one.
