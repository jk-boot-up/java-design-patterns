# Serverless Pattern — Video Narration Script

## 1. Serverless

Hello, and welcome. This video explains the Serverless pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Serverless runs each piece of work as a short function. A platform starts the function when an event arrives. It throws the function away when it is idle. And you pay for each call. Think of a taxi, compared with owning a car. You pay for a taxi only when you ride. But you may wait for one to arrive, and a taxi every day can cost more than a car. In our online store, a receipt must be sent whenever an order is placed. Orders come in bursts, with long quiet gaps in between. In this video, we compare an always-on server with functions. We will hear about scaling to zero, the slow first call, and why a function forgets. Then we will look at the bill.

## 2. The Scenario

Here is the scenario. When an order is placed, a receipt must be sent. We measure time in ticks. In one hundred ticks, only three orders arrive. But now and then, five orders arrive at the same moment. So here is the question. What should run, and when?

## 3. A Machine That Is Always On

First, the traditional way: a machine that is always on. It runs for one hundred ticks, and handles three orders. The bill is two hundred. We paid for one hundred ticks of running, and used it for just three orders.

## 4. The Pattern

Now, the pattern. Each piece of work is a short function. An event, such as a new order, starts it. The platform runs as many copies as are needed. It removes them when they are idle. And you pay for each call.

## 5. A Function Per Event

Second demo: one function per event. The same three orders arrive. Each one runs a function that sends the receipt. Three calls, and a bill of three. Between orders, nothing runs, and nothing is paid for.

## 6. Scale Out, And Back To Zero

Third demo: scaling out, and back to zero. Before any order arrives, there are no running copies at all. Then five orders arrive at the same moment. The platform starts five copies. Ten quiet ticks later, there are none again.

## 7. The Cold Start

Fourth demo: the cold start. Let's measure the extra wait before each call begins. The very first call waits five ticks. A call soon after that waits no extra time. A call after a long quiet period waits five ticks again. Why? After a quiet time, no copy is running, so a new one must be started first. That delay is called a cold start.

## 8. No Memory Between Calls

Fifth demo: a function has no memory between calls. Each call adds one to two counters. One counter lives inside the function. The other lives in a store outside it. After two calls in a row, both counters say two. Then there is a quiet time, and one more call. The counter inside the function says one, because it started again from nothing. The counter outside says three. Anything kept inside a function is lost. Anything that must last goes in a store outside.

## 9. The Bill

Finally, the bill. In a quiet hundred ticks, with three calls, functions cost three, and the server costs two hundred. In a busy hundred ticks, with three hundred calls, functions cost three hundred, and the server still costs two hundred. So paying per call is cheap when you are quiet. And expensive when you are busy all the time. There is one more limit. A job that needs twenty ticks, on a platform with a limit of fifteen, is stopped before it finishes. Long work does not fit.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for platforms like A W S Lambda, Google Cloud Functions, Azure Functions, or Cloudflare Workers. Look for a handler method that takes an event, returns a result, and keeps no fields. Look for a trigger, such as a file upload, a queue message, a schedule, or a web request. And look for settings for a timeout and memory, with a bill per request.

## 11. The Verdict

So, here is the verdict. Use serverless for work that is short, comes in bursts, and keeps nothing between calls. Then follow four rules. One. Keep any lasting state outside the function. Two. Expect a slow first call after a quiet time. Three. Work out the price at your busiest, not your quietest. And four. Keep long jobs somewhere else.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And time is counted in ticks, not by the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For heavy, steady traffic, for long jobs, or for work that needs memory between calls, an ordinary server is cheaper and simpler. Serverless suits work that is quiet, or comes in bursts.

## 14. Thanks for Watching

That's the Serverless pattern. If you remember one sentence, make it this one. Serverless pays per call and scales to zero, and the price is the cold start, no memory between calls, and a bill that grows with steady traffic. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Work out how many calls, in one hundred ticks, make the functions cost the same as the server. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
