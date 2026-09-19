# Serverless with LocalStack Pattern — Video Narration Script

## 1. Serverless with LocalStack

Hello, and welcome. This video explains the Serverless pattern with LocalStack and AWS Lambda, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Serverless video. That one counted a platform's instances on a clock. It showed a server paid for while idle, a function per event, scale out and back to zero, a cold start, lost memory, and the price when busy. This one shows the same idea inside LocalStack and AWS Lambda. The plain definition, in short: with Lambda, a function is uploaded once. The platform starts a container for each concurrent call, keeps it warm for a while, and removes it when it is idle. By the end you will see a function uploaded to a real Lambda API, see five orders at once start five real containers, see them removed when idle, see a real cold start, see a function forget its variables, and see a job stopped at its time limit.

## 2. The Partner Project

This video assumes the Serverless video. If you have not seen it, start there. It counts a platform's instances on a clock, and shows scale to zero, a cold start, lost memory, and the price when busy. This one uses the same example. It does not teach the pattern again. It shows what LocalStack and AWS Lambda does with it.

## 3. Before The First Line

Before the first line of code, what LocalStack and AWS Lambda is. Lambda is Amazon's function platform. LocalStack is a program that answers the same programming interface on your own machine, and runs each copy of a function in a container of its own. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. A Machine That Is Always On

First, a machine that is always on. In the earlier project's price units, a server costs two a tick. A hundred ticks with three orders costs two hundred. It was paid for a hundred ticks, and used for three orders.

## 5. A Function Per Event

Second, a function per event. The function is uploaded to a real Lambda API, and run for each of three orders. Three receipts are sent, and the bill at one per call is three. Between orders nothing has to be running, and nothing is paid for.

## 6. Scale Out, And Back To Zero

Third, scale out, and back to zero. Before any order, no copies are running. Five orders at the same moment: five distinct copies answered, and five containers are running. Five quiet seconds later, with no orders: none are running.

## 7. The Cold Start

Fourth, the cold start. The first call after a quiet time took several hundred milliseconds, and the call right after it, a few. The cold call was slower. The first call had to start a container for the function, and the second found it running.

## 8. No Memory Between Calls

Fifth, no memory between calls. A call to the copy that is running: it has handled three calls. After the quiet time, a different copy answers, and it has handled one. What the first copy kept in its variables went with it. Anything that must last goes in a store outside.

## 9. The Bill

Last, the bill. In the earlier project's price units, in a hundred ticks, with three calls, functions cost three and the server two hundred. With three hundred calls, functions cost three hundred, and the server two hundred. Paying per call is cheap when quiet, and dear when busy all the time. And a job that needs six seconds, with a limit of three, fails: the platform says the task timed out.

## 10. The Verdict

My verdict, plainly. Use functions for work that is short, bursty and keeps nothing between calls. Keep state outside. Expect a cold start after a quiet time, and set the time limit on purpose. Work out the price at your busiest, and keep long jobs off it.

## 11. How To Recognise It

How do you recognise this in code you did not write? A handler that takes an event and a context. A function's timeout and memorySize settings. InvokeRequest calls in the AWS SDK.

## 12. Where You Have Met This

You have met this in aws lambda, google cloud functions and azure functions, and image resizing, receipts and webhooks.

## 13. What Was Used

For the record. LocalStack, 4.14.0. AWS SDK for Java, 2.55.1. Lambda runtime, Python 3.12.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: a real Lambda API, real containers for each copy, and a real cold start. The prices in act six are the earlier project's units, and not real charges.

## 15. When This Is Too Much

So when is it too much? For steady heavy load, long jobs, or work that needs memory between calls, an ordinary server is cheaper and simpler.

## 16. Thanks for Watching

That's Serverless with LocalStack. If you take one sentence away, take this one: a real function platform starts a container for each concurrent call and drops it when idle, and the price is the cold start, lost memory and a time limit. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, raise the function's time limit to ten seconds, and rerun the last act. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
