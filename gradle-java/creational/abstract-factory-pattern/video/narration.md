# Abstract Factory Pattern — Video Narration Script

The full spoken script, scene by scene. This is the human-readable copy;
the authoritative text lives in the `narration` field of each scene in
[`scenes.py`](scenes.py), next to the slide it belongs to.

**Voice:** female (macOS `Samantha`, US English), rate 165 wpm.
**Runtime:** approximately 9 and a half minutes.

Some words are spelled out phonetically for the synthesiser — "V A T"
rather than "VAT". Keep that habit if you edit the script, or the
narration will mispronounce them.

The first and last scenes carry the channel branding: scene 1 credits the
author out loud over the poster, and the final scene asks for the thumbs up
and the subscribe.

The script is written to be spoken rather than read, and carries `[[slnc NNN]]`
pause markers in [`scenes.py`](scenes.py) that insert NNN milliseconds of
silence. Those are instructions to the synthesiser, not words: they are
stripped from the text below and from the subtitles.

---

## Scene 1 — The Abstract Factory Pattern

Hello, and welcome. This one is written and presented by Jayasekhar
Konduru. Today we're doing the abstract factory. It's the most ambitious
of the factory patterns in the Gang of Four book. It sounds intimidating,
and honestly, I think that's entirely the name's fault, because the idea
underneath is simple, and you'll recognise it straight away from real
life. We'll learn it by building a real working Java project. The checkout
step of an online store that sells into three countries. And by the end
you'll know what an abstract factory is, why it exists, and, just as
importantly, when not to use it.

## Scene 2 — The Scenario

So, imagine your online store has been selling in one country, and now it
sells in three. And you quickly discover that checkout isn't one piece of
logic. It's three. There's the tax to work out. There's the money to
format. And there's the delivery address to validate. In Britain that's
twenty percent value added tax, prices in pounds, and a postcode. In
America, sales tax, dollars, and a zip code. In India, goods and services
tax, rupees, and a pin code. Three countries, three sets of rules. And all
three parts change together.

## Scene 3 — Nine Classes, Three Legal Combinations

So you write the classes. Three tax calculators, three currency
formatters, three address validators. Nine small classes, and each one of
them is easy. Here they all are, laid out as a grid. Now read the grid
downwards. Each column is just an ordinary interface with three
implementations. Nothing new there. But read it across, and each row is
something more interesting. A row is a family. Three objects that were
designed to be used together. And here's the whole problem, in one
sentence. There are nine classes, but only three combinations of them are
legal.

## Scene 4 — The Problem

Without a pattern, the checkout picks each piece for itself. Here's what
that looks like. One chain of conditions to choose the tax calculator.
Another chain, on the very same string, to choose the currency formatter.
And a third one, off the bottom of the screen, for the address validator.
Now, none of this is wrong, exactly. It compiles. It runs. But look at
what you've built. Three separate decisions, that all have to agree with
each other, and nothing whatsoever checking that they do.

## Scene 5 — Why That Hurts

And that costs you. Reorder the cases in the middle chain, forget the
other two, and you've built a checkout that charges British tax and prints
it in dollars. A mismatched family is one copy and paste away. When
Germany arrives, you're opening a class that handles real money and
editing it in three separate places. And your checkout, which should be
about totals and receipts, has turned into a directory of nine class
names. But here's the worst part. None of this fails loudly. It compiles,
it runs, and it quietly produces a wrong invoice.

## Scene 6 — The Abstract Factory Pattern

And this is exactly the problem the abstract factory solves. The formal
definition goes like this. Provide an interface for creating families of
related or dependent objects, without specifying their concrete classes.
The word doing all the work in that sentence is families. In plain
English, the pattern says, choose a whole set at once, instead of a piece
at a time. And if your objects have got no reason to match each other,
then you don't need this pattern at all.

## Scene 7 — The Set Menu

Here's how to remember it forever. Think about ordering dinner. You can
order a la carte. Pick a starter, pick a main, pick a wine. Three free
decisions, and nothing at all stops you putting a delicate fish next to a
heavy red. The kitchen will serve it. It'll simply be wrong. Or, you order
the set menu. And you choose one thing. You say, the tasting menu, please.
And three courses arrive that were designed together. You never named a
single dish. The set menu takes your freedom away on purpose. And that's
exactly what you're paying for.

