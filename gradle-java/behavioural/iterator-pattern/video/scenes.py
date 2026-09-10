"""Scene definitions for the Iterator teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Iterator",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Iterator pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 300]] Let's start with the simple definition. An iterator "
            "is a small object whose only job is to remember where you have "
            "got to in a collection. It answers two questions. Is there "
            "another one, and give me it. [[slnc 350]] That's the idea in a "
            "sentence. The rest of the video does it properly, by building a "
            "real working Java project: browsing the product catalogue of an "
            "online shop, where the warehouse system will only hand the "
            "products over three at a time. [[slnc 250]] By the end you'll "
            "know exactly what your for-each loop turns into, why the position "
            "must not live on the collection, and when this pattern is "
            "ceremony you don't need."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The shop's catalogue lives in the warehouse system.",
            "",
            "It hands out products a page at a time:",
            "",
            "    List<Product> page(int number)",
            "",
            "  page(0)  ->  T-Shirt £12, Socks £4, Scarf £18",
            "  page(1)  ->  Lamp £30, Mug £8, Cushion £15",
            "  page(2)  ->  Novel £9, Cookbook £22",
            "  page(3)  ->  [ ]     <- that is how it says 'finished'",
            "",
            "There is no size(). There is no hasMorePages().",
        ],
        narration=(
            "So, imagine an online shop. [[slnc 250]] The catalogue doesn't "
            "live in your program. It lives in the warehouse system, and that "
            "system will only hand it over a page at a time. You ask for page "
            "zero and get three products. Page one, three more. Page two, the "
            "last two. [[slnc 300]] And how do you know you've finished? You "
            "ask for page three and get an empty list back. [[slnc 300]] "
            "That's the whole interface. There's no size. There's no has more "
            "pages. Everything else you might want to know, you work out "
            "yourself, by hand, in a loop. And that is where this goes wrong."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Look Closely at One Method",
        body=[
            "findCheapest() — what is the cheapest thing in the shop?",
            "",
            "    int pageNumber = 1;        <- someone typed 1, not 0",
            "",
            "It never looks at page 0.",
            "So it never sees the £4 socks.",
            "",
            "It returns the £8 Coffee Mug.",
            "",
            "A real product. A real price. Not the cheapest one.",
            "",
            "Nothing throws. Nothing logs. The page just isn't there.",
        ],
        narration=(
            "Before any code, look closely at one method. [[slnc 300]] Find "
            "cheapest walks the pages and returns the cheapest product in the "
            "shop. Somebody started the page counter at one instead of zero. "
            "[[slnc 300]] So it never looks at page zero, and the four pound "
            "socks are on page zero. [[slnc 250]] It returns the eight pound "
            "coffee mug. [[slnc 350]] Sit with that for a second, because it "
            "is the reason this pattern exists. That is a real product, at a "
            "real price, formatted perfectly, in exactly the shape the caller "
            "expected. Nothing throws. Nothing gets logged. The cheapest-first "
            "sort on your shop is simply wrong, quietly, for as long as nobody "
            "counts by hand."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Three Methods, Three Page Loops",
        body="""public List<Product> allProducts() {
    int pageNumber = 0;                    // correct
    ...
}

public int countProducts() {
    for (int pageNumber = 0; pageNumber < 3; pageNumber++) {
        ...                                // "there are 3 pages" — today
    }
}

