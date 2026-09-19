# Serverless Pattern — Video Narration Script

## 1. Serverless

Hello, and welcome. This video explains the Serverless pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: serverless runs each piece of work as a short function. A platform starts it when an event arrives, and throws it away when it is idle, and you pay for each call. This is another project in the architecture category, whose subject is how a whole application is arranged, and who may depend on whom. In our online store, a receipt must be sent when an order is placed, and orders come in bursts with long quiet gaps. By the end you will see a machine paid for while idle, see a function per event, see the platform scale out and back to zero, see the cold start, see that a function has no memory, and see the bill, which is the price when busy and the time limit.

## 2. The Scenario

Here is the scenario. When an order is placed, a receipt must be sent. In a hundred ticks, only three orders arrive, and now and then, five arrive at once. The question: what should run, and when?

## 3. A Machine That Is Always On

First, a machine that is always on. One hundred ticks, three orders. The bill is two hundred. It was paid for a hundred ticks, and used for three orders.

## 4. The Pattern

The pattern. Each piece of work is a short function. An event starts it. The platform runs as many as are needed, and drops them when they are idle. You pay per call.

## 5. A Function Per Event

Second, a function per event. The same three orders, each running a send receipt function. Three calls, and a bill of three. Between orders nothing runs, and nothing is paid for.

## 6. Scale Out, And Back To Zero

Third, scale out, and back to zero. Before any order, no instances. Five orders at the same moment: five instances, five cold starts. Ten ticks later, with no orders: no instances again.

## 7. The Cold Start

Fourth, the cold start. The extra wait: first call, five ticks. A call soon after, none. A call after a long quiet, five ticks. The first call after a quiet time is slow, because an instance must be started for it.

## 8. No Memory Between Calls

Fifth, no memory between calls. Two calls in a row: the instance remembers two, and the outside store two. After the quiet time: the instance remembers one, and the outside store three. What is kept in the function is gone. Anything that must last goes in a store outside.

## 9. The Bill

Last, the bill. In a hundred ticks, with three calls, functions cost three and the server two hundred. With three hundred calls, functions cost three hundred, and the server two hundred. Paying per call is cheap when quiet, and dear when busy all the time. And a job of twenty ticks against a limit of fifteen does not finish. Long work does not fit.

## 10. How To Recognise It

How do you recognise this in code you did not write? AWS Lambda, Google Cloud Functions, Azure Functions, Cloudflare Workers. A handler that takes an event and returns, with no fields. A trigger: an upload, a queue message, a schedule, an HTTP request. A setting for timeout and memory, and a bill per request.

## 11. The Verdict

Here is my verdict, plainly. Use serverless for work that is short, comes in bursts, and keeps nothing between calls. Keep state outside. Expect a slow first call after a quiet time. Work out the price at your busiest, not your quietest. Keep long jobs off it.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For steady heavy load, long jobs, or work that needs memory between calls, an ordinary server is cheaper and simpler. Serverless suits the quiet and the bursty.

## 14. Thanks for Watching

That's Serverless. If you take one sentence away, take this one: serverless pays per call and scales to zero, and the price is the cold start, no memory between calls, and a bill that grows with steady load. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, find how many calls in a hundred ticks make the functions cost the same as the server. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
