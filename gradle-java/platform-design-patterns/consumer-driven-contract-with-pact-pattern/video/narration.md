# Consumer-Driven Contract with Pact Pattern — Video Narration Script

## 1. Consumer-Driven Contract with Pact

Hello, and welcome. This video explains the Consumer-Driven Contract pattern with Pact, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Consumer-Driven Contract video. That one let each consumer write its contract as data, and let the provider check its real answer against every contract, naming the consumer and the field. It also showed that a contract cannot see a change of meaning. This one shows the same idea inside Pact. The plain definition, in short: with Pact, a consumer's test writes a pact file. The provider's build replays that file against the real service, and fails on any difference. By the end you will see a rename break checkout in production, see two consumers write real pact files, see the provider replay them over real HTTP and pass, see a rename caught before release with a name attached, see that adding a field is safe, and see what a pact cannot catch.

## 2. The Partner Project

This video assumes the Consumer-Driven Contract video. If you have not seen it, start there. It writes each consumer's contract as data, and shows a verifier that names the consumer and the field when a release breaks one. This one uses the same example. It does not teach the pattern again. It shows what Pact does with it.

## 3. Before The First Line

Before the first line of code, what Pact is. Pact is a library for contract testing. A consumer test uses it to write down what the consumer needs, into a pact file. The provider's build uses it to replay the file against the real service, and fail if the answer differs. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. Nobody Told The Consumer

First, nobody told the consumer. The catalog renamed price cents to price, and released. Checkout, two mugs: the order failed. It was found in production, by a customer.

## 5. The Consumer Writes A Pact

Second, the consumer writes a pact. Each consumer's own client is run against Pact's mock of the catalog, and agrees. Two pact files are written. Checkout's pact: price cents, an integer, and sku, a string. Reports' pact: sku, a string.

## 6. The Provider Replays The Pacts

Third, the provider replays the pacts. Pact replays each pact against the real catalog, over HTTP. Two interactions checked, no problems. Safe to release.

## 7. The Rename Is Caught

Fourth, the rename is caught. On the renamed release: two interactions checked, one failed. Checkout: the actual map is missing the following keys: price cents. The build fails, and Pact names the consumer and the field. Reports' pact still passes.

## 8. Adding Is Safe

Fifth, adding is safe. A release that adds a stock field: two interactions checked, no problems. Adding a field breaks nobody.

## 9. The Bill

Last, the bill. A release that now sends pounds, not pence, in the same field: no problems. It passes. Checkout, two mugs: total thirty two, where it should be thirty two hundred. A pact checks the shape, and not the meaning. And every consumer must keep its pact up to date, or the check protects nobody.

## 10. The Verdict

My verdict, plainly. Let each consumer write a pact for what it reads, and only that. Run the provider's verification in its build, against the real service. Keep pact files where the provider's build can find them, or in a broker. And add tests for meaning, since a pact checks only shape.

## 11. How To Recognise It

How do you recognise this in code you did not write? A @Pact method or ConsumerPactBuilder in a consumer's tests. @Provider and @PactFolder or @PactBroker in a provider's tests. A pacts folder of JSON files.

## 12. Where You Have Met This

You have met this in many microservice teams, and pact broker or pactflow in their pipelines.

## 13. What Was Used

For the record. Pact JVM, 4.7.5. JUnit, 5.10.2. Java, 21.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: real pact files, Pact's own mock, and a real HTTP server for the provider. The consumers and the catalog are small, and made for the demo.

## 15. When This Is Too Much

So when is it too much? If provider and consumer are one team with one release, an ordinary test is enough. Pact pays off across teams that release apart.

## 16. Thanks for Watching

That's Consumer-Driven Contract with Pact. If you take one sentence away, take this one: Pact lets a provider learn who a change breaks before it ships, and it still cannot tell a change of meaning. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, add a third consumer that reads the currency, and see its pact pass. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