## Scene 8 — The Roles

So let's map that onto code. There are five roles. At the top is the
client, our checkout service. It holds one factory, and it names no
country anywhere. In the middle is the abstract factory, market factory,
which declares one creation method per product kind. Below that are the
concrete factories, one per country, and each one builds a complete
family. And then the products themselves. Three interfaces, the abstract
products, and nine classes behind them, the concrete products. Now watch
the arrows. Every creates arrow leaves exactly one factory. There's no
path in this picture that puts a British tax rate next to an American
address.

## Scene 9 — The Abstract Factory

Here's the abstract factory itself, and it's smaller than you'd expect.
Four methods, and not one line of implementation. Look at the return
types. All three are interfaces, so nothing here even reveals that a pound
formatter exists. But the really important thing about this interface is
what's missing from it. Find me the parameter that says which country.
There isn't one. The country isn't an argument anywhere, because it was
already decided, at the moment somebody chose which factory to use.

## Scene 10 — A Concrete Factory

And here's one concrete factory. Three new calls, in a class whose name
says British. That's the entire consistency guarantee, and it's worth
pausing for a second to appreciate how cheap it is. Ask yourself, how many
lines of code in here check that these three products match? Zero. Nothing
is validated. They match because this is the only place the choice is
made, and there's nowhere else that could get it wrong. The American and
Indian factories are the same shape, with different nouns.

## Scene 11 — The Client

Now the client. And this is the part I really want you to look at. Four
lines in the constructor, and the whole world is set up. After that last
line, the factory has done its job, and it's never touched again. It was a
decision, not a dependency. And then read the method underneath. Search it
for the letters U, K. Search it for India. There's nothing. Not one branch
on the country. Even the error message is correct in every market, because
the words in it, United States, zip code, came from the products
themselves.

## Scene 12 — What You Gain

So what did all of that buy us? The headline is this. A mismatched family
isn't caught. It's impossible. Nothing is being validated. There's simply
no code anywhere that could produce one. There's one decision now, instead
of three. The client shrank from nine class names down to three
interfaces, and no country codes at all. Adding a new market is purely
additive, you add files and you edit none. In fact the test suite in this
project invents a German market inside a single test method, and the
unchanged checkout quotes it correctly. And finally, the British market is
now an actual object. Something you can build, pass around, and write a
test about.

## Scene 13 — The Honest Cost

But I'd be doing you a disservice if I stopped there, because this pattern
has a real cost, and you should know it before you reach for it. Adding a
new country is cheap. One factory, three products, nothing edited. But
suppose checkout now needs a receipt template as well. That's a new kind
of product, so you have to add a method to the abstract factory, which
means editing every single factory you've got. Rows are cheap. Columns are
expensive. Beyond that, your class count is countries multiplied by
product kinds, so do be sure the families are real. And something,
somewhere, still has to choose which factory to use. And here's the honest
test for whether you need this at all. Would a mismatched pair be a bug?
If the answer's no, inject the objects separately and walk away.

## Scene 14 — Running It

Here's the program actually running. The same order, worth one hundred and
twenty, quoted in three countries. Britain adds twenty percent and prints
pounds. America adds its sales tax and prints dollars. India adds eighteen
percent and prints rupees. Now, the important thing. Those nine lines were
produced by one method. And that method contains no condition on the
country at all. Only the factory changed. And look at the last line. The
demo deliberately sends a British postcode to the American market, and it
gets turned away, because the validator came from the same family as the
money.

## Scene 15 — Wrap Up

So, to wrap up. Reach for the abstract factory when several objects have
to agree with each other. And skip it when they don't, because then you're
only adding classes. If you've seen the other two factory patterns, here's
how they line up. A simple factory chooses with a switch. A factory method
chooses with inheritance. And an abstract factory chooses a whole family,
all at once. If you remember one sentence from this video, make it this
one. If getting two objects from different groups would be a bug, you want
an abstract factory.

## Scene 16 — Thanks for Watching

And that's the abstract factory. If you got something out of this, do give
it a thumbs up, and subscribe. It genuinely helps the channel, and it's
what makes more of these possible. And if there's a pattern you'd like me
to cover next, drop it in the comments. I read every one. All the source
code, the written notes and an interactive animation are in the
repository. Thanks for watching, and I'll see you in the next one.
