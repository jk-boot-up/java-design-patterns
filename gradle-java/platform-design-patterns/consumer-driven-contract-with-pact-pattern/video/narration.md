# Consumer-Driven Contract with Pact Pattern — Video Narration Script

## 1. Consumer-Driven Contract with Pact

Hello, and welcome. This video explains the Consumer-Driven Contract pattern in Java, using a library called Pact. This video is presented by Jayasekhar Konduru. First, a simple definition. Each consumer of a service writes down exactly what it needs from the service's answers. And the service checks every new release against those needs, before it goes out. With Pact, a consumer's test writes those needs into a file, called a pact. The service's build replays that file against the real service, and fails on any difference. In our online store, a renamed field in the catalog's price service broke checkout. By the end, you will hear that break happen for real customers. Two consumers write real pact files. The service replays them, and passes. A rename caught before release, with a name attached. And what a pact cannot catch.

## 2. The Partner Project

This video builds on the plain Java Consumer-Driven Contract video. If you have not seen it, start there. That video writes each consumer's contract as simple data. And it shows a checker that names the consumer and the field when a release breaks one. This video uses the same example. It does not teach the pattern again. It shows what Pact does with it.

## 3. Before The First Line

Before any code, what is Pact? Pact is a library for contract testing. A consumer's test uses it to write down what the consumer needs, into a pact file. The service's build uses it to replay that file against the real service. And the build fails if the answer is different. You only need Java. There is no server, no container, and no account. And a promise. Skipping this video loses none of the pattern. The plain Java video teaches all of it.

## 4. Nobody Told The Consumer

First demo: nobody told the consumer. The catalog renamed the field price cents, to just price, and released it. A customer checks out two mugs. The order fails. It was found in production, by a customer.

## 5. The Consumer Writes A Pact

Second demo: each consumer writes a pact. Each consumer's own code is run against a fake catalog that Pact provides. And it works. As a result, two pact files are written. Checkout's pact says: price cents, a whole number, and product code, some text. Reports' pact says: product code, some text.

## 6. The Provider Replays The Pacts

Third demo: the service replays the pacts. Pact replays each pact against the real catalog service, over real web requests. Two checks, and no problems. It is safe to release.

## 7. The Rename Is Caught

Fourth demo: the rename is caught. The pacts are replayed against the renamed release. Two checks, and one fails. For checkout, Pact reports that the answer is missing price cents. The build fails, and names the consumer and the field. The reports pact still passes.

## 8. Adding Is Safe

Fifth demo: adding is safe. A new release adds a stock field. Two checks, and no problems. Adding a field breaks nobody.

## 9. The Bill

Finally, the bill. A new release sends the price in pounds, not pence, in the same field. The field is still there, and still a number. So the check passes. A customer checks out two mugs. The total comes out as thirty-two, when it should be thirty-two hundred pence. A pact checks the shape of the answer, not its meaning. And every consumer must keep its pact up to date. Otherwise the check protects nobody.

## 10. The Verdict

So, here is the verdict. Let each consumer write a pact for what it reads, and only that. Run the service's check in its own build, against the real service. Keep the pact files where that build can find them, or in a shared store called a pact broker. And add separate tests for meaning, because a pact only checks shape.

## 11. How To Recognise It

How can you spot this in code someone else wrote? In a consumer's tests, look for Pact annotations, or a pact builder. In a service's tests, look for annotations naming the provider, and where the pacts are kept. Or look for a folder of pact files.

## 12. Where You Have Met This

Where have you met this before? In many microservice teams, using a pact broker, or the hosted service PactFlow, in their build pipelines.

## 13. What Was Used

For the record, here is what was used. Pact for Java, version four point seven point five. JUnit, version five point ten. And Java twenty-one.

## 14. What Is Real Here

A quick, honest note about this demo. Everything is real: real pact files, Pact's own fake service, and a real web server for the catalog. The consumers and the catalog are small, and made just for this demo.

## 15. When This Is Too Much

So, when is this too much? If the service and its consumer belong to one team, released together, an ordinary test is enough. Pact pays off between teams that release separately.

## 16. Thanks for Watching

That's Consumer-Driven Contract, with Pact. If you remember one sentence, make it this one. Pact tells a service who a change will break before it ships, but it still cannot see a change of meaning. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a third consumer that reads the currency. And check that its pact passes. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
