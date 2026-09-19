# Scatter-Gather Pattern — Video Narration Script

## 1. Scatter-Gather

Hello, and welcome. This video explains the Scatter-Gather pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: scatter gather sends one request to many parties at the same time, and then gathers their answers, up to a deadline, and combines them into one. This is another project in the microservices category, whose subject is how many small services stay reliable when they talk to each other. In our online store, the product page shows the best price from four suppliers. By the end you will see four suppliers asked one after another, then all at once, see a deadline stop the slowest one setting the pace, see the page say honestly what was left out, see one failure not fail the page, and see the bill, which is that one view becomes many calls.

## 2. The Scenario

Here is the scenario. The product page shows the best price for a mug. Four suppliers each know their price, and each takes a different time to answer. The question: how do we ask them?

## 3. Ask Them One After Another

First, ask them one after another. The four suppliers answer in eighty, a hundred and twenty, two hundred and nine hundred milliseconds. Asked in turn, the page waits thirteen hundred milliseconds, the sum of all four.

## 4. The Pattern

The pattern. Ask everyone at once. Gather the answers as they come, up to a deadline. Combine what arrived, and say what did not.

## 5. Ask Them All At Once

Second, ask them all at once. The same four suppliers, asked together. The page now waits for the slowest: nine hundred milliseconds, not thirteen hundred. But it is still held up by the slowest one.

## 6. Do Not Wait For The Slowest

Third, do not wait for the slowest. Four suppliers are being asked at the same moment. With a deadline of five hundred milliseconds, three quotes come back. Delta is too slow, and is left out. The best of the three is shown: Beta, at eleven ninety. The page waited five hundred milliseconds, not nine hundred.

## 7. Say What Was Left Out

Fourth, say what was left out. The page shows: the best of two of three suppliers, eleven ninety from Beta. The one that did not answer, Delta, would have been cheaper, at nine ninety. A partial answer is honest only if it says that it is partial.

## 8. A Supplier That Fails

Fifth, a supplier that fails. Beta is down. The page gets the other two quotes, and names Beta as missing, and says why. One failure did not fail the page.

## 9. The Bill

Last, the bill. One page view is now four supplier calls. A thousand views make four thousand. And the more you ask, the more often the slowest sets the pace. If each supplier is quick ninety nine times in a hundred, asking one gives ninety nine quick pages in a hundred. Asking four and waiting for all gives ninety six. Asking ten gives ninety. A deadline is what stops the slowest setting the pace.

## 10. How To Recognise It

How do you recognise this in code you did not write? CompletableFuture.allOf or invokeAll with a timeout. A price comparison, flight search, or federated search. A method that returns results and a list of sources that did not respond. Elasticsearch's search across shards, which scatters and gathers.

## 11. The Verdict

Here is my verdict, plainly. Use scatter-gather when several independent sources can answer the same question, and the best or a combination of the answers is what you want. Always give it a deadline, treat a failure like a late answer, and say when an answer is partial. Watch the fan-out: every request now costs as many calls as there are sources.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? With one source, or when you need every answer without exception, scatter-gather has nothing to gather. With a very large fan-out, the deadline decides more than the data.

## 14. Thanks for Watching

That's Scatter-Gather. If you take one sentence away, take this one: scatter-gather asks many at once and waits for a deadline, and the price is fan-out and partial answers. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a fifth supplier that is always slow, and see what the deadline does for the page. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
