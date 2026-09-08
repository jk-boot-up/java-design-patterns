# Factory Method Pattern — Narration Script

The full spoken script for `factory-method-pattern-explained.mp4`, scene by
scene. This is the human-readable copy used for review; the authoritative
text lives next to each slide in [`scenes.py`](scenes.py). If you change the
wording there, update this file too.

- **Voice:** macOS `Samantha` (female, US English) at 145 words per minute
- **Runtime:** approximately 8 minutes.
- **Audience:** beginners with no prior design-pattern knowledge

A note on spelling: a few words are written the way they should be *spoken*
rather than the way they are written in code — "sky link air" instead of
"SkyLink Air" — because the speech synthesiser mangles them otherwise. Keep
that habit if you edit the script.

The first and last scenes carry the channel branding: scene 1 credits
the author out loud over the poster, and the final scene asks for the
thumbs up and the subscribe.

The script is written to be spoken rather than read, and carries `[[slnc NNN]]`
pause markers in [`scenes.py`](scenes.py) that insert NNN milliseconds of
silence. Those are instructions to the synthesiser, not words: they are
stripped from the text below and from the subtitles.



## 1. The Factory Method Pattern

Hello, and welcome. This video explains the Factory Method pattern in Java,
and it is written and presented by Jayasekhar Konduru. Let's start with the
simple definition. The factory method pattern moves the creation of an
object into a method that subclasses override. A base class writes down the
steps that never change and calls that method wherever a new object is
needed, so each subclass decides which class gets created without a line of
the surrounding code changing. That's the idea in a sentence. It has a
reputation for being confusing, and honestly I think that's only the way it
usually gets explained, so the rest of the video does it properly, by
building a real working Java project: the delivery step of an online store.
By the end you'll know what a factory method is, why it exists, and how to
write one yourself.

## 2. The Scenario

So, imagine you're building an online store. A customer checks out, and
picks a delivery tier. Standard goes by post, takes five days. Express
flies overnight. Same day goes out on a bike. And international crosses a
border. Four different carriers, four different prices, four different
delivery dates. But here's the detail that matters. Every single one of
them runs the same shipping workflow around that carrier.

## 3. The Workflow Is Always the Same

Look at what shipping actually involves. First, we check the order really
has some weight to it. Then we log that we're preparing the parcel. Then
we hand it over to the carrier. And finally we log the tracking number and
the promised date. Steps one, two and four are identical for every tier.
Forever. Only step three, the hand over, is different. Hold on to that,
because it's the whole reason this pattern exists.

## 4. The Problem — One Class Doing Both Jobs

So here's the naive version. And honestly, it's what most of us would
write first. One shipping method, with a chain of if and else sitting
right in the middle of it. The workflow is in there. The choosing is in
there. They're tangled together in the same method, and you can't read one
without reading the other.

## 5. Why That Hurts

Now. We're launching drone delivery on Monday. Which file do you open?
This one. The one that already ships real parcels, for four tiers, today.
And every edit to working code is a chance to break something that was
perfectly fine. And it gets worse. If international also needs a customs
check, you now need a second if chain on the same string, and those two
have to stay in step with each other. A partner team can't add a tier at
all. And you can never test the shared workflow separately from the
choosing, because they're one method.

## 6. The Factory Method

The factory method fixes exactly this. The Gang of Four define it as,
define an interface for creating an object, but let subclasses decide
which class to instantiate. Now that sentence is precise. It's also
exactly why the pattern confuses people. So here it is in plain language.
You write the workflow once, and you leave a hole in the middle of it.
Then you let a subclass fill in that hole. That's it. That's the entire
pattern.

## 7. Remember It With a Coffee Chain

Here's how to remember it forever. Think about a coffee shop chain. Head
office writes the recipe card for serving a hot drink. Step one, greet the
customer. Step two, make the drink. Step three, put a lid on it, call out
the name, hand it over. Steps one and three are identical in every branch
in the world, and head office owns them. Step two is deliberately left
blank. The Tokyo branch makes matcha. The Rome branch makes espresso. And
head office never learns what matcha even is. It only knows that whatever
comes back can have a lid put on it.

## 8. The Four Roles

Every factory method has four roles. First, the product, which is our
Courier interface. Second, the concrete products, our four carrier
classes. Third, the creator, and that's Delivery Service, the abstract
class that owns the workflow and declares the factory method. And fourth,
the concrete creators, our four delivery tiers, each one answering a
single question. Which courier. And here's the most important idea in the
whole video. The parent class writes the call. The child class decides
what comes back.

## 9. A Product — Small, Focused, Unaware

Let's look at some code. This is the air courier. Notice how small it is.
How ordinary. It knows its own name, its own tracking prefix, its own
speed, and its own pricing. And it has absolutely no idea that a delivery
tier exists, or that three other carriers exist. Which is deliberate. The
other three carriers follow exactly the same shape.

## 10. The Creator — A Workflow With a Hole in It

And this is the heart of it. Read the ship method, and label every line as
either shared, or varies. The guard is shared. The two log lines are
shared. There's exactly one line that varies, and it's the call to create
courier. Now look at the top of the class. Create courier is abstract. It
has no body. So the parent class has written a call that it cannot answer
itself. And notice that ship is marked final. A subclass may change which
courier gets used, and nothing else. Not the guard. Not the logging. Not
the order of the steps.

## 11. A Concrete Creator — Six Lines

And here's an entire delivery tier. Six lines. It picks a courier, it
names itself, and that's all it does. All four tiers look exactly like
this. Now go and search the whole project for the word switch. There isn't
one. Search for an if statement testing a tier name. There isn't one of
those either. The decision that used to be a branch is now a class. And
choosing a class is something Java's own method dispatch does for us, for
free.

## 12. What You Gain

So what did that actually buy us? Monday's drone delivery is now a new
file, and we never touch an existing class. That's the Open Closed
Principle genuinely satisfied, not just talked about. The weight guard is
written once, and it protects every tier that will ever exist, including
ones written next year, by somebody else. A separate team can ship a tier
in their own jar. And if a subclass forgets to override the factory
method, it won't even compile. Now compare that to its simpler cousin. A
simple factory moves the switch into one file. A factory method removes
the switch entirely.

## 13. Running It

When we run the project, you can watch it happen. Here are two of the four
tiers, shipping the very same order. Look at the first and last line of
each block. Same shape, same wording, same workflow. Only the middle line,
the one the carrier itself printed, is different. And so are the price and
the delivery date. That's the pattern working. One shared workflow,
running completely different carriers.

## 14. Wrap Up

So, to recap. Use a factory method when you've got a workflow that's
shared, with one step that varies, and that step creates an object. Keep
the return type abstract. The moment your creator says it returns an air
courier, all that coupling you just removed comes straight back. Never
call the factory method from a constructor, because the subclass fields
aren't ready yet. And be honest with yourself. If the only difference
between your subclasses is one call to new, then a plain supplier passed
into the constructor may be all you need. Don't go building a hierarchy
just to avoid a two line switch. And if you remember one sentence from
today, make it this one. A simple factory chooses with a switch. A factory
method chooses with inheritance.

## 15. Thanks for Watching

And that's the factory method. If you got something out of this, do give
it a thumbs up, and subscribe. It genuinely helps the channel, and it's
what makes more of these possible. And if there's a pattern you'd like me
to cover next, drop it in the comments. I read every one. All the source
code, the written notes and an interactive animation are in the
repository. Thanks for watching, and I'll see you in the next one.
