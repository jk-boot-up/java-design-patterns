# Write-Behind Cache Pattern — Video Narration Script

## 1. Write-Behind Cache

Hello, and welcome. This video explains the Write-Behind Cache pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A write-behind cache keeps each change in fast memory, and answers straight away. A few seconds later, it saves the changes to the database, in one batch. A record that changed ten times is saved only once. Think of typing a long document on a computer. Every letter appears at once. But the file is saved only every few minutes. And everyone has lost a paragraph to a power cut, just before the save. In this video, the domain is an online shop. Customers change their shopping carts all the time. Add a mug, make it two, remove the tea, add it back. By the end, you will hear what it costs to save every change at once. How write-behind turns thirty writes into three. What happens when the database is down. And exactly what is lost in a crash.

## 2. The Scenario

Here is the scenario. Customers change their carts again and again. Every change was saved to the database before the page answered. A database is the safe, permanent store, but writing to it is slow. Here, twenty milliseconds, on every click. And most of those saves were replaced a second later, by the next change.

## 3. Act One — Write every change

First demo: write every change straight to the database. Three customers each change their cart ten times. Add a mug. Make it two. Remove the tea. Every change is saved to the database before the page answers. That is thirty database writes. Each one takes twenty milliseconds. Six hundred milliseconds of waiting, in total. And most of those writes are replaced a moment later, by the next change to the same cart.

## 4. Act Two — Write behind

Second demo: write to memory now, and to the database later. The same thirty changes go into memory. Each changed cart is marked as dirty, which just means: not saved yet. The customers wait zero milliseconds. After five seconds, a flush runs. Flush means: save everything that is dirty. Each cart is saved once, with its latest contents. Three writes, instead of thirty. Priya's cart reaches the database as ten mugs and nine teas. Her final choice.

## 5. Act Three — The database goes down

Third demo: the database goes down. Two customers change their carts. They wait zero milliseconds, and keep shopping. The flush tries to save, and fails. The two carts stay dirty, waiting. The database comes back. The next flush saves both carts. The customers never noticed.

## 6. Act Four — A crash before the flush

Fourth demo: the server crashes before a flush. Priya adds a teapot, and raises her mugs to twelve. Ana changes her tea. The next flush is five seconds away. Then the server crashes. Memory is wiped. All three changes are lost. The teapot is not in the database. The database still holds the carts from the last flush. That is the price of this pattern.

## 7. Act Five — The bill

Fifth demo: the bill. Priya changes her kettles from one to three. Checkout reads memory, and sees three. A stock report reads the database, and still sees one. The database is always a little behind. So never write behind an order, a payment, or stock. Use it only for data you can afford to lose.

## 8. The Pattern

Let's name the pattern. Make the change in memory, and answer at once. Mark the record as dirty. Every few seconds, flush. Save each dirty record once, with its latest contents. If the database is down, keep it dirty, and try again next time. And accept one thing. A change made after the last flush is lost if the server crashes.

## 9. Who Does What

Here is who does what. Cart store is the interface: set a quantity, and get a cart. The write-behind store keeps carts in memory, and a set of dirty carts. Its flush method saves each dirty cart once. The database is slow and safe. And the write-through store is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Your operating system keeps file writes in memory, and saves them to disk a moment later. Caches such as Hazelcast offer write-behind as a setting. Autosave in an editor is the same idea. And so are page view counters, collected in memory, and saved in batches.

## 11. When To Use It

So, when should you use it? Use write-behind for data that changes often, and can be lost without real harm. Carts, counters, drafts. Flush often. Flush when the server shuts down cleanly. And retry when the database is down. Never use it for orders, payments, or stock. Those must be safe the moment the customer is told they worked.

## 12. Thanks for Watching

That's the Write-Behind Cache pattern. If you remember one sentence, make it this one. Answer now, save in a moment, and only for what you can afford to lose. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a shutdown method that flushes before the server stops. Then ask which crashes it cannot help with. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
