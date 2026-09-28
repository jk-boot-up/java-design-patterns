# Iterator Pattern — Video Narration Script

## 1. Iterator

Hello, and welcome. This video explains the Iterator pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An iterator is a small object with one job: remembering where you are in a collection. It answers two questions. Is there another one? And, give me the next one. Think of a book and a bookmark. The book holds the pages. The bookmark remembers where you stopped reading. In this video, we browse the product catalogue of an online shop. The warehouse system only hands over products three at a time. By the end, you will know what your for-each loop really turns into. Why the reading position must not live on the collection. And when this pattern is ceremony you do not need.

## 2. The Scenario

Here is the scenario. The shop's catalogue lives in the warehouse system, not in our program. And the warehouse only hands it over one page at a time. Ask for page zero, and you get three products. Page one gives three more. Page two gives the last two. How do you know you have finished? You ask for page three, and get an empty list. That is the whole interface. There is no total count, and no way to ask whether more pages exist. Everything else, you work out yourself, in a loop. And that is where things go wrong.

## 3. Look Closely at One Method

Before any code, let's look closely at one method, called find cheapest. It walks through the pages, and returns the cheapest product in the shop. But someone started the page counter at one, instead of zero. So it never looks at page zero. And the four pound socks are on page zero. So it returns the eight pound coffee mug instead. Think about that for a moment. It is a real product, at a real price, in exactly the shape the caller expected. Nothing crashes, and nothing is logged. The shop's cheapest-first list is simply wrong, quietly, until someone counts by hand.

## 4. The Naive Approach — Three Methods, Three Page Loops

Here is why it happens. Three methods need to walk the catalogue. And each one writes its own paging loop. The first loop is correct. The second one assumes there are exactly three pages. That is true today. But when a ninth product is added, it will not fail. It will just start counting too few. The third is our off-by-one, starting at page one. The lesson is not that loops are hard. All three are the same bug. The page loop was written three times, so it could go wrong in three ways. And none of those ways causes an error.

## 5. Why That Hurts

So what exactly is wrong? Four separate things. One. Every caller must learn how the warehouse stores its pages. Change the page size, and you must edit every caller. Two. The bugs are silent. A crash gets fixed the same afternoon. A believable wrong answer can survive for a year. Three. Returning a full list means fetching everything. A caller that wanted just the first two products still causes every page to be fetched. And four. None of this works with a for-each loop, because that loop needs something the shop does not have.

## 6. The Iterator Pattern

Here is the pattern's definition, from the famous Gang of Four book. Provide a way to access the elements of a collection in order, without exposing how it is stored inside. How it is stored is the important part. In our shop, the catalogue is stored in pages. And right now, every caller knows about those pages. So here is the move. Write one object whose whole job is walking the pages. And let the catalogue hand one out to anyone who asks. Now the page loop is written once, in one named place, that can be tested on its own. And Java already has the two interfaces this pattern needs.

## 7. An Analogy

Here is the analogy to hold on to. A book, and a bookmark. The book knows what is in it. The bookmark knows where you are. Two different facts, so they belong in two different objects. Two people can read the same book at once, if each has their own bookmark. But glue a single bookmark into the spine, and they fight over it. Every time one reader turns a page, the other loses their place. That is the whole pattern. When an iterator behaves strangely, it is very often because a bookmark was glued into the spine.

## 8. The Roles

So here are the pieces, and we wrote very few of them. Java provides the two main roles. Iterable has one method, called iterator. And Iterator has two methods: has next, and next. Our Product Catalogue implements Iterable, in just four lines. It has no page number, no position, and no next method. It only holds the warehouse feed. Our Catalogue Iterator implements Iterator. Every one of its fields is about position: which page, where in that page, and whether it has started. It is the only class in the project with a page loop. And underneath sits the catalogue feed, the awkward paged system we are hiding.

## 9. The Aggregate — Notice What Is Missing

Let's look at the catalogue class, and focus on what is missing. There is no page number. No current position. No next method. It holds the feed, and it can hand you an iterator. That is all. It is tempting to put the position on the catalogue itself. It feels like the collection should know where you are. That is the most common mistake with this pattern. And it bites the day someone writes a loop inside a loop, over the same catalogue. Every time you ask for an iterator, you get a brand new one. Every caller gets their own bookmark, and nothing is shared.

## 10. The Iterator — The Only Page Loop in the Project

Now the iterator, where the page loop lives, just once. The has next method does all the work. If it has not started yet, it fetches page zero. Notice that happens here, not when the iterator is created. Creating an iterator costs nothing. The first fetch only happens when someone actually asks. Then, if it has reached the end of the current page, it fetches the next page. An empty page means the catalogue is finished. And this is the only place in the project that knows that. It uses a while loop, not a single if. That way, an empty page in the middle cannot leave it stuck. The next method is only three lines, because has next already did the work. And has next must be safe to call twice in a row. A has next that uses up an item is another classic bug.

## 11. The Tests — Asserting What Was NOT Fetched

The project has thirteen tests. Two of them prove the pattern. A test like, the catalogue has eight products, would pass for the naive code too. So it proves nothing about the pattern. The first special test checks what was not fetched. The feed counts its own calls. After creating an iterator, zero pages have been fetched. After reading two products, just one page has been fetched. Move the fetch into the constructor, and this test fails. The second test uses two iterators over one catalogue. Move one forward, and the other is still at the start. That is the glued bookmark problem, written as a test. Put the position on the catalogue, and this test fails.

## 12. Running It

Let's run the demo. First, the naive browser. Its product count is right, but only by luck. And its cheapest product is not the cheapest. Second, the same catalogue in a for-each loop. All eight products, in order. And the calling code never mentions pages at all. Third, the most telling result. Two products were read, and only one page was fetched. The other two pages were never requested. On a real system, that is two network calls that never happened. And fourth, two bookmarks. Two readers walk the same catalogue, and neither disturbs the other.

## 13. What to Remember

So, what should you remember? The collection knows what is in it. The iterator knows where you are. Keep those in two different objects, and the for-each loop comes free. There are three ways to walk through things. Use an index loop when you really need the position number. Use an iterator when you want each item in turn. And use a stream when you want to describe a pipeline of steps. Streams are not an alternative to this pattern. They are built on top of it. Now the honest cost. If you already have a list, it already has an iterator. Writing your own around it is pure ceremony. This pattern pays off when the storage is awkward. Pages, a tree, a file read one line at a time, or a sequence with no end.

## 14. Thanks for Watching

That's the Iterator pattern. If you remember one sentence, make it this one. The collection knows what is in it, and the iterator knows where you are, so keep them apart. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Move the page number and position off the iterator, and onto the catalogue. Run the tests, and watch the two-bookmarks test fail. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
