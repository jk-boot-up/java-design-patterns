# Servant Pattern — Video Narration Script

## 1. Servant

Hello, and welcome. This video explains the Servant pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A servant is a separate class that does one job for many classes that have nothing else in common. Each class only offers a few facts. The servant does the work, written once. Think of a car wash. Every car gets washed, but no car carries its own brushes and soap. The car wash does not care about the make or model. When its prices change, they change once, for every car. In this video, the domain is an online shop. It posts parcels, letters and gift cards, and later, pallets. By the end, you will hear how copies of the same code drift apart. How one servant fixes it. How a new kind of item needs no new code. And what the pattern costs.

## 2. The Scenario

Here is the scenario. The shop posts parcels, letters, and gift cards. Each one is a different class. Each had its own copy of the postage sum. A base price, plus a charge for every started kilo. Then the carrier raised its prices. Someone had to update every copy.

## 3. Act One — Copied postage

First demo: each item carries its own copy of the postage sum. The carrier's new rates are one pound twenty, plus one pound sixty for every started kilo. The parcel's copy was updated. Two point three kilos costs six pounds. The letter's copy was missed. It charges two pounds fifty, not two eighty. So was the gift card's. Each copy looks fine on its own. Together, they disagree.

## 4. Act Two — One servant

Second demo: one shipping servant serves every item. The rates and the sum now live in one class, the servant. Each item only promises three things. Its name, its weight, and the city it is going to. The servant prints a label for each. Parcel, six pounds. Letter, two eighty. Gift card, two eighty. The items hold no shipping code at all.

## 5. Act Three — A new kind of item

Third demo: a new kind of item. The shop starts sending pallets. A pallet only says its name, its weight, and its city. The same servant labels it. One hundred and eighty kilos, to Hull, two hundred and eighty-nine pounds twenty. Not one line of postage code was written for pallets.

## 6. Act Four — Tested alone

Fourth demo: the servant can be tested on its own. A test makes up an item of one thousand and one grams. That is two started kilos: four pounds forty. No real parcel, letter or pallet was needed. And the servant keeps nothing between calls. One servant object serves every item in the shop.

## 7. Act Five — The bill

Fifth demo: the bill. The behaviour is not on the item any more. A developer looking for parcel dot postage finds nothing. They have to know the servant exists. And every item now shows its weight and city, to anyone who asks. Because the servant needs them.

## 8. The Pattern

Let's name the pattern. Write the behaviour once, in a separate class. That class is the servant. Each class that needs the job done offers a small interface. Just the facts the servant needs. Here: a name, a weight, and a city. The servant takes any object with that interface, and does the work.

## 9. Who Does What

Here is who does what. Shippable is the small interface: name, grams, and city. Parcel, letter, gift card, and pallet are the served. They implement Shippable, and hold no shipping code. The shipping servant holds the rates, works out the postage, and prints the label. And copied postage is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Collections dot sort is a servant. It sorts any list of things that can be compared. Java's Files and Objects classes work the same way. And so do label printers, export helpers, and many service classes in Spring applications.

## 11. When To Use It

So, when should you use it? When several unrelated classes need the same job done, and a shared parent class does not fit. Keep the interface small. Keep the servant free of state. And give it a name people will find. When only one class needs the behaviour, keep it in that class.

## 12. Thanks for Watching

That's the Servant pattern. If you remember one sentence, make it this one. When many unrelated classes need the same job, write it once, in a servant. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add international postage, and notice that only the servant changes. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
