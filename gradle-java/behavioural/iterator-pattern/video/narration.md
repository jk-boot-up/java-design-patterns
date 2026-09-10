# Iterator Pattern — Video Narration Script

## 1. Iterator

Hello, and welcome. This video explains the Iterator pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. An iterator is a small object whose only job is to remember where you have got to in a collection. It answers two questions. Is there another one, and give me it. That's the idea in a sentence. The rest of the video does it properly, by building a real working Java project: browsing the product catalogue of an online shop, where the warehouse system will only hand the products over three at a time. By the end you'll know exactly what your for-each loop turns into, why the position must not live on the collection, and when this pattern is ceremony you don't need.

## 2. The Scenario

So, imagine an online shop. The catalogue doesn't live in your program. It lives in the warehouse system, and that system will only hand it over a page at a time. You ask for page zero and get three products. Page one, three more. Page two, the last two. And how do you know you've finished? You ask for page three and get an empty list back. That's the whole interface. There's no size. There's no has more pages. Everything else you might want to know, you work out yourself, by hand, in a loop. And that is where this goes wrong.

## 3. Look Closely at One Method

Before any code, look closely at one method. Find cheapest walks the pages and returns the cheapest product in the shop. Somebody started the page counter at one instead of zero. So it never looks at page zero, and the four pound socks are on page zero. It returns the eight pound coffee mug. Sit with that for a second, because it is the reason this pattern exists. That is a real product, at a real price, formatted perfectly, in exactly the shape the caller expected. Nothing throws. Nothing gets logged. The cheapest-first sort on your shop is simply wrong, quietly, for as long as nobody counts by hand.

## 4. The Naive Approach — Three Methods, Three Page Loops

Here's why. Three methods that want to walk the catalogue, and each one writes out the paging itself. The first one is correct. The second one hard-codes three pages, which is true today and stops being true the moment somebody adds a tenth product — and when it does, it won't fail, it will just start under-counting. The third is our off-by-one. And I want to be precise about the lesson, because it isn't loops are hard. All three of these are the same bug. The page loop was written three times, so it could be got wrong in three different ways, and not one of those ways throws an exception. Write it a fourth time and you get a fourth chance to be wrong.

## 5. Why That Hurts

Let's be precise, because it's four separate costs. One. Every caller has to learn how the storage works. The page size stops being the warehouse's business and becomes everybody's business, so changing it means editing every one of them. Two. The bugs are silent. A crash is a good outcome — somebody fixes it that afternoon. A plausible wrong answer can live in production for a year. Three. Returning a list means fetching everything. A caller that wanted the first two products just made four round trips to the warehouse, and on a real catalogue that's four hundred. And four. None of this works with a for-each loop, because a for-each loop needs something the shop doesn't have.

## 6. The Iterator Pattern

Here's the definition from the Gang of Four book. Provide a way to access the elements of an aggregate object sequentially, without exposing its underlying representation. Underlying representation is the important phrase. In our shop the representation is pages, and every caller currently knows about them. So the move is this. Write one object whose whole job is walking the pages, and give callers something that hands one out. Then the page loop is written once, in a place with a name, that can be tested on its own. And in Java there's a bonus, because the language already has the two interfaces this pattern asks for.

## 7. An Analogy

Here's the analogy to hold on to, and with this one, if you take nothing else away, take this. A book and a bookmark. The book knows what is in it. The bookmark knows where you are. Two different facts, and they belong in two different objects. Two people can read the same book at once, as long as they each have their own bookmark. Glue one bookmark into the spine and they fight over it — every time one reader turns a page, the other one loses their place. That is the whole pattern. When you write your first iterator and something behaves strangely, nine times out of ten it's because a bookmark got glued into a spine.

## 8. The Roles

