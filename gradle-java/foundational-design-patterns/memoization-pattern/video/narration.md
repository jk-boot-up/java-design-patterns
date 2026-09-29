# Memoization Pattern — Video Narration Script

## 1. Memoization

Hello, and welcome. This video explains the Memoization pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Memoization means remembering the answer a function gave for each question. The next time it is asked the same question, it answers from memory, instead of working it out again. Think of a shop assistant asked, twenty times a day, how much delivery to Leeds costs. The first time, they phone the courier. Then they write the answer on a sticky note by the till. After that, they just read the note. In this video, the domain is an online shop. It sells mugs with multi-buy offers, and shows a shipping quote on every product page. By the end, you will hear how a plain method can take ten million calls. How memoization brings it down to twenty-six. When it is not safe. And what it costs.

## 2. The Scenario

Here is the scenario. The shop sells mugs with multi-buy offers. One for four pounds. Two for seven. Three for ten. Five for fifteen. A customer orders twenty-five. What is the cheapest way to combine the offers? And every product page also asks the carrier for a shipping quote, which takes two hundred milliseconds.

## 3. Act One — The same questions again

First demo: the cheapest way to buy twenty-five mugs, worked out plainly. The offers are: one for four pounds, two for seven, three for ten, and five for fifteen. The method says: the best price for twenty-five is the cheapest of: one offer, plus the best price for whatever is left. That is correct. The answer is seventy-five pounds. But it took nearly ten million calls. The best price for twenty mugs was worked out again, every single time it was needed.

## 4. Act Two — Memoized

Second demo: memoized. The same method, with one change. Before working out an answer, it looks in a notebook. After working one out, it writes it down. Each size, from nought to twenty-five, is worked out exactly once. Twenty-six calls. The same seventy-five pounds.

## 5. Act Three — A reusable memo

Third demo: a reusable memo, around a slow shipping quote. Asking the carrier takes two hundred milliseconds. One thousand product page views ask for a quote. They come from twelve postcode areas. With the memo, the carrier is called twelve times. Two point four seconds of waiting, instead of two hundred seconds.

## 6. Act Four — Not safe to memoize

Fourth demo: a function that is not safe to memoize. Converting pounds to euros uses today's exchange rate. In the morning, one hundred pounds is one hundred and sixteen euros. The memo writes that down. At noon, the rate changes. The real price is now one hundred and twelve euros. But the memo still says one hundred and sixteen. The answer depended on the time, not only on the price.

## 7. Act Five — The bill

Fifth demo: the bill. A memo never forgets. Ask it about one hundred thousand different postcodes, and it keeps one hundred thousand answers in memory. Real caches add a size limit, and an expiry time.

## 8. The Pattern

Let's name the pattern. Before working out an answer, look it up in a memo. A memo is just a map, from question to answer. After working it out, write it down. And only do this when the answer depends on nothing but the question. Not on the time, not on a rate, not on anything else.

## 9. Who Does What

Here is who does what. Multi buy plain is the slow way. Multi buy memoized is the same code, plus a map. Memo is a small wrapper that adds a memo to any function. Shipping quotes stands in for the slow carrier. And euros is the example that is not safe to memoize.

## 10. Where You Have Seen It

You have probably met this pattern already. In Java, map dot compute if absent is memoization in one line. Dynamic programming, in algorithm courses, is memoization of recursive problems. Caching libraries such as Caffeine, and Spring's cacheable annotation, build on it. So does use memo, in React.

## 11. When To Use It

So, when should you use it? For expensive functions that are pure, and are asked the same questions again. Especially recursive ones. If the answer can go out of date, or there are huge numbers of different questions, use a real cache instead. One with an expiry time, and a size limit.

## 12. Thanks for Watching

That's the Memoization pattern. If you remember one sentence, make it this one. Work it out once, write it down, and only trust the note while the answer cannot change. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Fix the euro memo, by adding the date to its key. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
