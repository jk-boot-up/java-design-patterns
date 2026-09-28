# The Factory Method Pattern Pattern — Video Narration Script

## 1. The Factory Method Pattern

Hello, and welcome. This video explains the Factory Method pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Factory Method pattern moves the creation of an object into a method that subclasses override. A base class writes the steps that never change. Wherever it needs a new object, it calls that method. So each subclass decides which class gets created, and the surrounding code never changes. Think of a coffee chain's recipe card. Head office writes every step, but leaves, make the drink, blank. Each branch fills in its own drink. In this video, we build the delivery step of an online store. By the end, you will know what a factory method is, why it exists, and how to write one yourself.

## 2. The Scenario

Here is the scenario. A customer checks out, and picks a delivery option. Standard delivery goes by post, and takes five days. Express flies overnight, and takes two days. Same day goes out on a bike. And international crosses a border, and takes nine days. Four different carriers, with different prices, and different delivery dates. But here is the important detail. Every one of them runs the same shipping steps around its carrier.

## 3. The Workflow Is Always the Same

Let's list what shipping involves. Step one: check the order really has some weight. Step two: log that we are preparing the parcel. Step three: hand it to the carrier. Step four: log the tracking number, and the promised date. Steps one, two, and four are identical for every delivery option. Only step three, the hand-over, is different. Remember that, because it is the whole reason this pattern exists.

## 4. The Problem — One Class Doing Both Jobs

Here is the naive version, and it is what most of us would write first. One shipping method, with a chain of if statements in the middle, choosing the carrier by name. The shared steps are in there. The choosing is in there. They are tangled together, and you cannot read one without the other.

## 5. Why That Hurts

Now, drone delivery launches on Monday. Which file do you open? This one. The one that already ships real parcels, for four delivery options, today. And every edit to working code is a chance to break something. It gets worse. If international also needs a customs check, you need a second if chain, on the same name. And the two chains must always stay in step. A partner team cannot add a delivery option at all. And you cannot test the shared steps without the choosing, because they are one method.

## 6. The Factory Method

The Factory Method fixes exactly this. Here is its definition, from the famous Gang of Four book. Define an interface for creating an object, but let subclasses decide which class to create. That is precise, but it confuses many people. So here it is in plain words. Write the steps once, and leave a gap in the middle. Then let a subclass fill in that gap. That is the whole pattern.

## 7. Remember It With a Coffee Chain

Here is an easy way to remember it: a coffee shop chain. Head office writes the recipe card for serving a hot drink. Step one: greet the customer. Step two: make the drink. Step three: put a lid on, call out the name, and hand it over. Steps one and three are the same in every branch in the world. Step two is left blank, on purpose. The Tokyo branch makes matcha. The Rome branch makes espresso. And head office never needs to know what matcha is. It only knows that whatever comes back can have a lid put on it.

## 8. The Four Roles

Every factory method has four roles. First, the product: our Courier interface. Second, the concrete products: the four carrier classes. Third, the creator: an abstract class called Delivery Service. It owns the shared steps, and declares the factory method. Fourth, the concrete creators: the four delivery options. Each one answers a single question: which courier? And here is the most important idea in the video. The parent class makes the call. The child class decides what comes back.

## 9. A Product — Small, Focused, Unaware

Let's look at one product: the air courier. Notice how small, and ordinary, it is. It knows its own name, SkyLink Air. Its own tracking prefix, its own speed of two days, and its own pricing. And it has no idea that delivery options exist, or that three other carriers exist. That is deliberate. The other three carriers follow exactly the same shape.

## 10. The Creator — A Workflow With a Hole in It

And this is the heart of it: the Delivery Service class. Go through its ship method, step by step, and label each step shared, or varying. The weight check is shared. The two log lines are shared. Exactly one line varies: the call to create courier. And create courier is abstract. It has no body. So the parent class makes a call that it cannot answer itself. Notice too that the ship method is marked final. A subclass may change which courier is used, and nothing else. Not the check, not the logging, and not the order of the steps.

## 11. A Concrete Creator — Six Lines

Here is an entire delivery option: Express Delivery. It is six lines long. Its create courier method returns a new air courier. And it names itself, Express. That is all it does. All four delivery options look exactly like this. Search the whole project for a switch statement. There is none. Search for an if statement that tests a delivery name. There is none of those either. The decision that used to be a branch is now a class. And choosing a class is something Java already does for us, for free.

## 12. What You Gain

So what did that buy us? Monday's drone delivery is now one new file. No existing class is touched. That is the Open Closed Principle, really working. The weight check is written once, and it protects every delivery option that will ever exist. Another team can add a delivery option in their own library. And if a subclass forgets to provide a courier, it will not even compile. Compare that with its simpler cousin. A simple factory moves the switch statement into one file. A factory method removes the switch statement entirely.

## 13. Running It

Let's run the demo. Two of the delivery options ship the very same order, to Edinburgh. Each begins with the same line: preparing the order. And each ends with the same line: booked, with a tracking number and a delivery date. Only the middle line is different, printed by the carrier itself. Royal Post drops it into the postal network. SkyLink Air books it onto tonight's flight. One shared set of steps, running completely different carriers.

## 14. Wrap Up

So, to recap. Use a factory method when you have shared steps, with one step that varies, and that step creates an object. Keep the method's return type abstract. The moment it promises a specific carrier class, the coupling comes straight back. Never call the factory method from a constructor. The subclass is not fully ready at that point. And be honest with yourself. If the only difference between subclasses is one new object, simply passing in a supplier may be enough. Do not build a class hierarchy just to avoid a two-line switch. And one sentence to remember. A simple factory chooses with a switch. A factory method chooses with inheritance.

## 15. Thanks for Watching

That's the Factory Method pattern. If you remember one sentence, make it this one. Write the shared steps once, leave a gap, and let each subclass fill it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. If there is a pattern you would like to see covered, suggest it in the comments. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
