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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Iterator pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An iterator is a small '
            'object with one job: remembering where you are in a '
            'collection. [[slnc 300]] It answers two questions. [[slnc '
            '300]] Is there another one? [[slnc 200]] And, give me the '
            'next one. [[slnc 600]] Think of a book and a bookmark. '
            '[[slnc 300]] The book holds the pages. [[slnc 300]] The '
            'bookmark remembers where you stopped reading. [[slnc 700]] '
            'In this video, we browse the product catalogue of an online '
            'shop. [[slnc 300]] The warehouse system only hands over '
            'products three at a time. [[slnc 500]] By the end, you will '
            'know what your for-each loop really turns into. [[slnc 300]] '
            'Why the reading position must not live on the collection. '
            '[[slnc 300]] And when this pattern is ceremony you do not '
            'need.'
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
            "Here is the scenario. [[slnc 400]] The shop's catalogue "
            'lives in the warehouse system, not in our program. [[slnc '
            '300]] And the warehouse only hands it over one page at a '
            'time. [[slnc 500]] Ask for page zero, and you get three '
            'products. [[slnc 300]] Page one gives three more. [[slnc '
            '300]] Page two gives the last two. [[slnc 500]] How do you '
            'know you have finished? [[slnc 300]] You ask for page three, '
            'and get an empty list. [[slnc 500]] That is the whole '
            'interface. [[slnc 300]] There is no total count, and no way '
            'to ask whether more pages exist. [[slnc 300]] Everything '
            'else, you work out yourself, in a loop. [[slnc 300]] And '
            'that is where things go wrong.'
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
            "Before any code, let's look closely at one method, called "
            'find cheapest. [[slnc 400]] It walks through the pages, and '
            'returns the cheapest product in the shop. [[slnc 500]] But '
            'someone started the page counter at one, instead of zero. '
            '[[slnc 300]] So it never looks at page zero. [[slnc 300]] '
            'And the four pound socks are on page zero. [[slnc 500]] So '
            'it returns the eight pound coffee mug instead. [[slnc 600]] '
            'Think about that for a moment. [[slnc 300]] It is a real '
            'product, at a real price, in exactly the shape the caller '
            'expected. [[slnc 300]] Nothing crashes, and nothing is '
            "logged. [[slnc 300]] The shop's cheapest-first list is "
            'simply wrong, quietly, until someone counts by hand.'
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
            'Here is why it happens. [[slnc 400]] Three methods need to '
            'walk the catalogue. [[slnc 300]] And each one writes its own '
            'paging loop. [[slnc 500]] The first loop is correct. [[slnc '
            '400]] The second one assumes there are exactly three pages. '
            '[[slnc 300]] That is true today. [[slnc 300]] But when a '
            'ninth product is added, it will not fail. [[slnc 300]] It '
            'will just start counting too few. [[slnc 400]] The third is '
            'our off-by-one, starting at page one. [[slnc 600]] The '
            'lesson is not that loops are hard. [[slnc 300]] All three '
            'are the same bug. [[slnc 300]] The page loop was written '
            'three times, so it could go wrong in three ways. [[slnc '
            '300]] And none of those ways causes an error.'
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
            'So what exactly is wrong? [[slnc 300]] Four separate things. '
            '[[slnc 500]] One. [[slnc 200]] Every caller must learn how '
            'the warehouse stores its pages. [[slnc 300]] Change the page '
            'size, and you must edit every caller. [[slnc 500]] Two. '
            '[[slnc 200]] The bugs are silent. [[slnc 300]] A crash gets '
            'fixed the same afternoon. [[slnc 300]] A believable wrong '
            'answer can survive for a year. [[slnc 500]] Three. [[slnc '
            '200]] Returning a full list means fetching everything. '
            '[[slnc 300]] A caller that wanted just the first two '
            'products still causes every page to be fetched. [[slnc 500]] '
            'And four. [[slnc 200]] None of this works with a for-each '
            'loop, because that loop needs something the shop does not '
            'have.'
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
            "Here is the pattern's definition, from the famous Gang of "
            'Four book. [[slnc 400]] Provide a way to access the elements '
            'of a collection in order, without exposing how it is stored '
            'inside. [[slnc 500]] How it is stored is the important part. '
            '[[slnc 300]] In our shop, the catalogue is stored in pages. '
            '[[slnc 300]] And right now, every caller knows about those '
            'pages. [[slnc 500]] So here is the move. [[slnc 300]] Write '
            'one object whose whole job is walking the pages. [[slnc '
            '300]] And let the catalogue hand one out to anyone who asks. '
            '[[slnc 300]] Now the page loop is written once, in one named '
            'place, that can be tested on its own. [[slnc 500]] And Java '
            'already has the two interfaces this pattern needs.'
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
            'Here is the analogy to hold on to. [[slnc 300]] A book, and '
            'a bookmark. [[slnc 500]] The book knows what is in it. '
            '[[slnc 300]] The bookmark knows where you are. [[slnc 300]] '
            'Two different facts, so they belong in two different '
            'objects. [[slnc 500]] Two people can read the same book at '
            'once, if each has their own bookmark. [[slnc 400]] But glue '
            'a single bookmark into the spine, and they fight over it. '
            '[[slnc 300]] Every time one reader turns a page, the other '
            'loses their place. [[slnc 600]] That is the whole pattern. '
            '[[slnc 300]] When an iterator behaves strangely, it is very '
            'often because a bookmark was glued into the spine.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'So here are the pieces, and we wrote very few of them. '
            '[[slnc 500]] Java provides the two main roles. [[slnc 300]] '
            'Iterable has one method, called iterator. [[slnc 300]] And '
            'Iterator has two methods: has next, and next. [[slnc 500]] '
            'Our Product Catalogue implements Iterable, in just four '
            'lines. [[slnc 300]] It has no page number, no position, and '
            'no next method. [[slnc 300]] It only holds the warehouse '
            'feed. [[slnc 500]] Our Catalogue Iterator implements '
            'Iterator. [[slnc 300]] Every one of its fields is about '
            'position: which page, where in that page, and whether it has '
            'started. [[slnc 300]] It is the only class in the project '
            'with a page loop. [[slnc 500]] And underneath sits the '
            'catalogue feed, the awkward paged system we are hiding.'
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
            "Let's look at the catalogue class, and focus on what is "
            'missing. [[slnc 500]] There is no page number. [[slnc 300]] '
            'No current position. [[slnc 300]] No next method. [[slnc '
            '300]] It holds the feed, and it can hand you an iterator. '
            '[[slnc 300]] That is all. [[slnc 600]] It is tempting to put '
            'the position on the catalogue itself. [[slnc 300]] It feels '
            'like the collection should know where you are. [[slnc 300]] '
            'That is the most common mistake with this pattern. [[slnc '
            '300]] And it bites the day someone writes a loop inside a '
            'loop, over the same catalogue. [[slnc 600]] Every time you '
            'ask for an iterator, you get a brand new one. [[slnc 300]] '
            'Every caller gets their own bookmark, and nothing is shared.'
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
            'Now the iterator, where the page loop lives, just once. '
            '[[slnc 500]] The has next method does all the work. [[slnc '
            '300]] If it has not started yet, it fetches page zero. '
            '[[slnc 300]] Notice that happens here, not when the iterator '
            'is created. [[slnc 300]] Creating an iterator costs nothing. '
            '[[slnc 300]] The first fetch only happens when someone '
            'actually asks. [[slnc 500]] Then, if it has reached the end '
            'of the current page, it fetches the next page. [[slnc 300]] '
            'An empty page means the catalogue is finished. [[slnc 300]] '
            'And this is the only place in the project that knows that. '
            '[[slnc 500]] It uses a while loop, not a single if. [[slnc '
            '300]] That way, an empty page in the middle cannot leave it '
            'stuck. [[slnc 500]] The next method is only three lines, '
            'because has next already did the work. [[slnc 300]] And has '
            'next must be safe to call twice in a row. [[slnc 300]] A has '
            'next that uses up an item is another classic bug.'
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
            'The project has thirteen tests. [[slnc 300]] Two of them '
            'prove the pattern. [[slnc 500]] A test like, the catalogue '
            'has eight products, would pass for the naive code too. '
            '[[slnc 300]] So it proves nothing about the pattern. [[slnc '
            '500]] The first special test checks what was not fetched. '
            '[[slnc 300]] The feed counts its own calls. [[slnc 300]] '
            'After creating an iterator, zero pages have been fetched. '
            '[[slnc 300]] After reading two products, just one page has '
            'been fetched. [[slnc 300]] Move the fetch into the '
            'constructor, and this test fails. [[slnc 500]] The second '
            'test uses two iterators over one catalogue. [[slnc 300]] '
            'Move one forward, and the other is still at the start. '
            '[[slnc 300]] That is the glued bookmark problem, written as '
            'a test. [[slnc 300]] Put the position on the catalogue, and '
            'this test fails.'
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
            "Let's run the demo. [[slnc 400]] First, the naive browser. "
            '[[slnc 300]] Its product count is right, but only by luck. '
            '[[slnc 300]] And its cheapest product is not the cheapest. '
            '[[slnc 500]] Second, the same catalogue in a for-each loop. '
            '[[slnc 300]] All eight products, in order. [[slnc 300]] And '
            'the calling code never mentions pages at all. [[slnc 500]] '
            'Third, the most telling result. [[slnc 300]] Two products '
            'were read, and only one page was fetched. [[slnc 300]] The '
            'other two pages were never requested. [[slnc 300]] On a real '
            'system, that is two network calls that never happened. '
            '[[slnc 500]] And fourth, two bookmarks. [[slnc 300]] Two '
            'readers walk the same catalogue, and neither disturbs the '
            'other.'
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
            'So, what should you remember? [[slnc 400]] The collection '
            'knows what is in it. [[slnc 300]] The iterator knows where '
            'you are. [[slnc 300]] Keep those in two different objects, '
            'and the for-each loop comes free. [[slnc 600]] There are '
            'three ways to walk through things. [[slnc 300]] Use an index '
            'loop when you really need the position number. [[slnc 300]] '
            'Use an iterator when you want each item in turn. [[slnc '
            '300]] And use a stream when you want to describe a pipeline '
            'of steps. [[slnc 500]] Streams are not an alternative to '
            'this pattern. [[slnc 300]] They are built on top of it. '
            '[[slnc 600]] Now the honest cost. [[slnc 300]] If you '
            'already have a list, it already has an iterator. [[slnc '
            '300]] Writing your own around it is pure ceremony. [[slnc '
            '400]] This pattern pays off when the storage is awkward. '
            '[[slnc 300]] Pages, a tree, a file read one line at a time, '
            'or a sequence with no end.'
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
            "That's the Iterator pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] The collection '
            'knows what is in it, and the iterator knows where you are, '
            'so keep them apart. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Move the page number and position off the '
            'iterator, and onto the catalogue. [[slnc 300]] Run the '
            'tests, and watch the two-bookmarks test fail. [[slnc 500]] '
            'If this helped, a like really does help other people find '
            "it. [[slnc 300]] And subscribe, if you'd like the rest of "
            'the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
