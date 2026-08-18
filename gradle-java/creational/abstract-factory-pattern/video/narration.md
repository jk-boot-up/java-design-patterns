# Abstract Factory Pattern — Video Narration Script

The full spoken script, scene by scene. This is the human-readable copy;
the authoritative text lives in the `narration` field of each scene in
[`scenes.py`](scenes.py), next to the slide it belongs to.

**Voice:** female (macOS `Samantha`, US English), rate 170 wpm.
**Runtime:** approximately 9 minutes.

Some words are spelled out phonetically for the synthesiser — "V A T"
rather than "VAT". Keep that habit if you edit the script, or the
narration will mispronounce them.

---

## Scene 1 — The Abstract Factory Pattern

Hello, and welcome. In this short video we are going to learn the Abstract
Factory, the most ambitious of the factory patterns in the Gang of Four
book. It sounds intimidating, and I think that is entirely the name's fault.
The idea underneath is simple and you will recognise it from real life. So
we will learn it by building a real, working Java project, the checkout step
of an online store that sells into three countries. By the end you will know
what an abstract factory is, why it exists, and honestly, when not to use
it.

## Scene 2 — The Scenario

Imagine your online store has been selling in one country, and now it sells
in three. You quickly discover that checkout is not one piece of logic. It
is three. There is the tax to work out. There is the money to format. And
there is the delivery address to validate. In Britain that is twenty percent
value added tax, prices in pounds, and a postcode. In America it is sales
tax, dollars, and a zip code. In India it is goods and services tax, rupees,
and a pin code. Three countries, three sets of rules, and all three parts
change together.

## Scene 3 — Nine Classes, Three Legal Combinations

So you write the classes. Three tax calculators, three currency formatters,
three address validators. Nine small classes, and each one is easy. Here
they all are, laid out as a grid. Now read the grid downwards, and each
column is just an ordinary interface with three implementations. Nothing new
there. But read it across, and each row is something more interesting. A row
is a family. Three objects that were designed to be used together. And here
is the whole problem in one sentence. There are nine classes, but only three
combinations of them are legal.

## Scene 4 — The Problem

Without a pattern, the checkout picks each piece for itself. Here is what
that looks like. One chain of conditions to choose the tax calculator.
Another chain, on the very same string, to choose the currency formatter.
And a third one, off the bottom of the screen, for the address validator.
Now, none of this is wrong exactly. It compiles. It runs. But look at what
you have built. Three separate decisions, that must all agree with each
other, and nothing whatsoever checking that they do.

## Scene 5 — Why That Hurts

And that costs you. Reorder the cases in the middle chain and forget the
other two, and you have built a checkout that charges British tax and prints
it in dollars. A mismatched family is one copy and paste away. When Germany
arrives, you open a class that takes real money and edit it in three
separate places. And your checkout, which should be about totals and
receipts, has become a directory of nine class names. But here is the worst
part. None of this fails loudly. It compiles, it runs, and it quietly
produces a wrong invoice.

## Scene 6 — The Abstract Factory Pattern

This is exactly the problem the Abstract Factory pattern solves. The formal
definition goes like this. Provide an interface for creating families of
related or dependent objects, without specifying their concrete classes. The
word doing all the work in that sentence is families. In plain English, the
pattern says this. Choose a whole set at once, instead of a piece at a time.
And if your objects have no reason to match each other, then you do not need
this pattern at all.

## Scene 7 — The Set Menu

Here is the way to remember it forever. Think about ordering dinner. You can
order à la carte. Pick a starter, pick a main, pick a wine. Three free
decisions, and nothing at all stops you putting a delicate fish next to a
heavy red. The kitchen will serve it. It will simply be wrong. Or, you can
order the set menu. You choose one thing. You say, the tasting menu, please.
And three courses arrive that were designed together. You never named a
single dish. The set menu takes your freedom away on purpose, and that is
exactly what you are paying for.

## Scene 8 — The Roles

