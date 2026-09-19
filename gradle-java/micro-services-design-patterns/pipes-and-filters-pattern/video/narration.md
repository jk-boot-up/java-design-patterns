# Pipes and Filters Pattern — Video Narration Script

## 1. Pipes and Filters

Hello, and welcome. This video explains the Pipes and Filters pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: pipes and filters breaks a job into small independent steps, called filters, joined end to end, so each step does one thing, and steps can be added, swapped or reused. This is another project in the microservices category, whose subject is how many small services stay reliable when they talk to each other. In our online store, the job is importing a file of orders from a partner. By the end you will see one method do five jobs, see five small steps joined end to end, swap and add a step without touching the others, see bad lines rejected with reasons while the rest continue, see streaming keep memory small, and see the bill, which is that the steps must agree on a shape.

## 2. The Scenario

Here is the scenario. A partner sends a file of order lines: a customer, an item, and a quantity. Each line must be parsed, checked, priced, taxed, and turned into a confirmation. The question: one method, or five steps?

## 3. One Method Does It All

First, one method does it all. Six lines go in, and three come out. Five separate jobs are inside one loop: parsing, checking, pricing, tax and formatting. And the three lines that were dropped left no trace of why.

## 4. The Pattern

The pattern. Break the job into small steps. Each step takes an item and gives one back, or drops it and says why. Join them end to end. Items flow through, one at a time.

## 5. Small Steps, Joined

Second, small steps, joined. The same job is now five steps: parse, validate, price, UK tax, format. The price step, run on its own, turns one parsed line into a priced one, sixteen hundred pence. It needs none of the others to be tested.

## 6. Swap A Step, Add A Step

Third, swap a step, add a step. With the UK tax step, two mugs cost nineteen pounds twenty. Swap it for the EU one, and they cost nineteen thirty six. Then add a new step in the middle. No other step changed. The pipeline is a list of steps, and the steps do not know each other.

## 7. Bad Lines Are Rejected, And The Rest Go On

Fourth, bad lines are rejected, and the rest go on. Three orders come out. Three lines were rejected, each with the step that dropped it, and the reason: twelve is not a number, fifty of the blue mug is too many, and a line with only two fields. One bad line does not stop the file.

## 8. Streaming, Or One Stage At A Time

Fifth, streaming, or one stage at a time. Ten thousand lines. Streaming, where each item goes all the way through before the next, holds one item at once. Running each stage over the whole batch holds twenty thousand. The results are the same. Only the memory differs.

## 9. The Bill: The Steps Must Agree On The Shape

Last, the bill. If the steps pass loose maps, one step calls a field qty, and the next asks for quantity, and it fails at run time, in the later step. Typed items catch that when compiling, but now every step depends on the type before it, and changing one means changing its neighbours. And an error shows up in the step that noticed it, which may be far from the step that caused it.

## 10. How To Recognise It

How do you recognise this in code you did not write? A chain of .map(...).filter(...) on a stream. A Unix pipeline with |. Spring Batch's reader, processor and writer, and Camel routes. A list of processors, each with one process method.

## 11. The Verdict

Here is my verdict, plainly. Use pipes and filters when a job is a sequence of independent transformations, when steps will change or be reused, and when items can be handled one at a time. Type the items between steps, report rejects with the step and the reason, and stream where the data is large. Keep a pipeline short enough to read. Do not use it where steps need the whole batch.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For a job with two simple steps, a pipeline is more structure than the job. Where every step needs the whole batch, a pipeline gains nothing.

## 14. Thanks for Watching

That's Pipes and Filters. If you take one sentence away, take this one: pipes and filters make each step small and replaceable, and the price is that the steps must agree on the shape between them. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a step that removes duplicate customers, and see what it needs to hold. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
