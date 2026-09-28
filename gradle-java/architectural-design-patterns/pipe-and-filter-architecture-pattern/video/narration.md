# Pipe and Filter Architecture Pattern — Video Narration Script

## 1. Pipe and Filter Architecture

Hello, and welcome. This video explains the Pipe and Filter Architecture pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Pipe and Filter splits work into stages that run at the same time. The stages are joined by waiting lines, called pipes. Each stage can then be sized and limited on its own. Think of a car wash. One station soaps, one scrubs, and one dries. While one car is being dried, the next is being scrubbed, and the next is being soaped. In our online store, orders arrive faster than we can process them. So how should we organise the work? In this video, we split the work into stages, and find the slowest one. We widen only that stage, limit the waiting lines, and then look at the cost.

## 2. The Scenario

Here is the scenario. Every order goes through three jobs. It is parsed, then priced, then packed. We measure time in ticks. Parsing takes one tick. Pricing takes three ticks. Packing takes one tick. And a new order arrives every tick. So how should we organise the work?

## 3. One Big Step

First, the simple way: one big step. One worker does all three jobs for an order, which takes five ticks. Then it starts the next order. But a new order arrives every tick. After thirty ticks, only five orders are finished.

## 4. The Pattern

Now, the pattern. Split the work into stages. Put a waiting line in front of each stage. The stages all work at the same time. And each stage can be sized, and limited, on its own.

## 5. Stages With Waiting Lines

Second demo: three stages, with waiting lines. The same work is split into parse, price, and pack. Each stage works while the others work. After thirty ticks, eight orders are finished, instead of five. Parse can take a new order while price is still busy with the last one.

## 6. The Slowest Stage Sets The Pace

Third demo: the slowest stage sets the pace. Let's count who is waiting in front of each stage. Parse: one. Price: nineteen. Pack: none. Pricing takes three ticks. So only one order leaves pricing every three ticks, however fast the other stages are. And orders pile up in front of it.

## 7. Widen Only The Slow Stage

Fourth demo: widen only the slow stage. We give pricing three workers instead of one. After thirty ticks, twenty-two orders are finished. And every waiting line is down to one. Parse and pack were not changed at all. Now they handle one order per tick. And that is the new limit.

## 8. A Limit On Each Line

Fifth demo: a limit on each waiting line. With no limit, nineteen orders pile up in one line. With a limit of three, no more than three ever wait. And fourteen orders are turned away at the door. The number finished is still eight, the same as before. Here is what happens. When a line is full, the stage before it must hold on to its order. That pressure passes back, stage by stage, all the way to the door. This push-back is called backpressure.

## 9. The Bill

Finally, the cost. Imagine the pricing stage crashes. Twenty orders were inside it, either waiting or being worked on. Those orders were accepted from customers. And now they are gone. Unless the waiting lines are stored somewhere that survives a crash. There is a second cost. Each order now passes through three stages and two waiting lines. So whenever it has to wait, one order takes longer than its five ticks of actual work.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for stages joined by queues, as in log processing, or systems that extract, transform and load data. Look for pools of workers with a limited queue in front, such as Java's Thread Pool Executor. Look for a Blocking Queue between threads that produce work and threads that consume it. And look for reactive streams, where each stage asks for only as many items as it can handle.

## 11. The Verdict

So, here is the verdict. Use stages when parts of the work run at different speeds, and you want more orders finished per minute. Then follow three rules. One. Find the slowest stage, and widen only that one. Two. Put a limit on every waiting line, so trouble pushes back to the door. Three. If the orders matter, keep the lines somewhere that survives a crash.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And time is counted in ticks, not by the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? If the work is short, or the stages all take about the same time, a single step is simpler. The waiting lines would only add delay. Stages pay off when the parts run at different speeds, or need to grow separately.

## 14. Thanks for Watching

That's Pipe and Filter Architecture. If you remember one sentence, make it this one. Pipe and Filter lets stages run together and be sized on their own, and the price is the lines between them, and the orders lost if a stage crashes. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make parsing take two ticks instead of one. Then work out which stage is now the slowest. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
