# Retry with Backoff Pattern — Video Narration Script

## 1. Retry with Backoff

Hello, and welcome. This video explains the Retry with Backoff pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When a call to another service fails for a reason that might not happen again, you try once or twice more. Each time, you wait a little longer first. And you only do this if doing the job twice cannot actually do it twice. That last part is the half everybody skips. And it is the half that costs money. Think of calling a friend whose line is busy. You wait a minute and try again. But if they say no, calling back will not turn it into a yes. In our online store, the shop takes card payments through a payment gateway, on the other side of the internet. About one call in five fails, for reasons that have nothing to do with the payment. By the end, you will know which failures are worth retrying. Why the waits get longer, and are deliberately not all the same. And the failure that charges a shopper twice, while every test still passes.

## 2. The Scenario

Here is the scenario. The shop sells an espresso machine for four hundred and forty-nine pounds ninety-nine. To take the money, it calls a payment gateway owned by someone else, across the internet. About one call in five fails. And those failures have nothing to do with the payment. A connection drops. A router somewhere resets. The bank is fine, and the money is there. The request simply did not make the round trip. Think about what that means for the shop. Each one is a shopper who chose a product, typed in a card number, pressed pay, and got an error page. They did nothing wrong. And most of them do not come back.

## 3. The Obvious Answer — Just Try Again

Ask any room of developers what to do, and someone will say: just try again. And they are right. That really is the idea. Loop up to three times. Call the gateway. If it fails, go round again. To be fair, almost everybody writes this first, and it is not stupid. It rescues checkouts. It has nothing to configure wrongly. And every test written against it passes. So remember that. The rest of this video is about what the word just is hiding. And the answer is not a bug. It is one line of code in the wrong place.

## 4. Act One — A Timeout That Recovers

First demo: a timeout that recovers. The good case is real, so let's hear it. The first attempt goes out, and the gateway times out. Nothing was charged, because the request never arrived. The retrier looks at that failure, and decides it is worth another try. It waits a moment, and calls again. The second attempt goes through. The card is charged, and the checkout succeeds. Here is the only number that matters in this video. The card was charged one time. The shopper waited about two hundred milliseconds, instead of fifty. And in return, they got a finished order instead of an error page. That is a good trade. But notice one small thing. The retrier waited one hundred and three milliseconds, not one hundred. Hold that thought.

## 5. Wait Longer Each Time — And Not All The Same

Those three extra milliseconds have a name. But first, the wait itself. The retrier does not go straight back. It waits a hundred milliseconds before the second attempt. It would wait two hundred before a third, and four hundred before a fourth. Each wait is longer than the last. That is called backoff. The reason is not politeness. If the gateway is failing because it is overloaded, it needs room to recover. A caller that retries instantly takes that room away. Now, the extra three milliseconds. Each caller waits a slightly different, random amount. That is called jitter. With one caller, it seems pointless. So picture a thousand callers instead. They all failed at the same moment, because the same thing went wrong for all of them. If they all wait exactly a hundred milliseconds, they all come back at exactly the same moment. One big wave, and the crush that knocked the gateway over simply happens again. Jitter spreads them out, and turns the wave into a trickle.

## 6. Not Every Failure Is Worth Another Go

That was the retrier's first decision: how long to wait. Here is its second decision. Is this failure worth trying again at all? A timeout might not happen a second time. So, yes. But suppose the bank declines the card. That is not a network hiccup. That is an answer. No funds, a wrong expiry date, or a block on the account. All still true a hundred milliseconds later. So the rule is deliberate. Retry only the failures you recognise as temporary. Treat everything else as permanent. The tempting rule is the other way round: retry everything, unless you know it is hopeless. Write it that way, and one day a bug in your own code is retried four hundred times, to produce four hundred identical crashes.

## 7. Act Two — A Declined Card

Second demo: a declined card. The result is short, and that is the point. One attempt. Fifty milliseconds. The bank said no. The retrier recognised that as a permanent answer. So the shopper was told at once. Compare that with the plain three-times loop. It asks the gateway three times, and waits twice, to get exactly the same no. The shopper waits longer to hear the same thing. The gateway does three times the work, for nothing. And on a bad day, you triple your traffic against someone else's service.

## 8. The Pieces, And What Each One Decides

Let's name the pieces. There are only four. First, the checkout service, which is the caller. It builds the payment request. Then it asks a retrier to make the call. The order of those two steps turns out to be the whole safety of this project. Second, the retrier. It is the loop, and it makes the two decisions we have heard. Is this failure worth another try? And how long should I wait? Third, the retry policy. It answers only the second question: how long. A hundred milliseconds, doubling each time, plus a little jitter. Fourth, the payment gateway, which is the thing that fails. It can fail in three ways. It can time out before the request arrives. It can decline the card. Or, and we have not met this one yet, it can take the money, and then lose the reply on the way back. One more thing about the retrier. It knows nothing about payments or money. That makes it reusable. And it is exactly why it cannot warn you when something is unsafe to repeat.

