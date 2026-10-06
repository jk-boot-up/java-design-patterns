# Pipes and Filters Pattern — Video Narration Script

## 1. Pipes and Filters

Hello, and welcome. This video explains the Pipes and Filters pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Pipes and filters breaks a job into small, independent steps, called filters. The steps are joined end to end, by pipes. Each step does one thing, and steps can be added, swapped, or reused. Think of a car wash. The car rolls through: soap, then brushes, then rinse, then dry. Each station does one job, and you can add a wax station without changing the others. In our online store, the job is importing a file of orders from a partner. By the end, you will hear one method do five jobs. Then five small steps joined end to end. A step swapped, and a step added, without touching the others. Bad lines rejected, with reasons. Memory kept small. And the bill.

## 2. The Scenario

Here is the scenario. A partner sends a file of order lines. Each line has a customer, an item, and a quantity. Each line must be read, checked, priced, taxed, and turned into a confirmation. So here is the question. One big method, or five small steps?

## 3. One Method Does It All

First demo: one method does it all. Six lines go in. Three come out. Five separate jobs are packed into one loop. Reading, checking, pricing, tax, and formatting. And the three lines that were dropped left no trace of why.

## 4. The Pattern

Now, the pattern. Break the job into small steps. Each step takes an item, and gives one back. Or it drops the item, and says why. Join the steps end to end. And items flow through, one at a time.

## 5. Small Steps, Joined

Second demo: small steps, joined. The same job is now five steps. Read the line. Check it. Price it. Add U K tax. Format the confirmation. The price step can run on its own. It turns one read line into a priced one: sixteen pounds. So it can be tested without any of the other steps.

## 6. Swap A Step, Add A Step

Third demo: swap a step, and add a step. With the U K tax step, two mugs cost nineteen pounds twenty. Swap it for the European tax step, and they cost nineteen pounds thirty-six. Then add a brand new step in the middle. No other step changed. The pipeline is just a list of steps. And the steps do not know about each other.

## 7. Bad Lines Are Rejected, And The Rest Go On

Fourth demo: bad lines are rejected, and the rest carry on. Three orders come out. Three lines were rejected. Each one names the step that dropped it, and the reason. One says: twelve, written as a word, is not a number. One says: fifty blue mugs is too many. And one line had only two of its three fields. One bad line does not stop the whole file.

## 8. Streaming, Or One Stage At A Time

Fifth demo: streaming, or one stage at a time. Ten thousand lines. With streaming, each item goes all the way through before the next one starts. So only one item is held in memory at once. Running each step over the whole file before the next step holds twenty thousand items. The results are the same. Only the memory used is different.

## 9. The Bill: The Steps Must Agree On The Shape

Finally, the bill. The steps must agree on the shape of the data between them. Suppose the steps pass simple bags of named values. One step calls a field q t y. The next asks for quantity, spelled out. It fails only when the program runs, inside the later step. If the steps pass proper Java types instead, the compiler catches that mistake. But now every step depends on the shape the step before it produces. So changing one step can mean changing its neighbours. And an error shows up in the step that noticed it. Which may be far from the step that caused it.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a chain of map and filter calls on a Java stream. Look for a Unix command line with vertical bars joining commands together. Look for Spring Batch's reader, processor, and writer, or Apache Camel routes. Or a list of processors, each with one process method.

## 11. The Verdict

So, here is the verdict. Use pipes and filters when a job is a series of independent changes to each item. When steps will change, or be reused. And when items can be handled one at a time. Give the data between steps a proper type. Report every rejected item, with the step and the reason. Stream the data when it is large. And keep the pipeline short enough to read. Do not use it when a step needs the whole batch at once.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Nothing depends on a real clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For a job with only two simple steps, a pipeline is more structure than the job itself. And when every step needs the whole batch, a pipeline gains nothing.

## 14. Thanks for Watching

That's the Pipes and Filters pattern. If you remember one sentence, make it this one. Pipes and filters make each step small and replaceable, and the price is that the steps must agree on the shape of the data between them. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a step that removes duplicate customers. Then notice what that step needs to remember. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
