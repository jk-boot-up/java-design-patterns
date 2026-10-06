# The Flyweight Pattern Pattern — Video Narration Script

## 1. The Flyweight Pattern

Hello, and welcome. This video explains the Flyweight pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Flyweight pattern stops you paying for the same data twice. The parts of an object that are identical across thousands of copies are stored once, and shared. And the parts that differ are passed in, at the moment they are needed. Think of a rubber stamp. One stamp, used again and again, in a different place each time. In our online store, we look at the small badges shown on product listings. By the end, you will know what a flyweight is, what shared and passed-in state mean, and how to write one yourself.

## 2. The Scenario

Here is the scenario. The store lists one hundred thousand products. Every listing shows a small badge in the corner. New. Sale. Bestseller. Or low stock. Notice this already. There are only four different badge designs. But a hundred thousand listings each need one.

## 3. What a Badge Design Actually Is

Here is what makes up one badge design. An icon. A background colour. A text colour. Whether the text is bold. And a picture, sixty-four kilobytes in size. And here is the key point. Every sale badge in the whole catalog looks exactly the same. Same icon, same colours, same picture. Only the listing underneath it changes.

## 4. The Naive Approach — One Badge Object Per Listing

Here is the naive approach. Every time a badge is made for a listing, a brand new sixty-four-kilobyte picture is created. And the icon and colours are rebuilt from scratch. That happens once per listing. One hundred thousand times. So every sale badge holds its own private copy of exactly the same data.

## 5. Why That Hurts

That does real damage, to memory. One hundred thousand listings, each with a sixty-four-kilobyte picture, adds up to about six gigabytes. For just four different designs. Almost every one of those bytes is a duplicate. And Java's memory cleaner has to work through all those repeated copies. To be clear, no single badge is wrong. Each one displays correctly. The waste is in the structure, not a bug.

## 6. The Flyweight Pattern

The Flyweight pattern fixes exactly this. The classic book on design patterns, by the authors known as the Gang of Four, describes it like this. Use sharing to support large numbers of small objects efficiently. By separating the state that is shared, called intrinsic, from the state the caller supplies, called extrinsic. In plain words: stop paying for the same data twice.

## 7. Remember It With a Rubber Stamp

Here is how to remember it. Think about a rubber stamp. The stamp carries its ink and its shape. That never changes, however many times you use it. But where you press it on the page is different every time. The stamp is the flyweight. It is shared. The position on the page is extrinsic. You supply it fresh, each time.

## 8. The Four Roles

Every flyweight has four roles. The flyweight itself: here, the badge style. The factory: the only place a badge style is ever built. The context: a catalog badge, cheap and plentiful, one per listing. And the client: the demo code, which asks the factory for styles. Here is the most important idea in this video. The factory hands out the same shared style to everyone who asks for the same type. One badge style object. A hundred thousand listings pointing at it.

## 9. The Flyweight — Only Intrinsic State, No Setters

Here is the flyweight: the badge style. Everything it holds is shared state. The icon, the colours, the bold setting, and the picture. Identical for every sale badge, whichever listing asks. Now look at how it draws itself. The listing's I D, and any custom label, are passed in each time. That is the extrinsic state, and it is never stored on the shared object. And the style can never be changed after it is built, on purpose. Changing a shared object would change every listing that uses it.

## 10. The Factory — computeIfAbsent Does All the Work

Here is the factory. It keeps a small cache, one entry per badge type. The first time anyone asks for the sale style, it is built, and stored in the cache. Every request after that, for any listing, gets back that exact same object. The cache is a map built for many threads at once. So it is safe to use from anywhere, with no extra locking.

## 11. What the Flyweight Gives You

So the flyweight gives us three things. Sharing: one badge style per type, not per listing. Safety: a thread-safe cache, with no locks to write ourselves. And separation: shared data stored, and per-listing data passed in, never mixed. Now notice what the badge style does not contain. Nothing about any particular listing. A flyweight shares. It never remembers who asked.

## 12. The Client — This Is the Whole Thing

Here is the context object: the catalog badge. When it is created, it does not build a style. It asks the factory for one, and keeps a reference to the shared style. It only owns two things itself: the listing I D, and an optional custom label. Everything else, it borrows. So you can create a hundred thousand catalog badges. And behind them, just four badge styles do all the heavy lifting.

## 13. Running It

Let's run the project. Ask the factory for the sale style twice, and you get the very same object, both times. Two different listings share one style. Only four badge styles were ever created. Now the naive version. Two identical sale badges are two separate objects. And the memory numbers. About six gigabytes with the naive version. About two hundred and fifty-six kilobytes with the flyweight. Just by sharing four objects, instead of a hundred thousand.

## 14. Wrap Up

So, to recap. Use a flyweight when you have a huge number of objects, and most of each one's data repeats. Store shared data inside the flyweight. Pass per-use data in, each time. And never let a flyweight be changed. It is only worth it at scale. Five listings do not need a cache. And one comparison worth knowing. The Prototype pattern hands out copies. A flyweight hands out the same object, again and again.

## 15. Thanks for Watching

That's the Flyweight pattern. If you remember one sentence, make it this one. Store the shared part once, pass the changing part in, and a hundred thousand objects can share four. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a fifth badge type, like free delivery. And check that still only one style is built for it. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
