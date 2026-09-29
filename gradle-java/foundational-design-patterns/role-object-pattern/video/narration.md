# Role Object Pattern — Video Narration Script

## 1. Role Object

Hello, and welcome. This video explains the Role Object pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. With role objects, one core object holds who someone is. Each thing they do for a while, such as buying or selling, is a separate role object. Roles are added and removed as life changes, and the identity stays the same. Think of one person who is a parent, a nurse, and a weekend football coach. The same person, all along. When they stop coaching, the club removes that role. Nobody has to create a new person. In this video, the domain is an online shop. Its customers can also sell on its marketplace, and earn money by referring friends. By the end, you will hear why subclasses break when someone's role changes. How role objects fix it. How to drop a role. And what it costs.

## 2. The Scenario

Here is the scenario. Customers of the shop can also become sellers on its marketplace. And they can join an affiliate scheme, earning a small commission for referring others. The shop modelled each kind as a subclass. A subclass is a class that extends another. Customer, and selling customer extends customer. Then Priya, who had twelve orders, opened a shop.

## 3. Act One — A subclass per kind

First demo: a subclass for every kind of customer. Priya is a customer with twelve orders. Then she opens a shop on the marketplace. The code creates a new object, a selling customer. The new object has zero orders. It is not even the same object as Priya the customer. And there are three kinds of role: buyer, seller, and affiliate. Every combination needs its own class. Seven classes.

## 4. Act Two — One account, many roles

Second demo: one account, with roles added as life changes. Priya's account holds only who she is: an ID, and a name. A buyer role holds her twelve orders. When she opens a shop, a seller role is added. To the same account. She now plays two roles, buyer and seller. And all twelve orders are still there.

## 5. Act Three — Roles with behaviour

Third demo: each role brings its own data, and its own behaviour. The seller role lists a hand-thrown mug, under the shop name Priya's Pottery. Priya also joins the affiliate scheme, at five percent. She refers two orders, of forty and sixty pounds. She earns five pounds. The account itself knows nothing about shops, or commission.

## 6. Act Four — Dropping a role

Fourth demo: a role can be dropped, while the account lives on. The marketplace suspends Priya's selling. The seller role is removed. She tries to list another mug. Refused: Priya is not a seller. But she is still a buyer. She places her thirteenth order.

## 7. Act Five — The bill

Fifth demo: the bill. Every caller must ask first. Is she a seller right now? And what do we do if she is not? And her data is spread out. Her name is on the account. Her shop name was on a role that is now gone.

## 8. The Pattern

Let's name the pattern. A core object holds who someone is. Here, the account. Each thing they do for a while is a separate role object, with its own data and behaviour. Buyer, seller, affiliate. Roles are added and removed as life changes. The core object, and its identity, stay the same.

## 9. Who Does What

Here is who does what. The account holds an ID, a name, and the roles it plays right now. Role is a small base class. Every role remembers which account it belongs to. Buyer, seller, and affiliate are the roles, each with its own data and methods. And customer and selling customer are the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Marketplace accounts can be a buyer, a seller, and an admin, all at once. Enterprise data models often have a party, a person or a company, playing roles such as customer, supplier, and employee. And games give one character different roles over time.

## 11. When To Use It

So, when should you use it? When roles come and go during an object's life, combine freely, and bring their own behaviour. Keep the identity on the core object. Give each role its own data. And decide what should happen to that data when a role is removed. When an object's kind never changes, a subclass or a simple field is clearer.

## 12. Thanks for Watching

That's the Role Object pattern. If you remember one sentence, make it this one. One identity, many hats, and the hats come and go. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Keep Priya's shop name when selling is suspended, so it can be restored later. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