So let us map that onto code. There are five roles. At the top is the
client, our checkout service. It holds one factory and it names no country
anywhere. In the middle is the abstract factory, market factory, which
declares one creation method per product kind. Below it are the concrete
factories, one per country, and each of those builds one complete family.
And then there are the products themselves. Three interfaces, the abstract
products, and nine classes behind them, the concrete products. Now watch the
arrows. Every creates arrow leaves exactly one factory. There is no path in
this picture that puts a British tax rate next to an American address.

## Scene 9 — The Abstract Factory

Here is the abstract factory itself, and it is smaller than you might
expect. Four methods, and not one line of implementation. Look at the return
types. All three are interfaces, so nothing here reveals that a pound
formatter even exists. But the really important thing about this interface
is what is missing from it. Find me the parameter that says which country.
There isn't one. The country is not an argument anywhere, because it was
already decided, at the moment somebody chose which factory to use.

## Scene 10 — A Concrete Factory

And here is one concrete factory. Three new calls, in a class whose name
says British. That is the entire consistency guarantee, and it is worth
pausing to appreciate how cheap it is. Ask yourself, how many lines of code
here check that these three products match? Zero. Nothing is validated. They
match because this is the only place the choice is made, and there is
nowhere else that could get it wrong. The American and Indian factories are
the same shape with different nouns.

## Scene 11 — The Client

Now the client, and this is the part I want you to really look at. Four
lines in the constructor, and the whole world is set up. After that last
line, the factory has done its job and is never touched again. It was a
decision, not a dependency. And then read the method underneath. Search it
for the letters U, K. Search it for India. There is nothing. Not one branch
on the country. Even the error message is correct in every market, because
the words in it, United States, zip code, came from the products themselves.

## Scene 12 — What You Gain

So what did all that buy us? The headline is this. A mismatched family is
not caught, it is impossible. Nothing is being validated. There is simply no
code anywhere that could produce one. There is one decision now instead of
three. The client shrank from nine class names down to three interfaces and
no country codes at all. Adding a new market is purely additive, you add
files and edit none. In fact the test suite in this project invents a German
market inside a single test method, and the unchanged checkout quotes it
correctly. And finally, the British market is now an actual object, that you
can build, pass around, and write a test about.

## Scene 13 — The Honest Cost

But I would be doing you a disservice if I stopped there, because this
pattern has a real cost and you should know it before you reach for it.
Adding a new country is cheap. One factory, three products, nothing edited.
But suppose checkout now needs a receipt template as well. That is a new
kind of product, and you have to add a method to the abstract factory, which
means editing every single factory you have. Rows are cheap. Columns are
expensive. Beyond that, your class count is countries multiplied by product
kinds, so be sure the families are real. Something, somewhere, still has to
choose which factory to use. And here is the honest test for whether you
need this at all. Would a mismatched pair be a bug? If the answer is no,
inject the objects separately and walk away.

## Scene 14 — Running It

Here is the program actually running. The same order, worth one hundred and
twenty, quoted in three countries. Britain adds twenty percent and prints
pounds. America adds its sales tax and prints dollars. India adds eighteen
percent and prints rupees. Now, the important thing. Those nine lines were
produced by one method, and that method contains no condition on the country
at all. Only the factory changed. And look at the last line. The demo
deliberately sends a British postcode to the American market, and it is
turned away, because the validator came from the same family as the money.

## Scene 15 — Wrap Up

So, to wrap up. Reach for the Abstract Factory when several objects have to
agree with each other. Skip it when they do not, because then you are only
adding classes. And if you have seen the other two factory patterns, here is
how they line up. A simple factory chooses with a switch. A factory method
chooses with inheritance. An abstract factory chooses a whole family at
once. If you remember one sentence from this video, make it this one. If
getting two objects from different groups would be a bug, you want an
abstract factory. The full source code, the written notes and an interactive
animation are all in the repository. Thank you for watching, and enjoy the
pattern.