So here are the pieces, and the striking thing is how few of them we wrote. Iterable and Iterator are the two roles the pattern names, and both of them ship with Java. Iterable has one method, iterator. Iterator has two, has next and next. Product catalogue implements Iterable, and it's four lines long. Look at what it does not have: no page number, no position, no next. It holds the feed and nothing else. Catalogue iterator implements Iterator, and every single field on it is position — which page we're on, where we are inside it, whether we've started. It is the only class in the project that contains a page loop. And underneath, the catalogue feed: the awkward paged thing we're hiding.

## 9. The Aggregate — Notice What Is Missing

This is the catalogue, and I'd rather talk about what isn't here. There's no page number. No current position. No next method. It holds a feed, and it can hand you an iterator. That's it. The temptation, the first time you write one of these, is to put the position on this class, because it feels like the collection ought to know where you are. It's the single most common mistake with this pattern, and the day it bites you is the day somebody writes a loop inside a loop over the same catalogue. Look at the word new in iterator. Every caller gets their own bookmark. Nothing is shared, nothing is reused, and the catalogue doesn't keep the ones it hands out.

## 10. The Iterator — The Only Page Loop in the Project

And here's the page loop. Once. Has next does all the work. If we haven't started, fetch page zero — and notice that's here, not in the constructor. Creating an iterator costs nothing; the first fetch happens when somebody actually asks. Then, if we've run off the end of the current page, move to the next one and fetch it. An empty page means we're finished, and that's the only place in the whole project that knows an empty page means finished. It's a while, not an if, because a short page in the middle would leave you standing on a page with nothing left. And next is three lines, because has next already did everything. It calls has next again rather than trusting the caller — which is also why has next has to be safe to call twice. A has next that consumes something is the other classic bug here.

## 11. The Tests — Asserting What Was NOT Fetched

Thirteen tests, and these two are the ones that prove the pattern. A test that says the catalogue yields eight products passes against the naive code just as happily. It proves nothing. The first one asserts what was not fetched. The feed counts its own calls, so we can say: after creating an iterator, zero pages. After pulling two products, one page. Move that fetch into the constructor and this test goes red immediately. Laziness stops being a claim in a comment and becomes something the build checks. The second is my favourite. Two iterators over one catalogue. Advance one, and the other is still at the start. That is the glued bookmark, written as an assertion. Put the position on the catalogue and this is the test that goes red.

## 12. Running It

Run it, and the two halves sit side by side. Section one is the naive browser: a count that's right by luck, and a cheapest product that simply isn't the cheapest. Section two is the same catalogue in a for-each loop. Eight products, in order, and the word page appears nowhere in the calling code. Section three is the line I'd frame. Two products consumed, one page of three fetched. The other two pages were never requested, so on a real system that's two HTTP calls that never happened. Stop the loop early and the warehouse never hears about it. And section four is the two bookmarks. Same catalogue, two walkers, and neither one disturbs the other.

## 13. What to Remember

So, what to take away. The collection knows what is in it. The iterator knows where you are. Keep those two facts in two different objects, and the for-each loop is free. On the three ways to walk something: use an index loop when you genuinely need the index. Use an iterator when you want each element in turn. Use a stream when you want to describe a pipeline rather than a walk. And let me be clear about streams, because it's the question I'd expect. They are not an alternative to this pattern. They're built on top of it — a spliterator is an iterator that can also split itself in half. Now the honest bill. If you already have a list, it already has an iterator, and writing your own around it is pure ceremony. This pattern earns its keep when the storage is awkward: pages, a tree, a file you're reading a line at a time, a sequence with no end. That's when one carefully written has next is worth more than three hand-rolled loops.

## 14. Thanks for Watching

That's the iterator pattern. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository — including the exercise I'd most recommend. Move the page number and the index off the iterator and onto the catalogue, run the tests, and watch the independent-positions test go red. Five minutes, and you'll never glue a bookmark into a spine again. If this helped, a like genuinely does help other people find it, and subscribe if you'd like the rest of the behavioural series. Thanks for watching, and I'll see you in the next one.
