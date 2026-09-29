# Entity Pattern — Video Narration Script

## 1. Entity

Hello, and welcome. This video explains the Entity pattern, from domain-driven design, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An entity is something defined by who it is, not by its current details. It gets an identity that never changes. Its details can change, and it is still the same thing. Think of a car. Over the years it gets a new colour, new plates, and a new owner. It is still the same car, because its chassis number, stamped in at the factory, never changes. In this video, the domain is an online shop. Its customers change their emails, earn points, and sometimes share a name with someone else. By the end, you will hear how comparing customers by their values goes wrong. How an identity fixes it. How look-alikes stay apart. And what equality does not tell you.

## 2. The Scenario

Here is the scenario. Customers change their email. They earn loyalty points. Some share a name, and even an email, with someone in their family. The shop kept customers as records. Two records are equal when every field is equal.

## 3. Act One — Defined by values

First demo: a customer defined by its values. The customer is a record, compared by every field: name, email, and points. Priya changes her email. Now the old record and the new one are not equal. Her orders were stored under the old record. Looked up with the new one: nothing found. And the mailing list now has two customers. Both of them are Priya.

## 4. Act Two — Defined by identity

Second demo: an entity, a customer defined by its identity. The customer now has an ID, C 17, given when the account was opened. Two customer objects are equal when their IDs are equal. Nothing else is compared. Priya changes her email. She is still C 17. Her orders are found. And the mailing list holds one customer.

## 5. Act Three — Look-alikes are different

Third demo: two people who look the same are still two people. A father and his son are both called Tom Reed. They share a family email. As records, they are equal. The shop would mix up their orders. As entities, they are C 42 and C 43. Two different customers.

## 6. Act Four — A life story

Fourth demo: an entity has a life story. Priya's account was opened with her old email. Then she changed it. Then she changed it again, to her work email. She earned eighty points along the way. Three emails. One customer. The ID never changed.

## 7. Act Five — The bill

Fifth demo: the bill. Equal is not the same as up to date. A cached copy of Priya, and the live Priya, are equal. They share the same ID. But the copy has an old email, and the live one a new email. And every entity needs an ID that is unique, and never reused.

## 8. The Pattern

Let's name the pattern. Give each customer an identity when it is created. A customer ID. Never change it. Compare customers by that identity only. Everything else, the email, the points, is free to change.

## 9. Who Does What

Here is who does what. Customer ID is the identity: a small value that never changes. Customer is the entity. It holds the ID, and details that change, and a history of those changes. Its equals and hash code look at the ID only. And customer record is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. J P A entities have an ID field. Database tables have a primary key. Order numbers, account numbers, and parcel tracking numbers are all identities of entities. And any equals method that compares only an ID is treating its class as an entity.

## 11. When To Use It

So, when should you use it? For things the business follows one by one, through time. Customers, orders, parcels. For things where only the value matters, such as an amount of money or an address, use a value object instead. Ten pounds is ten pounds, whichever coins.

## 12. Thanks for Watching

That's the Entity pattern. If you remember one sentence, make it this one. Some things are who they are, not what they currently look like. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make the order an entity, with its own order ID. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
