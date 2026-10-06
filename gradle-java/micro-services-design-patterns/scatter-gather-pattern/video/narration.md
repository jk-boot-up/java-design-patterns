# Scatter-Gather Pattern — Video Narration Script

## 1. Scatter-Gather

Hello, and welcome. This video explains the Scatter-Gather pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Scatter-gather sends one request to many parties, all at the same time. Then it gathers their answers, up to a deadline. And it combines them into one. Think of asking several taxi firms for a quote at once. You give them two minutes, then take the best offer you have. In our online store, the product page shows the best price from four suppliers. By the end, you will hear four suppliers asked one after another, then all at once. A deadline stop the slowest one from holding up the page. The page say honestly what was left out. One failure not break the page. And the bill.

## 2. The Scenario

Here is the scenario. The product page shows the best price for a mug. Four suppliers each know their own price. And each takes a different amount of time to answer. So here is the question. How do we ask them?

## 3. Ask Them One After Another

First demo: ask them one after another. The four suppliers answer in eighty, a hundred and twenty, two hundred, and nine hundred milliseconds. Asked in turn, the page waits thirteen hundred milliseconds. That is all four times, added together.

## 4. The Pattern

Now, the pattern. Ask everyone at once. Gather the answers as they arrive, up to a deadline. Combine what arrived. And say what did not.

## 5. Ask Them All At Once

Second demo: ask them all at once. The same four suppliers, asked together. Now the page waits only for the slowest one: nine hundred milliseconds, not thirteen hundred. But it is still held up by that slowest supplier.

## 6. Do Not Wait For The Slowest

Third demo: do not wait for the slowest. All four suppliers are asked at the same moment. With a deadline of five hundred milliseconds. Three quotes come back in time. Delta is too slow, and is left out. The best of the three is shown: Beta, at eleven pounds ninety. The page waited five hundred milliseconds, not nine hundred.

## 7. Say What Was Left Out

Fourth demo: say what was left out. The page shows the best of the suppliers that answered: eleven pounds ninety, from Beta. But Delta, which did not answer in time, would have been cheaper, at nine pounds ninety. A partial answer is only honest if it says that it is partial.

## 8. A Supplier That Fails

Fifth demo: a supplier that fails. Beta is down. The page still gets the other quotes. It names Beta as missing, and says why. One failure did not break the page.

## 9. The Bill

Finally, the bill. One page view is now four supplier calls. A thousand views make four thousand calls. And the more suppliers you ask, the more often one of them is slow. Suppose each supplier is quick ninety-nine times in a hundred. Ask one, and ninety-nine pages in a hundred are quick. Ask four, and wait for all of them, and it drops to ninety-six. Ask ten, and it drops to ninety. A deadline is what stops the slowest supplier setting the pace.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for Java code that starts several calls together, and waits for all of them, with a timeout. Look for price comparison, flight search, or search across many sources. Look for a method that returns results, plus a list of sources that did not respond. Search engines like Elasticsearch do this too, across the pieces of their data.

## 11. The Verdict

So, here is the verdict. Use scatter-gather when several independent sources can answer the same question. And you want the best answer, or a combination of them. Always set a deadline. Treat a failure just like a late answer. And say clearly when an answer is partial. And watch the cost. Every request now costs as many calls as there are sources.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Nothing depends on a real clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? With only one source, there is nothing to gather. And if you truly need every single answer, a deadline does not help. And with a very large number of sources, the deadline decides more than the data does.

## 14. Thanks for Watching

That's the Scatter-Gather pattern. If you remember one sentence, make it this one. Scatter-gather asks many sources at once, and waits only until a deadline, and the price is many more calls, and answers that may be partial. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a fifth supplier that is always slow. Then see what the deadline does for the page. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
