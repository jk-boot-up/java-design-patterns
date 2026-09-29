# Immutable Object Pattern — Video Narration Script

## 1. Immutable Object

Hello, and welcome. This video explains the Immutable Object pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An immutable object is one that can never change after it is made. To change something, you make a new object with the difference. The old one stays exactly as it was, for everyone still holding it. Think of a whiteboard menu behind a café counter, and a printed till receipt. Anyone with a cloth can change the whiteboard, even while you are reading it. A receipt never changes. If something changes, the shop prints a new one. In this video, the domain is an online shop. It passes addresses and price lists around everywhere. Orders keep a shipping address, and checkout reads the price list. By the end, you will hear three bugs that changeable objects cause. How to write an object that cannot change. How to replace a price list in one step. And what immutability costs.

## 2. The Scenario

Here is the scenario. Each order keeps the address it ships to. Checkout reads the shop's price list. And a set records addresses where a delivery failed. All of these are ordinary objects with setters. A setter is a method that changes a field, such as set city. And they are shared by reference. That means two parts of the program can hold the very same object. Not two copies. One object.

## 3. Act One — Shared, then changed

First demo: one address, shared, then changed. Priya places order one. The order keeps her profile address: four Mill Lane, Leeds. But it does not keep a copy. It keeps the same object that her profile uses. Later, Priya moves house. She updates her profile, for future orders. Order one now ships to twelve High Street, York. An order she placed before she moved.

## 4. Act Two — Changed while being read

Second demo: a price list changed while someone reads it. A kettle, a mug and a teapot come to sixty-five pounds. A ten percent sale is applied, one price at a time. First the kettle. Then the mug. Then the teapot. A checkout reads the list just after the kettle changed. It sees the new kettle, and the old mug and teapot. Sixty-two pounds. That is neither the old price, nor the sale price. The customer paid a price that never existed.

## 5. Act Three — Lost in a set

Third demo: a changed object is lost in a set. Tom's address goes into a set of failed deliveries. A hash set files each object under a number, worked out from what the object contains. Like a filing cabinet, sorted by the first letter of a name. Then someone tidies the spelling. Road becomes R D. Now the set cannot find it. Contains says false. But the set's size is still one. It is filed in the wrong drawer.

## 6. Act Four — Immutable objects

Fourth demo: immutable objects. Now the address has no setters. A change makes a new address, and leaves the old one alone. Priya's profile moves to York. Order two still ships to Leeds. The price list is immutable too. The sale builds a whole new list, on the side. Checkout keeps reading sixty-five pounds. Then the shop swaps in the new list, in one single step. Checkout reads fifty-eight fifty. There is no moment in between. The list also copies whatever it was built from. So changing that later does nothing. And an address that cannot change is never lost in a set.

## 7. Act Five — The bill

Fifth demo: the bill. Every change is a copy. Change one price, in a list of a thousand items. You get a new list, of a thousand entries. And every field that might change needs its own with method, to build the new object. For small values that change rarely, that is cheap. For something that changes all the time, think twice.

## 8. The Pattern

Let's name the pattern. No setters, and every field is final. If the object holds a list or a map, copy it in when the object is made. And hand it out read-only. To change something, make a new object with the difference. And when many readers share the current version, such as the shop's price list, swap in the new object in one step.

## 9. Who Does What

Here is who does what. Address is a Java record. Its with street and with city methods return a new address. Price list copies the prices it is given, and hands them out read-only. A sale returns a whole new price list. Shop holds the current price list, and swaps in a new one in one step. And the mutable address and mutable price list are the old way, kept for comparison.

## 10. Where You Have Seen It

You have used immutable objects since your first Java program. String is immutable. So are Integer, Local Date, and Big Decimal. Java records make writing your own easy. And List dot of, and Map dot copy of, give you lists and maps that cannot change. The Value Object and Money patterns in this course are built on this idea. And so is state in React and Redux.

## 11. When To Use It

So, when should you use it? Make every value immutable by default. Addresses, prices, dates, IDs, messages, settings. Replace objects whole, instead of editing something that is shared. And keep mutation for the few objects that exist to change, such as a cart being filled. Give each of those exactly one owner.

## 12. Thanks for Watching

That's the Immutable Object pattern. If you remember one sentence, make it this one. Never change a shared object. Make a new one. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a list of delivery notes to the address. And make sure it stays immutable. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
