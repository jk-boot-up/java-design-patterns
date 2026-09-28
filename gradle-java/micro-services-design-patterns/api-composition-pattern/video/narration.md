# API Composition Pattern — Video Narration Script

## 1. API Composition

Hello, and welcome. This video explains the A P I Composition pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When one screen needs data that several different services own, you ask all of them. And you assemble the answer yourself. Think of making a sandwich, when no shop sells it ready-made. You need bread from the baker, tomatoes from the grocer, and cheese from the deli. There are two halves to this pattern. The easy half: calls made one after another cost the total of their waiting times. But calls sent together cost only the longest one. The harder half: for every service you ask, someone must decide in advance whether the screen can be shown without it. In this video, an online shop shows a customer one of their orders. By the end, you will know why that page takes two hundred and ten milliseconds, when it could take one hundred and fifty. And why three excellent services can combine into a page worse than any one of them.

## 2. The Scenario

Here is the scenario. A shopper clicks on one of their past orders. The page shows the order reference. Then a line for each item: its name, how many, and what it cost. Then the total. And finally, where the parcel is now. A completely ordinary page. Except that three different services own those facts. The Orders service knows what was bought, and what was paid. The Catalog service is the only one that knows a product code's real name. And the Shipping service is the only one that knows where the parcel is. Each has its own database, and none can see into the others. So no single query can build this page. Someone must ask all three, and put the answer together.

## 3. The Obvious Answer — Three Calls

Here is what everyone writes first: three ordinary lines of Java. Fetch the order. Ask Catalog for the product names. Ask Shipping for the delivery status. Then build the page from the three answers. To be fair, there is no bug here. It is easy to read, it returns exactly the right page, and every test passes. A code review would approve it without a comment. Because the cost of this code is not in the code. Let's run it, and listen to the clock.

## 4. Act One — Three Calls, One After Another

First demo: three calls, one after another. The call to Orders starts at zero, and returns at thirty milliseconds. The call to Catalog starts at thirty, and returns at ninety. The call to Shipping starts at ninety, and returns at two hundred and ten. Thirty, plus sixty, plus one hundred and twenty. The shopper waited two hundred and ten milliseconds, as each service took its turn. Now here is the key question. Which of those three calls actually needed the answer from the one before it?

## 5. Sixty Of Those Milliseconds Bought Nothing

Let's answer it. Catalog really did have to wait. To look up product names, it needs the product codes. And only the order knows which products are on it. But what does Shipping need? Just one thing: the order I D. And the shopper clicked on that order I D before any call was made. So the call to Shipping waited sixty milliseconds for Catalog's answer. And then never even looked at it. Sixty milliseconds, spent on nothing. No code review could catch this, because nothing is wrong with any single line. That is simply what a sequence of statements does. It does them in sequence.

## 6. The Sandwich From Three Shops

Forget software for a moment, and think about that sandwich. You need bread from the baker, tomatoes from the grocer, and cheese from the deli. Two things follow, and together they are the whole pattern. First: go to all three shops at once. Visit them one after another, and lunch takes three trips. Send three people at the same time, and lunch takes as long as the slowest trip. No shop got faster. You simply stopped waiting for one before starting the next. Second, and this is the part people skip. Decide, before you leave the house, what happens if a shop is shut. No bread means no sandwich at all. No tomatoes means a sandwich without tomatoes. That is fine, as long as nobody claims there were tomatoes on it. That second decision has nothing to do with programming. And it must be made before you reach the shops.

## 7. It Is Rarely One Flat Fan-Out

So the fix is to stop waiting. But be careful how far you take that. The tempting version is to send all three calls at the very start. This page cannot do that. Catalog must be told which product codes to look up, and only the order knows them. So the real shape is one call, and then two together. Fetch the order first, on its own. Then send Catalog and Shipping at the same instant. Working out which calls truly depend on which is most of the job. In real systems, it is rarely one flat burst of calls. It is usually a few waves. What can be asked at once, and what must wait for the first answers.

## 8. One Call, Then Two Together

Here is that shape, in code. The order is fetched first, on its own, because nothing else can start without it. Then a fan-out is created. The two remaining calls are handed to it, each with a name. Not called yet, just handed over. Catalog is given the job of naming the products on the order. Shipping is given the job of looking up the delivery status. Then one line says: wait for all of them. The fan-out starts both jobs at the same moment. And gives back a handle to each, called a branch. Remember that word, branch. The second half of this video is about what a branch does when its call fails.

## 9. Act Two — The Same Calls, Sent Together

