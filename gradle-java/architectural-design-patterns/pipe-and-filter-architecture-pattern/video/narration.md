# Pipe and Filter Architecture Pattern — Video Narration Script

## 1. Pipe and Filter Architecture

Hello, and welcome. This video explains the Pipe and Filter Architecture pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: pipe and filter architecture splits work into stages that run at the same time, joined by waiting lines. Each stage can then be sized and limited on its own. This is another project in the architecture category, whose subject is how a whole application is arranged, and who may depend on whom. In our online store, orders arrive faster than we can process them, and the question is how to organise the work. By the end you will see one big step finish few orders, see three stages overlap and finish more, see the slowest stage set the pace and a line pile up in front of it, see only that stage widened, see a limit on the lines push back on the door, and see the bill, which is orders lost when a stage crashes.

## 2. The Scenario

Here is the scenario. Every order is parsed, priced and packed. Parsing takes one tick, pricing takes three, and packing takes one. An order arrives every tick. The question: how should we organise the work?

## 3. One Big Step

First, one big step. One worker does all three jobs, five ticks for each order. An order arrives every tick. After thirty ticks, five orders are done.

## 4. The Pattern

The pattern. Split the work into stages. Each stage has a waiting line in front of it. The stages work at the same time, and each can be sized and limited on its own.

## 5. Stages With Waiting Lines

Second, stages with waiting lines. The same work in three stages, each working while the others do. After thirty ticks, eight orders are done. Parse takes a new order while price is still on the last one.

## 6. The Slowest Stage Sets The Pace

Third, the slowest stage sets the pace. Waiting in front of each stage: parse one, price nineteen, pack none. Price takes three ticks, so one order leaves every three ticks, however fast parse and pack are. Orders pile up in front of it.

## 7. Widen Only The Slow Stage

Fourth, widen only the slow stage. Three price workers. After thirty ticks, twenty two orders are done, and the lines are short. Parse and pack were not touched. Now they take one order a tick, and that is the new limit.

## 8. A Limit On Each Line

Fifth, a limit on each line. With no limit, nineteen orders wait in one line. With a limit of three, no more than three wait, and fourteen orders are refused at the door. Orders done is eight, the same as without a limit. A full line makes the stage before it hold its order, and so on, back to the door. That push-back is called backpressure.

## 9. The Bill

Last, the bill. The price stage crashes. Twenty orders were in it, waiting or being worked on. They were accepted from customers, and are gone, unless the lines are kept somewhere that survives. And an order now passes through three stages and two waiting lines, so a single order takes longer than its five ticks of work, whenever it has to wait.

## 10. How To Recognise It

How do you recognise this in code you did not write? Stages joined by queues, as in a log-processing or ETL system. Worker pools with a bounded queue in front, such as ThreadPoolExecutor. BlockingQueue between producer and consumer threads. Reactive streams and their request-n backpressure.

## 11. The Verdict

Here is my verdict, plainly. Use stages when the work has parts of different speed and you want throughput. Find the slowest stage, and widen only that one. Put a limit on each waiting line so that trouble pushes back to the door. Keep the lines somewhere that survives a crash if the orders matter.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? If the work is short, or the stages are about equally fast, a single step is simpler, and the queues only add delay. Stages pay off when parts differ in speed, or need separate scaling.

## 14. Thanks for Watching

That's Pipe and Filter Architecture. If you take one sentence away, take this one: pipe and filter architecture lets stages run together and be sized on their own, and the price is the lines between them, and the orders lost if a stage crashes. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, make parse two ticks and see which stage is now the slowest. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
