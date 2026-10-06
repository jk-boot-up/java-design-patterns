# Consumer-Driven Contract Pattern — Video Narration Script

## 1. Consumer-Driven Contract

Hello, and welcome. This video explains the Consumer-Driven Contract pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A service has consumers: other services that call it and read its answers. With consumer-driven contracts, each consumer writes down exactly what it needs from the answer. And the service checks every new release against those written needs, before it goes out. Think of a restaurant supplier. Each restaurant writes down exactly what it relies on. Before the supplier changes a product, it checks every restaurant's list. In our online store, the catalog team renamed a field in the price service, and checkout broke. By the end, you will hear a rename break checkout for real customers. Consumers write down what they read. A rename caught before release, with a name attached. Why adding a field is safe. And the bill: a contract checks shape, not meaning.

## 2. The Scenario

Here is the scenario. The catalog's price service answers with a few fields. Checkout reads two of them: the product code, and the price in pence. The reports service reads only the product code. The catalog team wants to change the shape of the answer. So here is the question. How do they know who will break?

## 3. Nobody Told The Consumer

First demo: nobody told the consumer. The catalog renamed the field price cents, to just price. And released it. A customer checks out two mugs. The order fails. The problem was found in production, by a customer.

## 4. The Pattern

Now, the pattern. Each consumer writes down what it reads: the field names, and their types. That written list is the contract. Before every release, the service checks its real answer against every contract. If something breaks, the check names which consumer, and which field.

## 5. The Consumer Writes It Down

Second demo: consumers write it down. Checkout's contract says: price cents, a whole number, and product code, some text. Reports' contract says: product code, some text. Each lists only the fields it actually reads, and their types.

## 6. The Provider Checks Itself

Third demo: the service checks itself. The catalog's real answer is checked against both contracts. No problems. It is safe to release.

## 7. The Rename Is Caught

Fourth demo: the rename is caught. The same check runs on the renamed release. It reports: checkout expects price cents, a whole number, and it is missing. The build fails. And it names the consumer, and the field.

## 8. Adding Is Safe

Fifth demo: adding is safe. A release adds a new stock field. No problems, because nobody's contract is broken. And the rename again, checked one consumer at a time. Checkout: one problem. Reports: none. Reports never used that field.

## 9. The Bill

Finally, the bill. A new release sends the price in pounds, not pence, in the same field. The field is still there, and still a number. So the check passes. A customer checks out two mugs. The total comes out as thirty-two, when it should be thirty-two hundred pence. A contract checks the shape of the answer, not its meaning. And every consumer must keep its contract up to date. Otherwise the check protects nobody.

## 10. How To Recognise It

How can you spot this in a system someone else built? Look for contract files from tools like Pact, or Spring Cloud Contract. Look for a service's build that fails with a consumer's name in the message. Look for a consumer test that runs against a fake service, generated from its own contract. Or a shared folder of contracts that the service's build reads.

## 11. The Verdict

So, here is the verdict. Let consumers state what they use. Let the service check against those contracts before every release. Keep contracts small: only the fields actually read. Keep them where the service's build can find them. And add tests for meaning, where shape is not enough.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Nothing depends on a real clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? If the service and its consumer belong to one team, released together, an ordinary test is enough. Contracts pay off between teams that release separately.

## 14. Thanks for Watching

That's the Consumer-Driven Contract pattern. If you remember one sentence, make it this one. A consumer-driven contract tells a service who a change will break before it ships, and the price is keeping contracts up to date, and their blindness to meaning. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a contract for a third consumer that reads the currency. And check that it passes. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