Second demo: the same calls, sent together. Orders still starts at zero, and returns at thirty milliseconds. But now Catalog and Shipping both start at thirty, at the same instant. Catalog returns at ninety. Shipping returns at one hundred and fifty. And the page is finished the moment the slower one arrives. One hundred and fifty milliseconds, instead of two hundred and ten. And notice that nothing got faster. Shipping still takes its full one hundred and twenty milliseconds. What disappeared was the queuing. So here is the easy half of the pattern, in one sentence. Calls made one after another cost the total of their waiting times. Calls sent together cost only the longest.

## 10. Who Decides What

There are four pieces, each with one job. The composer builds the page. It calls Orders first, then hands the other two calls to the fan-out. It is the only piece that knows anything about shopping. The fan-out runs several jobs from the same starting moment. It knows nothing about orders or parcels. It gives back one branch for each job. Each branch holds one of two things: an answer, or the failure that happened instead. And then there are the three services, described by what they mean to this page. Orders is required: without it, there is no page. Catalog is optional: without it, the page shows product codes instead of names. Shipping is optional: without it, the delivery section says it cannot check. That is the most important fact in this whole system. And it appears nowhere in the types. Only the composer knows which missing piece the page can live without.

## 11. Act Three — Shipping Stops Answering

Third demo: Shipping stops answering. The same failure is given to both versions. The three-line version fetches the order, which is fine. It gets the product names, which is fine. Then it calls Shipping, and throws an error. And look what is lost with it. The order had already arrived. The product names had already arrived. Both were perfectly good, and both are thrown away. The shopper gets an error page. The composed version works differently. When one job in the fan-out fails, the error is caught, and kept on that branch. Nothing else is disturbed. Then the composer asks, one branch at a time: is this missing piece fatal? For Shipping, no. So the shopper still sees what they bought, how many, and what it cost. And where the delivery section would be, the page says: unknown, we cannot check this right now. At the bottom, the page lists delivery status as missing.

## 12. Name The Gap. Never Fill It In.

This part is worth arguing about in a code review. When Shipping is down, the page says: we cannot check this right now. It would have been easy to write something else, like: in transit. That is tempting. It is nearly always true. It reads better, and looks less broken. Don't do it. A shopper told their parcel is in transit will never ring up about the parcel that never left the warehouse. You have not made the page nicer. You have hidden the one signal that something is wrong, from the only person who could notice. The page is allowed to say it does not know. It is not allowed to make something up. That is what the missing list is for. Naming the gap is what makes a partial answer honest, not just convenient.

## 13. Act Four — And When Orders Is Down

Fourth demo: Orders is down. Degrading is not always the answer. Orders stops answering. And the composer does not degrade anything. It throws an error, and the shopper gets an honest error page. That is correct. A page with no order on it is not a partial page. It is a blank one, with nothing honest to show. And Catalog was never called at all. The failure happened before the fan-out even existed. Knowing which piece is required is as much part of the pattern as knowing which can be missing. A composer that treats everything as optional will one day show someone a page about nothing.

## 14. Act Five — Why Any Of This Matters

Fifth demo, and this one is arithmetic. It is the reason the second half of this pattern matters. Suppose each of the three services is up ninety-nine point nine percent of the time. That is a genuinely good service: about forty-three minutes of downtime a month. So how available is a page that needs all three? Most people guess ninety-nine point nine. It is not. The page only works when all three are up at the same moment. So the chances multiply together. The result is ninety-nine point seven percent. That is one hundred and twenty-nine minutes of downtime a month. Over two hours. Three services that each behaved perfectly have combined into a page that is worse than any one of them. The fix is not better services. The fix is needing fewer of them. Once only Orders is required, the page works whenever Orders is up. Back to forty-three minutes a month. And the other outages cost a gap on the page, not the whole page.

## 15. What It Costs

Now the honest costs. First, the page can never be faster than its slowest required service. Sending calls together removed the adding up, but not the slowest one. Slow Shipping down to four hundred milliseconds, and the page takes four hundred and thirty. Second, the fan-out adds load. One page view is now three calls. Ten thousand shoppers become thirty thousand calls. Third, and most expensive: someone must make a business decision for every single service. Is it required, or optional? And revisit it every time a service is added. Which is exactly when nobody remembers. And a page where everything is optional says nothing at all. When the numbers stop working, the answer is to keep a ready-assembled copy of the data. But that is a different pattern.

## 16. Thanks for Watching

That's the A P I Composition pattern. If you remember one sentence, make it this one. Send independent calls together, and decide in advance which missing answers the page can live without, and never invent what you do not know. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Find the line where the composer asks the Shipping branch for its answer. Change it so a failure is thrown, instead of replaced. Two tests will fail. One line just turned an optional service into a required one, and cost the page an hour of uptime a month. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