public Product findCheapest() {
    int pageNumber = 1;                    // never sees page 0
    ...
}""",
        narration=(
            "Here's why. [[slnc 250]] Three methods that want to walk the "
            "catalogue, and each one writes out the paging itself. [[slnc "
            "300]] The first one is correct. The second one hard-codes three "
            "pages, which is true today and stops being true the moment "
            "somebody adds a tenth product — and when it does, it won't fail, "
            "it will just start under-counting. The third is our off-by-one. "
            "[[slnc 350]] And I want to be precise about the lesson, because "
            "it isn't loops are hard. All three of these are the same bug. "
            "The page loop was written three times, so it could be got wrong "
            "in three different ways, and not one of those ways throws an "
            "exception. [[slnc 300]] Write it a fourth time and you get a "
            "fourth chance to be wrong."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "1.  Every caller learns how the storage works.",
            "    Change the page size and you edit all of them.",
            "",
            "2.  The bugs are SILENT. A plausible answer is the worst kind.",
            "",
            "3.  allProducts() fetches everything —",
            "    even for a caller that wanted the first two.",
            "",
            "4.  None of it works with a for-each loop,",
            "    or with anything in the JDK that takes an Iterable.",
        ],
        narration=(
            "Let's be precise, because it's four separate costs. [[slnc 300]] "
            "One. Every caller has to learn how the storage works. The page "
            "size stops being the warehouse's business and becomes everybody's "
            "business, so changing it means editing every one of them. [[slnc "
            "300]] Two. The bugs are silent. A crash is a good outcome — "
            "somebody fixes it that afternoon. A plausible wrong answer can "
            "live in production for a year. [[slnc 300]] Three. Returning a "
            "list means fetching everything. A caller that wanted the first "
            "two products just made four round trips to the warehouse, and on "
            "a real catalogue that's four hundred. [[slnc 300]] And four. None "
            "of this works with a for-each loop, because a for-each loop needs "
            "something the shop doesn't have."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Iterator Pattern",
        # One line per rendered line: kind_quote lays these out as-is.
        body=[
            "Provide a way to access the elements of an",
            "aggregate object sequentially without exposing",
            "its underlying representation.",
            "",
            "— Gang of Four",
            "",
            "In plain terms:",
            "hand out a small object that remembers where you are,",
            "so nobody else has to know how the collection is stored.",
        ],
        narration=(
            "Here's the definition from the Gang of Four book. [[slnc 250]] "
            "Provide a way to access the elements of an aggregate object "
            "sequentially, without exposing its underlying representation. "
            "[[slnc 350]] Underlying representation is the important phrase. "
            "In our shop the representation is pages, and every caller "
            "currently knows about them. [[slnc 300]] So the move is this. "
            "Write one object whose whole job is walking the pages, and give "
            "callers something that hands one out. Then the page loop is "
            "written once, in a place with a name, that can be tested on its "
            "own. [[slnc 300]] And in Java there's a bonus, because the "
            "language already has the two interfaces this pattern asks for."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="An Analogy",
        body=[
            "A book, and a bookmark.",
            "",
            "  The book      knows what is in it.",
            "  The bookmark  knows where YOU are.",
            "",
            "Two people can read one book — with two bookmarks.",
            "",
            "Glue a single bookmark into the spine and they fight over it.",
            "",
            "That is the whole pattern. Everything else is syntax.",
        ],
        narration=(
            "Here's the analogy to hold on to, and with this one, if you take "
            "nothing else away, take this. [[slnc 250]] A book and a bookmark. "
            "[[slnc 300]] The book knows what is in it. The bookmark knows "
            "where you are. Two different facts, and they belong in two "
            "different objects. [[slnc 300]] Two people can read the same book "
            "at once, as long as they each have their own bookmark. Glue one "
            "bookmark into the spine and they fight over it — every time one "
            "reader turns a page, the other one loses their place. [[slnc "
            "350]] That is the whole pattern. When you write your first "
            "iterator and something behaves strangely, nine times out of ten "
            "it's because a bookmark got glued into a spine."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So here are the pieces, and the striking thing is how few of them "
            "we wrote. [[slnc 250]] Iterable and Iterator are the two roles the "
            "pattern names, and both of them ship with Java. Iterable has one "
            "method, iterator. Iterator has two, has next and next. [[slnc "
            "300]] Product catalogue implements Iterable, and it's four lines "
            "long. Look at what it does not have: no page number, no position, "
            "no next. It holds the feed and nothing else. [[slnc 300]] "
            "Catalogue iterator implements Iterator, and every single field on "
            "it is position — which page we're on, where we are inside it, "
            "whether we've started. It is the only class in the project that "
            "contains a page loop. [[slnc 250]] And underneath, the catalogue "
            "feed: the awkward paged thing we're hiding."
        ),
    ),
    dict(
        key="09-aggregate",
        kind="code",
        title="The Aggregate — Notice What Is Missing",
        body="""public class ProductCatalogue implements Iterable<Product> {

    private final CatalogueFeed feed;

    @Override
    public Iterator<Product> iterator() {
        return new CatalogueIterator(feed);   // a FRESH one, every time
    }
}

