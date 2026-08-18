# Factory Method Pattern — Narration Script

The full spoken script for `factory-method-pattern-explained.mp4`, scene by
scene. This is the human-readable copy used for review; the authoritative
text lives next to each slide in [`scenes.py`](scenes.py). If you change the
wording there, update this file too.

- **Voice:** macOS `Samantha` (female, US English) at 170 words per minute
- **Runtime:** approximately 7 minutes
- **Audience:** beginners with no prior design-pattern knowledge

A note on spelling: a few words are written the way they should be *spoken*
rather than the way they are written in code — "sky link air" instead of
"SkyLink Air" — because the speech synthesiser mangles them otherwise. Keep
that habit if you edit the script.

## 1. The Factory Method Pattern

Hello, and welcome. In this short video we are going to learn one of the most useful patterns in the Gang of Four book: the Factory Method. It has a reputation for being confusing, and I think that is only because of how it is usually explained. So we will learn it by building a real, working Java project, the delivery step of an online store. By the end you will know what a factory method is, why it exists, and how to write one yourself.

## 2. The Scenario

Imagine you are building an online store. A customer checks out and picks a delivery tier. Standard goes by post and takes five days. Express flies overnight. Same day goes out on a bike. International crosses a border. Four different carriers, four different prices, four different delivery dates. But, and this is the detail that matters, every single one of them runs the same shipping workflow around the carrier.

## 3. The Workflow Is Always the Same

Look at what shipping actually involves. First we check the order really has some weight. Then we log that we are preparing the parcel. Then we hand it over to the carrier. And finally we log the tracking number and the promised date. Steps one, two and four are identical for every tier, forever. Only step three, the hand over, is different. Hold on to that. It is the whole reason this pattern exists.

## 4. The Problem — One Class Doing Both Jobs

So here is the naive version, and honestly it is what most of us would write first. One shipping method, with a chain of if and else sitting right in the middle of it. The workflow is there. The choosing is there. They are tangled together in the same method, and you cannot read one without reading the other.

## 5. Why That Hurts

Now, we launch drone delivery on Monday. Which file do you open? This one. The one that already ships real parcels for four tiers today. Every edit to working code is a chance to break something that was fine. And it gets worse. If international also needs a customs check, you now need a second if chain on the same string, and the two have to stay in step. A partner team cannot add a tier at all. And you can never test the shared workflow separately from the choosing, because they are one method.

## 6. The Factory Method

The Factory Method solves exactly this. The Gang of Four define it as: define an interface for creating an object, but let subclasses decide which class to instantiate. That sentence is precise, and it is also why the pattern confuses people. So here it is in plain language. You write the workflow once, and you leave a hole in the middle of it. Then you let a subclass fill in that hole. That is the entire pattern.

## 7. Remember It With a Coffee Chain

Here is the way to remember it forever. Think about a coffee shop chain. Head office writes the recipe card for serving a hot drink. Step one, greet the customer. Step two, make the drink. Step three, put a lid on it, call out the name, hand it over. Steps one and three are identical in every branch in the world, and head office owns them. Step two is deliberately left blank. The Tokyo branch makes matcha. The Rome branch makes espresso. And head office never learns what matcha is. It only knows that whatever comes back can have a lid put on it.

## 8. The Four Roles

Every factory method has four roles. First, the product, which is our Courier interface. Second, the concrete products, our four carrier classes. Third, the creator. That is Delivery Service, the abstract class that owns the workflow and declares the factory method. And fourth, the concrete creators, our four delivery tiers, and each one answers a single question: which courier. Now here is the most important idea in this whole video. The parent class writes the call. The child class decides what comes back.

## 9. A Product — Small, Focused, Unaware

Let's look at some code. This is the air courier. Notice how small and how ordinary it is. It knows its own name, its own tracking prefix, its own speed and its own pricing. And it has absolutely no idea that a delivery tier exists, or that three other carriers exist. That is deliberate. The other three carriers follow exactly the same shape.

## 10. The Creator — A Workflow With a Hole in It

And this is the heart of it. Read the ship method and label every line as either shared, or varies. The guard is shared. The two log lines are shared. There is exactly one line that varies, and it is the call to create courier. Now look at the top of the class. Create courier is abstract. It has no body. The parent class has written a call that it cannot answer itself. Also notice that ship is marked final. A subclass may change which courier is used, and nothing else. Not the guard, not the logging, not the order of the steps.

## 11. A Concrete Creator — Six Lines

And here is an entire delivery tier. Six lines. It picks a courier, it names itself, and that is all it does. All four tiers look exactly like this. Now search the whole project for the word switch. There isn't one. Search for an if statement testing a tier name. There isn't one of those either. The decision that used to be a branch is now a class, and choosing a class is something Java's own method dispatch does for us, for free.

## 12. What You Gain

So what did that buy us? Monday's drone delivery is now a new file, and we never touch an existing class. That is the Open Closed Principle, actually satisfied, not just talked about. The weight guard is written once and it protects every tier that will ever exist, including ones written next year by somebody else. A separate team can ship a tier in their own jar. And if a subclass forgets to override the factory method, it will not compile. Now compare this to its simpler cousin. A Simple Factory moves the switch into one file. A Factory Method removes the switch entirely.

## 13. Running It

When we run the project, we can watch it happen. Here are two of the four tiers, shipping the very same order. Look at the first and last line of each block. Same shape, same wording, same workflow. Only the middle line, the one the carrier itself printed, is different, and so are the price and the delivery date. That is the pattern working. One shared workflow, running completely different carriers.

## 14. Wrap Up

So, to recap. Use a Factory Method when you have a workflow that is shared, with one step that varies, and that step creates an object. Keep the return type abstract. The moment your creator says it returns an air courier, all the coupling you removed comes straight back. Never call the factory method from a constructor, because the subclass fields are not ready yet. And be honest with yourself. If the only difference between your subclasses is one call to new, a plain supplier passed into the constructor may be all you need. Do not build a hierarchy to avoid a two line switch. If you remember just one sentence from today, make it this one: a Simple Factory chooses with a switch, and a Factory Method chooses with inheritance. Thank you for watching, and enjoy building your own creators.
