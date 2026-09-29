# Extension Object Pattern — Video Narration Script

## 1. Extension Object

Hello, and welcome. This video explains the Extension Object pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. With an extension object, the core class stays small. Other code attaches extra roles to individual objects. And code that needs a role asks the object whether it has it. Think of a passport. It holds only the basics: your name, and your photo. Other countries add visas to its pages. A border guard asks one question: is there a visa for here? And no country has to reprint your passport. In this video, the domain is an online shop. It sells e-books that can be downloaded, kettles with a warranty, plain mugs, and later, coffee subscriptions. By the end, you will hear how a product class fills up with empty fields. How attached roles fix it. How a new role needs no change to the core. And what the pattern costs.

## 2. The Scenario

Here is the scenario. The shop sells very different things. E-books need a download link. Kettles need a warranty. Mugs need nothing extra at all. Every one of those features became a field on one product class. And the whole shop depends on that class.

## 3. Act One — One class, every field

First demo: one product class, with a field for every feature. A download link, and a download limit, for e-books. A warranty, for electricals. Gift wrap. An age limit. The product class has eight fields. A plain mug leaves five of them empty. Now the shop wants to sell subscriptions. That means a ninth field, in the class that every part of the shop depends on.

## 4. Act Two — A small core, with roles

Second demo: a small core product, with extra roles attached. The product class now has three fields. A code, a name, and a price. Extra roles are attached to individual products. The e-book gets a download role. The kettle gets a warranty role. The mug gets nothing. The product class itself knows nothing about downloads, or warranties.

## 5. Act Three — Asking for a role

Third demo: checkout asks each product, do you have this role? Like a border guard asking for the right visa. The e-book has a download role. So checkout emails a download link, with a limit of three downloads. The kettle has a warranty role. So checkout registers a two-year warranty. The mug says no to both. Nothing extra happens.

## 6. Act Four — A new role

Fourth demo: a new role, added without editing the product class. The subscriptions team writes its own small role. A subscription, with how often to deliver. It is attached to the coffee beans. Checkout schedules a delivery every four weeks. The product class did not change at all.

## 7. Act Five — The bill

Fifth demo: the bill. Nothing checks that a product has the roles it should. A second e-book is added, without its download role. The compiler does not complain. The e-book sells. After payment, nothing happens. The customer paid, and got nothing. And reading the product class no longer tells you what a product can do.

## 8. The Pattern

Let's name the pattern. Keep the core class small. Attach extra roles to the individual objects that need them. This e-book can be downloaded. That kettle has a warranty. Code that needs a role asks for it by type. It gets the role, or an answer that says: not supported.

## 9. Who Does What

Here is who does what. Product holds a code, a name, a price, and whatever roles are attached to it. Download, warranty, and subscription are the roles. Each is a small record, owned by a different team. Checkout asks each product for the roles it knows about, and acts on the ones it finds. And fat product is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Eclipse asks objects for other roles with a method called get adapter. J D B C and J P A have a method called unwrap, which asks for a more specific role. Games build characters as a bag of components. And shop platforms give each product only the attributes it needs.

## 11. When To Use It

So, when should you use it? When abilities belong to some objects and not others. When new ones keep arriving. And when different teams own them. Check at startup that objects have the roles they must. And keep a list of the roles that exist, so developers can find them. When every object has the same abilities, plain fields are simpler.

## 12. Thanks for Watching

That's the Extension Object pattern. If you remember one sentence, make it this one. Keep the core small, and attach roles to the objects that need them. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Write a startup check that every e-book has its download role. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