// No page number.  No position.  No next().
// That absence is the design — it is what lets two walks
// run over one catalogue without colliding.""",
        narration=(
            "This is the catalogue, and I'd rather talk about what isn't here. "
            "[[slnc 250]] There's no page number. No current position. No "
            "next method. It holds a feed, and it can hand you an iterator. "
            "That's it. [[slnc 350]] The temptation, the first time you write "
            "one of these, is to put the position on this class, because it "
            "feels like the collection ought to know where you are. It's the "
            "single most common mistake with this pattern, and the day it "
            "bites you is the day somebody writes a loop inside a loop over "
            "the same catalogue. [[slnc 300]] Look at the word new in "
            "iterator. Every caller gets their own bookmark. Nothing is "
            "shared, nothing is reused, and the catalogue doesn't keep the "
            "ones it hands out."
        ),
    ),
    dict(
        key="10-iterator",
        kind="code",
        title="The Iterator — The Only Page Loop in the Project",
        body="""@Override
public boolean hasNext() {
    if (!started) { currentPage = feed.page(pageNumber); started = true; }

    while (indexInPage >= currentPage.size()) {   // ran off the end?
        if (currentPage.isEmpty()) return false;  // empty page = finished
        pageNumber++;
        indexInPage = 0;
        currentPage = feed.page(pageNumber);      // fetched only when reached
    }
    return true;
}

@Override
public Product next() {
    if (!hasNext()) throw new NoSuchElementException("no more products");
    return currentPage.get(indexInPage++);
}""",
        narration=(
            "And here's the page loop. Once. [[slnc 300]] Has next does all "
            "the work. If we haven't started, fetch page zero — and notice "
            "that's here, not in the constructor. Creating an iterator costs "
            "nothing; the first fetch happens when somebody actually asks. "
            "[[slnc 300]] Then, if we've run off the end of the current page, "
            "move to the next one and fetch it. An empty page means we're "
            "finished, and that's the only place in the whole project that "
            "knows an empty page means finished. [[slnc 350]] It's a while, "
            "not an if, because a short page in the middle would leave you "
            "standing on a page with nothing left. [[slnc 300]] And next is "
            "three lines, because has next already did everything. It calls "
            "has next again rather than trusting the caller — which is also "
            "why has next has to be safe to call twice. A has next that "
            "consumes something is the other classic bug here."
        ),
    ),
    dict(
        key="11-proof",
        kind="code",
        title="The Tests — Asserting What Was NOT Fetched",
        body="""@Test void fetchingIsLazy() {
    CatalogueFeed feed = CatalogueFeed.sampleShop();
    Iterator<Product> it = new ProductCatalogue(feed).iterator();
    assertEquals(0, feed.pagesFetched());       // iterator() touched nothing

    it.next();
    it.next();
    assertEquals(1, feed.pagesFetched());       // two products, ONE page
}

@Test void positionsAreIndependent() {
    ProductCatalogue catalogue = ...;
    Iterator<Product> outer = catalogue.iterator();
    Iterator<Product> inner = catalogue.iterator();

    outer.next();
    assertEquals("SKU-001", inner.next().sku());   // still at the start
}""",
        narration=(
            "Thirteen tests, and these two are the ones that prove the "
            "pattern. [[slnc 300]] A test that says the catalogue yields eight "
            "products passes against the naive code just as happily. It proves "
            "nothing. [[slnc 300]] The first one asserts what was not fetched. "
            "The feed counts its own calls, so we can say: after creating an "
            "iterator, zero pages. After pulling two products, one page. Move "
            "that fetch into the constructor and this test goes red "
            "immediately. Laziness stops being a claim in a comment and "
            "becomes something the build checks. [[slnc 350]] The second is my "
            "favourite. Two iterators over one catalogue. Advance one, and the "
            "other is still at the start. [[slnc 250]] That is the glued "
            "bookmark, written as an assertion. Put the position on the "
            "catalogue and this is the test that goes red."
        ),
    ),
    dict(
        key="12-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== 1.  The naive browser — three loops, two of them wrong ===
   countProducts() -> 8      (correct today; hard-coded to 3 pages)
   findCheapest()  -> SKU-005 Coffee Mug £8
                     but SKU-002 Cotton Socks £4 is cheaper

=== 2.  The same catalogue, in a for-each loop ===
   for (Product product : catalogue)
   -> all 8 products, in order, no page number in sight

=== 3.  Nothing is fetched until it is reached ===
   after two products:  pages fetched -> 1 of 3

=== 4.  Two walks, two positions ===
   outer -> SKU-002    inner -> SKU-001  (still at the start)""",
        narration=(
            "Run it, and the two halves sit side by side. [[slnc 250]] Section "
            "one is the naive browser: a count that's right by luck, and a "
            "cheapest product that simply isn't the cheapest. [[slnc 300]] "
            "Section two is the same catalogue in a for-each loop. Eight "
            "products, in order, and the word page appears nowhere in the "
            "calling code. [[slnc 300]] Section three is the line I'd frame. "
            "Two products consumed, one page of three fetched. The other two "
            "pages were never requested, so on a real system that's two HTTP "
            "calls that never happened. Stop the loop early and the warehouse "
            "never hears about it. [[slnc 350]] And section four is the two "
            "bookmarks. Same catalogue, two walkers, and neither one disturbs "
            "the other."
        ),
    ),
    dict(
        key="13-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "The collection knows WHAT is in it.",
            "The iterator knows WHERE YOU ARE.",
            "",
            "Keep those in different objects and for-each is free.",
            "",
            "  index loop  when you need the index",
            "  iterator    when you want each element in turn",
            "  stream      when you want to describe a pipeline",
            "Streams are BUILT ON this. They are not an alternative to it.",
            "",
            "Already have a List? It has an iterator. Use it.",
            "Write your own when the storage is awkward.",
        ],
        narration=(
            "So, what to take away. [[slnc 300]] The collection knows what is "
            "in it. The iterator knows where you are. Keep those two facts in "
            "two different objects, and the for-each loop is free. [[slnc "
            "350]] On the three ways to walk something: use an index loop when "
            "you genuinely need the index. Use an iterator when you want each "
            "element in turn. Use a stream when you want to describe a "
            "pipeline rather than a walk. [[slnc 300]] And let me be clear "
            "about streams, because it's the question I'd expect. They are not "
            "an alternative to this pattern. They're built on top of it — a "
            "spliterator is an iterator that can also split itself in half. "
            "[[slnc 350]] Now the honest bill. If you already have a list, it "
            "already has an iterator, and writing your own around it is pure "
            "ceremony. This pattern earns its keep when the storage is "
            "awkward: pages, a tree, a file you're reading a line at a time, a "
            "sequence with no end. That's when one carefully written has next "
            "is worth more than three hand-rolled loops."
        ),
    ),
    dict(
        key="14-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that moves",
            "the position onto the catalogue and watches a test go red.",
        ],
        narration=(
            "That's the iterator pattern. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in "
            "the repository — including the exercise I'd most recommend. Move "
            "the page number and the index off the iterator and onto the "
            "catalogue, run the tests, and watch the independent-positions test "
            "go red. Five minutes, and you'll never glue a bookmark into a "
            "spine again. [[slnc 300]] If this helped, a like genuinely does "
            "help other people find it, and subscribe if you'd like the rest of "
            "the behavioural series. [[slnc 250]] Thanks for watching, and I'll "
            "see you in the next one."
        ),
    ),
]
