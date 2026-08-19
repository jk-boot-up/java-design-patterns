# Simple Factory Pattern — Narration Script

The full spoken script for `simple-factory-pattern-explained.mp4`, scene by
scene. This is the human-readable copy used for review; the authoritative
text lives next to each slide in [`scenes.py`](scenes.py). If you change the
wording there, update this file too.

- **Voice:** macOS `Samantha` (female, US English) at 165 words per minute
- **Runtime:** approximately 7 and a half minutes.
- **Audience:** beginners with no prior design-pattern knowledge

A note on spelling: a few words are written the way they should be *spoken*
rather than the way they are written in code — "U P I" instead of "UPI",
"pay pal" instead of "PayPal" — because the speech synthesiser mangles them
otherwise. Keep that habit if you edit the script.

The first and last scenes carry the channel branding: scene 1 credits
the author out loud over the poster, and the final scene asks for the
thumbs up and the subscribe.

The script is written to be spoken rather than read, and carries `[[slnc NNN]]`
pause markers in [`scenes.py`](scenes.py) that insert NNN milliseconds of
silence. Those are instructions to the synthesiser, not words: they are
stripped from the text below and from the subtitles.



## 1. The Simple Factory Pattern

Hello, and welcome. This one is written and presented by Jayasekhar
Konduru. Today we are doing the pattern that almost every Java developer
writes long before they know it has a name. The simple factory. And we
will learn it properly, by building a real working Java project. The
payment step of an online store. By the end you'll know what a factory is,
why it exists, and how to write one yourself.

## 2. The Scenario

So, imagine you are building an online store. A customer gets to the
payment page, and picks how they want to pay. Now your code has to run one
of four things. A credit card payment. A U P I payment. A pay pal payment.
Or net banking. And here's the detail that matters. That choice arrives as
data. It comes from a dropdown, or a JSON field, or a database column.
It's a string, or an enum. It's not a Java type.

## 3. One Interface, Four Implementations

In our project, all four of them do the same job from the outside. They
take a payment request, and they give you back a receipt. So they share
one interface, called Payment Method, with two methods on it. Inside,
though, they're completely different. The card one authorises, and then
captures. The U P I one sends a collect request, and waits. But from the
outside? Interchangeable. And that's what makes everything else in this
video possible.

## 4. The Problem — Everyone Chooses for Themselves

Right, so here's the problem. Without a factory, whoever needs a payment
method decides for themselves. This chain of if and else lives inside the
checkout code. And our website has a copy of it. The mobile app has a
copy. The admin tool has a copy. The same fragile block, written out three
times, by three people, on three different days.

## 5. Why That Hurts

And that does real damage. A class whose only job is to check out now
knows the name of every single payment class in the system. When we add
wallet payments next month, we've to go and find every caller and edit it.
And if we miss one, it fails in front of a customer. One copy trims the
input string. Another one forgets. And you can't test the choosing on its
own, because it is welded to the checkout code around it.

## 6. The Simple Factory

The simple factory fixes exactly this. It takes the decision of which
class to instantiate, and puts it into one method, so callers can ask for
an object by name instead of building it themselves. One quick note,
because this confuses everybody at first. Simple factory isn't one of the
twenty three Gang of Four patterns. It's an idiom. It's the one everybody
actually writes. And it's the natural first step towards the real
creational patterns. In plain language? It's one place that knows how to
make things.

## 7. Remember It With a Coffee Shop

Here's how to remember it forever. Think about a coffee shop. You don't
walk behind the counter, find the espresso machine, grind the beans and
steam the milk. You say, a cappuccino please. And a cappuccino arrives.
You named what you wanted. Somebody else knew how to make it. And
tomorrow, when the shop buys a better machine, your order doesn't change
one bit. Because you never knew how it was made in the first place. The
counter is the factory.

## 8. The Four Roles

Every factory has four roles. First, the product, which is our Payment
Method interface. Second, the concrete products, which are our four
payment classes. Third, the factory itself, which here's the Payment
Method Factory. And fourth, the client. The code that just wants to take a
payment. Now this next bit's the single most important idea in the whole
video, so stay with me. The client names the type, as data. The factory
names the class. Go and search the client for the words credit card
payment. You'll not find them anywhere. That's the test of whether you
have actually applied the pattern.

## 9. A Product — Small, Focused, Unaware

Let's look at some code. This is the U P I payment. And notice how small
it is. How ordinary. It gives its display name, and it takes the payment.
That's it. It has absolutely no idea a factory exists. Which is
deliberate. Because it knows nothing about who created it, you could lift
this class straight into a completely different application tomorrow. The
other three payment methods follow exactly the same shape.

## 10. The Factory — One Switch, One Place

And this is the factory itself. One static method, one switch. This is now
the only place in the entire codebase that calls new on a payment class.
Now look carefully at that switch, because something is missing. There's
no default branch. And that's on purpose. Payment Type is an enum, and
Payment Method is a sealed interface, so the compiler knows the complete
list, and it knows this switch covers every case. Add a fifth payment type
tomorrow, and this file stops compiling until you handle it. So a
forgotten case becomes a build error, instead of a customer complaint.

## 11. What the Factory Gives You

So the factory is giving us three things. It chooses the implementation
from data, in exactly one place. It constructs it, so no caller ever
writes new. And it validates the input, so every caller gets the same
error message. Now, let's be honest about the cost, because a good teacher
always should be. Adding a new payment method means modifying the factory.
And that breaks the Open Closed Principle, which says code should be open
to extension, but closed to modification. The simple factory doesn't
remove that cost. It just centralises it, into one file you can actually
find.

## 12. The Client — This Is the Whole Thing

And now, the payoff. This is the entire client code. One line to get hold
of the object, and then ordinary, everyday polymorphism. Our checkout
doesn't know that pay pal exists. It doesn't know net banking exists. It's
holding something typed as Payment Method, and it simply calls pay. Add a
fifth payment method tomorrow, and this code doesn't change at all. That's
the whole point of the pattern.

## 13. Running It

When we run the project, you can watch it happen. Here are two of the four
payments. Look at the checkout lines, the first and the last of each
block. They are identical. Only the middle lines, the ones the payment
method itself printed, are different. And that's the pattern working. The
same client code, running completely different implementations, chosen by
nothing more than a value.

## 14. Wrap Up

So, to recap. Use a simple factory when the class you need is decided by
data, and you want to spare your callers from knowing how it gets built.
Keep the factory thin. Its job is to choose, and to construct. Nothing
else. If you have only got one implementation, plain new is clearer, so
don't go inventing a factory for its own sake. And if you ever reach forty
cases, reach for a registry instead. And if you remember one sentence from
today, make it this one. A simple factory chooses with a switch. A factory
method chooses with inheritance. That second one is where you go next.

## 15. Thanks for Watching

And that's the simple factory. If you got something out of this, do give
it a thumbs up, and subscribe. It genuinely helps the channel, and it's
what makes more of these possible. And if there's a pattern you'd like me
to cover next, drop it in the comments. I read every one. All the source
code, the written notes and an interactive animation are in the
repository. Thanks for watching, and I will see you in the next one.
