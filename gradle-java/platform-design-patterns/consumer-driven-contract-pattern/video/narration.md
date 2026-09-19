# Consumer-Driven Contract Pattern — Video Narration Script

## 1. Consumer-Driven Contract

Hello, and welcome. This video explains the Consumer-Driven Contract pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a consumer driven contract lets each consumer of a service write down exactly what it needs. The provider then checks every release against those contracts, before it goes out. This is another project in the platform category, whose subject is how software is shipped, run and operated. In our online store, the catalog team renamed a field in the price service, and the checkout broke in production. By the end you will see a rename break checkout in production, see consumers write down what they read, see the provider check itself and pass, see a rename caught before release with a name attached, see that adding a field is safe, and see the bill, which is that a contract checks shape and not meaning.

## 2. The Scenario

Here is the scenario. The checkout reads a price and a sku from the catalog's price service. The reports service reads only the sku. The catalog team wants to change the shape of the answer. The question: how do they know who will break?

## 3. Nobody Told The Consumer

First, nobody told the consumer. The catalog renamed price cents to price, and released. Checkout, two mugs: the order failed. It was found in production, by a customer.

## 4. The Pattern

The pattern. Each consumer writes down what it reads: field names, and types. The provider runs its real answer against every contract, before a release. A break names who, and what.

## 5. The Consumer Writes It Down

Second, the consumer writes it down. Checkout's contract: price cents, an integer, and sku, a string. Reports' contract: sku, a string. Each lists only the fields it reads, and their types.

## 6. The Provider Checks Itself

Third, the provider checks itself. The catalog's real answer is checked against both contracts. No problems. Safe to release.

## 7. The Rename Is Caught

Fourth, the rename is caught. The same check on the renamed release reports: checkout expects price cents, an integer, and it is missing. The build fails, and it names the consumer and the field.

## 8. Adding Is Safe

Fifth, adding is safe, and only the affected are named. A release that adds a stock field: no problems. And the rename again, per consumer: checkout, one problem; reports, none. Reports never used that field.

## 9. The Bill

Last, the bill. A release that now sends pounds, not pence, in the same field: no problems. It passes. Checkout, two mugs: total thirty two, where it should be thirty two hundred. A contract checks the shape, and not the meaning. And every consumer must keep its contract up to date, or the check protects nobody.

## 10. How To Recognise It

How do you recognise this in code you did not write? Pact files, or Spring Cloud Contract stubs. A provider build that fails with a consumer's name in the message. A consumer test that runs against a stub generated from its own contract. A broker or folder of contracts that the provider's pipeline reads.

## 11. The Verdict

Here is my verdict, plainly. Let consumers state what they use, and let providers check against it before every release. Keep contracts small: only the fields read. Share them where the provider's build can find them. Add tests for meaning where shape is not enough.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? If provider and consumer are one team with one release, an ordinary test is enough. Contracts pay off across teams that release apart.

## 14. Thanks for Watching

That's Consumer-Driven Contract. If you take one sentence away, take this one: a consumer driven contract lets a provider learn who a change breaks before it ships, and the price is keeping contracts up to date, and their blindness to meaning. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a contract for a third consumer that reads the currency, and see it pass. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