## 9. The Failure You Cannot See

Now the third kind of failure. This is the one the video is really about. The request leaves the shop. It reaches the gateway. The card is charged, and the money really moves. And then the reply is lost on the way back. So here is the question the whole pattern turns on. What does the caller see? It sees a timeout. Exactly the same timeout as in the first demo, when nothing had been charged at all. There is no flag to check, and nothing to read. No code can tell apart a request lost on the way out, from a reply lost on the way back. And this is not a weakness of a teaching project. The caller simply does not have that information. It is how networks work.

## 10. Act Four — And The Plain Loop Charges Twice

Fourth demo: give that failure to the plain three-times loop. First attempt. The card is charged, and the reply is lost. The loop sees a failure, and goes round again, immediately. Second attempt. The gateway charges the card again. Eight hundred and ninety-nine pounds ninety-eight. For one espresso machine. And the gateway did nothing wrong. The second attempt was a request it had never seen before. And a new request means a new job. So it did the job. Every double charge in this project is the caller's doing.

## 11. And Nothing Went Wrong. That Is The Problem.

Now think about what did not happen. No error was raised. Nothing was logged as a problem. The checkout returned a perfectly valid receipt. In the shop's own admin screens, the order would look completely fine. This project has a test file for that naive checkout. It has five tests. All five pass. And one of them deliberately checks that eight hundred and ninety-nine pounds ninety-eight left a customer's account. So here is the sentence to take away. A double charge does not show up as a failing test, or an alert. It shows up as a phone call from a customer, two days later. And by then, it has happened to everybody else too.

## 12. So Stop Trying To Tell Them Apart

So what does a careful caller do, when it cannot tell the two failures apart? It stops trying to. Instead, it makes the difference not matter. It attaches a value to the request, called an idempotency key. Idempotent means doing it twice has the same effect as doing it once. The key is a promise to the other end. If you have already seen this key, you have already done this job. So do not do it again. Just tell me what happened last time. Now listen to what the key is made from, because this is where it goes wrong. It is made from the order number, and nothing else. Not the attempt number, not the time, and nothing random. Otherwise the two attempts would not look like the same job, and the promise is worthless. And here is the line that decides where the money goes. The careful checkout builds the request once, before the first attempt, outside the retry. The naive loop builds its request inside the loop. So every attempt gets a fresh key. That one line, and where it sits, is the difference between charging a shopper once, and charging them twice.

## 13. Act Three — The Same Failure, The Same Key

Third demo: the same failure, with the same key. The money is charged, and the reply is lost, just as before. But this time, the caller is the careful one. The first attempt charges the card, and the reply vanishes. The retrier waits its hundred and three milliseconds, and tries again. Carrying the same key, because the request was built before any of this started. The gateway looks up the key. It finds it has already charged it. So it returns the first charge, instead of making a second one. The card was charged once. And the checkout still succeeded. Notice what the caller never had to do. It never found out which kind of failure it had. It could not have found out. And it did not need to.

## 14. Somebody Has To Keep The Record

One more thing about the key. People often miss this when they take the pattern back to work. A key is only a promise. And a promise is worth nothing, unless the other end remembers it. Inside the gateway, there is one record: each key, and its receipt. It is checked before any money moves. That record is the whole mechanism. Everything the caller does with keys only works because the far end keeps that record. So making an operation safe to repeat takes work at both ends. Your retry loop cannot decide it for you. And no library can hand it to you. Remember, the retrier just runs a piece of work. It cannot tell a harmless database read from a payment.

## 15. What It Costs, And When Not To

So what does retrying cost? Because it is not free. First, time, and the shopper pays it. That recovered checkout took two hundred milliseconds, instead of fifty. Sometimes a person would rather have the error quickly. Second, load, exactly when you can least afford it. Three attempts per caller against a struggling service triples the traffic. Backoff and jitter reduce that. They do not remove it. Third, and this is a rule, not a preference. Only retry an operation that is safe to repeat. No key, no retry. And do not retry a definite answer. A declined card, a validation error, or a page that does not exist. Retrying those just asks the same question louder. One more warning. If the service is not just flaky, but completely down, retrying makes things worse. Every caller waits three times as long, for something that will never answer. That is not an argument against retrying. It is an argument for knowing when to stop.

## 16. Thanks for Watching

That's the Retry with Backoff pattern. If you remember one sentence, make it this one. A safe retry needs two things: the failure must be temporary, and doing the job twice must not do it twice. Everybody thinks about the first one. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. In the careful checkout, move the line that builds the payment request inside the retry. So it is built on every attempt, instead of once. Then run the tests. One test fails, and its name tells you what you broke. Then ask yourself: in a code review on a Friday afternoon, would anyone have caught it? If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
